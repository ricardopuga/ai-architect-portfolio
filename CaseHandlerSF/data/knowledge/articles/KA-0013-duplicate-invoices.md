---
article_number: KA-0013
title: Duplicate or revised invoices in billing history
url_name: duplicate-invoices
article_type: FAQ
category: Account & Billing
plans: [Team, Business, Enterprise]
last_reviewed: 2026-09-20
related_cases: [CASE-1011]
summary: Why the same invoice can appear twice in billing history (a voided original and its revision, or a separate proration invoice) and how to give accounting a clean record.
---

## Question

"I see the same invoice twice in billing history. Will I be billed twice, and what should our accounting team use?"

## Answer

In most cases one of the two invoices is **void** and replaced by a **revised** invoice. Lumora creates a revision when billing details change after the invoice is issued, for example a new billing address, an added VAT/tax ID, or a change to the PO number.

How to tell them apart in **Settings > Billing > Invoices**:

- The original shows the status **Void** and the invoice number ends in `-V`.
- The revision has the same base number with the suffix `-R1` and the status **Paid** or **Open**.
- Only the revised invoice is charged.

Other reasons for invoices that look alike:

- A **proration invoice** for seats added in the middle of the cycle. It has a different number and a smaller amount.
- **Two workspaces** with the same billing contact (see KA-0012).

## For accounting

- Turn on **Settings > Billing > Hide voided invoices** to remove voided invoices from the list.
- Click **Export statement** to download a CSV that contains only valid invoices and credit notes.
- If the customer needs the voided invoice removed from the record completely (for example, it was already sent to an ERP), Billing can issue a formal credit note. Escalate to the Billing queue.
