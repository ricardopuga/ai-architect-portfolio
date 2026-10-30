---
article_number: KA-0018
title: API rate limits and handling HTTP 429 responses
url_name: api-rate-limits
article_type: Reference
category: API & Integrations
plans: [Team, Business, Enterprise]
last_reviewed: 2026-10-08
related_cases: [CASE-1025]
summary: How Lumora API rate limits are counted (per workspace, across all tokens and integrations), which response headers to read, and how to avoid 429 errors.
---

## How limits are counted

Limits apply **per workspace per minute**, shared by **every** API token and installed integration in that workspace. This is the most common reason a customer says "we're hitting the limit even though we're within it": their own integration is sharing the allowance with other apps, such as the Salesforce connector, Zapier-style tools or a BI connector.

| Plan | Requests per minute | Burst |
|---|---|---|
| Team | 100 | 20 |
| Business | 300 | 50 |
| Enterprise | 1,000 | 200 |

Search endpoints (`/v2/search`) have a separate limit of 30 per minute on every plan.

## Response headers

Every response includes:

- `X-RateLimit-Limit`: the workspace's allowance
- `X-RateLimit-Remaining`: requests left in the current window
- `X-RateLimit-Reset`: when the window resets, as Unix epoch seconds

When the limit is exceeded, the API returns **429 Too Many Requests** with a `Retry-After` header in seconds.

## Best practices

1. Honor `Retry-After`, and use exponential backoff with jitter.
2. Use **webhooks** instead of polling for changes (KA-0019).
3. Use batch endpoints (`POST /v2/tasks/batch`, up to 100 items).
4. Request only the fields you need with `?fields=`.

## Investigating a complaint

**Settings > API > Usage** shows requests per token and per integration for the last 7 days. Ask the customer for a screenshot. Usually one integration is using most of the allowance. Enterprise customers can buy a higher limit through their CSM.
