# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic", "pydantic"]
# ///
"""Run the versioned Case prompts in this folder.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    uv run prompts/case_prompts.py summarize Case07
    uv run prompts/case_prompts.py summarize Case07 --version v1
    uv run prompts/case_prompts.py classify Case07

A Case is a referenceId from CaseHandlerSF/data/salesforce/Case.json. Without
--version, each task uses the version in CURRENT.

Also imported by the scripts in experiments/, so every prompt is called the
same way everywhere.

Needs an API key in ANTHROPIC_API_KEY (or an `ant auth login` profile).
"""

import argparse
import json
from pathlib import Path
from typing import Literal

import anthropic
from pydantic import BaseModel, Field

MODEL = "claude-opus-5-5"
PROMPTS_DIR = Path(__file__).parent
DATA = PROMPTS_DIR.parent / "CaseHandlerSF/data/salesforce"
CURRENT = {"case_summary": "v2", "case_classify": "v1", "case_summary_judge": "v1"}
# Prompt versions written to take the Case as plain text rather than inside <case> tags.
PLAIN_CASE = {"case_summary_v1"}
SUMMARY_FIELDS = ("Subject", "Description", "Status", "Priority", "Origin", "Type", "Reason")
# If a safety classifier declines, retry on Anthropic's recommended fallback model.
FALLBACK = {"betas": ["server-side-fallback-2026-07-01"], "extra_body": {"fallbacks": "default"}}

_client: anthropic.Anthropic | None = None


class Classification(BaseModel):
    reasoning: str
    category: Literal[
        "outage",
        "software_defect",
        "equipment_fault",
        "account_access",
        "billing",
        "order_delivery",
        "service_request",
        "feedback",
    ]
    urgency: Literal["critical", "high", "medium", "low"]


class Grade(BaseModel):
    reasoning: str
    score: int = Field(ge=1, le=5)


def client() -> anthropic.Anthropic:
    global _client
    _client = _client or anthropic.Anthropic()
    return _client


def load_prompt(task: str, version: str | None = None) -> str:
    return (PROMPTS_DIR / f"{task}_{version or CURRENT[task]}.md").read_text()


def tagged(case_text: str) -> str:
    return f"<case>\n{case_text}\n</case>"


def summary_input(fields: dict, comments: list[str] = ()) -> str:
    """Case text for the summary prompts: the Case fields, then any comments."""
    text = "\n".join(f"{f}: {fields[f]}" for f in SUMMARY_FIELDS if fields.get(f))
    if comments:
        text += "\nComments:\n" + "\n".join(f"- {c}" for c in comments)
    return text


def classify_input(fields: dict, industry: str) -> str:
    """Case text for the classify prompt. Priority, Type and Reason are left out
    so the model can't copy them."""
    return f"Industry: {industry}\nSubject: {fields['Subject']}\nDescription: {fields['Description']}"


def summarize(case_text: str, version: str | None = None) -> str:
    version = version or CURRENT["case_summary"]
    plain = f"case_summary_{version}" in PLAIN_CASE
    response = client().beta.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=load_prompt("case_summary", version),
        # A short summary needs little reasoning; Opus 5.5 can't turn thinking off.
        output_config={"effort": "low"},
        messages=[{"role": "user", "content": case_text if plain else tagged(case_text)}],
        **FALLBACK,
    )
    if response.stop_reason == "refusal":
        return "[refused]"
    return "".join(b.text for b in response.content if b.type == "text").strip()


def classify(case_text: str, version: str | None = None) -> Classification | None:
    """Return the category and urgency, or None if the model refused."""
    response = client().beta.messages.parse(
        model=MODEL,
        max_tokens=4000,
        system=load_prompt("case_classify", version),
        output_config={"effort": "low"},
        output_format=Classification,
        messages=[{"role": "user", "content": tagged(case_text)}],
        **FALLBACK,
    )
    if response.stop_reason == "refusal":
        return None
    return response.parsed_output


def grade_summary(case_text: str, summary: str, version: str | None = None) -> Grade:
    """Score a summary 1-5 with the judge prompt. A refusal scores 1."""
    response = client().beta.messages.parse(
        model=MODEL,
        max_tokens=4000,
        system=load_prompt("case_summary_judge", version),
        output_config={"effort": "medium"},
        output_format=Grade,
        messages=[{
            "role": "user",
            "content": f"{tagged(case_text)}\n\n<summary>\n{summary}\n</summary>",
        }],
        **FALLBACK,
    )
    if response.stop_reason == "refusal" or response.parsed_output is None:
        return Grade(reasoning="[judge refused]", score=1)
    return response.parsed_output


def load_cases() -> tuple[list[dict], dict[str, str]]:
    """The sample Cases and {account referenceId: industry}."""
    accounts = json.loads((DATA / "Account.json").read_text())["records"]
    industries = {a["attributes"]["referenceId"]: a["Industry"] for a in accounts}
    return json.loads((DATA / "Case.json").read_text())["records"], industries


def industry_of(case: dict, industries: dict[str, str]) -> str:
    return industries[case["AccountId"].removeprefix("@")]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a versioned Case prompt on one sample Case.")
    parser.add_argument("task", choices=["summarize", "classify"])
    parser.add_argument("case", help="referenceId from Case.json, e.g. Case07")
    parser.add_argument("--version", help="prompt version, e.g. v1 (default: the current one)")
    args = parser.parse_args()

    task = {"summarize": "case_summary", "classify": "case_classify"}[args.task]
    if args.version and not (PROMPTS_DIR / f"{task}_{args.version}.md").exists():
        versions = sorted(p.stem.removeprefix(f"{task}_") for p in PROMPTS_DIR.glob(f"{task}_v*.md"))
        parser.error(f"no {task} prompt {args.version}; available: {', '.join(versions)}")

    cases, industries = load_cases()
    case = next((c for c in cases if c["attributes"]["referenceId"] == args.case), None)
    if case is None:
        parser.error(f"no Case with referenceId {args.case}")

    if args.task == "summarize":
        print(summarize(summary_input(case), args.version))
    else:
        result = classify(classify_input(case, industry_of(case, industries)), args.version)
        print(f"{result.category} / {result.urgency}\n{result.reasoning}" if result else "[refused]")


if __name__ == "__main__":
    main()
