---
article_number: KA-0004
title: Password reset email not received
url_name: password-reset-email-not-received
article_type: Troubleshooting
category: Sign-in & Security
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-09-02
related_cases: [CASE-1001]
summary: Why password reset emails sometimes don't arrive (spam filtering, SSO enforcement, suppression list) and how to fix each cause.
---

## Symptoms

A user requests a password reset from the sign-in page and gets no email, so they can't sign in.

## Causes and resolution

1. **Spam or quarantine filtering.** Reset emails come from `no-reply@mail.lumora.example`. Ask the user to check spam or junk, and ask their IT team to check the mail gateway quarantine. IT should allowlist the sending domain `mail.lumora.example`.
2. **SSO is enforced.** If the workspace requires SSO, Lumora does not send reset emails, because the password is managed by the identity provider. The user should sign in with **Continue with SSO** and reset their password through their company IdP.
3. **The address is on the suppression list.** After a hard bounce, Lumora stops sending to that address. In the Support Console, open the user and check **Email deliverability**. If it shows *Suppressed*, click **Remove from suppression list**, then have the user request the reset again.
4. **Typo or a different account email.** Confirm the exact email on the user record. Plus-addressing (`name+tag@`) is treated as a separate address.
5. **Rate limit.** The sign-in page sends at most 3 reset emails per address per hour. Ask the user to wait for the latest email and not keep clicking.

## Still not working

An Admin can send a reset link from **Settings > Members > ⋯ > Send password reset**. If that email doesn't arrive either, escalate to the Messaging team with the user's email address and the time of the attempt in UTC.

## Related

- KA-0005 Sign-in security policies: reset link expiry and lockout
