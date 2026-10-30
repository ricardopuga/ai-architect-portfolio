---
article_number: KA-0042
title: Backup retention and restoring deleted data
url_name: backup-retention-and-restore
article_type: Policy
category: Security & Compliance
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-09-08
related_cases: [CASE-1027]
summary: How long Lumora keeps backups, what users can restore themselves (trash, version history), and how to request a restore from backup.
---

## Backup policy

- Lumora takes encrypted snapshots of all workspace data **every 24 hours**, plus continuous transaction logs, in a separate region from production.
- **Retention:** 30 days (Starter, Team, Business). 90 days (Enterprise).
- Backups are for disaster recovery and restoring a whole workspace or project. They are not an archive the customer can browse.

## What users can restore themselves

| What | Where | How long |
|---|---|---|
| Deleted tasks, files, projects | **Trash** | 30 days |
| Earlier versions of a file or document | **Version history** on the item | Depends on the version setting (KA-0016) |
| Deleted custom fields | **Settings > Fields > Deleted** | 30 days |
| Field changes on a task | **Activity** tab, then **Revert** | Unlimited |

## Requesting a restore from backup

For anything not covered above (for example a project bulk-edited by mistake, or data deleted more than 30 days ago but still within the backup window):

1. A workspace **Owner** must ask for it in writing on the case.
2. Give the project or workspace name and a point in time (date, time and timezone) to restore to.
3. Restores are done **into a new copy of the project**, never over live data. The customer then copies back what they need.
4. Target time: 2 business days (Enterprise: 1 business day). There is no charge on Business and Enterprise. On Starter and Team, the first restore each year is free.

## Customer-side backups

Customers can set up their own regular exports with scheduled reports (KA-0024) or the bulk export API (`POST /v2/exports`).
