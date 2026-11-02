# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic", "pydantic", "fastembed", "psycopg[binary]", "pgvector", "numpy"]
# ///
"""Check the RAG answer judge (prompts/rag_answer_judge_v1.md) and use it.

The judge scores an answer 1-5 for groundedness (is every claim supported by
the retrieved chunks?) and correctness (does it match the reference answer in
rag_test_questions.csv?). A score of 4 or 5 counts as a pass.

Usage (database running, chunks loaded):
    export ANTHROPIC_API_KEY=sk-ant-...
    uv run experiments/rag_judge_test.py          # hand check: 10 Claude calls
    uv run experiments/rag_judge_test.py --all    # judge real answers: 80 Claude calls

Hand check: rag_judge_handcheck.csv holds 10 fixed answers, most with a planted
flaw (a value from the wrong column, a fact that wasn't retrieved, an invented
step, a wrong refusal...), and my pass/fail verdict for each score. The answers
are fixed so the check is repeatable; real answers change from run to run and
are nearly all good, so a judge that passes everything would look perfect on
them. Each answer is judged against the chunks hybrid + rerank retrieves for its
question. Results, with the judge's reasoning to read, go to
rag_judge_handcheck.md.

--all: answers all 40 questions with rag_answer.py's prompt and judges each.
Results go to rag_judge_results.md.
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "prompts"))
from case_prompts import grade_rag_answer
from hybrid_search import Searcher
from rag_answer import TOP_K, build_prompt, generate

HERE = Path(__file__).parent
QUESTIONS = HERE / "rag_test_questions.csv"
HANDCHECK = HERE / "rag_judge_handcheck.csv"
PASS = 4


def verdict(score):
    return "pass" if score >= PASS else "fail"


def read_csv(path):
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def judge(searcher, question, reference, answer):
    """Retrieve the chunks for the question and judge the answer against them."""
    chunks = searcher.hybrid_rerank(question, k=TOP_K)
    grade = grade_rag_answer(question, [(c["article_number"], c["content"]) for c in chunks], reference, answer)
    return chunks, grade


def chunk_list(chunks):
    return [f"- {c['article_number']} chunk {c['id']}: {c['content'].splitlines()[0]}" for c in chunks]


def hand_check(searcher, questions):
    agree = {"groundedness": 0, "correctness": 0}
    rows, details = [], []
    cases = read_csv(HANDCHECK)
    for case in cases:
        q = questions[case["question_id"]]
        chunks, grade = judge(searcher, q["question"], q["expected_answer"], case["answer"])
        if grade is None:
            print(f"{case['id']} judge refused")
            rows.append(f"| {case['id']} | {case['planted_flaw']} | {case['my_groundedness']} | refused | "
                        f"{case['my_correctness']} | refused |")
            continue
        g, c = verdict(grade.groundedness), verdict(grade.correctness)
        agree["groundedness"] += g == case["my_groundedness"]
        agree["correctness"] += c == case["my_correctness"]
        mark = lambda mine, theirs: theirs if mine == theirs else f"**{theirs}** (disagree)"
        print(f"{case['id']} G {grade.groundedness} {g:4} (mine {case['my_groundedness']:4})  "
              f"C {grade.correctness} {c:4} (mine {case['my_correctness']})")
        rows.append(f"| {case['id']} | {case['planted_flaw']} | {case['my_groundedness']} | "
                    f"{grade.groundedness} {mark(case['my_groundedness'], g)} | {case['my_correctness']} | "
                    f"{grade.correctness} {mark(case['my_correctness'], c)} |")
        details += [
            f"## {case['id']} ({case['question_id']}). {q['question']}", "",
            f"**Planted flaw:** {case['planted_flaw']}", "",
            "**Answer judged:**", "", *[f"> {line}" for line in case["answer"].splitlines()], "",
            "**Retrieved chunks:**", "", *chunk_list(chunks), "",
            f"**My verdict:** groundedness {case['my_groundedness']}, correctness {case['my_correctness']}. {case['why']}", "",
            (f"**Judge:** groundedness {grade.groundedness}, correctness {grade.correctness}. "
            f"Unsupported claims: {'; '.join(grade.unsupported_claims) or 'none'}"), "",
            *[f"> {line}" for line in grade.reasoning.splitlines()], "",
        ]
    n = len(cases)
    summary = [(f"Judge agrees with my verdict on groundedness {agree['groundedness']}/{n}, "
               f"correctness {agree['correctness']}/{n}.")]
    print("\n" + summary[0])
    (HERE / "rag_judge_handcheck.md").write_text("\n".join([
        "# RAG answer judge: hand check", "",
        f"{n} fixed answers judged with prompts/rag_answer_judge_v1.md. A score of {PASS} or 5 is a pass.", "",
        *summary, "",
        "| # | Planted flaw | My groundedness | Judge | My correctness | Judge |",
        "|---|---|---|---|---|---|", *rows, "", *details,
    ]) + "\n", encoding="utf-8")
    print("Wrote rag_judge_handcheck.md")


def judge_all(searcher, questions):
    by_kind = defaultdict(list)
    rows, details = [], []
    for q in questions.values():
        chunks = searcher.hybrid_rerank(q["question"], k=TOP_K)
        answer = generate(build_prompt(q["question"], [(c["article_number"], c["title"], c["content"]) for c in chunks]))
        grade = grade_rag_answer(q["question"], [(c["article_number"], c["content"]) for c in chunks],
                                 q["expected_answer"], answer)
        if grade is None:
            print(f"{q['id']} judge refused")
            rows.append(f"| {q['id']} | {q['kind']} | {q['question']} | refused | refused |")
            continue
        by_kind[q["kind"]].append(grade)
        print(f"{q['id']} G {grade.groundedness} C {grade.correctness}  {q['question'][:60]}")
        rows.append(f"| {q['id']} | {q['kind']} | {q['question']} | {grade.groundedness} | {grade.correctness} |")
        details += [
            f"## {q['id']}. {q['question']}", "",
            *[f"> {line}" for line in answer.splitlines()], "",
            (f"Groundedness {grade.groundedness}, correctness {grade.correctness}. "
            f"Unsupported claims: {'; '.join(grade.unsupported_claims) or 'none'}"), "",
            *[f"> {line}" for line in grade.reasoning.splitlines()], "",
        ]

    summary = ["| Kind | Answers | Groundedness pass | Correctness pass | Mean G | Mean C |", "|---|---|---|---|---|---|"]
    every = [g for grades in by_kind.values() for g in grades]
    for kind, grades in [*sorted(by_kind.items()), ("all", every)]:
        n = len(grades)
        summary.append(
            f"| {kind} | {n} | {sum(g.groundedness >= PASS for g in grades)}/{n} | "
            f"{sum(g.correctness >= PASS for g in grades)}/{n} | "
            f"{sum(g.groundedness for g in grades) / n:.1f} | {sum(g.correctness for g in grades) / n:.1f} |"
        )
    print("\n" + "\n".join(summary))
    (HERE / "rag_judge_results.md").write_text("\n".join([
        "# RAG answers scored by the judge", "",
        (f"All 40 questions, answered from the top {TOP_K} hybrid + rerank chunks with rag_answer.py's prompt, "
        f"then scored with prompts/rag_answer_judge_v1.md. A score of {PASS} or 5 is a pass."), "",
        *summary, "",
        "| # | Kind | Question | Groundedness | Correctness |", "|---|---|---|---|---|", *rows, "", *details,
    ]) + "\n", encoding="utf-8")
    print("Wrote rag_judge_results.md")


def main():
    questions = {q["id"]: q for q in read_csv(QUESTIONS)}
    searcher = Searcher()
    if "--all" in sys.argv:
        judge_all(searcher, questions)
    else:
        hand_check(searcher, questions)


if __name__ == "__main__":
    main()
