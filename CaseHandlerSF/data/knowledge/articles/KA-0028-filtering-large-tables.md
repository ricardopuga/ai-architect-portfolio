---
article_number: KA-0028
title: Browser lags when filtering tables with 100,000+ rows
url_name: filtering-large-tables
article_type: Troubleshooting
category: Performance
plans: [Team, Business, Enterprise]
last_reviewed: 2026-10-03
related_cases: [CASE-1039]
summary: How to keep very large tables responsive with server-side filtering, saved views, indexed fields and paging.
---

## Symptoms

Filtering or sorting a table view with more than about 100,000 rows makes the browser freeze for several seconds, or shows "Page unresponsive".

## Why it happens

By default, table views load up to 100,000 rows into the browser so that quick filters respond immediately. Above that size, filtering in the browser uses a lot of memory and CPU, especially with formula columns.

## Resolution

1. **Turn on server-side filtering.** In the view, go to **View settings > Performance > Filter on server**. Filters and sorts then run on Lumora's servers and only one page of results (500 rows) is loaded. This is the main fix.
2. **Filter on indexed fields.** Status, Assignee, Created date, Due date, Project and any custom field with **Indexed** ticked (**Settings > Fields > Edit**) filter much faster. Business includes up to 20 indexed custom fields, Enterprise up to 100.
3. **Use saved views** with the filters already set, so the full table never loads.
4. **Hide formula columns** you don't need in that view.
5. **Archive old rows.** Moving completed items older than 12 months to an archive table can make the main table much smaller.

## Notes

- From release 2026.11, server-side filtering turns on automatically above 50,000 rows.
- If the problem continues with server-side filtering on, collect a HAR file and a browser performance profile and escalate to Frontend Engineering.
