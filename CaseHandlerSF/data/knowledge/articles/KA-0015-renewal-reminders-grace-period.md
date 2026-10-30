---
article_number: KA-0015
title: Renewal reminders, the grace period and reactivating a lapsed subscription
url_name: renewal-reminders-grace-period
article_type: FAQ
category: Account & Billing
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-09-25
related_cases: [CASE-1017]
summary: When renewal and payment-failure emails are sent and to whom, what happens during the 14-day grace period, and how to restore access straight away.
---

## Who gets renewal emails?

Only **billing contacts**: Owners plus anyone listed under **Settings > Billing > Billing contacts**. Admins and members don't get them. Most "I never got a reminder" reports turn out to be a billing contact who has left the company.

## When are they sent?

| Event | Emails |
|---|---|
| Annual plan renewing | 30 days and 7 days before |
| Monthly plan renewing | No reminder. A receipt after each charge |
| Payment fails | Right away, then on days 3, 7 and 12 |
| Auto-renew turned off | 30, 7 and 1 day before expiry |

## What happens when payment fails?

1. **Days 0–14 (grace period):** Everything works. A banner is shown to Owners.
2. **After day 14:** The workspace becomes **read-only** for everyone except Owners, who can still reach billing.
3. **After day 60:** The workspace is suspended. Data is kept for 90 more days, then deleted.

## Restore access

An Owner updates the payment method under **Settings > Billing > Payment method** and clicks **Retry payment**. Access comes back within a minute of a successful charge.

## If the customer had no warning

- Check the billing contacts and the email suppression status (see KA-0004).
- Agents can grant a **7-day courtesy extension** once per 12 months from the Billing Console (**Subscription > Extend grace**).
