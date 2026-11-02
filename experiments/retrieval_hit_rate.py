# /// script
# requires-python = ">=3.10"
# dependencies = ["fastembed", "psycopg[binary]", "pgvector", "numpy"]
# ///
"""Retrieval hit rate on the 35 answerable questions in rag_test_questions.csv.

For each question and each search method, retrieve 5 chunks and record the rank
of the first chunk that comes from a source article. A hit means one of the
5 chunks is from the right article (any of them, if several are listed).
The 5 unanswerable questions have no right article, so they are skipped.

Usage (database running, chunks loaded):
    uv run experiments/retrieval_hit_rate.py

Results go to experiments/retrieval_hit_rate.md. No Claude calls.
"""

import csv
from pathlib import Path

from hybrid_search import Searcher

HERE = Path(__file__).parent
QUESTIONS = HERE / "rag_test_questions.csv"
RESULTS = HERE / "retrieval_hit_rate.md"
K = 5


def first_hit(chunks, articles):
    """Rank (1-based) of the first chunk from a source article, or None."""
    for rank, chunk in enumerate(chunks, start=1):
        if chunk["article_number"] in articles:
            return rank
    return None


def main():
    with QUESTIONS.open(encoding="utf-8") as f:
        questions = [q for q in csv.DictReader(f) if q["kind"] != "unanswerable"]

    searcher = Searcher()
    methods = {
        "vector": searcher.vector,
        "keyword (BM25)": searcher.keyword,
        "hybrid (vector + BM25)": searcher.hybrid,
        "hybrid + rerank": searcher.hybrid_rerank,
    }

    ranks = {name: [] for name in methods}
    rows, misses = [], []
    for q in questions:
        articles = [a.strip() for a in q["source_articles"].split(";")]
        cells = []
        for name, search in methods.items():
            chunks = search(q["question"], k=K)
            rank = first_hit(chunks, articles)
            ranks[name].append(rank)
            cells.append(str(rank) if rank else "MISS")
            if not rank:
                got = ", ".join(c["article_number"] for c in chunks)
                misses.append(f"- {q['id']} ({name}): wanted {', '.join(articles)}, got {got}")
        print(f"{q['id']} {' '.join(f'{c:>4}' for c in cells)}  {q['question'][:60]}")
        rows.append(f"| {q['id']} | {q['kind']} | {q['question']} | {', '.join(articles)} | " + " | ".join(cells) + " |")

    n = len(questions)
    summary = ["| Method | Hit@5 | Hit@1 | MRR@5 |", "|---|---|---|---|"]
    for name, rs in ranks.items():
        hit5 = sum(r is not None for r in rs)
        hit1 = sum(r == 1 for r in rs)
        mrr = sum(1 / r for r in rs if r) / n
        summary.append(f"| {name} | {hit5}/{n} ({hit5 / n:.0%}) | {hit1}/{n} ({hit1 / n:.0%}) | {mrr:.2f} |")

    kinds = sorted({q["kind"] for q in questions})
    by_kind = ["| Kind | Questions | " + " | ".join(methods) + " |", "|---|---|" + "---|" * len(methods)]
    for kind in kinds:
        idx = [i for i, q in enumerate(questions) if q["kind"] == kind]
        hits = [f"{sum(ranks[m][i] is not None for i in idx)}/{len(idx)}" for m in methods]
        by_kind.append(f"| {kind} | {len(idx)} | " + " | ".join(hits) + " |")

    print("\n" + "\n".join(summary) + "\n\n" + "\n".join(by_kind))
    RESULTS.write_text("\n".join([
        "# Retrieval hit rate", "",
        (f"{n} answerable questions from rag_test_questions.csv, top {K} chunks each. "
         "A hit means a chunk from the right article is in the top 5. "
         "MRR@5 is the average of 1 / rank of the first hit (0 for a miss)."), "",
        *summary, "", "## Hit@5 by question kind", "", *by_kind, "",
        "## Misses", "", *(misses or ["None."]), "",
        "## Rank of the first hit per question", "",
        "| # | Kind | Question | Source | " + " | ".join(methods) + " |",
        "|---|---|---|---|" + "---|" * len(methods), *rows,
    ]) + "\n", encoding="utf-8")
    print(f"\nWrote {RESULTS.name}")


if __name__ == "__main__":
    main()
