---
article_number: KA-0033
title: Payments failing through a connected payment gateway in Lumora Forms
url_name: forms-payment-gateway-failures
article_type: Troubleshooting
category: Forms
plans: [Business, Enterprise]
last_reviewed: 2026-10-11
related_cases: [CASE-1044]
summary: Steps to diagnose payment forms that stop processing payments (rotated keys, webhook secret, currency, gateway outage). This is always handled as Urgent.
---

## Priority

Failed payments mean the customer is losing revenue. Set the case to **Urgent**.

## Step 1: Rule out an outage

- Check `status.lumora.example` for **Forms** or **Payments**.
- Ask the customer to check their payment provider's own status page.

## Step 2: Check the payment log

In the form, open **Settings > Payments > Transaction log**. Each attempt shows the gateway's response code.

| Error in log | Cause | Fix |
|---|---|---|
| `authentication_failed` / `invalid_api_key` | The API key was rotated or revoked in the gateway dashboard | Reconnect the gateway: **Settings > Integrations > Payments > Reconnect** |
| `webhook_signature_invalid` | The webhook signing secret changed | Copy the new secret into Lumora's payment settings |
| `currency_not_supported` | The form's currency changed to one the merchant account doesn't support | Change the form currency back, or enable the currency in the gateway |
| `account_restricted` | The gateway has restricted the merchant account (verification, compliance) | The customer must resolve it with their payment provider |
| `test_mode_key_in_live` | A test key was entered on a live form | Use the live key |
| No entries at all | The form doesn't reach the payment step | Check the payment field's conditional logic |

## Step 3: Tell the customer

- Payments are processed by the customer's own payment provider. Lumora doesn't hold card data.
- Failed submissions are saved as **Unpaid**. After the fix, the customer can send each submitter a payment link from **Responses > Unpaid > Send payment link**.

## Escalate

If the log shows `gateway_timeout` or Lumora errors (`5xx`), escalate to the Forms team on-call with the form ID and the transaction IDs.
