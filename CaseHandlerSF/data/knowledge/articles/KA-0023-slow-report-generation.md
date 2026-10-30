---
article_number: KA-0023
title: Reports over long date ranges take a long time to generate
url_name: slow-report-generation
article_type: Troubleshooting
category: Reports & Data
plans: [Team, Business, Enterprise]
last_reviewed: 2026-09-22
related_cases: [CASE-1019]
summary: Why reports covering many months are slow and how to speed them up with summary mode, fewer calculated columns and cached snapshots.
---

## Symptoms

A report over a long date range (for example 6 months of task data) takes 5 to 15 minutes, or times out.

## Why it happens

Detail reports read every row in the range and work out calculated fields for each one when the report runs. These are the main costs:

- **Calculated and formula columns**, especially ones that look up data in other projects.
- **Grouping by a text field** that has many different values.
- **Including archived projects**.
- **"Status history" fields**, which read the full change log.

## Speed it up

1. **Turn on summary mode.** In the report, go to **Settings > Data source > Use daily summaries**. Summary mode reads pre-calculated daily totals. A 6-month report usually finishes in under 30 seconds. You lose row-level detail, but you can still drill into a single day.
2. **Remove calculated columns you don't need,** or move them into a separate report.
3. **Exclude archived projects** unless you need them.
4. **Use snapshots.** Business and Enterprise can choose **Save as snapshot (refresh nightly)**. Viewers then open the cached version immediately.
5. **Split the range.** Run one report per quarter and combine the exports.

## When to escalate

Escalate to Reports Engineering if a report in summary mode still takes more than 2 minutes, or one that used to be fast has become slow without any change. Include the report URL and the workspace ID.
