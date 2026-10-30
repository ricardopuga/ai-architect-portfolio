# /// script
# requires-python = ">=3.10"
# dependencies = ["fastembed", "psycopg[binary]", "pgvector", "numpy"]
# ///
"""Ask a question and get the 3 closest chunks from Postgres.

Usage:
    uv run experiments/search_pgvector.py "How do I set up SSO?"
"""

import sys

import psycopg
from fastembed import TextEmbedding
from pgvector.psycopg import register_vector

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/knowledge"


def main():
    question = " ".join(sys.argv[1:]) or "How long is the grace period after a failed payment?"

    # Embed the question with the same model used for the chunks.
    model = TextEmbedding("BAAI/bge-small-en-v1.5")
    question_embedding = next(iter(model.query_embed([question])))

    with psycopg.connect(DATABASE_URL) as conn:
        register_vector(conn)
        # <=> is pgvector's cosine distance: 0 means same meaning, bigger means less alike.
        results = conn.execute("""
            SELECT article_number, content, embedding <=> %s AS distance
            FROM chunks
            ORDER BY distance
            LIMIT 3
        """, (question_embedding,)).fetchall()

    print(f"Question: {question}\n")
    for article_number, content, distance in results:
        print(f"--- {article_number}  (distance {distance:.3f})")
        print(content[:300] + ("..." if len(content) > 300 else ""))
        print()


if __name__ == "__main__":
    main()
