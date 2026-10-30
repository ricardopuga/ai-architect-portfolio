---
article_number: KA-0003
title: How to collect a HAR file and browser console logs
url_name: collect-har-console-logs
article_type: How-to
category: Getting Help
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-08-20
related_cases: [CASE-1005, CASE-1039]
summary: Step-by-step instructions for capturing a HAR file and console output in Chrome, Edge, Firefox and Safari so Engineering can diagnose browser issues.
---

## When to ask for this

For any problem in the web app that you cannot reproduce: slow pages, errors, buttons that don't respond, data not loading.

## Chrome and Edge

1. Open Lumora Workspace in the tab where the problem happens.
2. Press **F12** (or **Cmd+Option+I** on Mac) and open the **Network** tab.
3. Tick **Preserve log**, then click the clear button (🚫).
4. Reproduce the problem.
5. Right-click any request and choose **Save all as HAR with content**.
6. Open the **Console** tab, right-click, and choose **Save as…**

## Firefox

1. Press **F12** and open **Network**. Tick **Persist Logs**.
2. Reproduce the problem.
3. Click the gear icon and choose **Save All As HAR**.

## Safari

1. Turn on **Develop** in **Settings > Advanced > Show features for web developers**.
2. Choose **Develop > Show Web Inspector > Network**, tick **Preserve Log**, and reproduce.
3. Click **Export**.

## Privacy

HAR files can contain session cookies. Ask customers to upload them through the secure attachment link on the case, never by email. Support deletes attachments 30 days after the case closes.

## Supported browsers

The latest two major versions of Chrome, Edge, Firefox and Safari. Internet Explorer and legacy Edge are not supported.
