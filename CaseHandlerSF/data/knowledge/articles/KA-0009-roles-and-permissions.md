---
article_number: KA-0009
title: Workspace roles and permissions, and why an admin sees read-only options
url_name: roles-and-permissions
article_type: Reference
category: Users & Permissions
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-09-05
related_cases: [CASE-1008]
summary: What each role (Owner, Admin, Member, Guest, Viewer seat) can do, how project-level roles override workspace roles, and how to fix "I should be admin but everything is read-only".
---

## Roles

| Role | Can do |
|---|---|
| **Owner** | Everything, including billing, security settings, SSO and deleting the workspace. A workspace has at least one Owner. |
| **Admin** | Manage members, projects, integrations and automations. Can't manage billing or SSO. |
| **Member** | Create and edit projects, tasks, forms and reports they have access to. |
| **Guest** | Access only to projects they are invited to. Can't see the member directory. |
| **Viewer seat** | Read-only everywhere and free. This is a *seat type*, not a role. |

**Seat type takes priority over role.** A user on a Viewer seat is read-only even if their role says Admin.

## Project-level roles

Each project can set its own roles (Project manager, Editor, Commenter, Viewer). A workspace Admin is automatically Project manager on every project. A Member can be a Viewer on one project and an Editor on another.

## "I should have admin access but only see read-only options"

Check these in order:

1. **Seat type.** In **Settings > Members**, find the user. If **Seat** says *Viewer*, change it to *Full* (this needs a free paid seat).
2. **Wrong workspace.** The user may belong to several workspaces and be an Admin in only one. They can switch with the workspace picker in the top-left corner.
3. **Locked during billing.** If the subscription is past due, the workspace becomes read-only for everyone except Owners (see KA-0015).
4. **Stale session.** Role changes take effect the next time the page loads. Ask the user to sign out and back in.
5. **SCIM group mapping (Enterprise).** If roles come from the IdP through SCIM, a change made in Lumora is overwritten at the next sync. Change the user's group in the IdP instead.
