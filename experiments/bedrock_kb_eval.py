# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic", "pydantic", "boto3[crt]>=1.43.64", "fastembed", "psycopg[binary]", "pgvector", "numpy"]
# ///
"""Our own RAG vs Bedrock's managed Knowledge Base, on the week 10 test set (rag_test_questions.csv).

Three arms, same 40 questions:
  own      Our build: pgvector + BM25 hybrid search + cross-encoder rerank, top 5 chunks,
           then rag_answer.py's prompt and Claude.
  kb       Bedrock Managed KB `Retrieve`, top 5 chunks, then the SAME prompt and Claude.
           Only retrieval differs from `own`, so this is the fair comparison of search quality.
  agentic  Bedrock `AgenticRetrieveStream` with generateResponse: AWS plans, retrieves,
           reranks and writes the answer with its managed model. This is the fully managed
           option, with nothing of ours in the loop.

For each arm and question:
  - Retrieval (35 answerable): is a chunk from the right article there, at what rank,
    and which key facts appear in the chunks?
  - Answer, scored by the same judge (prompts/rag_answer_judge_v1.md) against the chunks
    that arm retrieved. 4 or 5 is a pass.
  - Retrieval latency.

Usage (KB built with bedrock_kb_setup.py or in the console):
    export ANTHROPIC_API_KEY=sk-ant-...
    uv run experiments/bedrock_kb_eval.py --kb-id ABC123 --region eu-west-1   # kb + agentic
    uv run experiments/bedrock_kb_eval.py --only Q01,Q24 ...                  # quick check
    uv run experiments/bedrock_kb_eval.py --arms own,kb,agentic ...           # also re-run our build

By default our own build is not re-run: compare with its saved week 10 results in
topk_results.md (top-k 5). `own` needs the database from compose.yaml (Docker).

Without ANTHROPIC_API_KEY: retrieval checks only (the agentic arm still answers, but nothing is graded).
Results go to experiments/bedrock_kb_results.md, raw agentic stream events to
experiments/.bedrock_kb_raw.jsonl (for debugging, not committed).
"""

import argparse
import csv
import json
import os
import re
import sys
import time
from pathlib import Path

import boto3
from botocore.config import Config

sys.path.insert(0, str(Path(__file__).parent.parent / "prompts"))
from case_prompts import grade_rag_answer
from compare_retrieval import norm
from rag_answer import build_prompt, generate

HERE = Path(__file__).parent
STATE = HERE / ".bedrock_kb.json"
RESULTS = HERE / "bedrock_kb_results.md"
RAW = HERE / ".bedrock_kb_raw.jsonl"
RUNS = HERE / "bedrock_kb_runs.json"      # every arm's chunks and answers, saved by each AWS run
MANUAL = HERE / "bedrock_kb_manual.json"  # answers and grades written by hand (see --manual)
K = 5
PASS = 4
ARMS = ("own", "kb", "agentic")
LABELS = {"own": "Own build (hybrid + rerank)", "kb": "Bedrock KB Retrieve + our prompt",
          "agentic": "Bedrock agentic, managed answer"}
ARTICLE_ID = re.compile(r"KA-\d{4}")


def article_of(*parts):
    """The article ID found in a result's location / metadata (the S3 key is KA-0001-....md)."""
    m = ARTICLE_ID.search(json.dumps(parts, default=str))
    return m.group(0) if m else "?"


class Bedrock:
    def __init__(self, kb_id=None, region=None):
        """KB from --kb-id/--region (e.g. built in the console), else from bedrock_kb_setup.py's state file."""
        if not kb_id:
            if not STATE.exists():
                raise SystemExit("No KB: pass --kb-id and --region, or run bedrock_kb_setup.py first.")
            state = json.loads(STATE.read_text())
            kb_id, region = state["knowledge_base_id"], region or state["region"]
        self.kb_id = kb_id
        self.client = boto3.client("bedrock-agent-runtime", region_name=region,
                                   config=Config(retries={"max_attempts": 6, "mode": "adaptive"}))

    def retrieve(self, question):
        results = self.client.retrieve(
            knowledgeBaseId=self.kb_id, retrievalQuery={"text": question},
            retrievalConfiguration={"managedSearchConfiguration": {"numberOfResults": K}},  # defaults otherwise
        )["retrievalResults"]
        return [{"article_number": article_of(r.get("location"), r.get("metadata")),
                 "content": r["content"].get("text", ""), "score": r.get("score")} for r in results]

    def agentic(self, question, qid):
        """Fully managed: retrieve and answer. Returns (answer, chunks)."""
        resp = self.client.agentic_retrieve_stream(
            messages=[{"role": "user", "content": {"text": question}}],
            retrievers=[{"configuration": {"knowledgeBase": {"knowledgeBaseId": self.kb_id}}}],
            # AWS's own planner/answer model and reranker: the fully managed option, nothing of ours.
            agenticRetrieveConfiguration={"foundationModelType": "MANAGED", "rerankingModelType": "MANAGED"},
            generateResponse=True,
        )
        events, result = [], None
        for event in resp["stream"]:
            events.append(event)
            if "result" in event:  # the final event: the whole answer and the chunks it was built from
                result = event["result"]
            for key, value in event.items():
                if key.endswith("Exception"):
                    raise RuntimeError(f"AgenticRetrieveStream {key}: {value.get('message')}")
        with RAW.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"id": qid, "events": events}, default=str) + "\n")
        if result is None:
            raise RuntimeError(f"{qid}: AgenticRetrieveStream ended without a result event")
        chunks = [{"article_number": article_of(r.get("metadata")), "content": r["content"].get("text", "")}
                  for r in result.get("results", [])]
        return result.get("generatedResponse", {}).get("answer", "").strip(), chunks


def first_hit(chunks, articles):
    for rank, c in enumerate(chunks, start=1):
        if c["article_number"] in articles:
            return rank
    return None


def pct(n, d):
    return f"{n}/{d} ({n / d:.0%})" if d else "n/a"


def run_arm(arm, q, retrievers, use_claude):
    articles = [a.strip() for a in q["source_articles"].split(";")]
    keys = [k.strip() for k in q["key_facts"].split(";") if k.strip()]
    started = time.time()
    answer = None
    if arm == "own":
        chunks = retrievers["own"].hybrid_rerank(q["question"], k=K)
    elif arm == "kb":
        chunks = retrievers["kb"].retrieve(q["question"])
    else:
        answer, chunks = retrievers["kb"].agentic(q["question"], q["id"])
    seconds = time.time() - started
    if arm != "agentic" and use_claude:
        answer = generate(build_prompt(q["question"], [(c["article_number"], "", c["content"]) for c in chunks]))
    text = norm(" ".join(c["content"] for c in chunks))
    grade = None
    if use_claude and answer:
        grade = grade_rag_answer(q["question"], [(c["article_number"], c["content"]) for c in chunks],
                                 q["expected_answer"], answer)
    return {"rank": first_hit(chunks, articles), "facts_found": [k for k in keys if norm(k) in text],
            "facts_total": len(keys), "context_chars": sum(len(c["content"]) for c in chunks),
            "chunks": [c["article_number"] for c in chunks], "seconds": seconds, "answer": answer, "grade": grade,
            "chunk_texts": [c["content"] for c in chunks]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arms", default="kb,agentic", help="any of own,kb,agentic")
    parser.add_argument("--only", help="comma-separated question IDs, e.g. Q01,Q24 (for a quick check)")
    parser.add_argument("--kb-id", help="Knowledge Base ID, if built in the console")
    parser.add_argument("--region", help="the KB's region (default: your AWS config)")
    parser.add_argument("--manual", action="store_true", help=(
        "no AWS or API calls: rebuild the report from bedrock_kb_runs.json, taking the kb answers and all "
        "grades from bedrock_kb_manual.json (written by Claude in a chat session instead of the API)"))
    args = parser.parse_args()
    arms = [a for a in ARMS if a in args.arms.split(",")]

    with (HERE / "rag_test_questions.csv").open(encoding="utf-8") as f:
        questions = list(csv.DictReader(f))
    if args.only:
        questions = [q for q in questions if q["id"] in args.only.split(",")]
    if args.manual:
        return report(questions, *load_manual(questions), how=(
            "The kb answers and every grade were written by Claude Opus 5.5 in a Claude Code chat session, not through "
            "the API: the kb answers first, blind (question and chunks only, no reference answers), following "
            "rag_answer.py's system prompt; then the grades, following prompts/rag_answer_judge_v1.md."))
    use_claude = bool(os.environ.get("ANTHROPIC_API_KEY"))
    if not use_claude:
        print("No ANTHROPIC_API_KEY: retrieval checks only, nothing graded.\n")

    retrievers = {}
    if "own" in arms:
        from hybrid_search import Searcher
        retrievers["own"] = Searcher()
    if {"kb", "agentic"} & set(arms):
        retrievers["kb"] = Bedrock(args.kb_id, args.region)
    RAW.unlink(missing_ok=True)

    results = {a: {} for a in arms}
    for q in questions:
        line = [q["id"]]
        for arm in arms:
            r = results[arm][q["id"]] = run_arm(arm, q, retrievers, use_claude)
            cell = f"{arm}: rank {r['rank'] or '-'} {r['seconds']:.1f}s"
            if r["grade"]:
                cell += f" G{r['grade'].groundedness} C{r['grade'].correctness}"
            line.append(cell)
        print("  ".join(line), flush=True)

    RUNS.write_text(json.dumps({a: {qid: {k: v for k, v in r.items() if k != "grade"} for qid, r in rs.items()}
                                for a, rs in results.items()}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Saved chunks and answers to {RUNS.name}")
    report(questions, arms, results, how=(
        "`own` and `kb` use rag_answer.py's prompt and Claude through the API; `agentic` is AWS's managed answer. "
        "Every answer is scored by prompts/rag_answer_judge_v1.md against the chunks its arm retrieved."
        if use_claude else "No API key: retrieval checks only, nothing graded."))


def load_manual(questions):
    """Saved runs plus hand-written answers and grades -> (arms, results) in the same shape as a live run."""
    from types import SimpleNamespace

    runs = json.loads(RUNS.read_text(encoding="utf-8"))
    manual = json.loads(MANUAL.read_text(encoding="utf-8")) if MANUAL.exists() else {}
    arms = [a for a in ARMS if a in runs]
    results = {a: {} for a in arms}
    for a in arms:
        for q in questions:
            r = dict(runs[a][q["id"]])
            if a != "agentic" and not r.get("answer"):
                r["answer"] = manual.get("answers", {}).get(a, {}).get(q["id"])
            g = manual.get("grades", {}).get(a, {}).get(q["id"])
            r["grade"] = SimpleNamespace(**g) if g else None
            results[a][q["id"]] = r
    return arms, results


def report(questions, arms, results, how):
    use_claude = any(r["grade"] for rs in results.values() for r in rs.values())
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    unanswerable = [q for q in questions if q["kind"] == "unanswerable"]
    n = len(answerable)
    table = ["| Measure | " + " | ".join(LABELS[a] for a in arms) + " |", "|---|" + "---|" * len(arms)]

    def add(label, cell):
        table.append(f"| {label} | " + " | ".join(cell(results[a]) for a in arms) + " |")

    add(f"Right article in the chunks ({n} answerable)", lambda rs: pct(sum(rs[q["id"]]["rank"] is not None for q in answerable), n))
    add("Right article ranked 1st", lambda rs: pct(sum(rs[q["id"]]["rank"] == 1 for q in answerable), n))
    add("MRR", lambda rs: f"{sum(1 / rs[q['id']]['rank'] for q in answerable if rs[q['id']]['rank']) / n:.2f}" if n else "n/a")
    add("Key facts present in the chunks", lambda rs: pct(sum(len(rs[q["id"]]["facts_found"]) for q in answerable),
                                                          sum(rs[q["id"]]["facts_total"] for q in answerable)))
    add("Questions with every key fact in the chunks",
        lambda rs: pct(sum(len(rs[q["id"]]["facts_found"]) == rs[q["id"]]["facts_total"] for q in answerable), n))
    add("Chunks per question (mean)", lambda rs: f"{sum(len(r['chunks']) for r in rs.values()) / len(rs):.1f}")
    add("Context per question (characters, mean)", lambda rs: f"{sum(r['context_chars'] for r in rs.values()) / len(rs):,.0f}")
    add("Retrieval latency, median (s)", lambda rs: f"{sorted(r['seconds'] for r in rs.values())[len(rs) // 2]:.2f}")
    if use_claude:
        def graded(rs, qs):
            return [rs[q["id"]]["grade"] for q in qs if rs[q["id"]]["grade"]]

        for label, qs in ((f"all {len(questions)}", questions), (f"{n} answerable", answerable),
                          (f"{len(unanswerable)} unanswerable", unanswerable)):
            add(f"Groundedness pass, {label}", lambda rs, qs=qs: pct(sum(g.groundedness >= PASS for g in graded(rs, qs)), len(graded(rs, qs))))
            add(f"Correctness pass, {label}", lambda rs, qs=qs: pct(sum(g.correctness >= PASS for g in graded(rs, qs)), len(graded(rs, qs))))
        add("Mean groundedness / correctness", lambda rs: (
            f"{sum(g.groundedness for g in graded(rs, questions)) / max(len(graded(rs, questions)), 1):.2f} / "
            f"{sum(g.correctness for g in graded(rs, questions)) / max(len(graded(rs, questions)), 1):.2f}"))

    per_q = ["| # | Kind | " + " | ".join(arms) + " |", "|---|---|" + "---|" * len(arms)]
    details = []
    for q in questions:
        cells = []
        for a in arms:
            r = results[a][q["id"]]
            g = r["grade"]
            cell = f"rank {r['rank'] or '–'}, facts {len(r['facts_found'])}/{r['facts_total']}"
            cells.append(cell + (f", G{g.groundedness} C{g.correctness}" if g else ""))
        per_q.append(f"| {q['id']} | {q['kind']} | " + " | ".join(cells) + " |")
        details.append(f"## {q['id']}. {q['question']}\n")
        for a in arms:
            r = results[a][q["id"]]
            g = r["grade"]
            details += [f"### {LABELS[a]}: {', '.join(r['chunks']) or 'no chunks'}", ""]
            details += [f"> {line}" for line in (r["answer"] or "(no answer)").splitlines()] + [""]
            if g:
                details += [(f"Groundedness {g.groundedness}, correctness {g.correctness}. "
                            f"Unsupported: {'; '.join(g.unsupported_claims) or 'none'}"), ""]
                details += [f"> {line}" for line in g.reasoning.splitlines()] + [""]

    print("\n" + "\n".join(table))
    RESULTS.write_text("\n".join([
        "# Own RAG vs Bedrock Managed Knowledge Base", "",
        (f"Week 10 test set, {len(questions)} questions, top {K} chunks. Run date: {time.strftime('%Y-%m-%d')}. {how} "
        "Every answer is scored against the chunks its own arm retrieved; 4 or 5 is a pass."), "",
        *table, "", "## Per question", "", *per_q, "", *details,
    ]) + "\n", encoding="utf-8")
    print(f"\nWrote {RESULTS.name}")


if __name__ == "__main__":
    main()
