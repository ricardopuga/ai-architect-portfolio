---
article_number: KA-0019
title: Setting up webhooks and fixing delivery failures
url_name: webhooks-setup-troubleshooting
article_type: Troubleshooting
category: API & Integrations
plans: [Team, Business, Enterprise]
last_reviewed: 2026-09-14
related_cases: [CASE-1004]
summary: How webhook registration, verification, signatures and retries work, and how to diagnose 500 errors and failed deliveries.
---

## How webhooks work

1. Register an endpoint: **Settings > API > Webhooks > Add endpoint**, or `POST /v2/webhooks`.
2. Lumora sends a **verification request** with `{"type":"verification","challenge":"..."}`. Your endpoint must reply `200` within 10 seconds with the `challenge` value in the body.
3. Each event is a `POST` with a JSON body. It is signed in the `X-Lumora-Signature` header (HMAC-SHA256 of the raw body using the endpoint secret).
4. If your endpoint returns anything other than 2xx, or takes longer than 10 seconds, Lumora retries 5 times over 24 hours with exponential backoff. After 24 hours of failures, the endpoint is **disabled**.

## "500 errors when setting up webhooks"

First work out **who** is returning the 500:

- **The customer's endpoint returns 500** (shown in **Webhooks > Endpoint > Delivery log**). The problem is in their code. Common causes:
  - The verification `challenge` isn't handled, so their code fails trying to parse an event it doesn't expect.
  - The signature is checked against *parsed and re-serialized* JSON instead of the raw request body.
  - The handler does slow work before responding. Respond `200` first and process the event in the background.
- **The Lumora API returns 500 to `POST /v2/webhooks`.** Usually the URL is invalid, isn't HTTPS, or points to a private IP address, and the API returns a 500 where it should return a 400. That is known defect ENG-4210. Check that the URL is public HTTPS with a valid certificate. If it still fails, escalate with the `X-Request-Id` from the response.

## Re-enable a disabled endpoint

Fix the endpoint, then click **Re-enable**. Choose **Replay failed events** to resend events from the last 72 hours.

## Testing

Use **Send test event** on the endpoint page. Customers can also point a temporary request-inspection URL at it to see the exact payload.
