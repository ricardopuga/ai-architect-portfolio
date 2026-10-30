---
article_number: KA-0044
title: Using a custom domain for your workspace
url_name: custom-domain-setup
article_type: How-to
category: Account & Billing
plans: [Enterprise]
last_reviewed: 2026-09-29
related_cases: [CASE-1043]
summary: How Enterprise workspaces serve Lumora from their own domain (for example work.example.com) using a CNAME record and an automatically managed TLS certificate.
---

## Availability

Custom domains are available on **Enterprise** only. On other plans, the workspace uses `<subdomain>.lumora.example`. The subdomain can be changed once every 30 days under **Settings > Workspace > Address**.

If a customer on a lower plan asks for this, explain that it's an Enterprise feature and offer to bring in their account manager. Close the case as **Resolved – Plan limitation**.

## Setup (Enterprise)

1. Go to **Settings > Workspace > Custom domain** and enter the domain, for example `work.example.com`. Only subdomains are supported, not apex domains like `example.com`.
2. In your DNS, create a **CNAME** record: `work.example.com → custom.lumora.example`.
3. Click **Verify**. DNS changes can take up to 24 hours to spread, but usually take minutes.
4. Lumora issues and renews the TLS certificate automatically. If your domain has **CAA** records, add `letsencrypt.org`.
5. When the status shows **Active**, the old `lumora.example` address redirects to the custom domain.

## After switching

- Update the SSO settings in your IdP: the Entity ID and ACS URL change to the custom domain (KA-0007). Lumora accepts both the old and new addresses for 14 days.
- Webhook and API URLs **don't change**. The API stays on `api.lumora.example`.
- Links in existing emails and bookmarks keep working through the redirect.

## Troubleshooting

| Status | Fix |
|---|---|
| `CNAME not found` | Check the record. Some DNS providers add the zone name automatically |
| `Certificate pending` for more than 1 hour | Check CAA records. Make sure there's no proxy (orange-cloud style) in front of the CNAME |
