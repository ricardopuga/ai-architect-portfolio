# Prompts

System prompts for working with support Cases, one file per version. A version never changes once it has been measured: to change a prompt, copy it to the next version number and edit the copy.

| Task | Current | File | What it does |
|---|---|---|---|
| Case summary | v2 | `case_summary_v2.md` | Three lines: Issue, Actions taken, Next step |
| Case classification | v1 | `case_classify_v1.md` | One of 8 categories and one of 4 urgency levels |
| Summary judge | v1 | `case_summary_judge_v1.md` | Scores a summary 1–5 against its Case |

All prompts run on `claude-opus-5-5`. The current version of each task is set in `CURRENT` in `case_prompts.py`.

## Run a prompt

```bash
export ANTHROPIC_API_KEY=sk-ant-...
uv run prompts/case_prompts.py summarize Case07
uv run prompts/case_prompts.py summarize Case07 --version v1
uv run prompts/case_prompts.py classify Case07
```

The Case is a `referenceId` from `CaseHandlerSF/data/salesforce/Case.json`. From Python, import `summarize`, `classify` and `grade_summary` from `case_prompts.py`. The scripts in `experiments/` do this.

What each prompt receives:

- **Summary:** Subject, Description, Status, Priority, Origin, Type and Reason, then any comments. From v2 on, the Case is wrapped in `<case>` tags; v1 takes it as plain text.
- **Classification:** only the account's industry, the Subject and the Description, in `<case>` tags. Priority, Type and Reason are left out so the model can't copy them. The answer is constrained to the allowed labels.

## Versions

### case_summary

- **v1:** plain instructions and rules. On 10 sample Cases, all 10 summaries were in the right format. Weak spots: generic next steps on Working Cases, and occasional details not in the Case (a team, a cause).
- **v2:** the same rules in XML tags, plus 3 examples (Case02, Case06 and a made-up Case with comments), none of them in the test set. Not yet scored against v1: run `experiments/case_summary_test.py`.

### case_classify

- **v1:** 8 categories, 4 urgency levels defined by impact on core operations and safety. Against draft labels for the 20 sample Cases, which still need checking by hand: category 20/20, urgency 15/20. All 5 misses were one level off, at boundaries the definitions leave open: whether lost patient data counts as critical, and how to rate a broken device when the Case doesn't state the impact.

### case_summary_judge

- **v1:** 1–5 scale with anchors. It sees one summary at a time and is not told which prompt version wrote it.

## Tests

| Script | Measures |
|---|---|
| `experiments/case_summary_test.py` | Summary versions side by side on 10 Cases: format check and judge score |
| `experiments/case_classify_test.py` | Classification accuracy against `experiments/case_labels.csv` |
| `experiments/robustness_test.py` | Portuguese Cases, very long Cases and hidden instructions, through all current prompts |
