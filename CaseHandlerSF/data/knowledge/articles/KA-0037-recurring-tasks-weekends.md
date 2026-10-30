---
article_number: KA-0037
title: Recurring tasks are created on weekends
url_name: recurring-tasks-weekends
article_type: Troubleshooting
category: Tasks & Projects
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-10-04
related_cases: [CASE-1030]
summary: The difference between "Daily" and "Every weekday" recurrence, how to use custom working days, and a fixed defect where the weekend-skip setting was ignored after a daylight saving change.
---

## Symptoms

A task set to repeat daily is created on Saturdays and Sundays, even though the user expected weekends to be skipped.

## Causes and resolution

1. **"Daily" includes weekends.** This is expected. In the task, go to **Repeat** and choose **Every weekday (Mon–Fri)** instead of **Daily**.
2. **Working days aren't set up.** For other working weeks (for example Sunday to Thursday), an Admin sets **Settings > Workspace > Working days**. Then choose **Repeat > Every working day**.
3. **Holidays.** To skip public holidays as well, add a holiday calendar under **Settings > Workspace > Holidays** and tick **Skip holidays** on the recurrence.
4. **Known defect (fixed in 2026.09.3):** recurrences set to *Every weekday* that were created before a daylight saving change could produce one task on the weekend. The cause was the next date being calculated in UTC. After the fix, open each affected recurrence and **Save** it again. That recalculates the schedule.

## Clean up tasks created by mistake

Filter the project by **Created by: Recurrence** and **Due date: is weekend**, select the tasks, and delete them. Deleting one occurrence doesn't affect the rest of the series.
