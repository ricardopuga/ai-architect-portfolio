# RAG answer judge: hand check

10 fixed answers judged with prompts/rag_answer_judge_v1.md. A score of 4 or 5 is a pass.

Judge agrees with my verdict on groundedness 10/10, correctness 10/10.

| # | Planted flaw | My groundedness | Judge | My correctness | Judge |
|---|---|---|---|---|---|
| H01 | none (clean, short) | pass | 5 pass | pass | 5 pass |
| H02 | none (clean, long, many claims) | pass | 5 pass | pass | 5 pass |
| H03 | value from the wrong column (2 hours is Enterprise; Business is 4 hours) | fail | 1 fail | fail | 1 fail |
| H04 | true facts from KA-0043 that weren't retrieved (only the Retention chunk was) | fail | 3 fail | pass | 5 pass |
| H05 | invented, plausible extra step (Login History / 'OAuth token expired') | fail | 3 fail | pass | 5 pass |
| H06 | none (correct refusal with related facts) | pass | 5 pass | pass | 4 pass |
| H07 | iOS-only known issue extended to Android | fail | 1 fail | fail | 1 fail |
| H08 | wrong refusal: chunk 159 answers it | pass | 5 pass | fail | 2 fail |
| H09 | 'planned / being fixed' turned into 'fixed', and the fix's scope widened | fail | 1 fail | fail | 1 fail |
| H10 | grounded but misses the main point (Viewer seat) | pass | 5 pass | fail | 2 fail |

## H01 (Q28). A scheduled automation rule updates 200 tasks. How many runs does that use?

**Planted flaw:** none (clean, short)

**Answer judged:**

> 200 runs: a scheduled rule counts one run per task it updates [KA-0036]. Runs where the conditions aren't met don't count [KA-0036].

**Retrieved chunks:**

- KA-0036 chunk 142: Automation rule limits and what counts as a run > What counts as a run?
- KA-0036 chunk 144: Automation rule limits and what counts as a run > Other limits
- KA-0036 chunk 141: Automation rule limits and what counts as a run > How many rules can we create?
- KA-0036 chunk 143: Automation rule limits and what counts as a run > What happens at the limit?
- KA-0001 chunk 1: Lumora Workspace plans and limits > Overview

**My verdict:** groundedness pass, correctness pass. Both claims are in KA-0036 chunk 142 and match the reference.

**Judge:** groundedness 5, correctness 5. Unsupported claims: none

> The answer makes two claims. First, that a scheduled rule updating 200 tasks uses 200 runs, one per task. KA-0036 states this explicitly, so it is supported. Second, that runs where the conditions aren't met don't count. KA-0036 also states this, so it is supported. Both citations are correct. Compared with the reference ("200 runs, one per task"), the answer gives the same main point. The extra detail about unmet conditions is accurate and does not contradict the reference.

## H02 (Q20). A customer got a scheduled export on 2026-09-10 that contained Sensitive fields. How should I handle it?

**Planted flaw:** none (clean, long, many claims)

**Answer judged:**

> This matches known issue ENG-4388: scheduled exports in releases 2026.08.1 to 2026.09.1 kept including Sensitive fields, and it was fixed in 2026.09.2 on 2026-09-16 [KA-0022]. Treat it as a possible data exposure and set the priority to at least High [KA-0022].
> 
> 1. Ask for the export file name, the report or schedule name and the date it arrived, but don't ask them to attach the file [KA-0022].
> 2. Escalate to the Security & Privacy queue, which decides whether the customer must be formally notified under the DPA [KA-0022].
> 3. Recommend they delete any copies, review the schedule's recipients and check who holds Export sensitive data under Settings > Roles [KA-0022].

**Retrieved chunks:**

- KA-0022 chunk 87: Sensitive fields and data exports, including the scheduled-export known issue > If a customer reports sensitive data in an export
- KA-0022 chunk 86: Sensitive fields and data exports, including the scheduled-export known issue > Known issue (resolved)
- KA-0022 chunk 85: Sensitive fields and data exports, including the scheduled-export known issue > How it should work
- KA-0045 chunk 179: Handling feature requests and finding out what's on the roadmap > Status of frequently requested features (October 2026)
- KA-0042 chunk 168: Backup retention and restoring deleted data > Customer-side backups

**My verdict:** groundedness pass, correctness pass. Every claim is in KA-0022 chunks 86 and 87. Tests that the judge doesn't nitpick a long answer.

**Judge:** groundedness 5, correctness 5. Unsupported claims: none

> Claims in the answer, checked against the retrieved excerpts:
> 1. The case matches ENG-4388, with affected releases 2026.08.1 to 2026.09.1, fixed in 2026.09.2 on 2026-09-16. Supported: the known-issue table gives these values, and step 2 says a scheduled export received before 2026-09-16 matches ENG-4388. The question's date (2026-09-10) is before the fix, so applying the rule is direct.
> 2. The issue is described as scheduled exports "kept including Sensitive fields." Supported as a summary. The excerpt narrows the trigger to cases where the creator lost the Export sensitive data permission or the schedule was handed to another owner. The answer drops that condition, but this is only a slight broadening and does not change the guidance.
> 3. Treat it as a possible data exposure with priority at least High. Supported.
> 4. Ask for the file name, the report or schedule name and the date, and don't ask them to attach the file. Supported.
> 5. Escalate to Security & Privacy, which decides on formal DPA notification. Supported.
> 6. Recommend deleting copies, reviewing recipients and checking Export sensitive data holders under Settings > Roles. Supported.
> The answer correctly leaves out the regression step, since the date is before the fix.
> 
> Comparison with the reference: the answer covers every point. It identifies ENG-4388 with the right releases and fix date, says to treat it as a possible exposure at High priority, says not to ask for the file, and says to escalate to Security & Privacy. It only omits that the issue was limited to scheduled exports and that manual and API exports were unaffected. That is a minor detail, and it is partly implied because the answer describes the issue as affecting scheduled exports. Nothing in the answer contradicts the reference.

## H03 (Q01). What is the first-response target for a High priority case on the Business plan?

**Planted flaw:** value from the wrong column (2 hours is Enterprise; Business is 4 hours)

**Answer judged:**

> The first-response target for a High priority case on the Business plan is 2 hours [KA-0002].

**Retrieved chunks:**

- KA-0002 chunk 5: Contacting Lumora Support and how case priority is set > First-response targets (Business and Enterprise)
- KA-0002 chunk 4: Contacting Lumora Support and how case priority is set > Priority definitions
- KA-0002 chunk 3: Contacting Lumora Support and how case priority is set > Support channels
- KA-0002 chunk 6: Contacting Lumora Support and how case priority is set > Before you escalate
- KA-0022 chunk 87: Sensitive fields and data exports, including the scheduled-export known issue > If a customer reports sensitive data in an export

**My verdict:** groundedness fail, correctness fail. The table in KA-0002 chunk 5 says 4 hours for Business. 2 hours is in the same row, under Enterprise.

**Judge:** groundedness 1, correctness 1. Unsupported claims: The first-response target for a High priority case on the Business plan is 2 hours

> The answer makes one claim: High priority on Business has a 2-hour first-response target. The retrieved table gives High as 4 hours for Business and 2 hours for Enterprise, so the answer took the value from the wrong column. The excerpt contradicts this main claim. The reference says 4 hours, so the answer is wrong on the main point.

## H04 (Q33). Can a workspace Owner delete audit log entries, and how long does Enterprise keep them?

**Planted flaw:** true facts from KA-0043 that weren't retrieved (only the Retention chunk was)

**Answer judged:**

> No. Audit log entries can't be edited or deleted, even by Owners, and Enterprise keeps them for 7 years [KA-0043]. Enterprise can also stream them to Splunk HEC, Datadog, Amazon S3 or a generic HTTPS endpoint, with events arriving within 60 seconds [KA-0043].

**Retrieved chunks:**

- KA-0043 chunk 170: Using the audit log for compliance > Retention
- KA-0042 chunk 165: Backup retention and restoring deleted data > Backup policy
- KA-0042 chunk 167: Backup retention and restoring deleted data > Requesting a restore from backup
- KA-0044 chunk 174: Using a custom domain for your workspace > Availability
- KA-0001 chunk 1: Lumora Workspace plans and limits > Overview

**My verdict:** groundedness fail, correctness pass. The streaming sentence is true in KA-0043 but the retrieved chunk 170 only says 'Can also be streamed out (below)'. Correct but not grounded: secondary claim, so groundedness 3.

**Judge:** groundedness 3, correctness 5. Unsupported claims: Enterprise can stream audit log entries to Splunk HEC, Datadog, Amazon S3 or a generic HTTPS endpoint; Streamed events arrive within 60 seconds

> Claims in the answer:
> 1. Owners can't edit or delete audit log entries. Supported by KA-0043.
> 2. Enterprise keeps entries for 7 years. Supported by KA-0043 and KA-0001.
> 3. Enterprise can stream entries out. Supported: KA-0043 says "Can also be streamed out (below)."
> 4. The streaming destinations (Splunk HEC, Datadog, Amazon S3, generic HTTPS endpoint) and the 60-second delivery time. Not supported. The streaming section is referenced as "below" but was not retrieved, so these details are not in the excerpts. This is a secondary claim; the main answer stands without it.
> 
> Compared with the reference, the main points match: entries can't be deleted, even by Owners, and Enterprise keeps them 7 years. The answer omits Business's 1-year retention, which is a minor secondary detail. The extra streaming details don't contradict the reference.

## H05 (Q25). The Salesforce connector disconnects like clockwork every 12 hours.

**Planted flaw:** invented, plausible extra step (Login History / 'OAuth token expired')

**Answer judged:**

> The Salesforce connected app's refresh token policy is set to expire, so the connector disconnects on that schedule [KA-0031]. In Salesforce Setup, go to Connected Apps OAuth Usage > Lumora Workspace > Manage > Edit Policies and set Refresh Token Policy to 'Refresh token is valid until revoked' [KA-0031]. You can confirm the pattern in Salesforce under Setup > Login History, where each disconnect is logged as an 'OAuth token expired' event.

**Retrieved chunks:**

- KA-0031 chunk 121: Salesforce connector keeps disconnecting > Symptoms
- KA-0031 chunk 122: Salesforce connector keeps disconnecting > Causes and resolution
- KA-0031 chunk 123: Salesforce connector keeps disconnecting > Reconnect
- KA-0018 chunk 70: API rate limits and handling HTTP 429 responses > How limits are counted
- KA-0035 chunk 137: Custom field can't be deleted > Cause

**My verdict:** groundedness fail, correctness pass. The main fix matches chunk 122 and the reference. The Login History claim is in no chunk; it's secondary, so groundedness 3, and it doesn't contradict the reference.

**Judge:** groundedness 3, correctness 5. Unsupported claims: You can confirm the pattern in Salesforce under Setup > Login History, where each disconnect is logged as an 'OAuth token expired' event.

> Claims in the answer:
> 1. The refresh token policy is set to expire, so the connector disconnects on that schedule. Supported: KA-0031 says that with "Expire refresh token after X hours" the connector disconnects on that schedule. Saying it "is set" this way applies the rule to the 12-hour pattern the user describes.
> 2. The menu path Connected Apps OAuth Usage > Lumora Workspace > Manage > Edit Policies, setting Refresh Token Policy to 'Refresh token is valid until revoked'. Supported word for word by KA-0031.
> 3. The pattern can be confirmed under Setup > Login History, where each disconnect is logged as an 'OAuth token expired' event. Not in any excerpt. This is an invented menu location and event name. It is secondary: the main answer stands without it.
> 
> Correctness: the answer matches the reference on both the cause and the fix, and the extra claim doesn't contradict the reference. It is an unverified detail that could mislead the user slightly if that log entry doesn't exist, but the main point is fully correct.

## H06 (Q36). How much does the Business plan cost per user per month?

**Planted flaw:** none (correct refusal with related facts)

**Answer judged:**

> The knowledge base articles don't say what the Business plan costs. They list each plan's limits, such as 1 TB of storage and 300 API requests per minute on Business [KA-0001], but not prices.

**Retrieved chunks:**

- KA-0001 chunk 1: Lumora Workspace plans and limits > Overview
- KA-0036 chunk 141: Automation rule limits and what counts as a run > How many rules can we create?
- KA-0036 chunk 143: Automation rule limits and what counts as a run > What happens at the limit?
- KA-0018 chunk 70: API rate limits and handling HTTP 429 responses > How limits are counted
- KA-0001 chunk 2: Lumora Workspace plans and limits > Notes

**My verdict:** groundedness pass, correctness pass. The two limits are in KA-0001 chunk 1. Refusing is right: the reference says the knowledge base can't answer.

**Judge:** groundedness 5, correctness 4. Unsupported claims: none

> Claims in the answer:
> 1. The knowledge base doesn't give the Business plan's price. This is a statement about coverage, not a product claim, so it doesn't affect groundedness.
> 2. Business has 1 TB of storage. Supported by KA-0001.
> 3. Business has 300 API requests per minute. Supported by KA-0001.
> 4. The articles list limits but not prices. Accurate; none of the excerpts mention pricing.
> 
> Every claim is supported.
> 
> Compared with the reference: the reference says the knowledge base has no prices, and the answer correctly declines to give a figure. The reference also suggests pointing the user to the pricing page or the account team, which the answer omits. That is a minor secondary gap; the main point is right.

## H07 (Q40). Does the Android app version 2.3.1 also crash on launch?

**Planted flaw:** iOS-only known issue extended to Android

**Answer judged:**

> Yes. Version 2.3.1 crashes on launch for users who have offline mode turned on, because a database migration fails on devices with offline data [KA-0040]. Update to 2.3.2 or later from the Play Store [KA-0040].

**Retrieved chunks:**

- KA-0040 chunk 159: Known issue: iOS app crashes on launch in version 2.3.1 > Agent notes
- KA-0040 chunk 156: Known issue: iOS app crashes on launch in version 2.3.1 > Cause
- KA-0040 chunk 157: Known issue: iOS app crashes on launch in version 2.3.1 > Resolution
- KA-0040 chunk 158: Known issue: iOS app crashes on launch in version 2.3.1 > Workaround if updating isn't possible
- KA-0040 chunk 155: Known issue: iOS app crashes on launch in version 2.3.1 > Symptoms

**My verdict:** groundedness fail, correctness fail. Every chunk is about the iOS app (iOS 17 and 18, App Store). Nothing says Android is affected, and the reference says the KB can't answer.

**Judge:** groundedness 1, correctness 1. Unsupported claims: Yes, the Android app version 2.3.1 also crashes on launch; The offline-mode database migration crash applies to Android; Update to 2.3.2 or later from the Play Store

> Claims in the answer:
> 1. "Yes": the Android app 2.3.1 also crashes on launch. Unsupported. KA-0040 covers iOS only (iOS 17 and 18), and none of the excerpts mention Android.
> 2. 2.3.1 crashes for users who have offline mode on, because a database migration fails on devices with offline data. This is supported for iOS, but the answer applies it to Android, which the excerpts don't support.
> 3. "Update to 2.3.2 or later from the Play Store." Unsupported. The excerpt says the App Store, and the Play Store appears nowhere.
> 
> Groundedness: the main claim extends an iOS-only issue to Android and adds a platform the excerpts never mention. Most of the answer is unsupported and contradicts the excerpts' iOS scope on the main point.
> 
> Correctness: the reference says the knowledge base doesn't cover Android and the answer should not extend the iOS article to it. The assistant answered "Yes" anyway, so it answers a question the knowledge base can't answer.

## H08 (Q30). A user on iOS app version 2.3.2 says the app still crashes on launch. Is that the known 2.3.1 issue?

**Planted flaw:** wrong refusal: chunk 159 answers it

**Answer judged:**

> The articles don't cover crashes in version 2.3.2, so I can't tell whether this is the known issue.

**Retrieved chunks:**

- KA-0040 chunk 159: Known issue: iOS app crashes on launch in version 2.3.1 > Agent notes
- KA-0040 chunk 157: Known issue: iOS app crashes on launch in version 2.3.1 > Resolution
- KA-0040 chunk 156: Known issue: iOS app crashes on launch in version 2.3.1 > Cause
- KA-0040 chunk 155: Known issue: iOS app crashes on launch in version 2.3.1 > Symptoms
- KA-0040 chunk 158: Known issue: iOS app crashes on launch in version 2.3.1 > Workaround if updating isn't possible

**My verdict:** groundedness pass, correctness fail. No product claims, so groundedness passes under the prompt's rule. KA-0040 chunk 159 says the article doesn't apply from 2.3.2 and to escalate to Mobile Engineering, so correctness is 2.

**Judge:** groundedness 5, correctness 2. Unsupported claims: none

> The answer makes one claim: the articles don't cover 2.3.2 crashes, so it can't tell whether this is the known issue. That is a statement about coverage, not a product claim, so groundedness isn't penalized. It is inaccurate, though. KA-0040's agent notes say plainly that if a user still reports a crash with 2.3.2 or later, the article doesn't apply. They also say to collect the app version, iOS version and crash log, then escalate to Mobile Engineering. The answer contains no unsupported product claims, so groundedness is 5. For correctness, the reference answers that it is not the known issue and gives the escalation steps. The assistant wrongly says it can't answer and misses the main point. Correctness is 2.

## H09 (Q06). After users log out of Okta, their open Lumora tabs keep working. Is this fixed yet?

**Planted flaw:** 'planned / being fixed' turned into 'fixed', and the fix's scope widened

**Answer judged:**

> Yes, this was fixed in release 2026.11.1 [KA-0008]. Once you're on that release, logging out through the identity provider ends the Lumora session and clears the offline cache.

**Retrieved chunks:**

- KA-0008 chunk 33: Known issue: SSO logout does not fully end the Lumora session > Symptoms
- KA-0008 chunk 34: Known issue: SSO logout does not fully end the Lumora session > Cause
- KA-0008 chunk 35: Known issue: SSO logout does not fully end the Lumora session > Workarounds
- KA-0004 chunk 14: Password reset email not received > Causes and resolution
- KA-0044 chunk 176: Using a custom domain for your workspace > After switching

**My verdict:** groundedness fail, correctness fail. Chunk 34 says 'being fixed in 2026.11.1' and that the release only fixes the cache; ending the session needs Single Logout configured. The reference says it's open.

**Judge:** groundedness 1, correctness 1. Unsupported claims: this was fixed in release 2026.11.1; Once you're on that release, logging out through the identity provider ends the Lumora session and clears the offline cache

> Claims: (1) "Yes, this was fixed in release 2026.11.1." KA-0008 says the cache defect is "being fixed in 2026.11.1", so it is in progress, not done. This contradicts the excerpt. (2) "Once on that release, logging out through the IdP ends the Lumora session and clears the offline cache." This is unsupported. The excerpt says the session only ends if Single Logout is configured, and the planned fix covers only the cache. The answer contradicts the excerpts on the main point and gives no workarounds.
> 
> Against the reference: the issue is still open with a fix planned for 2026.11.1, and workarounds apply. Saying it is fixed contradicts the main point and would mislead the user.

## H10 (Q07). A user's role is Admin but every option they see is read-only. What should I check first?

**Planted flaw:** grounded but misses the main point (Viewer seat)

**Answer judged:**

> Ask the user to sign out and back in, because role changes only take effect the next time the page loads [KA-0009].

**Retrieved chunks:**

- KA-0009 chunk 39: Workspace roles and permissions, and why an admin sees read-only options > "I should have admin access but only see read-only options"
- KA-0009 chunk 38: Workspace roles and permissions, and why an admin sees read-only options > Project-level roles
- KA-0009 chunk 37: Workspace roles and permissions, and why an admin sees read-only options > Roles
- KA-0010 chunk 41: User invitation emails not being delivered > Check first: is this affecting everyone?
- KA-0022 chunk 85: Sensitive fields and data exports, including the scheduled-export known issue > How it should work

**My verdict:** groundedness pass, correctness fail. Supported by chunk 39, item 4. The question asks what to check first: chunk 39 and the reference both say seat type. Correctness 2.

**Judge:** groundedness 5, correctness 2. Unsupported claims: none

> Claim: role changes take effect on next page load and the user should sign out and back in. KA-0009 step 4 supports this, so the answer is grounded. But the question asks what to check first. The excerpt and the reference both put seat type first: a Viewer seat is read-only even with the Admin role, and the fix is to change the seat to Full in Settings > Members. The answer gives only step 4 (stale session) and leaves out the main point, so it misses what the user needs.

