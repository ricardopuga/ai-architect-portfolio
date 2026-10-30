---
article_number: KA-0006
title: Two-factor authentication code rejected during setup or sign-in
url_name: 2fa-code-rejected
article_type: Troubleshooting
category: Sign-in & Security
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-08-28
related_cases: [CASE-1013]
summary: Fixes for "Invalid verification code" when turning on or using 2FA, which is most often caused by the phone's clock being out of sync.
---

## Symptoms

The user scans the QR code in their authenticator app, types the 6-digit code, and sees **Invalid verification code**. This can happen during setup or at sign-in.

## Cause

Lumora uses time-based one-time passwords (TOTP, 30-second window, with a tolerance of one window either side). The usual causes are:

- **The phone's clock is wrong.** If it is more than about 60 seconds off, every code fails.
- **An old QR code was scanned.** Each time the setup dialog opens it creates a new secret, so a code from a previous attempt won't work.
- **The code was entered after it expired.**

## Resolution

1. On the phone, turn on automatic date and time:
   - iOS: **Settings > General > Date & Time > Set Automatically**
   - Android: **Settings > System > Date & time > Set time automatically**
   - Google Authenticator on Android also has **⋮ > Settings > Time correction for codes > Sync now**.
2. In the authenticator app, delete any old *Lumora* entries.
3. In Lumora, cancel the setup dialog and start again at **Profile > Security > Two-factor authentication**, scanning the **new** QR code.
4. Enter the code that is currently showing, not one that is about to expire.

## Lost device

The user signs in with one of their backup codes. If they have none, a workspace Admin can reset 2FA for them from **Settings > Members > ⋯ > Reset 2FA**. Support can only reset 2FA after verifying identity under the account recovery procedure.
