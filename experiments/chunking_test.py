# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "fastembed"]
# ///
"""Which chunking strategy helps search find the answer?

Steps:
  1. Cut all 47 Knowledge articles into chunks, once per strategy.
  2. Turn every chunk into an embedding (a list of numbers that captures meaning).
  3. For each test question, find the 3 chunks whose embeddings are closest.
  4. Count how often one of those chunks contains the answer.

Usage:
    uv run experiments/chunking_test.py
"""

import json
from pathlib import Path

import numpy as np
from fastembed import TextEmbedding

from chunker import fixed_size_chunks, heading_chunks

ARTICLES = Path(__file__).parent.parent / "CaseHandlerSF/data/knowledge/knowledge.jsonl"

# Each test: a question, and the exact text that answers it.
QUESTIONS = [
    ("How long do we keep full access after our card payment fails?", "Days 0–14"),
    ("Can a support agent give a lapsed customer extra time to pay?", "7-day courtesy extension"),
    ("How quickly must our webhook endpoint answer before Lumora retries?", "10 seconds"),
    ("Which HTTP header carries the webhook HMAC?", "X-Lumora-Signature"),
    ("What idle timeout should our firewall allow for live update connections?", "at least 120 seconds"),
    ("Which refresh token policy should the Salesforce connected app use?", "valid until revoked"),
    ("How many OAuth refresh tokens can one Salesforce user hold for the app?", "5 refresh tokens per user"),
    ("How many years of audit history does Enterprise keep?", "**Enterprise:** 7 years"),
    ("Which release fixed sensitive fields leaking into scheduled exports?", "**2026.09.2**"),
    ("What should our custom domain CNAME point to?", "custom.lumora.example"),
    ("For how long does a copied invitation link work?", "valid for 7 days"),
    ("How many password reset emails can one address request per hour?", "at most 3 reset emails"),
    ("How much clock skew does the SAML integration tolerate?", "Allowed skew is 3 minutes"),
    ("What is the largest CSV export allowed?", "1,000,000 rows per export"),
    ("How often are account-level form drafts saved?", "saved to the server every 15 seconds"),
    ("Does an agent need approval to refund a double charge?", "refund duplicates without approval"),
    ("At what row count will server-side filtering switch on by itself?", "above 50,000 rows"),
    ("How many custom fields can be indexed on Enterprise?", "Enterprise up to 100"),
    ("Which iOS app version fixed the crash on launch?", "**2.3.2**"),
    ("How long does a backup restore take for Enterprise customers?", "Enterprise: 1 business day"),
    ("How deep can automation rules trigger other rules?", "up to 10 levels deep"),
    ("What is the rate limit on the search API?", "30 per minute"),
    ("Who gets the 95% storage warning?", "Owners, billing contacts and Admins"),
]


def main():
    articles = [json.loads(line) for line in open(ARTICLES, encoding="utf-8")]
    model = TextEmbedding("BAAI/bge-small-en-v1.5")  # small model that runs on your laptop

    # Embed the questions once. Dividing by the length lets us compare with a dot product.
    question_vectors = np.array(list(model.query_embed([q for q, _ in QUESTIONS])))
    question_vectors /= np.linalg.norm(question_vectors, axis=1, keepdims=True)

    strategies = {
        "fixed-size (100 words)": lambda a: fixed_size_chunks(a["body"]),
        "heading-based": lambda a: heading_chunks(a["body"], a["title"]),
    }

    for name, make_chunks in strategies.items():
        chunks = [chunk for article in articles for chunk in make_chunks(article)]
        chunk_vectors = np.array(list(model.passage_embed(chunks)))
        chunk_vectors /= np.linalg.norm(chunk_vectors, axis=1, keepdims=True)

        # scores[i, j] = how similar question i is to chunk j (higher = closer)
        scores = question_vectors @ chunk_vectors.T

        found_first, found_top3 = 0, 0
        print(f"\n=== {name}: {len(chunks)} chunks ===")
        for i, (question, answer) in enumerate(QUESTIONS):
            top3 = np.argsort(-scores[i])[:3]  # positions of the 3 best chunks
            if answer in chunks[top3[0]]:
                found_first += 1
            if any(answer in chunks[j] for j in top3):
                found_top3 += 1
            else:
                print(f"  missed: {question}")
        print(f"  answer in the 1st chunk: {found_first}/{len(QUESTIONS)}")
        print(f"  answer in the top 3:     {found_top3}/{len(QUESTIONS)}")


if __name__ == "__main__":
    main()
