---
article_number: KA-0038
title: Notification preferences go back to the defaults
url_name: notification-preferences-not-saving
article_type: Troubleshooting
category: Notifications
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-10-06
related_cases: [CASE-1028]
summary: Why notification settings seem to reset after signing out (device settings versus account settings, workspace-enforced settings, SCIM) and how to make them stick.
---

## Symptoms

A user changes their notification preferences, signs out, signs back in, and finds the old settings again.

## Causes and resolution

1. **Device setting versus account setting.** **Desktop push** and **sound** settings are stored *in the browser*. Clearing site data on sign-out, using private mode, or switching browsers resets them. Email and in-app settings are stored on the account and follow the user everywhere. Ask which settings reset.
2. **Settings enforced by the workspace.** Admins can lock certain notifications (for example *Mentions* and *Assigned to me*) under **Settings > Notifications > Enforced defaults**. Users can change them in the dialog, but the change is undone when they save. A padlock icon shows which settings are locked. **Known UI defect:** in 2026.10.1 the padlock doesn't show on the mobile web layout.
3. **Notifications are set separately for each workspace.** Users in more than one workspace need to change their settings in each one. The selector is at the top of **Profile > Notifications**.
4. **The change wasn't saved.** The dialog saves only when **Save changes** is clicked. Closing the panel discards changes.

## Still resetting

If the user's **account** settings (not device settings), for a setting that isn't locked, reset after signing in again, escalate to the Notifications team with the user's email, the setting, and the time of the change.
