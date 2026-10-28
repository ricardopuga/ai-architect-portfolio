# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic", "pydantic"]
# ///
"""Classify 20 Cases by category and urgency and measure accuracy against hand labels.

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    uv run experiments/case_classify_test.py

Classifies every Case in CaseHandlerSF/data/salesforce/Case.json with the
current prompts/case_classify_<version>.md, compares the answers with
case_labels.csv, and prints the accuracy for category, urgency and both.
The model sees only the account's industry, the Subject and the Description:
Priority, Type and Reason are left out so it can't copy them. Results go to
experiments/case_classify_results.md.

Needs an API key in ANTHROPIC_API_KEY (or an `ant auth login` profile).
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "prompts"))
from case_prompts import CURRENT, MODEL, classify, classify_input, industry_of, load_cases  # noqa: E402

HERE = Path(__file__).parent
LABELS_FILE = HERE / "case_labels.csv"
RESULTS_FILE = HERE / "case_classify_results.md"


def main() -> None:
    cases, industries = load_cases()
    with LABELS_FILE.open(newline="") as f:
        labels = {row["case"]: row for row in csv.DictReader(f)}

    rows, misses = [], []
    correct = {"category": 0, "urgency": 0, "both": 0}
    for case in cases:
        ref = case["attributes"]["referenceId"]
        label = labels[ref]
        result = classify(classify_input(case, industry_of(case, industries)))
        got = (result.category, result.urgency) if result else ("[refused]", "[refused]")
        cat_ok = got[0] == label["category"]
        urg_ok = got[1] == label["urgency"]
        correct["category"] += cat_ok
        correct["urgency"] += urg_ok
        correct["both"] += cat_ok and urg_ok

        mark = lambda ok: "" if ok else " ✗"  # noqa: E731
        print(f"{ref}: {got[0]}{mark(cat_ok)} / {got[1]}{mark(urg_ok)}  ({case['Subject']})")
        rows.append(
            f"| {ref} | {case['Subject']} | {label['category']} | {got[0]}{mark(cat_ok)} "
            f"| {label['urgency']} | {got[1]}{mark(urg_ok)} |"
        )
        if not (cat_ok and urg_ok):
            misses.append(
                f"- **{ref}** ({case['Subject']}): labeled {label['category']}/{label['urgency']}, "
                f"model said {got[0]}/{got[1]}. Label note: {label['note'] or 'none'}. "
                f"Model: {result.reasoning if result else 'refused'}"
            )

    n = len(cases)
    tally = [f"- {k}: {v}/{n} ({v / n:.0%})" for k, v in correct.items()]
    print("\nAccuracy\n" + "\n".join(tally))
    RESULTS_FILE.write_text("\n".join([
        "# Case classification accuracy\n",
        f"Model: {MODEL}, effort low. Prompt: prompts/case_classify_{CURRENT['case_classify']}.md. Labels: case_labels.csv\n",
        *tally,
        "",
        "| Case | Subject | Label category | Model category | Label urgency | Model urgency |",
        "|---|---|---|---|---|---|",
        *rows,
        "",
        "## Disagreements\n",
        *(misses or ["None."]),
        "",
    ]))
    print(f"Wrote {RESULTS_FILE}")


if __name__ == "__main__":
    main()
