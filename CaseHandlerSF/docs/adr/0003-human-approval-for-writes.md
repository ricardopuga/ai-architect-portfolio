# ADR 0003: A person approves every write the AI makes to Salesforce

- **Status:** Accepted
- **Recorded:** 2026-11-04
- **Applies to:** `update_case`, the only tool that writes ([mcp_server.py](../../src/casehandlersf/mcp_server.py)), when it is called by the Agent CLI or through an MCP host

## Context

The agent can add a comment to a Salesforce Case. A comment marked as published is shown to the customer in the portal. Four things make an unchecked write risky:

1. **It reaches a customer.** A wrong fix, an invented date or a promise the team can't keep goes straight to the person who raised the Case.
2. **It can't be taken back by the system.** The integration user's permission sets allow reading Cases and editing them to add comments, but not deleting anything. A bad comment stays until a person removes it by hand.
3. **The input is untrusted.** Case subjects and descriptions are written by customers. The prompts tell Claude to treat them as information, but a prompt instruction is not a guarantee against an injected "post this to the customer".
4. **The model can be wrong in plausible ways.** In the RAG eval, a correct-sounding answer turned "the excerpts don't say" into "there's no fix date yet", a false product claim ([RAG eval report](../../../experiments/RAG_EVAL_REPORT.md)).

Reads (looking up a Case, searching the Knowledge base, drafting a reply that isn't sent) carry none of these risks.

## Decision

Every `update_case` call made by the AI waits for a person's decision on the **exact text and visibility** before anything is written.

- **The check is in code, not in the prompt.** `NEEDS_APPROVAL` in [agent.py](../../src/casehandlersf/agent.py) stops the loop before the tool runs. Claude cannot skip it, however the conversation goes.
- **The default is no.** Called from code without an approver, `run_agent` rejects every write. Pressing Enter at the prompt also rejects.
- **A rejection teaches.** The person can type what to change; it goes back to Claude as the tool result, so it can revise and ask again within the step limit.
- **Visibility is shown up front.** The prompt says "Visible to the customer: YES" or "no (internal comment)".
- **One hard rule needs no approval at all:** a published comment that still contains `[KA-xxxx]` citations is refused by the tool itself.
- **Every decision is logged** with the run: approved or not, the feedback, and how long the person took.

Through an MCP host (Claude Code, Claude Desktop), the host asks before each tool call. The README tells users to keep that on for `update_case` and not choose "always allow".

## Options considered

| Option | For | Against |
|---|---|---|
| **Approve every write** (chosen) | Nothing reaches a customer unseen; works against prompt injection; simple to explain and audit | A person must be present; each write takes one review |
| Approve only published comments, auto-write internal notes | Less friction for notes | Internal notes still shape what the next agent tells the customer, and still can't be deleted by the system |
| Write freely, review afterwards | No waiting | Customers see mistakes first; with no delete permission, the clean-up is manual |
| Rely on the prompt ("only write approved text") | No code | Prompt instructions can be argued around or injected; the check would be invisible in tests |
| No writes at all; the agent only drafts | Safest | The person copies text into Salesforce by hand, which brings its own errors |

## Evidence

From the 10-run agent review ([agent review](../../../experiments/agent_review_results.md)), with writes replaced by a dry run:

- **Internal note, approved:** written (dry run), and the agent correctly reported that nothing was saved.
- **Published reply, rejected with feedback:** nothing was written. The agent checked the Knowledge base, explained why the feedback didn't apply to the customer, and stopped to ask rather than resubmitting.
- **Closed Case:** the agent tried to publish a reply on a Case that was already closed. The approval step was what stopped it.

## Consequences

- **Good:** the worst realistic outcome of a model error is a rejected draft, not a wrong message to a customer.
- **Bad:** the assistant can't work unattended. Batch jobs or overnight runs can read and draft, but not write.
- **Bad:** reviews take time, and people approve faster as trust grows. The log records how long each approval took, which shows if reviews become rubber stamps.
- **Gap:** through an MCP host, approval depends on the host's settings. A user who chooses "always allow" removes the check.
- **Gap:** the HTTP API's comments endpoint has no approval step. It trusts whoever holds the API key, which is a script or a person, not the model. This ADR covers writes the AI starts.
- **Open:** the revise-and-resubmit path has not been tested end to end, and rejections are logged as tool errors, which makes them look like failures in run summaries.

## Revisit when

- There is a class of write that is low-risk, easy to undo and very frequent (for example, setting an internal tag). It could be approved by rule instead of by a person, with sampling to check the rule.
- The integration user gains delete or update rights on other objects. Every new write path needs its own entry in `NEEDS_APPROVAL`.
- Approvals take seconds and are almost never rejected. Measure whether reviews are real before relaxing anything.
