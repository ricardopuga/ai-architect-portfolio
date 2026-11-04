# ADR 0002: Use Claude Opus 5.5 for every generation step, with effort as the cost lever

- **Status:** Accepted, with an open follow-up (no cheaper model has been compared)
- **Recorded:** 2026-11-04
- **Applies to:** the Agent CLI, the MCP server's `draft_reply`, the RAG answer script, the prompts in `prompts/`, and the LLM judge

## Context

The assistant uses a language model in four places:

| Step | What the model does | How hard |
|---|---|---|
| Agent loop ([agent.py](../../src/casehandlersf/agent.py)) | Decides which tools to call, in what order, and when to stop; must not overclaim | Hardest: multi-step judgement with tools |
| Reply drafting (`draft_reply`) | Writes a customer reply from 5 retrieved chunks, citing each fact | Easy: the facts are in the prompt |
| Case summary and classification ([prompts](../../../prompts/README.md)) | Fixed formats and fixed labels | Easy |
| LLM judge | Scores answers for groundedness and correctness | Medium: must notice subtle unsupported claims |

What mattered, in order: correct and grounded output (wrong answers reach customers), safe behaviour in the agent loop, then cost and latency. Volume is low today: one support agent, a few dozen requests a day.

Two embedding and reranking models are also used. They are small, run locally and are out of scope here; see [ADR 0001](0001-vector-store-pgvector.md).

## Decision

Use **`claude-opus-5-5` for all four steps**, and tune cost with the `effort` setting rather than by switching models:

- **Effort `low`** for drafting, summaries and classification: the work is reading, not reasoning.
- **Effort `medium`** for the agent loop and the judge.

Every call opts into **server-side fallback**: if a safety check declines a request, it is retried on Anthropic's recommended fallback model, and the agent logs which model actually answered.

## Options considered

Prices are Anthropic first-party API rates per million tokens (input / output).

| Option | For | Against |
|---|---|---|
| **Opus 5.5 everywhere** (chosen), $4 / $20 | Strongest generally available model short of Fable; one model to prompt, test and cache for; effort gives a cost range inside one model | Twice Sonnet's price; easy steps pay for capability they don't use |
| Sonnet 5.5, $2 / $10 | Half the price; built for everyday agent and enterprise work | Not yet measured on this test set or the agent review. A second model means a second cache namespace and a second prompt baseline |
| Haiku 5.5, $0.10 / $0.50 | About 40 times cheaper than Opus; good candidate for classification and summaries at volume | Weakest at multi-step tool use; no server-side fallback on refusals. Not measured |
| Fable 5.1, $10 / $50 | Most capable model | 2.5 times Opus's price. Nothing in the results shows Opus is the limit |
| Mixed: Opus for the agent, a cheaper model for easy steps | Lowest cost per request at scale | More moving parts, before measurements show the saving is needed |

Anthropic's own guidance points the same way: before building a multi-model setup, measure the most capable model at lower effort, because one model keeps one cache and lower effort often holds quality.

## Evidence

- **RAG answers:** 40/40 groundedness and correctness at top-k 5 ([RAG eval report](../../../experiments/RAG_EVAL_REPORT.md)).
- **Agent:** behaved correctly in 10 of 10 review runs, including a missing Case, an out-of-scope Case and two writes ([agent review](../../../experiments/agent_review_results.md)).
- **Cost of the agent:** those 10 runs used 78,546 input and 6,994 output tokens, about **$0.45 in total, or $0.045 per question**, before any prompt caching.
- **Judge:** agreed with hand labels on 10 of 10 answers, 7 of which had planted flaws.

**Not measured:** any model other than Opus 5.5 on these tasks. The decision is a sensible default, not a proven optimum.

## Consequences

- **Good:** one model to reason about; the effort setting can be raised on a hard route without changing anything else.
- **Bad:** at higher volume, easy steps cost more than they need to. At 10,000 agent questions a month, the agent alone costs roughly $450 a month at current measurements.
- **Risk:** the judge is the same model as the answerer, so it may favour its own style. The 10-answer hand check is the only guard so far.
- **Risk:** the model ID is set separately in several files (`agent.py`, `mcp_server.py`, `rag_answer.py`, `case_prompts.py`). Moving to another model means changing them together and re-running both evals.

## Revisit when

- Volume grows enough that cost matters (a few thousand requests a day). First run the RAG eval and the agent review on Sonnet 5.5 for drafting and classification, and keep Opus wherever scores drop.
- A new model is released. Re-run both evals before switching; never switch on benchmarks alone.
- The judge disagrees with a human on more than an occasional answer. Then try a different model as judge.
