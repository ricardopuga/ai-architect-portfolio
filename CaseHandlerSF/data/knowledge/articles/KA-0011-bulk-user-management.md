---
article_number: KA-0011
title: Adding, updating and removing users in bulk
url_name: bulk-user-management
article_type: How-to
category: Users & Permissions
plans: [Team, Business, Enterprise]
last_reviewed: 2026-09-12
related_cases: [CASE-1015]
summary: Three ways to manage many users at once (CSV import, selecting several rows in the member list, and SCIM provisioning) and when to use each.
---

## Choose a method

| Method | Plans | Best for |
|---|---|---|
| Select several rows in the member list | Team+ | Changing the role or seat for up to 500 users at once |
| CSV import | Team+ | Onboarding or offboarding a large group in one go |
| SCIM 2.0 provisioning | Enterprise | Keeping users in sync with your IdP automatically |

## Member list (several rows)

1. Go to **Settings > Members**.
2. Tick the users, or use the filter and then **Select all matching**.
3. Choose **Change role**, **Change seat**, **Deactivate** or **Remove**.

## CSV import

1. Go to **Settings > Members > Import > Download template**.
2. Fill in the columns `email`, `first_name`, `last_name`, `role` (`admin`, `member` or `guest`), `seat` (`full` or `viewer`), `action` (`add`, `update`, `deactivate` or `remove`) and an optional `projects` column, separated by semicolons.
3. Upload the file. Lumora shows a preview with row-level errors before anything changes.
4. Confirm. You can import up to 5,000 rows per file. Invitations go out as each row is processed.

## Deactivate or remove?

- **Deactivate** frees the seat and keeps everything the user created assigned to them. You can reverse it.
- **Remove** frees the seat and moves their open tasks to the person you choose. You can't reverse it.

## SCIM

On Enterprise, generate a token under **Settings > Security > SCIM** and enter it with the base URL `https://api.lumora.example/scim/v2` in your IdP. Users and group-to-role mappings then come from the IdP.
