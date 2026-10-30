# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic", "fastembed", "psycopg[binary]", "pgvector", "numpy"]
# ///
"""Compare vector search, hybrid search, and hybrid + rerank on 10 questions.

For each question and each search method:
  1. Retrieve 5 chunks.
  2. Retrieval check: does one of them contain the key fact?
  3. Ask Claude to answer from those 5 chunks (same prompt as rag_answer.py).
  4. Answer check: does the answer contain the key fact, and are its citations valid?

Usage (database running, chunks loaded):
    export ANTHROPIC_API_KEY=sk-ant-...
    uv run experiments/compare_retrieval.py

Without an API key it runs only the retrieval check. Results go to
experiments/retrieval_comparison.md. With a key it makes 30 Claude calls.
"""

import os
import re
from pathlib import Path

from hybrid_search import Searcher
from rag_answer import build_prompt, generate

RESULTS = Path(__file__).parent / "retrieval_comparison.md"

# (question, article(s) that answer it, key facts: the answer should contain at least one)
# Half use exact terms (error codes, IDs, versions), where keyword search should help.
QUESTIONS = [
    ("What does the payment error currency_not_supported mean?", ["KA-0033"], ["merchant account", "enable the currency"]),
    ("What is ENG-4388?", ["KA-0022"], ["scheduled"]),
    ("Our SAML login fails with Audience mismatch. How do I fix it?", ["KA-0007"], ["case-sensitive", "trailing slash"]),
    ("Which HTTP header carries the webhook signature?", ["KA-0019"], ["X-Lumora-Signature"]),
    ("The iOS app closes at the splash screen on version 2.3.1.", ["KA-0040"], ["2.3.2"]),
    ("Our custom domain has said Certificate pending for over an hour.", ["KA-0044"], ["CAA"]),
    ("Teammates' edits show up half a minute late. How do we fix it?", ["KA-0029"], ["443", "120 seconds", "TLS inspection"]),
    ("The payment log shows test_mode_key_in_live.", ["KA-0033"], ["live key"]),
    ("How many API requests per minute does the Business plan allow?", ["KA-0018", "KA-0001"], ["300"]),
    ("CSV export opens in Excel with everything in one column.", ["KA-0021"], ["Text/CSV", "Excel compatible"]),
]


def norm(text):
    """Lowercase and ignore dashes, stars and backticks, so "case sensitive" matches "case-sensitive"."""
    return re.sub(r"[\s\-*`]+", " ", text.lower())


def has_fact(text, keys):
    return any(norm(k) in norm(text) for k in keys)


def main():
    searcher = Searcher()
    methods = {
        "vector": searcher.vector,
        "hybrid (vector + BM25)": searcher.hybrid,
        "hybrid + rerank": searcher.hybrid_rerank,
    }
    use_claude = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if not use_claude:
        print("No ANTHROPIC_API_KEY: checking retrieval only, no answers.\n")

    totals = {m: {"retrieved": 0, "answered": 0, "cited": 0} for m in methods}
    rows, details = [], []
    for n, (question, articles, keys) in enumerate(QUESTIONS, start=1):
        print(f"Q{n}: {question}")
        details += [f"## Q{n}. {question}", "", f"Expected: {' or '.join(keys)} ({', '.join(articles)})", ""]
        cells = []
        for name, search in methods.items():
            chunks = search(question)
            retrieved = any(c["article_number"] in articles and has_fact(c["content"], keys) for c in chunks)
            totals[name]["retrieved"] += retrieved
            cell = "found" if retrieved else "MISSED"

            details += [f"### {name}: fact {'found' if retrieved else 'not found'} in the 5 chunks", ""]
            details += [f"- {c['article_number']} {c['content'].splitlines()[0]}" for c in chunks] + [""]

            if use_claude:
                answer = generate(build_prompt(question, [(c["article_number"], c["title"], c["content"]) for c in chunks]))
                answered = has_fact(answer, keys)
                cited = set(re.findall(r"KA-\d{4}", answer))
                valid = bool(cited) and cited <= {c["article_number"] for c in chunks}
                totals[name]["answered"] += answered
                totals[name]["cited"] += valid
                cell += f" / {'yes' if answered else 'no'}"
                details += [f"Answer ({'has' if answered else 'missing'} the fact, citations "
                            f"{'OK' if valid else 'NOT OK'}):", "", *[f"> {line}" for line in answer.splitlines()], ""]
            cells.append(cell)
            print(f"  {name:24} {cell}")
        rows.append(f"| Q{n} | {question} | " + " | ".join(cells) + " |")

    names = list(methods)
    summary = ["| Method | Fact in the 5 chunks | Fact in Claude's answer | Citations valid |", "|---|---|---|---|"]
    for name, t in totals.items():
        answer_cols = f"{t['answered']}/10 | {t['cited']}/10" if use_claude else "not run | not run"
        summary.append(f"| {name} | {t['retrieved']}/10 | {answer_cols} |")
    print("\n" + "\n".join(summary))

    cell_note = "Each cell: was the fact in the 5 chunks / was it in Claude's answer." if use_claude \
        else "Each cell: was the fact in the 5 chunks (no API key, so no answers)."
    RESULTS.write_text("\n".join([
        "# Vector vs hybrid vs hybrid + rerank", "",
        "10 questions, top 5 chunks each. The answer prompt is the same as rag_answer.py.", "",
        *summary, "", cell_note, "",
        "| # | Question | " + " | ".join(names) + " |", "|---|---|" + "---|" * len(names), *rows, "",
        *details,
    ]) + "\n", encoding="utf-8")
    print(f"\nWrote {RESULTS.name}")


if __name__ == "__main__":
    main()
