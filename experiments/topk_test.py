# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic", "pydantic", "fastembed", "psycopg[binary]", "pgvector", "numpy"]
# ///
"""One change to the RAG pipeline: top-k 5 -> 3. Everything else stays the same.

Runs all 40 questions in rag_test_questions.csv with each top-k in K_VALUES.
Retrieval is hybrid + rerank. It sorts its 20 candidates by reranker score and
keeps the first k, so the top 3 is exactly the first 3 of the top 5: chunks are
retrieved once and sliced, and only the number of chunks changes.

For each question and each k:
  1. Retrieval: is a chunk from the right article there, and which of the
     question's key facts appear in the chunks? (35 answerable questions)
  2. With an API key: answer with rag_answer.py's prompt from those k chunks,
     then score the answer with the judge (prompts/rag_answer_judge_v1.md),
     against the same k chunks. 4 or 5 is a pass.

Usage (database running, chunks loaded):
    uv run experiments/topk_test.py               # no key: retrieval only
    export ANTHROPIC_API_KEY=sk-ant-...
    uv run experiments/topk_test.py               # 160 Claude calls

Results go to experiments/topk_results.md.
"""

import csv
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "prompts"))
from case_prompts import grade_rag_answer
from compare_retrieval import norm
from hybrid_search import Searcher
from rag_answer import build_prompt, generate

HERE = Path(__file__).parent
RESULTS = HERE / "topk_results.md"
K_VALUES = (5, 3)  # baseline first
PASS = 4


def run(q, chunks, use_claude):
    """Retrieval checks and, with a key, the answer and its grade, for one question and one k."""
    articles = [a.strip() for a in q["source_articles"].split(";")]
    keys = [k.strip() for k in q["key_facts"].split(";") if k.strip()]
    text = norm(" ".join(c["content"] for c in chunks))
    result = {
        "article_hit": any(c["article_number"] in articles for c in chunks),
        "facts_found": [k for k in keys if norm(k) in text],
        "facts_total": len(keys),
        "context_chars": sum(len(c["content"]) for c in chunks),
        "chunks": [f"{c['article_number']}#{c['id']}" for c in chunks],
        "answer": None,
        "grade": None,
    }
    if use_claude:
        result["answer"] = generate(build_prompt(q["question"], [(c["article_number"], c["title"], c["content"]) for c in chunks]))
        result["grade"] = grade_rag_answer(
            q["question"], [(c["article_number"], c["content"]) for c in chunks], q["expected_answer"], result["answer"]
        )
    return result


def pct(n, d):
    return f"{n}/{d} ({n / d:.0%})" if d else "n/a"


def main():
    with (HERE / "rag_test_questions.csv").open(encoding="utf-8") as f:
        questions = list(csv.DictReader(f))
    use_claude = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if not use_claude:
        print("No ANTHROPIC_API_KEY: retrieval checks only, no answers or grades.\n")

    searcher = Searcher()
    results = {k: {} for k in K_VALUES}
    for q in questions:
        top = searcher.hybrid_rerank(q["question"], k=max(K_VALUES))
        line = [q["id"]]
        for k in K_VALUES:
            r = results[k][q["id"]] = run(q, top[:k], use_claude)
            cell = f"k={k}: facts {len(r['facts_found'])}/{r['facts_total']}"
            if r["grade"]:
                cell += f" G{r['grade'].groundedness} C{r['grade'].correctness}"
            line.append(cell)
        print("  ".join(line))

    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    unanswerable = [q for q in questions if q["kind"] == "unanswerable"]
    summary = ["| Measure | " + " | ".join(f"top-k {k}" for k in K_VALUES) + " |", "|---|" + "---|" * len(K_VALUES)]

    def add(label, cell):
        summary.append(f"| {label} | " + " | ".join(cell(results[k]) for k in K_VALUES) + " |")

    add("Right article in the chunks (35 answerable)",
        lambda rs: pct(sum(rs[q["id"]]["article_hit"] for q in answerable), len(answerable)))
    add("Key facts present in the chunks (35 answerable)",
        lambda rs: pct(sum(len(rs[q["id"]]["facts_found"]) for q in answerable),
                       sum(rs[q["id"]]["facts_total"] for q in answerable)))
    add("Questions with every key fact in the chunks",
        lambda rs: pct(sum(len(rs[q["id"]]["facts_found"]) == rs[q["id"]]["facts_total"] for q in answerable),
                       len(answerable)))
    add("Context per question (characters, mean)",
        lambda rs: f"{sum(r['context_chars'] for r in rs.values()) / len(rs):,.0f}")

    if use_claude:
        def graded(rs, qs):
            return [rs[q["id"]]["grade"] for q in qs if rs[q["id"]]["grade"]]

        for label, qs in (("all 40", questions), ("35 answerable", answerable), ("5 unanswerable", unanswerable)):
            add(f"Groundedness pass, {label}",
                lambda rs, qs=qs: pct(sum(g.groundedness >= PASS for g in graded(rs, qs)), len(graded(rs, qs))))
            add(f"Correctness pass, {label}",
                lambda rs, qs=qs: pct(sum(g.correctness >= PASS for g in graded(rs, qs)), len(graded(rs, qs))))
        add("Mean groundedness / correctness, all 40",
            lambda rs: (f"{sum(g.groundedness for g in graded(rs, questions)) / len(graded(rs, questions)):.2f} / "
                        f"{sum(g.correctness for g in graded(rs, questions)) / len(graded(rs, questions)):.2f}"))
        refused = [f"{k}: {q['id']}" for k in K_VALUES for q in questions if results[k][q["id"]]["grade"] is None
                   and results[k][q["id"]]["answer"] is not None]
        if refused:
            summary.append(f"\nJudge refused (left out of the counts): {', '.join(refused)}")

    base, new = K_VALUES
    changed, details = [], []
    for q in questions:
        a, b = results[base][q["id"]], results[new][q["id"]]
        lost = [k for k in a["facts_found"] if k not in b["facts_found"]]
        ga, gb = a["grade"], b["grade"]
        moved = ga and gb and (verdict(ga.groundedness), verdict(ga.correctness)) != \
            (verdict(gb.groundedness), verdict(gb.correctness))
        if lost or moved or a["article_hit"] != b["article_hit"]:
            scores = (f" | G {ga.groundedness} → {gb.groundedness}, C {ga.correctness} → {gb.correctness}"
                      if ga and gb else "")
            changed.append(f"| {q['id']} | {q['kind']} | {q['question']} | "
                           f"{', '.join(lost) or 'none'}{scores} |")
        if use_claude:
            details.append(f"## {q['id']}. {q['question']}\n")
            for k in K_VALUES:
                r = results[k][q["id"]]
                g = r["grade"]
                details += [f"### top-k {k}: {', '.join(r['chunks'])}", ""]
                details += [f"> {line}" for line in (r["answer"] or "").splitlines()] + [""]
                if g:
                    details += [(f"Groundedness {g.groundedness}, correctness {g.correctness}. "
                                f"Unsupported: {'; '.join(g.unsupported_claims) or 'none'}"), ""]
                    details += [f"> {line}" for line in g.reasoning.splitlines()] + [""]

    header = "| # | Kind | Question | Key facts lost at top-k 3"
    header += " | Judge scores, 5 → 3 |" if use_claude else " |"
    print("\n" + "\n".join(summary))
    RESULTS.write_text("\n".join([
        "# Top-k 5 vs 3", "",
        ("One change: the number of hybrid + rerank chunks retrieved and given to Claude, 5 (current) vs 3. "
         "Top 3 is the first 3 of the top 5, so nothing else differs. "
         + ("Answers use rag_answer.py's prompt and are scored with prompts/rag_answer_judge_v1.md "
            "against the chunks they were given; 4 or 5 is a pass."
            if use_claude else "No API key, so retrieval checks only.")), "",
        *summary, "",
        "## Questions that changed", "",
        ("Lost key facts, a changed article hit, or a judge verdict that moved between pass and fail."), "",
        *([header, "|---|---|---|---|" + ("---|" if use_claude else ""), *changed] if changed else ["None."]), "",
        *details,
    ]) + "\n", encoding="utf-8")
    print(f"\nWrote {RESULTS.name}")


def verdict(score):
    return "pass" if score >= PASS else "fail"


if __name__ == "__main__":
    main()
