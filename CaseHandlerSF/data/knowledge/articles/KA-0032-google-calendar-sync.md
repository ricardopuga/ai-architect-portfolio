---
article_number: KA-0032
title: Google Calendar two-way sync isn't working
url_name: google-calendar-sync
article_type: Troubleshooting
category: API & Integrations
plans: [Team, Business, Enterprise]
last_reviewed: 2026-09-19
related_cases: [CASE-1016]
summary: How to fix Lumora events and task due dates not appearing in Google Calendar, or Google events not appearing in Lumora.
---

## How the sync works

- Each user connects their own Google account under **Profile > Integrations > Google Calendar**.
- **Lumora → Google:** tasks with a due date and time, and Lumora events, are written to one chosen calendar (by default a new calendar called *Lumora*).
- **Google → Lumora:** events from the calendars you tick show up on your Lumora calendar view.
- Changes usually sync within 2 minutes.

## Troubleshooting

1. **Looking at the wrong calendar.** Lumora items go to the *Lumora* calendar, not the user's primary calendar. In Google Calendar, make sure the *Lumora* calendar is visible (ticked in the left sidebar).
2. **Tasks without a time.** Tasks with only a due date are added as all-day events only if **Sync all-day tasks** is on.
3. **Google calendars not ticked.** Under **Profile > Integrations > Google Calendar > Calendars to show**, tick the calendars that should appear in Lumora.
4. **Permission not granted.** If the user unticked calendar permissions on Google's consent screen, the sync works in only one direction. Disconnect, reconnect, and grant every requested permission.
5. **Google Workspace admin restrictions.** The customer's Google admin may block third-party apps. They need to allow *Lumora Workspace* under **Admin console > Security > API controls > App access control**.
6. **Token revoked.** A password change or Google security review can revoke access. The integration page then shows **Reconnect required**.

## Escalate

If the integration shows **Connected** and the steps above don't help, collect the user's email, an example item (its title and time, with timezone), and the direction of sync that fails. Escalate to the Integrations team.
