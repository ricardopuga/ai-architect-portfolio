# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic", "pydantic"]
# ///
"""Compare Case summary prompt versions on the same 10 Cases and score them 1-5.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    uv run experiments/case_summary_test.py

Runs every version in VERSIONS (prompts/case_summary_<version>.md) on every
other Case in CaseHandlerSF/data/salesforce/Case.json, so the 10 Cases cover
all four accounts and every Status. v2's examples use Cases outside that set.
Each summary gets a format check and a 1-5 score from the judge prompt
(prompts/case_summary_judge_v1.md). The judge sees one summary at a time and
is not told which version wrote it. Results go to
experiments/case_summary_results.md.

Needs an API key in ANTHROPIC_API_KEY (or an `ant auth login` profile).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "prompts"))
from case_prompts import MODEL, grade_summary, load_cases, summarize, summary_input  # noqa: E402

VERSIONS = ("v1", "v2")
RESULTS_FILE = Path(__file__).parent / "case_summary_results.md"
SUMMARY_FORMAT = re.compile(r"Issue: .+\nActions taken: .+\nNext step: .+")


def main() -> None:
    cases = load_cases()[0][::2]
    rows, details = [], []
    totals = {v: {"score": 0, "format": 0} for v in VERSIONS}

    for case in cases:
        ref = case["attributes"]["referenceId"]
        case_text = summary_input(case)
        details.append(f"## {ref}: {case['Subject']}\n\n```\n{case_text}\n```\n")
        scores = []
        for version in VERSIONS:
            summary = summarize(case_text, version)
            ok = SUMMARY_FORMAT.fullmatch(summary) is not None
            result = grade_summary(case_text, summary)
            totals[version]["score"] += result.score
            totals[version]["format"] += ok
            scores.append(result.score)
            print(f"=== {ref} {version}: score {result.score}, format {'OK' if ok else 'FAILED'} ===\n{summary}\n")
            details.append(
                f"### {version}: score {result.score}/5, format {'OK' if ok else 'FAILED'}, "
                f"{len(summary.split())} words\n\n```\n{summary}\n```\n\n"
                f"Judge: {result.reasoning}\n"
            )
        rows.append(f"| {ref} | {case['Status']} | " + " | ".join(map(str, scores)) + " |")

    n = len(cases)
    summary_lines = [
        f"- {v}: average {t['score'] / n:.1f}/5, {t['format']}/{n} in the three-line format"
        for v, t in totals.items()
    ]
    print("\n".join(summary_lines))
    RESULTS_FILE.write_text("\n".join([
        "# Case summary prompt: before and after\n",
        f"Model: {MODEL} (summaries at effort low, judge at effort medium). "
        "Prompts: prompts/case_summary_<version>.md, judge: prompts/case_summary_judge_v1.md\n",
        *summary_lines,
        "",
        "| Case | Status | " + " | ".join(VERSIONS) + " |",
        "|---|---|" + "---|" * len(VERSIONS),
        *rows,
        "",
        *details,
    ]))
    print(f"Wrote {RESULTS_FILE}")


if __name__ == "__main__":
    main()
