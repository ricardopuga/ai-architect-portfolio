# Production readiness: the Support Knowledge Assistant against the AWS Generative AI Lens

This compares the assistant's design ([architecture](CaseHandlerSF/docs/architecture.md), [ADRs](ADRS.md)) with the [AWS Well-Architected Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/), and lists three gaps to close before production. The lens was chosen over Microsoft's Azure guidance because its best practices have IDs, so each gap can point to one. Reviewed 2026-11-04.

## Where the design already meets the lens

| Lens practice | This design |
|---|---|
| GENOPS05-BP01: start with prompt engineering, then move to RAG or fine-tuning | Prompts first, RAG for knowledge, no fine-tuning ([when to use what](WHEN_TO_USE_WHAT.md)) |
| GENSEC05-BP01: least privilege and permission boundaries for agentic workflows | Four narrow tools, one write path, a human approval gate in code, no delete permission ([ADR 0003](CaseHandlerSF/docs/adr/0003-human-approval-for-writes.md)) |
| GENSEC02: response validation | Citations are checked against what was retrieved; published comments with citations are refused |
| GENOPS01-BP01: periodically evaluate functional performance | 40-question RAG eval, an LLM judge checked by hand, a 10-run agent review. All run by hand, not periodically |
| GENOPS02-BP03: mitigate the risk of system overload | At most 5 Claude calls per agent run; server-side fallback when a safety check declines |

## Three gaps to close before production

### 1. The AI acts as a powerful service account, not as the person using it

**Lens:** GENSEC01-BP01 (least privilege access to model endpoints), GENSEC01-BP03 (least privilege for models accessing data stores), GENSEC05-BP01 (least privilege for agentic workflows)

**Today:**

- Every request reaches Salesforce as one integration user. That user can read all Accounts, Contacts and Cases, including fields no tool uses, such as Contact birthdate and home phone.
- Salesforce sharing rules never apply to the person asking: anyone who can run the agent can read any Case.
- The HTTP API is protected by one shared key and serves plain HTTP.
- The run log records what was approved, but not who approved it.

**Close it by:**

- Calling Salesforce on behalf of the signed-in user (per-user OAuth), so their own access rules apply.
- Cutting the integration user's field access down to the Case fields the tools read.
- Putting the API behind SSO and TLS, and moving secrets from `.env` into a secrets manager.
- Recording the approver's identity with every write.

### 2. Nothing watches the system once it is running

**Lens:** GENOPS01-BP01 (periodically evaluate functional performance), GENOPS01-BP02 (collect and monitor user feedback), GENOPS02-BP01 (monitor all application layers), GENOPS02-BP02 (monitor foundation model metrics)

**Today:**

- The only telemetry is a JSON Lines file on one machine. There are no dashboards and no alerts.
- The evals run only when someone runs them.
- User feedback already exists, since every rejected draft says what was wrong, but it is logged as a tool error and never collected.

**Close it by:**

- Sending run events to a central store, with dashboards and alerts on: latency; tokens and cost per question; tool errors; refusals and fallbacks; approval rate and time to approve.
- Running the RAG eval and the agent review in CI whenever a prompt, model or retrieval setting changes.
- Putting a weekly sample of real answers through the judge.
- Turning each rejection's feedback into a new eval case.

### 3. The knowledge pipeline is manual and can serve the wrong passages

**Lens:** the reliability practices (GENREL), and GENOPS02-BP03 (mitigate the risk of system overload)

**Today:**

- The loader empties the table and reloads it (`TRUNCATE chunks RESTART IDENTITY`), so row ids are reused.
- A running MCP server keeps the copy of the chunks it loaded on the first search, keyed by row id, and never refreshes it. After a reload, ids returned by the vector search point to a different chunk's text in that stale copy, or raise a `KeyError` if the table grew. This is found by reading the code ([knowledge.py](CaseHandlerSF/src/casehandlersf/knowledge.py)) and **not yet reproduced by a test**.
- The database runs from `experiments/compose.yaml` with a default password and no backups, and everything runs on one machine.

**Close it by:**

- Writing a test that reproduces the stale-index problem, then fixing it: build each new index next to the old one, switch over in one step, and give the index a version number that the server checks before searching.
- Moving to managed Postgres with backups and a real secret.
- Later, loading articles automatically from Salesforce Knowledge, keeping their visibility rules.

## Order

Gap 3's stale index is the only one that can produce a wrong answer today, so it goes first. Gap 1 must be closed before anyone outside the team uses the assistant. Gap 2 should be in place before usage grows past what one person can review by hand.

## Sources

- [Generative AI Lens – AWS Well-Architected (PDF)](https://docs.aws.amazon.com/pdfs/wellarchitected/latest/generative-ai-lens/generative-ai-lens.pdf)
- [GENSEC01 Endpoint security](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec01.html)
- [GENSEC02 Response validation](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec02.html)
- [GENSEC05 Excessive agency](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/gensec05.html)
- [GENOPS01 Model performance evaluation](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/genops01.html)
- [GENOPS02 Monitor and manage operational health](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/genops02.html)
- [GENOPS05 Model customization](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/genops05.html)
- [Reliability – Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/reliability.html)
- [Appendix A: Best practice lifecycle mapping](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/appendix-a.html)
