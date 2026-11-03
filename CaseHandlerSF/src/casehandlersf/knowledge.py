"""Search the Knowledge base chunks in Postgres with hybrid search + rerank.

The same retrieval as experiments/hybrid_search.py, which won the comparison in
experiments/compare_retrieval.py: vector search (pgvector) and keyword search
(BM25) merged with Reciprocal Rank Fusion, then a cross-encoder reranks the pool.

The chunks are loaded by experiments/embed_to_pgvector.py.
"""

import math
import re
from collections import Counter
from dataclasses import dataclass
from functools import cache

import psycopg
from fastembed import TextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder
from pgvector.psycopg import register_vector
from pydantic_settings import BaseSettings, SettingsConfigDict

# Must match the model used to embed the chunks.
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
RERANK_MODEL = "Xenova/ms-marco-MiniLM-L-6-v2"


class KnowledgeSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="KNOWLEDGE_", extra="ignore"
    )

    database_url: str = "postgresql://postgres:postgres@localhost:5432/knowledge"


@dataclass(frozen=True, slots=True)
class Chunk:
    id: int
    article_number: str
    title: str
    content: str


def tokenize(text: str) -> list[str]:
    """Lowercase words. Joined terms like "x-lumora-signature" are kept whole and also split up."""
    tokens = []
    for word in re.findall(r"[a-z0-9][a-z0-9_.-]*[a-z0-9]|[a-z0-9]", text.lower()):
        tokens.append(word)
        parts = re.split(r"[_.-]", word)
        if len(parts) > 1:
            tokens.extend(parts)
    return tokens


class BM25:
    """Keyword scoring: rare words count more, long chunks count less."""

    def __init__(self, texts: list[str], k1: float = 1.5, b: float = 0.75) -> None:
        self.k1, self.b = k1, b
        self.docs = [Counter(tokenize(t)) for t in texts]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg_length = sum(self.lengths) / len(self.lengths)
        doc_freq = Counter(word for d in self.docs for word in d)
        n = len(self.docs)
        self.idf = {
            w: math.log(1 + (n - f + 0.5) / (f + 0.5)) for w, f in doc_freq.items()
        }

    def scores(self, query: str) -> list[float]:
        words = tokenize(query)
        result = []
        for doc, length in zip(self.docs, self.lengths):
            score = 0.0
            for w in words:
                if tf := doc.get(w):
                    score += (
                        self.idf[w]
                        * tf
                        * (self.k1 + 1)
                        / (
                            tf
                            + self.k1 * (1 - self.b + self.b * length / self.avg_length)
                        )
                    )
            result.append(score)
        return result


class Searcher:
    def __init__(self, database_url: str) -> None:
        self.database_url = database_url
        with psycopg.connect(database_url) as conn:
            rows = conn.execute(
                "SELECT id, article_number, title, content FROM chunks ORDER BY id"
            ).fetchall()
        if not rows:
            raise RuntimeError(
                "the chunks table is empty; load it with experiments/embed_to_pgvector.py"
            )
        self.chunks = {row[0]: Chunk(*row) for row in rows}
        self.ids = list(self.chunks)
        self.bm25 = BM25([self.chunks[i].content for i in self.ids])
        self.embedder = TextEmbedding(EMBEDDING_MODEL)
        self.reranker = TextCrossEncoder(RERANK_MODEL)

    def vector(self, question: str, k: int) -> list[Chunk]:
        embedding = next(iter(self.embedder.query_embed([question])))
        with psycopg.connect(self.database_url) as conn:
            register_vector(conn)
            rows = conn.execute(
                "SELECT id FROM chunks ORDER BY embedding <=> %s LIMIT %s",
                (embedding, k),
            ).fetchall()
        return [self.chunks[r[0]] for r in rows]

    def keyword(self, question: str, k: int) -> list[Chunk]:
        scores = self.bm25.scores(question)
        best = sorted(range(len(scores)), key=lambda i: -scores[i])[:k]
        return [self.chunks[self.ids[i]] for i in best if scores[i] > 0]

    def hybrid(self, question: str, k: int, pool: int) -> list[Chunk]:
        """Reciprocal Rank Fusion: each list gives a chunk 1 / (60 + its position)."""
        points: Counter[int] = Counter()
        for results in (self.vector(question, pool), self.keyword(question, pool)):
            for position, chunk in enumerate(results, start=1):
                points[chunk.id] += 1 / (60 + position)
        return [self.chunks[i] for i, _ in points.most_common(k)]

    def search(self, question: str, k: int = 5, pool: int = 20) -> list[Chunk]:
        """The `k` best chunks: top `pool` hybrid results, reordered by the reranker."""
        candidates = self.hybrid(question, k=pool, pool=pool)
        scores = list(self.reranker.rerank(question, [c.content for c in candidates]))
        ranked = sorted(zip(scores, range(len(candidates))), reverse=True)
        return [candidates[i] for _, i in ranked[:k]]


@cache
def searcher() -> Searcher:
    """The shared Searcher. Built on first use: it loads every chunk and two models."""
    return Searcher(KnowledgeSettings().database_url)
