---
article_number: KA-0036
title: Automation rule limits and what counts as a run
url_name: automation-rule-limits
article_type: FAQ
category: Automation
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-09-16
related_cases: [CASE-1021]
summary: How many automation rules each plan allows, how runs are counted, and what happens when a limit is reached.
---

## How many rules can we create?

The limit is on **active** rules per workspace. You can keep any number of inactive (paused) rules.

| Plan | Active rules | Runs per month | Actions per rule |
|---|---|---|---|
| Starter | 5 | 1,000 | 3 |
| Team | 50 | 25,000 | 10 |
| Business | 250 | 250,000 | 25 |
| Enterprise | 1,000 | Unlimited (fair use) | 50 |

## What counts as a run?

One run is one rule triggering once, however many actions it carries out. Some examples:

- A rule that runs when a task's status changes, and posts a comment and sends an email, counts as **1 run**.
- A scheduled rule that updates 200 tasks counts as **200 runs** (one per task).
- Runs where the conditions aren't met **don't** count.

## What happens at the limit?

- **Active rules:** You can't activate another rule until one is paused.
- **Monthly runs:** Owners get an email at 80% and 100%. At 100%, rules stop running until the next billing month. Paid plans can buy run packs (+25,000) under **Settings > Billing > Add-ons**.

## Other limits

- Rules can call each other up to 10 levels deep. After that, the chain is stopped to prevent loops.
- Each scheduled rule can process up to 5,000 items per run.
- See usage under **Settings > Automations > Usage**.
