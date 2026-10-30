---
article_number: KA-0014
title: Billing address form shows validation errors
url_name: billing-address-validation-errors
article_type: Troubleshooting
category: Account & Billing
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-08-30
related_cases: [CASE-1020]
summary: The billing address form checks the postal code, state/region and tax ID against the selected country. Here is how to clear errors on an address that is correct.
---

## Symptoms

When the user saves the billing address, the form shows "Please enter a valid address" or highlights the postal code, even though the address is correct.

## Causes and resolution

1. **The country doesn't match the address.** The country field is filled in from the browser's locale. Check that it's right *before* entering the postal code. The postal code and region checks depend on the country.
2. **Postal code format.**
   - US ZIP: 5 digits or ZIP+4 (`12345-6789`).
   - UK: include the space (`SW1A 1AA`).
   - Canada: `A1A 1A1`.
   - Ireland: Eircode is optional. Leave the field blank instead of typing `N/A`.
3. **State or region is required.** For the US, Canada, Australia, India and Brazil, choose a value from the drop-down. Free text isn't accepted.
4. **Tax ID format.** If a VAT/GST number is entered, it's checked against the relevant government service (VIES for EU numbers). Include the country prefix (`DE123456789`). If VIES is down, the form fails. Save without the tax ID and add it later.
5. **PO box (US).** Allowed in address line 1. Make sure line 2 isn't filled with only spaces.
6. **Browser autofill** sometimes adds invisible characters. Type the address by hand or paste it as plain text.

## Agent workaround

If the customer is still blocked, an agent can update the address in **Billing Console > Customer > Edit address** with **Skip validation** ticked. Add a case comment saying what was entered.
