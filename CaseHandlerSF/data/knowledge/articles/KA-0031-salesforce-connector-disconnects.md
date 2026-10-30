---
article_number: KA-0031
title: Salesforce connector keeps disconnecting
url_name: salesforce-connector-disconnects
article_type: Troubleshooting
category: API & Integrations
plans: [Business, Enterprise]
last_reviewed: 2026-10-09
related_cases: [CASE-1007]
summary: Why the Lumora–Salesforce connector loses its connection (refresh token policy, the connecting user's session or password, IP restrictions, API limits) and how to make it stable.
---

## Symptoms

The Salesforce connector shows **Disconnected — reauthorization required** every few hours or days. Syncs stop until someone reconnects it.

## Causes and resolution

1. **Refresh token policy in Salesforce.** In Salesforce Setup, go to **Connected Apps OAuth Usage > Lumora Workspace > Manage > Edit Policies**. Set **Refresh Token Policy** to *Refresh token is valid until revoked*. If it's set to "Expire refresh token after X hours", the connector disconnects on that schedule. This is the most common cause.
2. **The connecting user's password changed or they were deactivated.** The connector runs as the Salesforce user who authorized it. Use a dedicated **integration user** whose password never expires.
3. **IP restrictions.** If **Permitted Users** is set to *Admin approved users are pre-authorized* or IP relaxation is set to *Enforce IP restrictions*, allow Lumora's outbound IPs (listed at `https://lumora.example/ips`) on the integration user's profile, or set **IP Relaxation** to *Relax IP restrictions* for the Lumora connected app.
4. **Salesforce API limit reached.** When the org hits its daily API limit, Salesforce rejects the calls. Lumora shows this as a disconnect. Check **Setup > Company Information > API Requests, Last 24 Hours**.
5. **Sandbox refresh.** Refreshing a sandbox removes all OAuth grants. Reconnect afterwards.
6. **Too many tokens.** Salesforce allows 5 refresh tokens per user per connected app. Authorizing more than that silently revokes the oldest one. Don't share one integration user across several Lumora workspaces.

## Reconnect

**Settings > Integrations > Salesforce > Reconnect**, signed in as the integration user. Field mappings are kept.
