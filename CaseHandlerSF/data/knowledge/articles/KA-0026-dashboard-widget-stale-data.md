---
article_number: KA-0026
title: Dashboard widget shows old or incorrect data
url_name: dashboard-widget-stale-data
article_type: Troubleshooting
category: Reports & Data
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-09-28
related_cases: [CASE-1023]
summary: How to fix a dashboard widget showing figures from weeks or months ago (fixed date ranges, paused snapshots, cache, a broken data source).
---

## Symptoms

A widget shows numbers that are clearly out of date, for example revenue from two months ago, while other widgets on the same dashboard are current.

## Causes and resolution

1. **Fixed date range.** The widget's filter is set to absolute dates (for example *1 Jul – 31 Jul*) instead of a relative range. Edit the widget, go to **Filters > Date**, and choose a relative option such as **This month** or **Last 30 days**. This is the most common cause.
2. **The source report is a paused snapshot.** If the widget's source report uses **Save as snapshot**, the widget shows the last snapshot. Snapshots pause when the report owner is deactivated. Open the source report and check **Last refreshed**. Assign a new owner or switch to live data.
3. **Data connector stopped syncing.** If the data comes from an external source (for example a billing system through a connector), check **Settings > Integrations > [connector] > Sync log** (see KA-0030).
4. **Cache.** Widgets are cached for up to 15 minutes. Click **⋯ > Refresh** on the widget. A widget that is still out of date after refreshing isn't a cache problem.
5. **Wrong source report.** After a dashboard is duplicated, widgets still point to the *original* report. Check **Edit widget > Source**.

## Escalation

If none of these apply, escalate to Reports Engineering with the dashboard URL, the widget name, the value expected, and the value shown.
