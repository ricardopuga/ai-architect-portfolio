---
article_number: KA-0034
title: How form auto-save and drafts work
url_name: form-autosave-drafts
article_type: FAQ
category: Forms
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-09-24
related_cases: [CASE-1042]
summary: When Lumora Forms saves a draft, why answers can be lost after a disconnect, and how form authors turn on reliable drafts.
---

## Does Lumora save my form answers automatically?

It depends on how the form author set it up.

| Setting (on the form) | Behavior |
|---|---|
| **Save drafts: Off** (default for public forms) | Nothing is saved until **Submit** |
| **Save drafts: This device** | Answers are saved in the browser every 15 seconds and when you leave a field. They come back if you reopen the form on the same device and browser |
| **Save drafts: Account** (signed-in respondents only) | Answers are saved to the server every 15 seconds and are available on any device |

## Why were answers lost after a disconnect?

- Drafts were **off** for that form.
- With **This device**, the browser was in private or incognito mode, or a privacy setting cleared site data when the browser closed.
- With **Account**, the connection dropped before the next 15-second save. You can lose up to 15 seconds of typing.
- File uploads aren't kept in drafts saved to the device. They have to be uploaded again.

## For form authors

1. Open the form, then **Settings > Responses > Save drafts**.
2. Choose **Account** for internal forms where respondents sign in, or **This device** for public forms.
3. Turn on **Warn before leaving with unsaved answers**.

## Offline

Lumora's mobile apps keep form answers offline and submit them when the connection returns. The web app doesn't submit while offline.
