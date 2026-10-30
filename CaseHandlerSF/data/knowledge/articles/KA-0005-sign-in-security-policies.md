---
article_number: KA-0005
title: "Sign-in security policies: reset link expiry and account lockout"
url_name: sign-in-security-policies
article_type: How-to
category: Sign-in & Security
plans: [Business, Enterprise]
last_reviewed: 2026-09-10
related_cases: [CASE-1010, CASE-1034]
summary: How admins set password reset link lifetime, the failed-attempt threshold and lockout duration, and how to unlock a user.
---

## Defaults

| Setting | Default | Configurable range | Plans |
|---|---|---|---|
| Password reset link lifetime | 60 minutes | 15 minutes – 24 hours | Enterprise |
| Failed attempts before lockout | 5 | 3 – 10 | Business, Enterprise |
| Lockout duration | 15 minutes | 15 minutes – 24 hours | Business, Enterprise |

On Starter and Team the defaults apply and can't be changed.

## Change the settings

1. Sign in as a workspace **Owner** or **Admin**.
2. Go to **Settings > Security > Sign-in policy**.
3. Change **Reset link lifetime**, **Failed attempts before lockout**, and **Lockout duration**.
4. Click **Save**. The new settings apply to the next sign-in attempt or reset request. Links that were already sent keep their original lifetime.

## "I was locked out for 24 hours after only 3 tries"

That's not a bug. It means the workspace admin has set a strict policy (3 attempts, 24-hour lockout). Explain that their own admin controls this setting. The admin can unlock the account right away (see below).

## Unlock a user

**Settings > Members**, select the user, then **⋯ > Unlock account**. The user can sign in immediately. Support agents can also unlock a user from the Support Console after confirming the request with a workspace Admin.

## Security guidance

For reset links longer than 4 hours, we recommend turning on 2FA (KA-0006) so a forwarded or intercepted link can't be used on its own.
