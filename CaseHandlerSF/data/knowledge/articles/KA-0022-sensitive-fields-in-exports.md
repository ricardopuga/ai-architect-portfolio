---
article_number: KA-0022
title: Sensitive fields and data exports, including the scheduled-export known issue
url_name: sensitive-fields-in-exports
article_type: Known Issue
category: Reports & Data
plans: [Business, Enterprise]
last_reviewed: 2026-10-01
related_cases: [CASE-1045]
summary: How fields marked Sensitive are handled in exports, and a fixed defect (2026.08.1 to 2026.09.1) where scheduled exports included sensitive fields. Includes the security escalation steps.
---

## How it should work

Admins mark a custom field as **Sensitive** in **Settings > Fields > Edit > Sensitive**. Sensitive fields:

- Are masked in the UI (`••••`) for users without the **View sensitive data** permission.
- Are **left out of all exports** (manual, scheduled and API bulk export) unless the person running the export has **Export sensitive data**.
- Are recorded in the audit log whenever someone reveals or exports them.

## Known issue (resolved)

| | |
|---|---|
| Ticket | ENG-4388 |
| Affected releases | 2026.08.1 to 2026.09.1 |
| Fixed in | **2026.09.2** (released 2026-09-16) |
| Scope | **Scheduled** report exports only. Manual and API exports were not affected |

Scheduled exports created by a user with **Export sensitive data** kept including sensitive fields after the creator lost that permission, or when the schedule was handed to another owner.

## If a customer reports sensitive data in an export

Treat it as a possible data exposure. Set priority to at least **High**.

1. Ask for the export file name, the report or schedule name, and the date it was received. **Don't** ask them to attach the file.
2. Check the date. If it was before 2026-09-16 and the export was scheduled, it matches ENG-4388.
3. Escalate to the **Security & Privacy** queue in every case. They decide whether the customer must be formally notified under the DPA.
4. Recommend the customer delete any copies, review the schedule's recipients, and check who holds **Export sensitive data** under **Settings > Roles**.
5. If the date is **after** the fix, escalate to Reports Engineering as a possible regression and mention ENG-4388.
