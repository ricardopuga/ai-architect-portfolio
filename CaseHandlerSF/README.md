# CaseHandlerSF

A small command-line tool that reads a Salesforce case export (CSV), cleans the data, and prints a summary: how many cases there are per priority, how many are still open, and the average age of the open ones.

## Requirements

- [uv] installed

## Run it

clone repo and run
uv run casehandlersf data/sample_cases.csv
```

Expected output:

```
Loaded 50 cases from data/sample_cases.csv (0 rows skipped)

Cases per priority:
  High        18
  Medium      17
  Low         12
  Unknown      3

Open cases: 32
Average age of open cases: 41.2 days - depends on the date of the run
```

The file must be UTF-8 encoded and have a header row.

| Field | Required | Accepted column names |
|---|---|---|
| Case number | yes | `CaseNumber`, `Case ID`, `Id` |
| Created date | yes | `CreatedDate`, `Date/Time Opened`, `Date Opened`, `Opened` |
| Subject | no | `Subject`, `Title` |
| Status | no | `Status` |
| Priority | no | `Priority` |
| Closed date | no | `ClosedDate`, `Date/Time Closed`, `Date Closed`, `Closed` |

How the data is cleaned:

- Rows with no case number, an unreadable created date, or a duplicate case number are skipped and counted in "rows skipped".
- Priorities are normalized to Critical, High, Medium or Low (for example, `P1 - High` becomes `High`). Anything else is counted as Unknown.
- A case counts as open if it has no closed date and its status is not Closed, Resolved or Cancelled.
- Dates can be in ISO format (`2026-09-01`, `2026-09-01T14:03:00.000+0000`) or day-first (`01/09/2026`). US-style month-first dates are not supported.

If the file is missing, empty, not UTF-8, or lacks a required column, the tool prints a one-line error explaining what's wrong and exits.
