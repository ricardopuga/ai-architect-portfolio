---
article_number: KA-0043
title: Using the audit log for compliance
url_name: audit-log-compliance
article_type: Reference
category: Security & Compliance
plans: [Business, Enterprise]
last_reviewed: 2026-10-16
related_cases: [CASE-1040]
summary: Which user and admin actions the audit log records, how long it keeps them, and how to export or stream it to a SIEM.
---

## What is recorded

| Category | Example events |
|---|---|
| Authentication | Sign-in success and failure, SSO assertion, 2FA turned on or reset, lockout, sign-out |
| Members and roles | Invite, role change, seat change, deactivate, SCIM changes |
| Data access | Sensitive field revealed, export started and downloaded, file downloaded (Enterprise) |
| Content | Project or task created, updated, deleted, restored, or permission changed |
| Admin settings | Security policy, SSO, integrations, API tokens, webhooks |
| Billing | Plan change, payment method change |

Each entry records who did it (the user or the API token), the IP address, the user agent, the time in UTC, the object, and the values before and after.

## Retention

- **Business:** 1 year, viewable in the app.
- **Enterprise:** 7 years. Can also be streamed out (below).
- Entries can't be edited or deleted, including by Owners.

## View and export

**Settings > Security > Audit log**. You can filter by user, event type, object and date. Click **Export** to download CSV or JSON (up to 1 million rows per export). There is also an API: `GET /v2/audit-events`.

## Stream to a SIEM (Enterprise)

**Settings > Security > Audit log > Streaming** supports Splunk HEC, Datadog, Amazon S3, and a generic HTTPS endpoint. Events arrive within 60 seconds.

## Compliance documents

Customers can download SOC 2 Type II and ISO 27001 reports, plus the DPA, from the Trust Center at `trust.lumora.example` after signing an NDA. Don't attach these documents to cases.
