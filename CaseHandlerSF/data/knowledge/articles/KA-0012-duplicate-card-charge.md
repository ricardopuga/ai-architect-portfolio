---
article_number: KA-0012
title: Charged twice for a subscription
url_name: duplicate-card-charge
article_type: Troubleshooting
category: Account & Billing
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-09-20
related_cases: [CASE-1002]
summary: How to tell an authorization hold, a proration charge, a second workspace and a true double charge apart, and how to issue a refund.
---

## Work out what the second charge is

Open the customer in the Billing Console and compare the card statement with **Invoices** and **Payments**.

| What the customer sees | Likely cause | Action |
|---|---|---|
| A small or matching amount marked *pending*, which disappears within 3–7 business days | A card **authorization hold** taken when the card was added or updated | Explain that it's a hold, not a charge. Nothing to refund. |
| A second, smaller charge in the same month | **Proration** after adding seats or upgrading mid-cycle | Send the proration invoice and explain the line items. |
| Two full charges, each with its own invoice number and workspace | The customer pays for **two workspaces** | Confirm with the customer. Offer to merge or cancel one (KA-0047). |
| Two identical charges for the same invoice | A **true duplicate** caused by a payment retry | Refund one (below). |

## Refund a true duplicate

1. In the Billing Console, open the duplicate **payment** (not the invoice).
2. Click **Refund > Full**, reason *Duplicate*.
3. Refunds reach the card in 5–10 business days, depending on the bank.
4. Add a case comment with the refund ID.

Agents can refund duplicates without approval. Any other refund over $500 needs approval from a Billing Lead.

## Related

- KA-0013 Duplicate or revised invoices in billing history
