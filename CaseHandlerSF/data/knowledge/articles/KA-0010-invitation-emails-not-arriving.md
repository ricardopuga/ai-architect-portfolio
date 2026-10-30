---
article_number: KA-0010
title: User invitation emails not being delivered
url_name: invitation-emails-not-arriving
article_type: Troubleshooting
category: Users & Permissions
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-10-02
related_cases: [CASE-1024]
summary: How to diagnose invitations that never arrive (domain restrictions, spam filtering, suppression list, seat limits) and how to send an invite link directly instead.
---

## Symptoms

An Admin invites people from **Settings > Members > Invite**. The invitees never get the email, and the invite shows as *Pending*.

## Check first: is this affecting everyone?

If **no** invitations are arriving for **any** workspace, check the status page for an email delivery incident. If there is none, escalate as **Urgent** to the Messaging team. For a single workspace, work through the list below.

## Causes and resolution

1. **Domain restriction.** **Settings > Security > Allowed email domains** blocks invites to other domains *without showing an error*. Add the domain, or invite the user as a Guest.
2. **Spam or quarantine.** Invitations come from `invites@mail.lumora.example`. Ask IT to allowlist `mail.lumora.example`. Microsoft 365 tenants with strict impersonation protection often quarantine these emails.
3. **Suppression list.** If an earlier email to that address bounced, it is suppressed. Check **Email deliverability** on the pending invite in the Support Console and remove the suppression.
4. **No seats left.** If every paid seat is in use, invites wait in *Pending — awaiting seat* and no email is sent. Add seats or free one up.
5. **SSO with JIT provisioning.** If SSO is required and just-in-time provisioning is on, no invite is needed. Users can simply sign in with SSO.

## Workaround: send the link directly

On the pending invite, click **⋯ > Copy invite link** and send it through another channel. The link is valid for 7 days and works only for the invited email address.
