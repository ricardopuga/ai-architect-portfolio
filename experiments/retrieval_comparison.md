# Vector vs hybrid vs hybrid + rerank

10 questions, top 5 chunks each. The answer prompt is the same as rag_answer.py.

| Method | Fact in the 5 chunks | Fact in Claude's answer | Citations valid |
|---|---|---|---|
| vector | 9/10 | 9/10 | 10/10 |
| hybrid (vector + BM25) | 10/10 | 10/10 | 10/10 |
| hybrid + rerank | 10/10 | 10/10 | 9/10 |

Each cell: was the fact in the 5 chunks / was it in Claude's answer.

| # | Question | vector | hybrid (vector + BM25) | hybrid + rerank |
|---|---|---|---|---|
| Q1 | What does the payment error currency_not_supported mean? | found / yes | found / yes | found / yes |
| Q2 | What is ENG-4388? | found / yes | found / yes | found / yes |
| Q3 | Our SAML login fails with Audience mismatch. How do I fix it? | found / yes | found / yes | found / yes |
| Q4 | Which HTTP header carries the webhook signature? | found / yes | found / yes | found / yes |
| Q5 | The iOS app closes at the splash screen on version 2.3.1. | found / yes | found / yes | found / yes |
| Q6 | Our custom domain has said Certificate pending for over an hour. | found / yes | found / yes | found / yes |
| Q7 | Teammates' edits show up half a minute late. How do we fix it? | MISSED / no | found / yes | found / yes |
| Q8 | The payment log shows test_mode_key_in_live. | found / yes | found / yes | found / yes |
| Q9 | How many API requests per minute does the Business plan allow? | found / yes | found / yes | found / yes |
| Q10 | CSV export opens in Excel with everything in one column. | found / yes | found / yes | found / yes |

## Q1. What does the payment error currency_not_supported mean?

Expected: merchant account or enable the currency (KA-0033)

### vector: fact found in the 5 chunks

- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Step 2: Check the payment log
- KA-0014 Billing address form shows validation errors > Causes and resolution
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Escalate
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Priority
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Step 1: Rule out an outage

Answer (has the fact, citations OK):

> The `currency_not_supported` error means the form's currency was changed to one the merchant account doesn't support [KA-0033].
> 
> To fix it, either change the form currency back, or enable that currency in the payment gateway [KA-0033]. You can see this error in the form under **Settings > Payments > Transaction log**, which shows the gateway's response code for each payment attempt [KA-0033].

### hybrid (vector + BM25): fact found in the 5 chunks

- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Step 2: Check the payment log
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Priority
- KA-0008 Known issue: SSO logout does not fully end the Lumora session > Status
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Step 3: Tell the customer
- KA-0012 Charged twice for a subscription > Work out what the second charge is

Answer (has the fact, citations OK):

> The `currency_not_supported` error means the form's currency was changed to one the merchant account doesn't support [KA-0033].
> 
> **To fix it, either:**
> - Change the form's currency back, or
> - Enable the new currency in the payment gateway [KA-0033].
> 
> **Other things to know:**
> - You can see this error in the form under **Settings > Payments > Transaction log** [KA-0033].
> - Failed submissions are saved as **Unpaid**. After the fix, the customer can send each submitter a payment link from **Responses > Unpaid > Send payment link** [KA-0033].
> - Failed payments mean lost revenue for the customer, so set the case to **Urgent** [KA-0033].

### hybrid + rerank: fact found in the 5 chunks

- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Step 2: Check the payment log
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Escalate
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Priority
- KA-0015 Renewal reminders, the grace period and reactivating a lapsed subscription > What happens when payment fails?
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Step 3: Tell the customer

Answer (has the fact, citations OK):

> The `currency_not_supported` error means the form's currency was changed to one the merchant account doesn't support [KA-0033].
> 
> To fix it, either:
> - Change the form's currency back, or
> - Enable that currency in the payment gateway [KA-0033].
> 
> You can see this error, with the gateway's response code for each attempt, under **Settings > Payments > Transaction log** in the form [KA-0033].
> 
> After the fix, failed submissions are saved as **Unpaid**. The customer can send each submitter a payment link from **Responses > Unpaid > Send payment link** [KA-0033].

## Q2. What is ENG-4388?

Expected: scheduled (KA-0022)

### vector: fact found in the 5 chunks

- KA-0022 Sensitive fields and data exports, including the scheduled-export known issue > If a customer reports sensitive data in an export
- KA-0022 Sensitive fields and data exports, including the scheduled-export known issue > Known issue (resolved)
- KA-0008 Known issue: SSO logout does not fully end the Lumora session > Status
- KA-0011 Adding, updating and removing users in bulk > CSV import
- KA-0014 Billing address form shows validation errors > Symptoms

Answer (has the fact, citations OK):

> ENG-4388 is a **resolved known issue** with scheduled report exports [KA-0022].
> 
> - **What happened:** If a user with **Export sensitive data** created a scheduled export, it kept including sensitive fields after that user lost the permission, or after the schedule was handed to another owner [KA-0022].
> - **Scope:** Only **scheduled** report exports were affected. Manual and API exports were not [KA-0022].
> - **Affected releases:** 2026.08.1 to 2026.09.1 [KA-0022].
> - **Fix:** Release **2026.09.2**, released 2026-09-16 [KA-0022].
> 
> **If a customer reports sensitive data in an export:**
> - Treat it as a possible data exposure with priority **High** or above [KA-0022].
> - Ask for the file name, the report or schedule name, and the date received. Don't ask them to attach the file [KA-0022].
> - A scheduled export received before 2026-09-16 matches ENG-4388 [KA-0022].
> - Always escalate to **Security & Privacy** [KA-0022].
> - If the export is dated after the fix, also escalate to Reports Engineering as a possible regression and mention ENG-4388 [KA-0022].

### hybrid (vector + BM25): fact found in the 5 chunks

- KA-0022 Sensitive fields and data exports, including the scheduled-export known issue > If a customer reports sensitive data in an export
- KA-0022 Sensitive fields and data exports, including the scheduled-export known issue > Known issue (resolved)
- KA-0008 Known issue: SSO logout does not fully end the Lumora session > Status
- KA-0014 Billing address form shows validation errors > Agent workaround
- KA-0045 Handling feature requests and finding out what's on the roadmap > Status of frequently requested features (October 2026)

Answer (has the fact, citations OK):

> ENG-4388 is a resolved known issue with **scheduled** report exports. If a user with the **Export sensitive data** permission created a scheduled export, it kept including sensitive fields even after that user lost the permission, or after the schedule was handed to another owner [KA-0022].
> 
> - **Affected releases:** 2026.08.1 to 2026.09.1 [KA-0022]
> - **Fixed in:** 2026.09.2, released 2026-09-16 [KA-0022]
> - **Scope:** Scheduled exports only. Manual and API exports were not affected [KA-0022]
> 
> **If a customer reports sensitive data in an export:**
> - If it was a scheduled export received before 2026-09-16, it matches ENG-4388 [KA-0022].
> - Always escalate to the **Security & Privacy** queue, whatever the date [KA-0022].
> - If the export was received after the fix, also escalate to Reports Engineering as a possible regression and mention ENG-4388 [KA-0022].

### hybrid + rerank: fact found in the 5 chunks

- KA-0022 Sensitive fields and data exports, including the scheduled-export known issue > Known issue (resolved)
- KA-0022 Sensitive fields and data exports, including the scheduled-export known issue > If a customer reports sensitive data in an export
- KA-0008 Known issue: SSO logout does not fully end the Lumora session > Customer messaging
- KA-0008 Known issue: SSO logout does not fully end the Lumora session > Status
- KA-0014 Billing address form shows validation errors > Causes and resolution

Answer (has the fact, citations OK):

> ENG-4388 is a resolved known issue with **scheduled** report exports [KA-0022].
> 
> - **What happened:** If a user with **Export sensitive data** created a scheduled export, that export kept including sensitive fields after the creator lost the permission. The same happened when the schedule was handed to another owner [KA-0022].
> - **Scope:** Only scheduled exports were affected. Manual and API exports were not [KA-0022].
> - **Affected releases:** 2026.08.1 to 2026.09.1 [KA-0022].
> - **Fix:** Release **2026.09.2**, released 2026-09-16 [KA-0022].
> 
> **If a customer reports sensitive data in an export:**
> 1. Treat it as a possible data exposure, with priority at least **High** [KA-0022].
> 2. Ask for the export file name, the report or schedule name, and the date it was received. Don't ask them to attach the file [KA-0022].
> 3. If it was a scheduled export received before 2026-09-16, it matches ENG-4388 [KA-0022].
> 4. Always escalate to the **Security & Privacy** queue. They decide whether the customer must be formally notified under the DPA [KA-0022].
> 5. Recommend the customer delete any copies, review the schedule's recipients, and check who holds **Export sensitive data** under **Settings > Roles** [KA-0022].
> 6. If the date is after the fix, also escalate to Reports Engineering as a possible regression and mention ENG-4388 [KA-0022].

## Q3. Our SAML login fails with Audience mismatch. How do I fix it?

Expected: case-sensitive or trailing slash (KA-0007)

### vector: fact found in the 5 chunks

- KA-0007 Setting up SAML single sign-on > Common errors
- KA-0007 Setting up SAML single sign-on > Related
- KA-0007 Setting up SAML single sign-on > Values to enter in your IdP
- KA-0008 Known issue: SSO logout does not fully end the Lumora session > Status
- KA-0007 Setting up SAML single sign-on > Steps in Lumora

Answer (has the fact, citations OK):

> The `Audience mismatch` error means the **Entity ID / Audience URI** in your identity provider doesn't exactly match the value Lumora expects [KA-0007].
> 
> 1. In your IdP, copy the Entity ID / Audience URI value again. It must be exactly `https://<subdomain>.lumora.example/sso/saml/metadata` [KA-0007]. The value is case-sensitive and must have no trailing slash [KA-0007].
> 2. In Lumora, click **Test connection** in a private browser window to confirm it works [KA-0007].
> 
> Until SSO is confirmed working, keep at least one Owner account able to sign in with a password [KA-0007].

### hybrid (vector + BM25): fact found in the 5 chunks

- KA-0007 Setting up SAML single sign-on > Common errors
- KA-0007 Setting up SAML single sign-on > Values to enter in your IdP
- KA-0007 Setting up SAML single sign-on > Before you start
- KA-0007 Setting up SAML single sign-on > Related
- KA-0007 Setting up SAML single sign-on > Steps in Lumora

Answer (has the fact, citations OK):

> `Audience mismatch` means the entity ID set in your identity provider (IdP) doesn't exactly match what Lumora expects [KA-0007].
> 
> **To fix it:**
> 
> 1. In your IdP, set the Entity ID / Audience URI to exactly `https://<subdomain>.lumora.example/sso/saml/metadata`, using your workspace subdomain [KA-0007].
> 2. Copy the value again rather than typing it. It's case-sensitive and must not have a trailing slash [KA-0007].
> 3. In Lumora, go to **Settings > Security > Single sign-on** and click **Test connection** in a private browser window [KA-0007].
> 
> Until SSO works, keep at least one Owner account that can sign in with a password [KA-0007].

### hybrid + rerank: fact found in the 5 chunks

- KA-0007 Setting up SAML single sign-on > Common errors
- KA-0008 Known issue: SSO logout does not fully end the Lumora session > Cause
- KA-0019 Setting up webhooks and fixing delivery failures > "500 errors when setting up webhooks"
- KA-0007 Setting up SAML single sign-on > Values to enter in your IdP
- KA-0007 Setting up SAML single sign-on > Steps in Lumora

Answer (has the fact, citations OK):

> An `Audience mismatch` error means the entity ID configured in your IdP doesn't exactly match what Lumora expects [KA-0007].
> 
> To fix it:
> 
> 1. In your IdP, set the **Entity ID / Audience URI** to `https://<subdomain>.lumora.example/sso/saml/metadata`, using your own subdomain [KA-0007].
> 2. Copy the value again rather than retyping it. It's case-sensitive and must not have a trailing slash [KA-0007].
> 3. In Lumora, click **Test connection** in a private browser window to confirm it works [KA-0007].
> 
> Until SSO is confirmed working, keep at least one Owner account that can sign in with a password [KA-0007].

## Q4. Which HTTP header carries the webhook signature?

Expected: X-Lumora-Signature (KA-0019)

### vector: fact found in the 5 chunks

- KA-0019 Setting up webhooks and fixing delivery failures > "500 errors when setting up webhooks"
- KA-0019 Setting up webhooks and fixing delivery failures > How webhooks work
- KA-0019 Setting up webhooks and fixing delivery failures > Testing
- KA-0018 API rate limits and handling HTTP 429 responses > Best practices
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Step 2: Check the payment log

Answer (has the fact, citations OK):

> Webhook events are signed in the `X-Lumora-Signature` header. The signature is an HMAC-SHA256 of the raw request body, made with the endpoint secret [KA-0019].
> 
> When you verify it, compute it from the raw request body. Don't use JSON that has been parsed and re-serialized, because that is a common cause of failures [KA-0019].

### hybrid (vector + BM25): fact found in the 5 chunks

- KA-0019 Setting up webhooks and fixing delivery failures > How webhooks work
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Step 2: Check the payment log
- KA-0044 Using a custom domain for your workspace > After switching
- KA-0018 API rate limits and handling HTTP 429 responses > Best practices
- KA-0019 Setting up webhooks and fixing delivery failures > "500 errors when setting up webhooks"

Answer (has the fact, citations OK):

> Lumora signs each webhook event in the **`X-Lumora-Signature`** header [KA-0019]. The value is an HMAC-SHA256 of the raw request body, computed with the endpoint secret [KA-0019].
> 
> When verifying it, compute the HMAC over the raw body as received. Using JSON that has been parsed and re-serialized is a common cause of failures [KA-0019].

### hybrid + rerank: fact found in the 5 chunks

- KA-0019 Setting up webhooks and fixing delivery failures > How webhooks work
- KA-0019 Setting up webhooks and fixing delivery failures > "500 errors when setting up webhooks"
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Step 2: Check the payment log
- KA-0018 API rate limits and handling HTTP 429 responses > Best practices
- KA-0019 Setting up webhooks and fixing delivery failures > Testing

Answer (has the fact, citations OK):

> Webhook signatures are in the `X-Lumora-Signature` header. The value is an HMAC-SHA256 of the raw request body, computed with the endpoint secret [KA-0019].
> 
> Verify the signature against the raw body, not JSON that has been parsed and re-serialized. Checking against re-serialized JSON is a common cause of failures [KA-0019].

## Q5. The iOS app closes at the splash screen on version 2.3.1.

Expected: 2.3.2 (KA-0040)

### vector: fact found in the 5 chunks

- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Symptoms
- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Status
- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Resolution
- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Cause
- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Workaround if updating isn't possible

Answer (has the fact, citations OK):

> This is a known issue with Lumora for iOS **2.3.1** on iOS 17 and 18. It only affects users who had **offline mode** turned on [KA-0040]. A database migration in 2.3.1 failed on devices that already had offline data stored, so the app crashes every time it starts [KA-0040]. It's **resolved in version 2.3.2**, released 2026-07-15 [KA-0040].
> 
> **To fix it:**
> 1. Update to **2.3.2 or later** from the App Store [KA-0040].
> 2. If the App Store doesn't offer the update yet, delete and reinstall the app. Any offline data that hasn't synced will be lost, but data that's already synced is safe on the server [KA-0040].
> 3. If your company manages your iOS device (MDM), IT may need to push the update [KA-0040].
> 
> **If you can't update yet:** use the mobile web version at `https://app.lumora.example` in Safari until the update is installed [KA-0040].

### hybrid (vector + BM25): fact found in the 5 chunks

- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Symptoms
- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Status
- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Workaround if updating isn't possible
- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Cause
- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Resolution

Answer (has the fact, citations OK):

> This is a known issue in Lumora for iOS **2.3.1**. The app closes right after the splash screen on iOS 17 and 18 for users who had offline mode turned on [KA-0040]. It's caused by a failed database migration on devices that already had offline data stored [KA-0040].
> 
> **Fix:** It's resolved in version **2.3.2** (released 2026-07-15) [KA-0040].
> 1. Update to **2.3.2 or later** from the App Store [KA-0040].
> 2. If the App Store doesn't offer the update yet, delete and reinstall the app. Any offline data that hasn't synced will be lost, but data already synced is safe on the server [KA-0040].
> 3. If your company manages your iOS device (MDM), IT may need to push the update [KA-0040].
> 
> **Workaround:** If you can't update yet, use the mobile web version at `https://app.lumora.example` in Safari [KA-0040].

### hybrid + rerank: fact found in the 5 chunks

- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Symptoms
- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Status
- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Resolution
- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Agent notes
- KA-0040 Known issue: iOS app crashes on launch in version 2.3.1 > Workaround if updating isn't possible

Answer (has the fact, citations OK):

> This is a known issue in Lumora for iOS version 2.3.1. It affects users on iOS 17 and 18 who had offline mode turned on [KA-0040]. It's fixed in version 2.3.2, released 2026-07-15 [KA-0040].
> 
> **To fix it:**
> 1. Update to version 2.3.2 or later from the App Store [KA-0040].
> 2. If the App Store doesn't offer the update yet, delete and reinstall the app. **Offline data that hasn't synced will be lost.** Data that already synced is safe on the server [KA-0040].
> 3. If your company manages your iOS device (MDM), you may need IT to push the update [KA-0040].
> 
> **Until you can update:** use the mobile web version at `https://app.lumora.example` in Safari [KA-0040].
> 
> If the app still crashes on launch after you update to 2.3.2 or later, please send your app version, iOS version, and crash log so we can escalate it [KA-0040]. To find the crash log, go to Settings > Privacy & Security > Analytics & Improvements > Analytics Data and look for entries starting with `Lumora` [KA-0040].

## Q6. Our custom domain has said Certificate pending for over an hour.

Expected: CAA (KA-0044)

### vector: fact found in the 5 chunks

- KA-0044 Using a custom domain for your workspace > Setup (Enterprise)
- KA-0044 Using a custom domain for your workspace > Troubleshooting
- KA-0044 Using a custom domain for your workspace > Availability
- KA-0007 Setting up SAML single sign-on > Common errors
- KA-0044 Using a custom domain for your workspace > After switching

Answer (has the fact, citations OK):

> If the status has shown **Certificate pending** for more than an hour, check these two things:
> 
> 1. **CAA records:** If your domain has CAA records, add `letsencrypt.org` so Lumora can issue the TLS certificate. Lumora issues and renews the certificate automatically. [KA-0044]
> 2. **No proxy on the CNAME:** Make sure there's no proxy (orange-cloud style) in front of the CNAME. It should point directly to `custom.lumora.example`. [KA-0044]
> 
> Once the certificate is issued and the status shows **Active**, the old `lumora.example` address redirects to your custom domain. [KA-0044]

### hybrid (vector + BM25): fact found in the 5 chunks

- KA-0044 Using a custom domain for your workspace > Setup (Enterprise)
- KA-0044 Using a custom domain for your workspace > Troubleshooting
- KA-0044 Using a custom domain for your workspace > Availability
- KA-0044 Using a custom domain for your workspace > After switching
- KA-0007 Setting up SAML single sign-on > Common errors

Answer (has the fact, citations OK):

> When "Certificate pending" lasts more than an hour, check two things [KA-0044]:
> 
> 1. **CAA records:** If your domain has CAA records, add `letsencrypt.org` [KA-0044].
> 2. **Proxy:** Make sure there's no proxy (orange-cloud style) in front of the CNAME record. It should point directly to `custom.lumora.example` [KA-0044].
> 
> Once those are fixed, Lumora issues the TLS certificate automatically [KA-0044]. When the status shows **Active**, the old `lumora.example` address redirects to your custom domain [KA-0044].

### hybrid + rerank: fact found in the 5 chunks

- KA-0044 Using a custom domain for your workspace > Troubleshooting
- KA-0044 Using a custom domain for your workspace > Setup (Enterprise)
- KA-0044 Using a custom domain for your workspace > Availability
- KA-0044 Using a custom domain for your workspace > After switching
- KA-0007 Setting up SAML single sign-on > Common errors

Answer (has the fact, citations OK):

> If the status has said **Certificate pending** for over an hour, check these:
> 
> 1. **CAA records:** Lumora issues the TLS certificate automatically, so if your domain has CAA records, they must include `letsencrypt.org` [KA-0044].
> 2. **No proxy on the CNAME:** Make sure there's no proxy (orange-cloud style) in front of the CNAME record [KA-0044]. The record should point straight to `custom.lumora.example` [KA-0044].
> 
> After fixing either one, click **Verify** again in **Settings > Workspace > Custom domain**. DNS changes usually take minutes but can take up to 24 hours [KA-0044].

## Q7. Teammates' edits show up half a minute late. How do we fix it?

Expected: 443 or 120 seconds or TLS inspection (KA-0029)

### vector: fact not found in the 5 chunks

- KA-0029 Real-time collaboration changes appear with a delay > Symptoms
- KA-0029 Real-time collaboration changes appear with a delay > If WebSockets are connected and it's still slow
- KA-0029 Real-time collaboration changes appear with a delay > Confirm
- KA-0029 Real-time collaboration changes appear with a delay > Cause
- KA-0026 Dashboard widget shows old or incorrect data > Causes and resolution

Answer (missing the fact, citations OK):

> A delay of about 30 seconds usually means Lumora has lost its live connection and switched to slower polling.
> 
> **Why it happens:** Live updates use a WebSocket connection to `wss://rt.lumora.example`. If something on the network blocks or breaks WebSockets, the app quietly falls back to polling every 30 seconds, which causes the delay [KA-0029]. Common causes are:
> - A corporate proxy or secure web gateway that doesn't support WebSocket upgrades or inspects TLS traffic [KA-0029]
> - A firewall that closes idle connections after a short time [KA-0029]
> - Browser extensions such as privacy or ad-blocking tools [KA-0029]
> 
> **Check which mode you're in:**
> 1. Open **Help > Connection diagnostics**. It shows either **Live updates: Connected (WebSocket)** or **Fallback (polling)** [KA-0029].
> 2. Or open the browser DevTools **Network** tab, filter by **WS**, and look for a connection to `rt.lumora.example` [KA-0029].
> 
> **Next steps:**
> - **If it shows Fallback (polling):** look into the causes above. The knowledge base doesn't give specific steps for fixing them, so you may need your network or IT team.
> - **If WebSockets are connected but updates are still slow:** collect the diagnostics output and a HAR file. Then escalate to the Realtime team with the workspace ID and the object that was being edited [KA-0029].

### hybrid (vector + BM25): fact found in the 5 chunks

- KA-0029 Real-time collaboration changes appear with a delay > Symptoms
- KA-0030 Data connector sync is slower than usual > Expected interval
- KA-0019 Setting up webhooks and fixing delivery failures > Re-enable a disabled endpoint
- KA-0029 Real-time collaboration changes appear with a delay > Fix
- KA-0018 API rate limits and handling HTTP 429 responses > How limits are counted

Answer (has the fact, citations OK):

> This is a known issue: when several people edit the same board, document or task at once, changes reach others about 30 seconds late, and you may also see edit conflicts [KA-0029].
> 
> To fix it, send these steps to your IT team [KA-0029]:
> 
> 1. Allow WebSocket (HTTP Upgrade) traffic to `rt.lumora.example` on port 443 [KA-0029].
> 2. Exclude `*.lumora.example` from TLS inspection [KA-0029].
> 3. Set the idle timeout for these connections to at least 120 seconds. The app sends a heartbeat every 45 seconds [KA-0029].

### hybrid + rerank: fact found in the 5 chunks

- KA-0029 Real-time collaboration changes appear with a delay > Symptoms
- KA-0029 Real-time collaboration changes appear with a delay > Fix
- KA-0026 Dashboard widget shows old or incorrect data > Causes and resolution
- KA-0029 Real-time collaboration changes appear with a delay > If WebSockets are connected and it's still slow
- KA-0019 Setting up webhooks and fixing delivery failures > Re-enable a disabled endpoint

Answer (has the fact, citations OK):

> This delay usually means real-time (WebSocket) connections are being blocked or interrupted on your network. When several people edit the same item, changes arrive about 30 seconds late, and you may also see edit conflicts [KA-0029].
> 
> **Fix:** send these steps to your IT team [KA-0029]:
> - Allow WebSocket (HTTP Upgrade) traffic to `rt.lumora.example` on port 443.
> - Exclude `*.lumora.example` from TLS inspection.
> - Set the idle timeout for these connections to at least 120 seconds. The app sends a heartbeat every 45 seconds.
> 
> **If WebSockets connect and edits are still slow:** collect the diagnostics output and a HAR file. Then escalate to the Realtime team with the workspace ID and the object being edited [KA-0029].

## Q8. The payment log shows test_mode_key_in_live.

Expected: live key (KA-0033)

### vector: fact found in the 5 chunks

- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Step 2: Check the payment log
- KA-0019 Setting up webhooks and fixing delivery failures > Testing
- KA-0043 Using the audit log for compliance > What is recorded
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Escalate
- KA-0008 Known issue: SSO logout does not fully end the Lumora session > Status

Answer (has the fact, citations OK):

> The `test_mode_key_in_live` error means **a test key was entered on a live form** [KA-0033]. To fix it, **replace it with the live key** from your payment gateway [KA-0033].
> 
> You can find this error in the form under **Settings > Payments > Transaction log**, where each payment attempt shows the gateway's response code [KA-0033].

### hybrid (vector + BM25): fact found in the 5 chunks

- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Step 2: Check the payment log
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Escalate
- KA-0029 Real-time collaboration changes appear with a delay > Confirm
- KA-0019 Setting up webhooks and fixing delivery failures > Testing
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Step 1: Rule out an outage

Answer (has the fact, citations OK):

> The `test_mode_key_in_live` error means a **test API key was entered on a live form** [KA-0033]. The fix is to **replace it with the live key** from the payment gateway [KA-0033].
> 
> You can confirm the error and later check whether payments succeed in the form under **Settings > Payments > Transaction log** [KA-0033].
> 
> The articles don't say exactly where to enter the live key. The closest documented path is the gateway reconnect option at **Settings > Integrations > Payments > Reconnect**, but that's listed for rotated or revoked keys, not this error specifically [KA-0033].

### hybrid + rerank: fact found in the 5 chunks

- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Step 2: Check the payment log
- KA-0033 Payments failing through a connected payment gateway in Lumora Forms > Escalate
- KA-0043 Using the audit log for compliance > What is recorded
- KA-0029 Real-time collaboration changes appear with a delay > Confirm
- KA-0015 Renewal reminders, the grace period and reactivating a lapsed subscription > Restore access

Answer (has the fact, citations OK):

> That error means a **test key was entered on a live form**. To fix it, **replace it with the live key** from your payment gateway [KA-0033].
> 
> The article doesn't say where in Lumora to enter the live key. If payments still fail afterward, check the transaction log under **Settings > Payments > Transaction log** for a different error code [KA-0033].

## Q9. How many API requests per minute does the Business plan allow?

Expected: 300 (KA-0018, KA-0001)

### vector: fact found in the 5 chunks

- KA-0018 API rate limits and handling HTTP 429 responses > How limits are counted
- KA-0018 API rate limits and handling HTTP 429 responses > Investigating a complaint
- KA-0001 Lumora Workspace plans and limits > Overview
- KA-0002 Contacting Lumora Support and how case priority is set > First-response targets (Business and Enterprise)
- KA-0018 API rate limits and handling HTTP 429 responses > Best practices

Answer (has the fact, citations OK):

> The Business plan allows **300 API requests per minute**, with a burst of 50 [KA-0018]. This matches the plan limits table [KA-0001].
> 
> - **The limit is shared:** it applies per workspace and covers every API token and installed integration in that workspace [KA-0018].
> - **Search has its own limit:** search endpoints (`/v2/search`) are limited separately to 30 requests per minute on every plan [KA-0018].

### hybrid (vector + BM25): fact found in the 5 chunks

- KA-0018 API rate limits and handling HTTP 429 responses > How limits are counted
- KA-0001 Lumora Workspace plans and limits > Overview
- KA-0018 API rate limits and handling HTTP 429 responses > Investigating a complaint
- KA-0018 API rate limits and handling HTTP 429 responses > Response headers
- KA-0002 Contacting Lumora Support and how case priority is set > First-response targets (Business and Enterprise)

Answer (has the fact, citations OK):

> The Business plan allows **300 API requests per minute**, with a burst of 50 [KA-0018][KA-0001].
> 
> This limit is per workspace, not per token. Every API token and installed integration in the workspace shares it [KA-0018].
> 
> Search endpoints (`/v2/search`) have their own separate limit of 30 requests per minute on every plan [KA-0018].

### hybrid + rerank: fact found in the 5 chunks

- KA-0018 API rate limits and handling HTTP 429 responses > How limits are counted
- KA-0001 Lumora Workspace plans and limits > Overview
- KA-0018 API rate limits and handling HTTP 429 responses > Investigating a complaint
- KA-0018 API rate limits and handling HTTP 429 responses > Response headers
- KA-0030 Data connector sync is slower than usual > Expected interval

Answer (has the fact, citations OK):

> The Business plan allows **300 API requests per minute**, with a burst of 50 [KA-0018][KA-0001].
> 
> This limit applies to the whole workspace, not to each token. Every API token and installed integration in the workspace shares the same allowance [KA-0018]. Search endpoints (`/v2/search`) have their own separate limit of 30 requests per minute [KA-0018].

## Q10. CSV export opens in Excel with everything in one column.

Expected: Text/CSV or Excel compatible (KA-0021)

### vector: fact found in the 5 chunks

- KA-0021 CSV export downloads an empty or incomplete file > Causes and resolution
- KA-0021 CSV export downloads an empty or incomplete file > Symptoms
- KA-0021 CSV export downloads an empty or incomplete file > Still empty
- KA-0011 Adding, updating and removing users in bulk > CSV import
- KA-0043 Using the audit log for compliance > View and export

Answer (has the fact, citations OK):

> This matches the Excel issue in the CSV export article. Lumora's CSV files are UTF-8, and on some systems Excel shows the contents in one column when the file is opened by double-clicking [KA-0021].
> 
> There are two fixes:
> 
> 1. **Import instead of double-clicking:** in Excel, use **Data > From Text/CSV** to open the file [KA-0021].
> 2. **Re-export in Excel format:** in Lumora, choose **Export > CSV (Excel compatible)**. This adds a byte-order mark so Excel reads the file correctly [KA-0021].

### hybrid (vector + BM25): fact found in the 5 chunks

- KA-0021 CSV export downloads an empty or incomplete file > Causes and resolution
- KA-0021 CSV export downloads an empty or incomplete file > Symptoms
- KA-0021 CSV export downloads an empty or incomplete file > Still empty
- KA-0011 Adding, updating and removing users in bulk > CSV import
- KA-0043 Using the audit log for compliance > View and export

Answer (has the fact, citations OK):

> This is usually an encoding issue: Lumora CSV files are UTF-8, and Excel on some systems shows one blank column when the file is opened by double-click [KA-0021].
> 
> There are two ways to fix it:
> 
> 1. **Import instead of double-clicking:** In Excel, use **Data > From Text/CSV** to open the file [KA-0021].
> 2. **Re-export in Excel format:** In Lumora, choose **Export > CSV (Excel compatible)**. This version adds a byte-order mark so Excel reads it correctly [KA-0021].
> 
> If the file is actually empty or missing rows, collect the report URL, the export time, the browser, and a HAR file, then escalate to Reports Engineering [KA-0021].

### hybrid + rerank: fact found in the 5 chunks

- KA-0021 CSV export downloads an empty or incomplete file > Causes and resolution
- KA-0021 CSV export downloads an empty or incomplete file > Symptoms
- KA-0021 CSV export downloads an empty or incomplete file > Still empty
- KA-0043 Using the audit log for compliance > View and export
- KA-0011 Adding, updating and removing users in bulk > CSV import

Answer (has the fact, citations NOT OK):

> This matches the Excel issue in KA-0021. Lumora CSV files are UTF-8, and on some systems Excel shows them wrongly when you open the file by double-clicking [KA-0021]. The article describes this as "one blank column," which may or may not be exactly what you're seeing [KA-0021].
> 
> Two fixes:
> 1. In Excel, use **Data > From Text/CSV** to import the file instead of double-clicking it [KA-0021].
> 2. Or re-export with **Export > CSV (Excel compatible)**. This version adds a byte-order mark [KA-0021].
> 
> If the export itself turns out to be empty or missing rows, collect the report URL, the export time, the browser, and a HAR file (KA-0003). Then escalate to Reports Engineering [KA-0021].

