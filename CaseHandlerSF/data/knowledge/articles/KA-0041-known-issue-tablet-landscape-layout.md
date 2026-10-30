---
article_number: KA-0041
title: "Known issue: layout breaks on iPad and Android tablets in landscape"
url_name: known-issue-tablet-landscape-layout
article_type: Known Issue
category: Mobile
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-10-14
related_cases: [CASE-1037]
summary: In the web app on tablets in landscape orientation, the sidebar overlaps the content and the toolbars are cut off. Workarounds are available, and a fix is planned for 2026.11.2.
---

## Status

**Open.** Ticket FE-1290. Fix planned for release **2026.11.2**.

## Symptoms

When the Lumora **web app** is used in a tablet browser (Safari on iPad, Chrome on Android tablets) in **landscape** orientation:

- The left sidebar overlaps the board or table instead of pushing it across.
- The top toolbar is cut off, so filter and share buttons can't be reached.
- Pinch zoom makes it worse.

Portrait orientation and the native iPad app aren't affected.

## Cause

The responsive layout treats screens between 1024 and 1366 px wide as desktop width but still applies the touch layout. The two clash.

## Workarounds

1. **Use the native app.** *Lumora for iPad* and the Android app have proper tablet layouts. This is the recommended option.
2. In Safari, tap **aA > Request Desktop Website**. The full desktop layout loads, with smaller touch targets.
3. Collapse the sidebar with the **«** button. It stays collapsed for the session.
4. Use portrait orientation.

## Agent notes

Link the case to FE-1290 so the customer is notified when the fix ships. Change the status to **Pending Release**, not Closed.
