# Experiment: top-k 5 → 3

## The change

One setting: the number of chunks retrieved and given to Claude, from 5 (current, `TOP_K` in `rag_answer.py`) to 3. Retrieval stays hybrid + rerank, with the same prompt, model and judge. Hybrid + rerank sorts its 20 candidates and keeps the first k, so the top 3 is exactly the first 3 of the top 5. Nothing else can differ.

**Why this change:** at top-k 5 the right article was retrieved for all 35 answerable questions (`retrieval_hit_rate.md`), so the open question is whether 5 chunks are needed. Fewer chunks mean a shorter, cheaper prompt and less unrelated text for the model to draw on. The risk is losing a second or third chunk the answer needs.

**Run:** `uv run experiments/topk_test.py`. Results are in `topk_results.md`.

## Retrieval (run 2026-11-02, no API calls)

| Measure | top-k 5 | top-k 3 |
|---|---|---|
| Right article in the chunks (35 answerable) | 35/35 (100%) | 35/35 (100%) |
| Key facts present in the chunks (35 answerable) | 57/59 (97%) | 55/59 (93%) |
| Questions with every key fact in the chunks | 33/35 (94%) | 31/35 (89%) |
| Context per question (characters, mean) | 2,396 | 1,426 (−40%) |

Article-level hit rate doesn't change, but 2 questions lose a key fact:

| # | Lost at top-k 3 | Why |
|---|---|---|
| Q24 (browser freezes filtering 200,000 rows) | **Filter on server**, the main fix | KA-0028's *Resolution* chunk ranks 4th, behind *Symptoms*, *Notes* and *Why it happens* |
| Q27 (Delete on a custom field does nothing) | ENG-4502 | KA-0035's *Cause* chunk ranks 5th. The fix (the Usage tab, in *Resolution*) ranks 2nd and is kept |

**Pattern:** for questions that describe a symptom, the reranker ranks the article's *Symptoms* section first, because it is worded like the question. The fix sits in a sibling chunk lower down. Troubleshooting articles spread one answer over several chunks, so cutting k hits them first. The 2 losses are 2 of the 7 paraphrase questions, which are the ones worded like a customer.

**Gaps that exist at top-k 5 too** (not caused by the change, but found by this check):

- Q03 (locked out after 3 attempts): KA-0005's *Unlock a user* chunk isn't retrieved. A 2FA chunk (KA-0006) and a password reset chunk (KA-0004) take its places.
- Q06 ("Is this fixed yet?" for the SSO logout issue): KA-0008's *Status* chunk, with ENG-4471, isn't retrieved. The answer can still get "being fixed in 2026.11.1" from the *Cause* chunk.

## Answers and judge scores (run 2026-11-02, 160 Claude calls)

| Measure | top-k 5 | top-k 3 |
|---|---|---|
| Groundedness pass, all 40 | 40/40 | 38/40 |
| Correctness pass, all 40 | 40/40 | 38/40 |
| Correct refusals, 5 unanswerable | 5/5 | 5/5 |
| Mean groundedness / correctness | 4.95 / 4.85 | 4.83 / 4.75 |

Four answers scored lower at top-k 3. In each, the chunk that was cut (ranked 4th or 5th) held part of the answer:

| # | Chunk cut | What the top-k 3 answer did | Scores, 5 → 3 |
|---|---|---|---|
| Q24 | KA-0028 *Resolution* (Filter on server) | Said the articles don't explain how to turn server-side filtering on | G 5 → 5, C 5 → 3 |
| Q31 | KA-0041 *Status* (fix planned for 2026.11.2) | Opened with "There's no fix date yet" | G 5 → 3, C 5 → 3 |
| Q32 | KA-0042 *What users can restore themselves* (Activity tab revert) | Called customer exports "the only other option" | G 5 → 3, C 5 → 4 |
| Q27 | KA-0035 *Cause* (still in use; ENG-4502) | Still gave the fix (Usage tab), but called it "a known issue" with no excerpt saying so, and didn't explain that the field is still in use | G 5 → 4, C 5 → 4 |

The retrieval check flagged only Q24 and Q27. Q31 and Q32 kept their key facts, because the fix date and the Activity tab revert weren't listed as key facts. Only the judge caught them.

The 5 unanswerable questions were refused correctly at both settings, so fewer chunks didn't make refusals better or worse.

## Decision

Keep top-k 5. Top-k 3 saves 40% of the context, but 2 of 40 answers fail and 2 more get worse. In all 4 cases the cause is the chunk that was cut, not run-to-run variation. Two of the failures are worse than a missing fact: the answer presents the gap as a fact ("no fix date yet", "the only other option").
