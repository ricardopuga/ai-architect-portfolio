---
article_number: KA-0039
title: Email notifications show raw HTML tags
url_name: email-notifications-raw-html
article_type: Troubleshooting
category: Notifications
plans: [Team, Business, Enterprise]
last_reviewed: 2026-10-13
related_cases: [CASE-1041]
summary: Why notification emails can show tags such as <b> or <p> as text (custom templates, automation emails, plain-text mail clients) and how to fix each.
---

## Symptoms

Notification emails show tags like `<p>`, `<br>` or `<b>` as plain text instead of formatting.

## Causes and resolution

1. **Custom automation email with HTML typed into the plain-text box.** The **Send email** automation action has two editors, **Rich text** and **Plain text**. HTML typed into **Plain text** is sent as literal characters. Switch the action to **Rich text** and use the formatting toolbar, or paste the HTML with **Insert > HTML block**.
2. **Field values that contain HTML.** When an email includes a field value (for example `{{task.description}}`) and that field holds HTML imported from another system, the HTML is escaped for safety. Use `{{task.description | rich}}` to show the formatting, or clean up the imported data.
3. **Custom workspace email template (Enterprise).** If an Admin edited **Settings > Branding > Email templates** and saved it while the editor was in *Source* mode, the template may now be double-encoded. Click **Restore default template**, then make the changes again in the visual editor.
4. **The mail client shows plain text only.** Some mail clients, and security gateways that remove HTML, show the plain-text version. That version shouldn't contain tags. If it does, it matches defect ENG-4530 (fix in 2026.11.1).

## Escalate

Ask the customer to forward an affected email **as an attachment** (.eml) so the headers are kept, and escalate to the Notifications team.
