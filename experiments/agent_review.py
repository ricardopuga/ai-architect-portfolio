"""Run the support agent on 10 questions and log every step, for review by hand.

Each question probes a different way the agent can go wrong: a Case the knowledge
base covers, one it covers only partly, one it doesn't cover, a Case outside the
product, a Case that doesn't exist, questions with no Case, a paraphrase, two Cases
at once (step pressure), and two requests that write to Salesforce.

Nothing is written to Salesforce: add_case_comment is replaced with a dry run, so
the approval and revision path runs in full against your real Cases and knowledge base.

Run from CaseHandlerSF, so .env is found:
    cd CaseHandlerSF
    export ANTHROPIC_API_KEY=sk-ant-...
    uv run python ../experiments/agent_review.py

The log goes to CaseHandlerSF/logs/agent_review.jsonl (replaced on each run).
"""

import asyncio
from pathlib import Path

from casehandlersf import agent, mcp_server
from casehandlersf.agent import Decision

LOG_PATH = Path("logs/agent_review.jsonl")


def dry_run_comment(case_id: str, body: str, is_published: bool) -> str:
    return "DRY-RUN-NOT-WRITTEN"


class Reviewer:
    """Answers approval requests from a script: each request takes the next decision.
    When the script runs out, it rejects."""

    def __init__(self, *decisions: Decision) -> None:
        self.decisions = list(decisions)

    def __call__(self, name: str, arguments: dict) -> Decision:
        if not self.decisions:
            return Decision(False, "no more approvals in this review")
        return self.decisions.pop(0)


# (label, question, approvals for update_case calls)
RUNS = [
    ("kb_covered", "Is there a knowledge article that solves case 00001030?", ()),
    ("kb_partial", "Can we resolve case 00001029 from the knowledge base?", ()),
    ("kb_missing", "Can we answer case 00001028 from the knowledge base?", ()),
    ("out_of_domain", "What should we tell the customer on case 00001018?", ()),
    ("no_such_case", "Summarize case 00009999 for me.", ()),
    ("kb_only", "How should a customer handle HTTP 429 errors from the API?", ()),
    (
        "paraphrase",
        "A customer says their teammates' edits show up half a minute late. What's the fix?",
        (),
    ),
    (
        "two_cases",
        "Compare cases 00001029 and 00001030: which one does the knowledge base cover better?",
        (),
    ),
    (
        "reply_with_feedback",
        "Draft a reply to case 00001030 and send it to the customer.",
        (
            Decision(False, "Also tell them to check the suppression list"),
            Decision(True),
        ),
    ),
    (
        "internal_note",
        "Add an internal note to case 00001030 saying we sent the allowlisting steps.",
        (Decision(True),),
    ),
]


async def main() -> None:
    mcp_server.add_case_comment = dry_run_comment
    LOG_PATH.unlink(missing_ok=True)

    print(f"{'label':<20} {'run_id':<12} steps  tools")
    for label, question, approvals in RUNS:
        try:
            result = await agent.run_agent(
                question, approve=Reviewer(*approvals), log_path=LOG_PATH
            )
        except Exception as e:  # noqa: BLE001 - logged as run_error; keep going.
            print(f"{label:<20} {'-':<12} failed: {type(e).__name__}")
            continue
        tools = ", ".join(
            c.name + ("!" if c.is_error else "") for c in result.tool_calls
        )
        print(f"{label:<20} {result.run_id:<12} {result.steps:>5}  {tools}")
    print(f"\n! = tool returned an error. Log: {LOG_PATH.resolve()}")


if __name__ == "__main__":
    asyncio.run(main())
