---
article_number: KA-0008
title: "Known issue: SSO logout does not fully end the Lumora session"
url_name: known-issue-sso-logout-session
article_type: Known Issue
category: Sign-in & Security
plans: [Business, Enterprise]
last_reviewed: 2026-10-12
related_cases: [CASE-1049]
summary: After logging out through the identity provider, Lumora sessions and cached data can stay on the device. Workarounds are available, and a fix is planned for release 2026.11.1.
---

## Status

**Open.** Engineering ticket ENG-4471. Fix planned for release **2026.11.1**.

## Symptoms

- A user logs out through their identity provider portal (IdP-initiated logout), but Lumora tabs that are already open keep working.
- After logout, pressing Back or reopening the app shows cached project data until the page is refreshed.

## Cause

There are two separate problems:

1. If the SAML connection has no **Single Logout URL**, Lumora never hears about the IdP logout. The Lumora session lasts until it times out on its own (12 hours by default).
2. Even when Single Logout is set up, the web app's offline cache (service worker) isn't cleared on logout. This is the defect being fixed in 2026.11.1.

## Workarounds

1. Make sure Single Logout is configured in **both** the IdP and in Lumora (**Settings > Security > Single sign-on > Edit > Single Logout URL**). This ends the server-side session.
2. Shorten **Settings > Security > Session lifetime** to as little as 1 hour.
3. On shared or kiosk devices, turn on **Settings > Security > Disable offline cache**. Users lose offline access, but nothing is cached on the device.
4. Users can sign out with **Profile > Sign out** in Lumora as well as in the IdP. That clears the local cache.

## Customer messaging

Tell customers that server-side sessions **are** ended when Single Logout is configured. The remaining risk is data cached in the browser on that device. Link the case to ENG-4471 so the customer is notified when the fix ships.
