---
article_number: KA-0030
title: Data connector sync is slower than usual
url_name: data-connector-sync-delays
article_type: Troubleshooting
category: API & Integrations
plans: [Team, Business, Enterprise]
last_reviewed: 2026-10-07
related_cases: [CASE-1014]
summary: How to diagnose data connectors that take 30+ minutes to sync instead of the usual interval (source throttling, full resyncs, errors, plan interval).
---

## Expected interval

Incremental syncs run every **15 minutes on Team** and **5 minutes on Business and Enterprise** (KA-0001). A sync normally takes under a minute for a few thousand changed records.

## Diagnose

Open **Settings > Integrations > [connector] > Sync log**. For each run it shows the start time, duration, records processed, and any warnings.

| What the sync log shows | Meaning | Action |
|---|---|---|
| `Throttled by source (429)` | The *external system* is limiting Lumora's requests | Raise the API limit in the source system, or reduce the fields being synced |
| `Full resync in progress` | A schema change or a re-authorization started a full resync | Wait. Incremental syncs resume afterwards. Large sources can take hours |
| Runs are skipped or overlap | The previous sync hadn't finished when the next was due | Reduce the objects or fields synced, or ask for a longer interval |
| `Auth error` | The connection's credentials expired | Reconnect (see KA-0031 for Salesforce) |
| Nothing unusual, but runs are long | Possibly a backlog on Lumora's side | Check the status page, then escalate |

## Reduce sync volume

- Under **Connector > Objects**, turn off objects you don't use.
- Under **Connector > Filters**, sync only active records, for example `Status != Closed`.
- Avoid formula or rollup fields in the source system that change on every record each night. They make every record look modified.

## Escalate

Include the connector type, the workspace ID, and a screenshot or export of the sync log covering the slow period.
