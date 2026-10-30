---
article_number: KA-0027
title: Lumora Workspace is slow or pages take a long time to load
url_name: slow-performance
article_type: Troubleshooting
category: Performance
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-09-30
related_cases: [CASE-1005]
summary: A checklist for slowness reports (status page, network, browser, workspace size) and what information to collect before escalating.
---

## Step 1: Is it an incident?

Check `status.lumora.example` and the internal incident channel. If there is an active incident, link the case to it and send the customer the status page link.

## Step 2: Narrow it down

Ask:

- **When?** Slowness at the same time every day (for example 2–4 PM ET) points to network congestion on the customer's side, or to heavy automations or syncs scheduled for that time.
- **Who?** One user, one office, or everyone?
- **Where?** Everywhere in the app, or only certain pages (large boards, reports, search)?

## Step 3: Customer-side checks

1. Open `https://lumora.example/speedtest`, which measures latency to the nearest Lumora region.
2. Try a private browser window with extensions turned off. Ad blockers and some security extensions slow down the app considerably.
3. Make sure the corporate proxy allows WebSockets to `rt.lumora.example`. Without them the app falls back to slower polling (KA-0029).
4. Check the browser is supported and the device has at least 8 GB of RAM if it opens boards with thousands of cards.

## Step 4: Workspace-side checks (agent)

In the Support Console, open **Workspace > Health**:

- **Automation runs per hour.** Bulk automations scheduled at a fixed time can slow down that workspace. Suggest spreading them out.
- **Connector syncs.** Large full syncs can be moved to off-peak hours.

## Step 5: Escalate with data

Include the workspace ID, the affected users, time windows **with timezone**, speed test results, and a HAR file captured while the app was slow (KA-0003).
