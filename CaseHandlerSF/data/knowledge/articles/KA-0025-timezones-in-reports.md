---
article_number: KA-0025
title: How timezones work in reports, dashboards and scheduled reports
url_name: timezones-in-reports
article_type: Reference
category: Reports & Data
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-10-15
related_cases: [CASE-1035, CASE-1046]
summary: Explains why two users can see different times in the same report, how to set a fixed report timezone, and how to fix scheduled reports that run at the wrong hour.
---

## Default behavior

Timestamps are stored in UTC and shown in **each viewer's profile timezone** (**Profile > Preferences > Timezone**). That's why users in New York and Lisbon see different times for the same task. Both are correct.

Date-only fields (for example *Due date*) have no time and are the same for everyone.

**Grouping by day** uses the viewer's timezone too. A task completed at 23:30 in New York counts as "Tuesday" for a New York viewer and "Wednesday" for a Lisbon viewer, so daily totals can differ between users.

## Make a report consistent for everyone

Open the report, go to **Settings > Timezone > Fixed**, and choose a timezone (for example *America/New_York*). All viewers, exports and schedules then use that timezone, and the report header shows it.

Recommended for any report used in finance, SLA or compliance reviews.

## Scheduled report runs at the wrong time

1. Open the schedule and check its **Timezone** field.
2. **Known defect (fixed in 2026.08.2):** Schedules created before that release saved the timezone as UTC, whatever was chosen. Opening the schedule shows the right timezone, but it runs in UTC. **Fix:** edit the schedule, change any setting and change it back, then **Save**. Saving rewrites the stored timezone.
3. Daylight saving time: schedules follow the local time of their timezone, so a 09:00 New York schedule stays at 09:00 after the clocks change.

## Dashboards

Each dashboard widget can use the viewer's timezone or the dashboard's fixed timezone (**Dashboard settings > Timezone**).
