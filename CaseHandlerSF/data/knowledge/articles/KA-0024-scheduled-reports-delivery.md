---
article_number: KA-0024
title: Scheduling reports and choosing delivery destinations
url_name: scheduled-reports-delivery
article_type: How-to
category: Reports & Data
plans: [Team, Business, Enterprise]
last_reviewed: 2026-10-15
related_cases: [CASE-1022, CASE-1046]
summary: How to schedule recurring report delivery by email, Slack or (in beta) cloud storage, and how the schedule's timezone works.
---

## Create a schedule

1. Open a saved report and click **Schedule**.
2. Choose the frequency (daily, weekdays, weekly, monthly), the time, and the **timezone**.
3. Choose the format: CSV, XLSX or PDF.
4. Choose where to send it (see below), then click **Save**.

## Destinations

| Destination | Plans | Status |
|---|---|---|
| Email (up to 50 recipients) | Team+ | Generally available |
| Slack or Microsoft Teams channel | Team+ | Generally available |
| Cloud storage: Amazon S3, Google Drive, SharePoint | Business+ | **Beta** (since 2026.10.1) |

### Joining the cloud storage beta

An Owner turns it on under **Settings > Labs > Scheduled exports to cloud storage**. Each destination needs an integration connection (an S3 bucket with an IAM role ARN, or OAuth for Drive and SharePoint). Files are named `<report>_<YYYY-MM-DD>.<ext>`. Beta feedback goes to the in-app **Labs feedback** form.

If a customer asked for this as a feature request, tell them about the beta, link their case to feature request FR-118, and close it as **Resolved – Available in beta**.

## Timezone

Schedules run in the timezone set **on the schedule**, not the viewer's timezone. Schedules created before 2026.08.2 had a defect where the timezone was saved as UTC. See KA-0025.

## Who owns the schedule

The schedule runs with the **owner's permissions**. If the owner is deactivated, the schedule pauses and Admins receive an email asking them to choose a new owner.
