# RAG evaluation report

The Lumora Workspace Knowledge base assistant answers support questions from 47 synthetic articles (186 chunks). It retrieves the top 5 chunks with hybrid search (pgvector + BM25, merged with Reciprocal Rank Fusion) and a cross-encoder reranker, then Claude Opus 5.5 answers from those chunks with article citations. This report covers how it was evaluated and what was found. Run date: 2026-11-02.

## What was done

1. **Test set** (`rag_test_questions.csv`): 40 questions, each with an expected answer, its source article(s) and the key facts a good answer must contain. 35 are answerable. They cover 35 of the 47 articles and are tagged by type: plain fact, paraphrase in a customer's words, reasoning (apply a rule), version/date, multi-article. 5 can't be answered from the articles, and each sits close to a real article (pricing, Outlook sync, EU data residency, HIPAA, an Android crash) to tempt the model to guess. Every key fact was checked against its article by script.
2. **Retrieval hit rate** (`retrieval_hit_rate.py`): is a chunk from the right article in the top 5? Four methods compared.
3. **LLM judge** (`prompts/rag_answer_judge_v1.md`): two independent 1–5 scores, with 4 or 5 as a pass. **Groundedness**: is every claim supported by the retrieved chunks (not by the judge's own knowledge)? **Correctness**: does the answer match the reference? On unanswerable questions, a refusal is correct.
4. **Judge hand check** (`rag_judge_handcheck.csv`): 10 fixed answers, 7 with a planted flaw (a value from the wrong table column, a fact that wasn't retrieved, an invented menu path, an iOS issue extended to Android, "planned" changed to "fixed", a wrong refusal, an answer that misses the main point), each labelled by hand before the judge ran.
5. **One change** (`topk_experiment.md`): top-k 5 → 3, all 40 questions answered and judged again.

## Metrics

| Measure | Result |
|---|---|
| Right article in top 5, 35 answerable (vector / BM25 / hybrid / hybrid + rerank) | 35/35 for all four |
| Right article ranked 1st (same order) | 33 / 34 / 34 / **35** of 35 |
| Judge agrees with hand labels (groundedness / correctness) | 10/10 / 10/10 |
| End to end, top-k 5: groundedness / correctness pass, all 40 | **40/40 / 40/40** (mean 4.95 / 4.85) |
| Unanswerable questions correctly refused | 5/5 |
| Top-k 3: groundedness / correctness pass | 38/40 / 38/40, with 40% less context |

**Caveat:** a perfect score at top-k 5 says more about the test set than the system. I wrote the questions after reading the articles, so they share its wording, and the judge hand check used flaws I planted myself.

## Three failures (all at top-k 3)

In each one, the chunk with the answer ranked 4th, so cutting to 3 dropped it. The reranker puts the *Symptoms* section of a troubleshooting article first because it is worded like the question, and the fix lands in a sibling chunk below it.

1. **Q24 "The browser freezes when I filter a table with 200,000 rows."** The *Resolution* chunk (View settings > Performance > Filter on server) was cut. The answer was honest ("the articles don't explain how to turn server-side filtering on"), so groundedness stayed at 5, but correctness fell to 3. Grounded is not the same as useful.
2. **Q31 "When will the iPad landscape layout be fixed?"** The *Status* chunk (fix planned for 2026.11.2) was cut. The answer opened with **"There's no fix date yet"**: it turned "the excerpts don't say" into a false product claim (groundedness 3, correctness 3). The key-fact check missed this, because the fix date wasn't listed as a key fact. Only the judge caught it.
3. **Q32 "Can we restore a project bulk-edited 45 days ago?"** The chunk saying task field changes can be reverted with no time limit was cut. The answer got the main point right (no, outside the 30-day window) but called customer exports **"the only other option"**, which steers the agent away from the fix that works (groundedness 3, correctness 4).

## What I'd fix next

1. **Retrieve by article, not just by chunk.** When an article's chunks dominate the results, add its *Resolution* and *Status* sections. This should fix all three failures (untested), and two gaps that already exist at top-k 5: Q03 never retrieves KA-0005's *Unlock a user* chunk, and Q06 never retrieves KA-0008's *Status* chunk with ENG-4471.
2. **Answer prompt v2: "not in the excerpts" is not "doesn't exist".** Add a rule against stating absences ("no date yet", "the only option") as facts, and re-test on Q31 and Q32 at top-k 3, where the failures are known to occur.
3. **Make the test set harder.** It is at its ceiling. Add questions in the wording of the real sample Cases, cover the 12 articles with no question, add fix dates and statuses as key facts, and run each setting twice so run-to-run variation can be told apart from a real change.
