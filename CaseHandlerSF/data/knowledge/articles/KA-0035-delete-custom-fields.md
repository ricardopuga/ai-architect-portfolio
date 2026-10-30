---
article_number: KA-0035
title: Custom field can't be deleted
url_name: delete-custom-fields
article_type: Troubleshooting
category: Forms
plans: [Team, Business, Enterprise]
last_reviewed: 2026-09-11
related_cases: [CASE-1012]
summary: Why Delete does nothing or fails for a custom field (it's used in automations, reports, forms, formulas or integrations) and how to find and remove those references.
---

## Symptoms

In **Settings > Fields**, the user clicks **Delete** on a custom field. Nothing happens, or a short message appears: "This field can't be deleted."

## Cause

A field can't be deleted while anything still uses it:

- Automation rule conditions or actions
- Report filters, columns or groupings, and dashboard widgets
- Form questions mapped to the field
- Formula fields that refer to it
- Integration field mappings (for example the Salesforce connector)
- Required-field rules on a project

**Known UI defect (ENG-4502):** the message that lists these references sometimes closes straight away, so it looks as though nothing happened. Fix due in 2026.11.1.

## Resolution

1. In **Settings > Fields**, open the field and go to the **Usage** tab. It lists every reference with a link.
2. Remove or change each reference: edit the automation, report or form, or remap the integration field.
3. Return to the field and click **Delete** again.

## Alternative: hide instead of delete

If the field is used in a lot of places, choose **Archive field**. It disappears from forms, views and pickers, but past values and references are kept. You can restore an archived field at any time.

## After deletion

Deleted fields can be restored for 30 days (**Settings > Fields > Deleted**), along with their values.
