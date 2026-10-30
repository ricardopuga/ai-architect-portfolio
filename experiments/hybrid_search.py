"""Three ways to find the chunks that answer a question.

1. Vector search: compares meaning (embeddings in Postgres/pgvector).
   Good at paraphrases: "half a minute late" finds "30 seconds".
2. Keyword search (BM25): counts matching words, and rare words count more.
   Good at exact terms: error codes, header names, version numbers.
3. Hybrid + rerank: merge the results of 1 and 2, then let a reranker model
   read the question and each candidate together and put them in order.

Used by compare_retrieval.py. Needs the database running with chunks loaded
(see embed_to_pgvector.py).
"""

import math
import re
from collections import Counter

import psycopg
from fastembed import TextEmbedding
from fastembed.rerank.cross_encoder import TextCrossEncoder
from pgvector.psycopg import register_vector

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/knowledge"


def tokenize(text):
    """Lowercase words. Joined terms like "x-lumora-signature" are kept whole and also split up."""
    tokens = []
    for word in re.findall(r"[a-z0-9][a-z0-9_.-]*[a-z0-9]|[a-z0-9]", text.lower()):
        tokens.append(word)
        parts = re.split(r"[_.-]", word)
        if len(parts) > 1:
            tokens.extend(parts)
    return tokens


class BM25:
    """Keyword scoring. A chunk scores higher when it contains the question's words,
    especially rare words, and less when it is long and full of other words."""

    def __init__(self, texts, k1=1.5, b=0.75):
        self.k1, self.b = k1, b
        self.docs = [Counter(tokenize(t)) for t in texts]  # word counts for each chunk
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg_length = sum(self.lengths) / len(self.lengths)
        # How many chunks contain each word. Rare words get a big weight (IDF).
        doc_freq = Counter(word for d in self.docs for word in d)
        n = len(self.docs)
        self.idf = {w: math.log(1 + (n - f + 0.5) / (f + 0.5)) for w, f in doc_freq.items()}

    def scores(self, query):
        words = tokenize(query)
        result = []
        for doc, length in zip(self.docs, self.lengths):
            score = 0.0
            for w in words:
                if w in doc:
                    tf = doc[w]  # how often the word appears in this chunk
                    score += self.idf[w] * tf * (self.k1 + 1) / (
                        tf + self.k1 * (1 - self.b + self.b * length / self.avg_length))
            result.append(score)
        return result


class Searcher:
    def __init__(self):
        with psycopg.connect(DATABASE_URL) as conn:
            rows = conn.execute("SELECT id, article_number, title, content FROM chunks ORDER BY id").fetchall()
        self.chunks = {r[0]: {"id": r[0], "article_number": r[1], "title": r[2], "content": r[3]} for r in rows}
        self.ids = list(self.chunks)
        self.bm25 = BM25([self.chunks[i]["content"] for i in self.ids])
        self.embedder = TextEmbedding("BAAI/bge-small-en-v1.5")
        self.reranker = TextCrossEncoder("Xenova/ms-marco-MiniLM-L-6-v2")

    def vector(self, question, k=5):
        """Closest chunks by meaning, using pgvector in Postgres."""
        embedding = next(iter(self.embedder.query_embed([question])))
        with psycopg.connect(DATABASE_URL) as conn:
            register_vector(conn)
            rows = conn.execute("SELECT id FROM chunks ORDER BY embedding <=> %s LIMIT %s",
                                (embedding, k)).fetchall()
        return [self.chunks[r[0]] for r in rows]

    def keyword(self, question, k=5):
        """Highest BM25 scores."""
        scores = self.bm25.scores(question)
        best = sorted(range(len(scores)), key=lambda i: -scores[i])[:k]
        return [self.chunks[self.ids[i]] for i in best if scores[i] > 0]

    def hybrid(self, question, k=5, pool=20):
        """Merge vector and keyword results with Reciprocal Rank Fusion:
        each list gives a chunk 1 / (60 + its position), and the points are added up.
        A chunk near the top of both lists wins."""
        points = Counter()
        for results in (self.vector(question, pool), self.keyword(question, pool)):
            for position, chunk in enumerate(results, start=1):
                points[chunk["id"]] += 1 / (60 + position)
        return [self.chunks[i] for i, _ in points.most_common(k)]

    def hybrid_rerank(self, question, k=5, pool=20):
        """Take the top 20 hybrid results, and let the reranker pick the best 5.
        The reranker reads the question and each chunk *together*, which is slower
        than comparing embeddings but better at judging if the chunk answers it."""
        candidates = self.hybrid(question, k=pool, pool=pool)
        scores = list(self.reranker.rerank(question, [c["content"] for c in candidates]))
        ranked = sorted(zip(scores, range(len(candidates))), reverse=True)
        return [candidates[i] for _, i in ranked[:k]]
