---
article_number: KA-0040
title: "Known issue: iOS app crashes on launch in version 2.3.1"
url_name: known-issue-ios-crash-2-3-1
article_type: Known Issue
category: Mobile
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-07-20
related_cases: [CASE-1009]
summary: Lumora for iOS 2.3.1 crashed on launch for users with offline mode turned on. Fixed in 2.3.2, released 2026-07-15.
---

## Status

**Resolved** in Lumora for iOS **2.3.2** (released 2026-07-15). Ticket MOB-982.

## Symptoms

- The iOS app closes straight after the splash screen.
- Affects version **2.3.1** on iOS 17 and 18, but only for users who had **offline mode** turned on.

## Cause

A database migration in 2.3.1 failed on devices that already had offline data stored, and the app crashed every time it started.

## Resolution

1. Update to **2.3.2 or later** from the App Store.
2. If the App Store doesn't offer the update yet, delete and reinstall the app. Offline data that hasn't synced will be lost. Data already synced is safe on the server.
3. Users whose company manages iOS devices (MDM) may need IT to push the update.

## Workaround if updating isn't possible

Use the mobile web version at `https://app.lumora.example` in Safari until the update is installed.

## Agent notes

If a user still reports a crash on launch with 2.3.2 or later, this article doesn't apply. Ask for the app version, the iOS version, and the crash log (**Settings > Privacy & Security > Analytics & Improvements > Analytics Data**, entries starting with `Lumora`), then escalate to Mobile Engineering.
