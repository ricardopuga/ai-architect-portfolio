---
article_number: KA-0001
title: Lumora Workspace plans and limits
url_name: plans-and-limits
article_type: Reference
category: Account & Billing
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-10-01
related_cases: [CASE-1021, CASE-1031, CASE-1036]
summary: The limits for each Lumora Workspace plan (storage, upload size, API rate, automations, connectors) in one table.
---

## Overview

Use this table when a customer asks "what does my plan include?" or reports hitting a limit. Other articles link here so the numbers stay in one place.

| Limit | Starter | Team | Business | Enterprise |
|---|---|---|---|---|
| Storage per workspace | 10 GB | 100 GB | 1 TB | Custom (from 5 TB) |
| Max file upload (web) | 50 MB | 50 MB | 250 MB | 2 GB |
| API requests per minute (per workspace) | n/a | 100 | 300 | 1,000 |
| Active automation rules per workspace | 5 | 50 | 250 | 1,000 |
| Automation runs per month | 1,000 | 25,000 | 250,000 | Unlimited (fair use) |
| Data connector sync interval | n/a | 15 min | 5 min | 5 min (1 min on request) |
| SSO (SAML / OIDC) | No | No | Yes | Yes |
| SCIM provisioning | No | No | No | Yes |
| Audit log retention | n/a | n/a | 1 year | 7 years |
| Backup snapshot retention | 30 days | 30 days | 30 days | 90 days |
| Custom domain | No | No | No | Yes |

## Notes

- Limits apply **per workspace**, not per user or per API token.
- Customers can see current usage under **Settings > Workspace > Usage**.
- To raise a limit, the customer upgrades their plan or, on Enterprise, contacts their Customer Success Manager. Support agents cannot raise limits themselves.
