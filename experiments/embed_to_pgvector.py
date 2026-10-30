# /// script
# requires-python = ">=3.10"
# dependencies = ["fastembed", "psycopg[binary]", "pgvector", "numpy"]
# ///
"""Cut the Knowledge articles into chunks, embed them, and save them in Postgres.

Steps:
  1. Cut each article into heading-based chunks (see chunker.py).
  2. Turn each chunk into an embedding: 384 numbers that capture its meaning.
  3. Save each chunk's text and embedding as one row in the `chunks` table.

Run the database first:
    docker compose -f experiments/compose.yaml up -d
Then:
    uv run experiments/embed_to_pgvector.py

Safe to run again: it empties the table and reloads everything.
"""

import json
from pathlib import Path

import psycopg
from fastembed import TextEmbedding
from pgvector.psycopg import register_vector

from chunker import heading_chunks

ARTICLES = Path(__file__).parent.parent / "CaseHandlerSF/data/knowledge/knowledge.jsonl"
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/knowledge"


def main():
    # 1. Chunk
    articles = [json.loads(line) for line in open(ARTICLES, encoding="utf-8")]
    rows = []  # (article number, title, chunk text)
    for article in articles:
        for chunk in heading_chunks(article["body"], article["title"]):
            rows.append((article["article_number"], article["title"], chunk))
    print(f"{len(articles)} articles -> {len(rows)} chunks")

    # 2. Embed (bge-small makes vectors of 384 numbers)
    model = TextEmbedding("BAAI/bge-small-en-v1.5")
    embeddings = list(model.passage_embed([text for _, _, text in rows]))
    print(f"embedded {len(embeddings)} chunks, {len(embeddings[0])} numbers each")

    # 3. Store
    with psycopg.connect(DATABASE_URL) as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector")  # turns on pgvector
        register_vector(conn)  # lets Python send vectors to Postgres
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id             serial PRIMARY KEY,
                article_number text NOT NULL,
                title          text NOT NULL,
                content        text NOT NULL,
                embedding      vector(384) NOT NULL
            )
        """)
        conn.execute("TRUNCATE chunks RESTART IDENTITY")  # start fresh on every run
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO chunks (article_number, title, content, embedding) VALUES (%s, %s, %s, %s)",
                [(num, title, text, emb) for (num, title, text), emb in zip(rows, embeddings)],
            )
        count = conn.execute("SELECT count(*) FROM chunks").fetchone()[0]
    print(f"saved {count} rows in the chunks table")


if __name__ == "__main__":
    main()
