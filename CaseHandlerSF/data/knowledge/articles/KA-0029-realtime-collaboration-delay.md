---
article_number: KA-0029
title: Real-time collaboration changes appear with a delay
url_name: realtime-collaboration-delay
article_type: Troubleshooting
category: Performance
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-09-26
related_cases: [CASE-1032]
summary: Changes from other users showing up about 30 seconds late almost always means WebSockets are blocked and the app has fallen back to polling. Here is how to confirm and fix it.
---

## Symptoms

When several people edit the same board, document or task at once, each person's changes reach the others about **30 seconds** late instead of immediately. Users may also see edit conflicts.

## Cause

Lumora sends live updates over a WebSocket connection to `wss://rt.lumora.example`. If something on the network blocks or breaks WebSockets, the app quietly falls back to **polling every 30 seconds**. That matches the delay users describe. Common culprits:

- A corporate proxy or secure web gateway that doesn't support WebSocket upgrades, or that inspects TLS traffic.
- A firewall that closes idle connections after a short time.
- Browser extensions (privacy or ad-blocking tools).

## Confirm

1. In the app, open **Help > Connection diagnostics**. It shows **Live updates: Connected (WebSocket)** or **Fallback (polling)**.
2. Or, in the browser DevTools **Network** tab, filter by **WS** and look for a connection to `rt.lumora.example`.

## Fix

Send this to the customer's IT team:

- Allow WebSocket (HTTP Upgrade) traffic to `rt.lumora.example` on port 443.
- Exclude `*.lumora.example` from TLS inspection.
- Set the idle timeout for these connections to at least 120 seconds. The app sends a heartbeat every 45 seconds.

## If WebSockets are connected and it's still slow

Collect the diagnostics output and a HAR file, and escalate to the Realtime team with the workspace ID and the object that was being edited.
