# Architecture decision records

The three decisions behind the Support Knowledge Assistant, in one file. Each one is also kept as its own file in [CaseHandlerSF/docs/adr/](CaseHandlerSF/docs/adr/README.md); this file is built from those, so edit them, not this one.

- [ADR 0001: Store Knowledge base embeddings in Postgres with pgvector](#adr-0001)
- [ADR 0002: Use Claude Opus 5.5 for every generation step, with effort as the cost lever](#adr-0002)
- [ADR 0003: A person approves every write the AI makes to Salesforce](#adr-0003)

---

<a id="adr-0001"></a>

## ADR 0001: Store Knowledge base embeddings in Postgres with pgvector

- **Status:** Accepted
- **Recorded:** 2026-11-04
- **Applies to:** the Knowledge base container and the MCP server's `search_knowledge` and `draft_reply` tools ([architecture](CaseHandlerSF/docs/architecture.md))

### Context

The assistant answers support questions from 47 Knowledge articles, cut into 186 heading-based chunks. Each chunk needs a 384-number embedding (`BAAI/bge-small-en-v1.5`, run locally) and must be searchable by meaning and by exact terms such as error codes (`test_mode_key_in_live`) and ticket numbers (`ENG-4388`).

What mattered:

- **Retrieval quality**, measured, not assumed. The answer can only be as good as what search finds.
- **Hybrid search.** Vector search alone missed a fix that keyword search and the merged list found ([retrieval comparison](experiments/retrieval_comparison.md)).
- **Few moving parts.** One developer, local Docker, no budget for a managed service.
- **A path to production** without rewriting the search code.

### Decision

Store chunks, metadata and embeddings in one Postgres table (`chunks`) using the pgvector extension, running in Docker (`pgvector/pgvector:pg17`).

Search is hybrid: pgvector does the vector half (cosine distance), BM25 keyword scoring runs in memory in Python, the two lists are merged with Reciprocal Rank Fusion, and a local cross-encoder reranks the top 20 down to 5 ([knowledge.py](CaseHandlerSF/src/casehandlersf/knowledge.py)).

### Options considered

| Option | For | Against |
|---|---|---|
| **Postgres + pgvector** (chosen) | One store for text, metadata and vectors, queried with SQL. Runs locally in Docker; managed Postgres with pgvector is available from the major clouds. Joins and filters (by article, product, permission) are plain SQL | No built-in BM25; keyword scoring has to live elsewhere. Needs an index tuned by hand at larger sizes |
| Dedicated vector database (managed or self-hosted) | Built for vector search at scale; some include hybrid search and filtering | Another service to run, secure and pay for. Text and metadata either duplicated or split across two stores. Nothing at 186 chunks needs it |
| In-memory only (numpy or FAISS in the app) | Fastest to build, nothing to run | Rebuilt on every start, not shared between processes, nothing to query or inspect |

### Evidence

On a 40-question test set (35 answerable, 5 deliberately not) ([RAG eval report](experiments/RAG_EVAL_REPORT.md)):

| Retrieval method | Right article in top 5 | Right article ranked 1st |
|---|---|---|
| Vector only (pgvector) | 35/35 | 33/35 |
| BM25 only | 35/35 | 34/35 |
| Hybrid | 35/35 | 34/35 |
| Hybrid + rerank (chosen) | 35/35 | 35/35 |

End to end at top-k 5, answers passed groundedness and correctness 40/40, and all 5 unanswerable questions were refused. The report's caveat applies here too: the questions were written after reading the articles, so these numbers flatter the system.

### Consequences

- **Good:** one store to back up and inspect (`psql`), SQL filters available when the Knowledge base gains permissions or product tags, and a standard managed-Postgres path to production.
- **Bad:** BM25 lives in the MCP server, which loads **every chunk into memory** on first search. That is fine for hundreds of chunks and wrong for hundreds of thousands.
- **Bad:** there is no vector index. Every query scans all 186 rows. Add an HNSW index before the table grows into the tens of thousands.
- **Risk:** the embedding model name is set in two places, [`embed_to_pgvector.py`](experiments/embed_to_pgvector.py) and [`knowledge.py`](CaseHandlerSF/src/casehandlersf/knowledge.py). If they drift apart, search quietly gets worse with no error.
- **Debt:** the database and its loader live under `experiments/`, although the MCP server depends on them at runtime.

### Revisit when

- The Knowledge base passes about 50,000 chunks, or BM25 start-up time becomes noticeable. Move keyword search into Postgres (full-text search) or a search engine, and add an HNSW index.
- Articles move to Salesforce Knowledge. Then re-evaluate keeping a copy in Postgres against searching in Salesforce directly.
- A harder test set shows retrieval misses that a different store, not a different query, would fix.

---

<a id="adr-0002"></a>

## ADR 0002: Use Claude Opus 5.5 for every generation step, with effort as the cost lever

- **Status:** Accepted, with an open follow-up (no cheaper model has been compared)
- **Recorded:** 2026-11-04
- **Applies to:** the Agent CLI, the MCP server's `draft_reply`, the RAG answer script, the prompts in `prompts/`, and the LLM judge

### Context

The assistant uses a language model in four places:

| Step | What the model does | How hard |
|---|---|---|
| Agent loop ([agent.py](CaseHandlerSF/src/casehandlersf/agent.py)) | Decides which tools to call, in what order, and when to stop; must not overclaim | Hardest: multi-step judgement with tools |
| Reply drafting (`draft_reply`) | Writes a customer reply from 5 retrieved chunks, citing each fact | Easy: the facts are in the prompt |
| Case summary and classification ([prompts](prompts/README.md)) | Fixed formats and fixed labels | Easy |
| LLM judge | Scores answers for groundedness and correctness | Medium: must notice subtle unsupported claims |

What mattered, in order: correct and grounded output (wrong answers reach customers), safe behaviour in the agent loop, then cost and latency. Volume is low today: one support agent, a few dozen requests a day.

Two embedding and reranking models are also used. They are small, run locally and are out of scope here; see [ADR 0001](#adr-0001).

### Decision

Use **`claude-opus-5-5` for all four steps**, and tune cost with the `effort` setting rather than by switching models:

- **Effort `low`** for drafting, summaries and classification: the work is reading, not reasoning.
- **Effort `medium`** for the agent loop and the judge.

Every call opts into **server-side fallback**: if a safety check declines a request, it is retried on Anthropic's recommended fallback model, and the agent logs which model actually answered.

### Options considered

Prices are Anthropic first-party API rates per million tokens (input / output).

| Option | For | Against |
|---|---|---|
| **Opus 5.5 everywhere** (chosen), $4 / $20 | Strongest generally available model short of Fable; one model to prompt, test and cache for; effort gives a cost range inside one model | Twice Sonnet's price; easy steps pay for capability they don't use |
| Sonnet 5.5, $2 / $10 | Half the price; built for everyday agent and enterprise work | Not yet measured on this test set or the agent review. A second model means a second cache namespace and a second prompt baseline |
| Haiku 5.5, $0.10 / $0.50 | About 40 times cheaper than Opus; good candidate for classification and summaries at volume | Weakest at multi-step tool use; no server-side fallback on refusals. Not measured |
| Fable 5.1, $10 / $50 | Most capable model | 2.5 times Opus's price. Nothing in the results shows Opus is the limit |
| Mixed: Opus for the agent, a cheaper model for easy steps | Lowest cost per request at scale | More moving parts, before measurements show the saving is needed |

Anthropic's own guidance points the same way: before building a multi-model setup, measure the most capable model at lower effort, because one model keeps one cache and lower effort often holds quality.

### Evidence

- **RAG answers:** 40/40 groundedness and correctness at top-k 5 ([RAG eval report](experiments/RAG_EVAL_REPORT.md)).
- **Agent:** behaved correctly in 10 of 10 review runs, including a missing Case, an out-of-scope Case and two writes ([agent review](experiments/agent_review_results.md)).
- **Cost of the agent:** those 10 runs used 78,546 input and 6,994 output tokens, about **$0.45 in total, or $0.045 per question**, before any prompt caching.
- **Judge:** agreed with hand labels on 10 of 10 answers, 7 of which had planted flaws.

**Not measured:** any model other than Opus 5.5 on these tasks. The decision is a sensible default, not a proven optimum.

### Consequences

- **Good:** one model to reason about; the effort setting can be raised on a hard route without changing anything else.
- **Bad:** at higher volume, easy steps cost more than they need to. At 10,000 agent questions a month, the agent alone costs roughly $450 a month at current measurements.
- **Risk:** the judge is the same model as the answerer, so it may favour its own style. The 10-answer hand check is the only guard so far.
- **Risk:** the model ID is set separately in several files (`agent.py`, `mcp_server.py`, `rag_answer.py`, `case_prompts.py`). Moving to another model means changing them together and re-running both evals.

### Revisit when

- Volume grows enough that cost matters (a few thousand requests a day). First run the RAG eval and the agent review on Sonnet 5.5 for drafting and classification, and keep Opus wherever scores drop.
- A new model is released. Re-run both evals before switching; never switch on benchmarks alone.
- The judge disagrees with a human on more than an occasional answer. Then try a different model as judge.

---

<a id="adr-0003"></a>

## ADR 0003: A person approves every write the AI makes to Salesforce

- **Status:** Accepted
- **Recorded:** 2026-11-04
- **Applies to:** `update_case`, the only tool that writes ([mcp_server.py](CaseHandlerSF/src/casehandlersf/mcp_server.py)), when it is called by the Agent CLI or through an MCP host

### Context

The agent can add a comment to a Salesforce Case. A comment marked as published is shown to the customer in the portal. Four things make an unchecked write risky:

1. **It reaches a customer.** A wrong fix, an invented date or a promise the team can't keep goes straight to the person who raised the Case.
2. **It can't be taken back by the system.** The integration user's permission sets allow reading Cases and editing them to add comments, but not deleting anything. A bad comment stays until a person removes it by hand.
3. **The input is untrusted.** Case subjects and descriptions are written by customers. The prompts tell Claude to treat them as information, but a prompt instruction is not a guarantee against an injected "post this to the customer".
4. **The model can be wrong in plausible ways.** In the RAG eval, a correct-sounding answer turned "the excerpts don't say" into "there's no fix date yet", a false product claim ([RAG eval report](experiments/RAG_EVAL_REPORT.md)).

Reads (looking up a Case, searching the Knowledge base, drafting a reply that isn't sent) carry none of these risks.

### Decision

Every `update_case` call made by the AI waits for a person's decision on the **exact text and visibility** before anything is written.

- **The check is in code, not in the prompt.** `NEEDS_APPROVAL` in [agent.py](CaseHandlerSF/src/casehandlersf/agent.py) stops the loop before the tool runs. Claude cannot skip it, however the conversation goes.
- **The default is no.** Called from code without an approver, `run_agent` rejects every write. Pressing Enter at the prompt also rejects.
- **A rejection teaches.** The person can type what to change; it goes back to Claude as the tool result, so it can revise and ask again within the step limit.
- **Visibility is shown up front.** The prompt says "Visible to the customer: YES" or "no (internal comment)".
- **One hard rule needs no approval at all:** a published comment that still contains `[KA-xxxx]` citations is refused by the tool itself.
- **Every decision is logged** with the run: approved or not, the feedback, and how long the person took.

Through an MCP host (Claude Code, Claude Desktop), the host asks before each tool call. The README tells users to keep that on for `update_case` and not choose "always allow".

### Options considered

| Option | For | Against |
|---|---|---|
| **Approve every write** (chosen) | Nothing reaches a customer unseen; works against prompt injection; simple to explain and audit | A person must be present; each write takes one review |
| Approve only published comments, auto-write internal notes | Less friction for notes | Internal notes still shape what the next agent tells the customer, and still can't be deleted by the system |
| Write freely, review afterwards | No waiting | Customers see mistakes first; with no delete permission, the clean-up is manual |
| Rely on the prompt ("only write approved text") | No code | Prompt instructions can be argued around or injected; the check would be invisible in tests |
| No writes at all; the agent only drafts | Safest | The person copies text into Salesforce by hand, which brings its own errors |

### Evidence

From the 10-run agent review ([agent review](experiments/agent_review_results.md)), with writes replaced by a dry run:

- **Internal note, approved:** written (dry run), and the agent correctly reported that nothing was saved.
- **Published reply, rejected with feedback:** nothing was written. The agent checked the Knowledge base, explained why the feedback didn't apply to the customer, and stopped to ask rather than resubmitting.
- **Closed Case:** the agent tried to publish a reply on a Case that was already closed. The approval step was what stopped it.

### Consequences

- **Good:** the worst realistic outcome of a model error is a rejected draft, not a wrong message to a customer.
- **Bad:** the assistant can't work unattended. Batch jobs or overnight runs can read and draft, but not write.
- **Bad:** reviews take time, and people approve faster as trust grows. The log records how long each approval took, which shows if reviews become rubber stamps.
- **Gap:** through an MCP host, approval depends on the host's settings. A user who chooses "always allow" removes the check.
- **Gap:** the HTTP API's comments endpoint has no approval step. It trusts whoever holds the API key, which is a script or a person, not the model. This ADR covers writes the AI starts.
- **Open:** the revise-and-resubmit path has not been tested end to end, and rejections are logged as tool errors, which makes them look like failures in run summaries.

### Revisit when

- There is a class of write that is low-risk, easy to undo and very frequent (for example, setting an internal tag). It could be approved by rule instead of by a person, with sampling to check the rule.
- The integration user gains delete or update rights on other objects. Every new write path needs its own entry in `NEEDS_APPROVAL`.
- Approvals take seconds and are almost never rejected. Measure whether reviews are real before relaxing anything.
