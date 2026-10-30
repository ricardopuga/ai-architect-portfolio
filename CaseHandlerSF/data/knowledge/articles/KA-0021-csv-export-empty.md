---
article_number: KA-0021
title: CSV export downloads an empty or incomplete file
url_name: csv-export-empty
article_type: Troubleshooting
category: Reports & Data
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-09-09
related_cases: [CASE-1006]
summary: Why report or table exports sometimes contain only headers, or nothing at all, and how to get a complete export.
---

## Symptoms

The user clicks **Export > CSV** on a report or table view. A file downloads, but it is empty, contains only the header row, or has fewer rows than shown on screen.

## Causes and resolution

1. **Too big for an immediate download.** Exports over **50,000 rows** run in the background, but older browser bookmarks still trigger the immediate download, which returns an empty file. Ask the user to choose **Export > CSV (email me when ready)**. They'll receive a download link valid for 7 days. The maximum is 1,000,000 rows per export.
2. **Filters aren't applied the same way.** The on-screen view may include a temporary filter that the export doesn't use, or the other way round. Save the view first (**Save view**) and export from the saved view.
3. **Field-level permissions.** Columns the user isn't allowed to see are left out. If *every* selected column is restricted, the file is empty. Check the user's project role (KA-0009).
4. **Sensitive fields.** Fields marked *Sensitive* are removed unless the user has the **Export sensitive data** permission (KA-0022).
5. **Opening in Excel.** Files are UTF-8. Excel on some systems shows one blank column when opening by double-click. Use **Data > From Text/CSV** in Excel, or choose **Export > CSV (Excel compatible)**, which adds a byte-order mark.

## Still empty

Collect the report URL, the time of export, the browser, and a HAR file (KA-0003), then escalate to Reports Engineering.
