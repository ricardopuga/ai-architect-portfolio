---
article_number: KA-0016
title: Storage limits and usage alerts
url_name: storage-limits-and-alerts
article_type: How-to
category: Files & Storage
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-10-05
related_cases: [CASE-1031]
summary: How storage is counted, who gets the 80% and 95% alerts, what stops working at 100%, and how to free up space.
---

## How storage is counted

Storage counts every file attachment, every file version, form uploads and items in the trash. Task text, comments and report definitions don't count. See KA-0001 for the limit on each plan.

Current usage: **Settings > Workspace > Usage > Storage**.

## Alerts

| Threshold | Who is notified | How |
|---|---|---|
| 80% | Owners and billing contacts | Email and in-app banner |
| 95% | Owners, billing contacts and Admins | Email and a banner for all members |
| 100% | Everyone | Error shown when uploading |

**Known gap:** If storage goes from below 80% to 100% in one day (for example after a large bulk import), only the 100% message appears. A daily check that catches this is planned for 2026.11.

Admins can add more people to these alerts: **Settings > Notifications > Workspace alerts > Storage**.

## What happens at 100%

New uploads and new file versions are blocked. Everything else, including viewing and downloading existing files, keeps working.

## Free up space

1. **Empty the trash.** Deleted files count until they are purged (30 days, or right away with **Empty trash**).
2. **Limit file versions.** In **Settings > Files > Version history**, keep the last 10 versions instead of all of them.
3. Use **Usage > Storage > Largest files** to find large files and delete or archive them.
4. Archived projects still count. Export the project and delete it if it's no longer needed.

To add capacity, upgrade the plan or buy storage packs (100 GB each, Team and above).
