# TO-DO VIDEO: 5-minute architecture walkthrough

Script for presenting the Support Knowledge Assistant to a client's architecture board. Six steps, timed to 5 minutes. Each step says what to have on screen, the points to make, and a line you can say as written.

**Before recording**

- Open these in browser tabs, in this order (all on the `adrs` branch on GitHub, so the diagrams render):
  1. `CaseHandlerSF/docs/architecture.md` (context diagram, then scroll to the container diagram)
  2. `ADRS.md`
  3. `experiments/RAG_EVAL_REPORT.md` and `experiments/agent_review_results.md`
  4. `PRODUCTION_READINESS.md`
- Optional: a terminal with one agent run ready to show (`uv run casehandlersf-agent "Is there a knowledge article that solves case 00001030?"`). Only include it if it runs in under 20 seconds; otherwise skip it and keep to time.
- Speak to decisions and evidence, not code. A board wants to know what was chosen, why, what it costs and what could go wrong.

---

## Step 1. The problem and the outcome (0:00–0:30)

**On screen:** the top of `architecture.md`.

**Points:**

- Support agents spend time finding the right Knowledge article and writing replies to Salesforce Cases.
- The assistant looks up the Case, finds the relevant articles, drafts a cited reply, and adds it to the Case **only after a person approves it**.

**Say:** "This is a support assistant for Salesforce. It answers from the company's own Knowledge articles, cites every fact, and never writes to a Case without a person approving the exact text."

## Step 2. System context: who and what it touches (0:30–1:15)

**On screen:** the system context diagram.

**Points:**

- Three people: the support agent who uses it, the Knowledge maintainer who keeps the articles current, and the customer, who never uses it but writes the Case text it reads.
- Three ways in: a terminal agent, Claude Code or Claude Desktop through MCP, and an HTTP API for scripts.
- Three outside systems: Salesforce, the system of record; the Claude API for reasoning and drafting; Hugging Face, only to download two small search models once.

**Say:** "The important line is the one to Salesforce. That's the only place this system can change anything, and it's the only place a mistake reaches a customer."

## Step 3. Containers: follow one question through the system (1:15–2:30)

**On screen:** the container diagram. Trace the path with the cursor as you talk.

**Points (one request, start to finish):**

1. The support agent asks a question in the Agent CLI.
2. The agent loop calls Claude, which picks tools: `get_case` reads the Case from Salesforce, `search_knowledge` searches the Knowledge base.
3. Search is hybrid: meaning-based search in Postgres with pgvector, plus keyword search for error codes and ticket numbers, then a reranker picks the best five passages.
4. Claude drafts a reply citing articles like `[KA-0029]`.
5. If it wants to write, the loop **stops** and shows the person the exact text and whether the customer will see it. Nothing is written without a yes.
6. Every step is logged with timings and the approval decision.

- At most 5 calls to Claude per question, so a run can't loop or spend without limit.
- The Knowledge base is rebuilt from articles kept in Git by a loader script.

**Say:** "The approval check is in the code, not in the prompt. Whatever the model is told, and whatever a customer writes into a Case, it can't skip that step."

## Step 4. Three decisions and their trade-offs (2:30–3:30)

**On screen:** `ADRS.md`, scrolling past each heading.

**Points (about 20 seconds each):**

- **Vector store: Postgres with pgvector.** One store for text, metadata and vectors, queried with SQL, available as managed Postgres in every major cloud. Trade-off: keyword search runs in the app and loads every passage into memory, which is fine at hundreds of passages but needs changing at tens of thousands.
- **Model: Claude Opus 5.5 everywhere, with the effort setting as the cost lever.** Low effort for drafting, medium for the agent. About 4.5 cents per agent question as measured. Trade-off: no cheaper model has been compared yet; that is the first test to run when volume grows.
- **Human approval before every write.** A published comment reaches the customer, the system has no permission to delete it, and Case text comes from customers and can't be trusted. Trade-off: the assistant can't write unattended.

**Say:** "Each of these is written down with the options we rejected and the point at which we'd revisit it."

## Step 5. Evidence (3:30–4:15)

**On screen:** `RAG_EVAL_REPORT.md` metrics table, then the results table in `agent_review_results.md`.

**Points:**

- 40-question test set, including 5 questions the articles can't answer: answers passed groundedness and correctness 40 of 40, and all 5 unanswerable questions were refused rather than guessed.
- Cutting retrieval from 5 passages to 3 caused 3 failures, so the setting was kept at 5. Evidence decided it, not opinion.
- Agent review, 10 scenarios including a missing Case, an off-topic Case and two writes: correct behaviour in 10 of 10.
- Be honest about the limit: the test set was written by the builder and is easy. A harder set is on the list.

**Say:** "These numbers show the design works on our test set. They don't yet show it works on your Cases, which is why the next slide matters."

## Step 6. Gaps before production, and the ask (4:15–5:00)

**On screen:** `PRODUCTION_READINESS.md`.

**Points:** compared against the AWS Well-Architected Generative AI Lens, three gaps to close first:

1. **Access:** today the assistant reads Salesforce as one powerful integration user. Production should act as the signed-in agent, with their own permissions, behind SSO.
2. **Monitoring:** today there's a local log file. Production needs dashboards, alerts, cost per question, and the evals running in CI.
3. **Knowledge pipeline:** reloading articles while the server runs can return the wrong passage. Fix that first, then move to managed Postgres with backups.

**The ask:** approval to run a pilot with a small group of agents on real Cases, after gaps 3 and 1 are closed, measuring answer quality and approval rate for four weeks.

**Say:** "We know what's missing and in what order. We're asking for a limited pilot, with a person approving every write, so we can measure it on your real Cases before going further."

---

## Questions the board is likely to ask

| Question | Short answer |
|---|---|
| Does customer data leave our environment? | Case text is sent to the Claude API to draft replies. Retention and region settings need agreeing with security before the pilot. |
| What if the model makes something up? | It answers only from retrieved articles and cites each fact; citations are checked against what was retrieved, and a person approves every write. On the test set it refused all 5 questions it couldn't answer. |
| Can we switch model or cloud later? | Yes. The model is called through one API, and Postgres with pgvector runs on any major cloud. Switching models means re-running both evals first. |
| What does it cost? | About 4.5 cents per agent question on today's measurements, before prompt caching. Cheaper models are the first thing to test at volume. |
| Why not fine-tune a model on our articles? | Fine-tuning changes behaviour, not knowledge: facts go stale and can't be cited. RAG keeps answers current and checkable. |
| What stops it from posting to a customer by itself? | The approval check in code. The default is no, and the system has no permission to delete or change anything but comments. |
