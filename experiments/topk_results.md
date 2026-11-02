# Top-k 5 vs 3

One change: the number of hybrid + rerank chunks retrieved and given to Claude, 5 (current) vs 3. Top 3 is the first 3 of the top 5, so nothing else differs. Answers use rag_answer.py's prompt and are scored with prompts/rag_answer_judge_v1.md against the chunks they were given; 4 or 5 is a pass.

| Measure | top-k 5 | top-k 3 |
|---|---|---|
| Right article in the chunks (35 answerable) | 35/35 (100%) | 35/35 (100%) |
| Key facts present in the chunks (35 answerable) | 57/59 (97%) | 55/59 (93%) |
| Questions with every key fact in the chunks | 33/35 (94%) | 31/35 (89%) |
| Context per question (characters, mean) | 2,396 | 1,426 |
| Groundedness pass, all 40 | 40/40 (100%) | 38/40 (95%) |
| Correctness pass, all 40 | 40/40 (100%) | 38/40 (95%) |
| Groundedness pass, 35 answerable | 35/35 (100%) | 33/35 (94%) |
| Correctness pass, 35 answerable | 35/35 (100%) | 33/35 (94%) |
| Groundedness pass, 5 unanswerable | 5/5 (100%) | 5/5 (100%) |
| Correctness pass, 5 unanswerable | 5/5 (100%) | 5/5 (100%) |
| Mean groundedness / correctness, all 40 | 4.95 / 4.85 | 4.83 / 4.75 |

## Questions that changed

Lost key facts, a changed article hit, or a judge verdict that moved between pass and fail.

| # | Kind | Question | Key facts lost at top-k 3 | Judge scores, 5 → 3 |
|---|---|---|---|---|
| Q24 | paraphrase | The browser freezes when I filter a table with 200,000 rows. | Filter on server | G 5 → 5, C 5 → 3 |
| Q27 | paraphrase | I click Delete on a custom field and nothing happens. | ENG-4502 | G 5 → 4, C 5 → 4 |
| Q31 | version-date | On iPad Safari in landscape, the sidebar covers the board and the toolbar is cut off. When will it be fixed, and how should I close the case? | none | G 5 → 3, C 5 → 3 |
| Q32 | reasoning | A Business customer bulk-edited a project by mistake 45 days ago. Can we restore it from backup? | none | G 5 → 3, C 5 → 4 |

## Q01. What is the first-response target for a High priority case on the Business plan?

### top-k 5: KA-0002#5, KA-0002#4, KA-0002#3, KA-0002#6, KA-0022#87

> The first-response target for a **High** priority case on the Business plan is **4 hours** [KA-0002].
> 
> A case is High when a major feature is broken or badly degraded and the workaround is painful, such as webhooks returning 500 or exports coming out empty [KA-0002].

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer:
> 1. The High-priority first-response target on Business is 4 hours. This is supported by the KA-0002 table.
> 2. A case is High when a major feature is broken or badly degraded and the workaround is painful, with webhooks returning 500 and empty exports as examples. This is supported by the KA-0002 priority definitions.
> 
> Every claim is supported. Compared with the reference, the main point (4 hours) matches. Omitting the Enterprise figure is fine because the question asks only about Business.

### top-k 3: KA-0002#5, KA-0002#4, KA-0002#3

> The first-response target for a **High** priority case on the Business plan is **4 hours** [KA-0002].
> 
> High priority covers cases where a major feature is broken or badly degraded and the workaround is painful, such as webhooks returning 500 errors or exports coming out empty [KA-0002]. The agent may change the priority you selected, but must add a case comment explaining why [KA-0002].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the retrieved excerpts:
> 1. High on Business is 4 hours. Supported by the first-response table.
> 2. High means a major feature is broken or badly degraded and the workaround is painful, for example webhooks returning 500 or exports coming out empty. Supported by the priority definitions.
> 3. Agents may change the priority the customer picked and must add a case comment explaining why. Supported.
> 
> Every claim is supported.
> 
> Compared with the reference: the main point, 4 hours, matches. The answer leaves out the Enterprise figure of 2 hours, but that is secondary and not needed to answer a question about the Business plan. Nothing in the answer contradicts the reference.

## Q02. A user in a workspace that requires SSO says the password reset email never arrives. Why?

### top-k 5: KA-0004#14, KA-0004#15, KA-0004#13, KA-0006#25, KA-0004#16

> **Lumora does not send password reset emails when a workspace enforces SSO.** The password is managed by the company's identity provider, not by Lumora [KA-0004].
> 
> To fix it:
> 1. Have the user sign in with **Continue with SSO** [KA-0004].
> 2. Have them reset their password through their company IdP [KA-0004].

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer:
> 1. Lumora does not send reset emails when a workspace enforces SSO. Supported by KA-0004, cause 2.
> 2. The password is managed by the identity provider. Supported by KA-0004.
> 3. The user should sign in with Continue with SSO. Supported.
> 4. The user should reset their password through the company IdP. Supported.
> 
> Every claim is supported by the excerpts, and the citations point to the right article.
> 
> Compared with the reference, the answer matches it fully: same cause, same reason, same two actions. Nothing contradicts it.

### top-k 3: KA-0004#14, KA-0004#15, KA-0004#13

> **Because the workspace requires SSO, Lumora doesn't send password reset emails.** The password is managed by the company's identity provider (IdP), not by Lumora [KA-0004].
> 
> **What the user should do:**
> 1. Sign in with **Continue with SSO** [KA-0004].
> 2. If they need a new password, reset it through their company IdP [KA-0004].

Groundedness 5, correctness 5. Unsupported: none

> Each claim in the answer, checked against the excerpts:
> 1. "Because the workspace requires SSO, Lumora doesn't send password reset emails." Supported by KA-0004 cause #2.
> 2. "The password is managed by the company's identity provider (IdP), not by Lumora." Supported: the excerpt says the password is managed by the identity provider.
> 3. "Sign in with Continue with SSO." Supported.
> 4. "Reset it through their company IdP." Supported.
> 
> The citations are correct and nothing is added beyond the excerpts.
> 
> Compared with the reference, the answer makes the same main point (SSO enforced means no reset email, because the IdP manages the password) and gives the same actions. Nothing contradicts the reference.

## Q03. Someone got locked out for a whole day after only three wrong passwords. Is that a bug?

### top-k 5: KA-0005#19, KA-0006#23, KA-0004#16, KA-0005#17, KA-0004#14

> No, that isn't a bug. It means the workspace admin has set a strict sign-in policy: 3 failed attempts and a 24-hour lockout [KA-0005]. Their own admin controls this setting, and the admin can unlock the account right away [KA-0005].
> 
> For context, the defaults are 5 failed attempts and a 15-minute lockout. Admins can change the attempts (3–10) and the lockout duration (15 minutes to 24 hours) only on the Business and Enterprise plans. On Starter and Team, the defaults apply and can't be changed [KA-0005].
> 
> The articles provided don't include the steps an admin uses to unlock an account.

Groundedness 5, correctness 4. Unsupported: none

> Claims checked against the excerpts:
> - "Not a bug; the admin set a strict policy of 3 attempts and a 24-hour lockout." Supported by KA-0005.
> - "Their own admin controls this setting, and the admin can unlock the account right away." Supported by KA-0005.
> - "Defaults are 5 attempts and a 15-minute lockout." Supported by the KA-0005 table.
> - "Attempts are configurable from 3 to 10 and lockout from 15 minutes to 24 hours, on Business and Enterprise only." Supported by the table.
> - "On Starter and Team the defaults apply and can't be changed." Supported.
> - "The articles don't include the unlock steps." This is accurate: the excerpt says "see below," but the steps were not retrieved. It is not a product claim.
> Every claim is grounded.
> 
> Against the reference: the main point (not a bug; the admin set a strict policy; the admin can unlock) matches, and the configurable ranges and plans match. The one gap is the unlock path (Settings > Members > ⋯ > Unlock account), which the reference includes and the answer leaves out, saying honestly that it lacks it. That is a secondary detail.

### top-k 3: KA-0005#19, KA-0006#23, KA-0004#16

> No, that's not a bug. It means the workspace admin has set a strict sign-in policy: 3 attempts, then a 24-hour lockout [KA-0005]. Their own workspace admin controls this setting [KA-0005].
> 
> The admin can also unlock the account right away [KA-0005]. The steps for doing that aren't included in the article text I have.

Groundedness 5, correctness 4. Unsupported: none

> Claims in the answer:
> 1. "Not a bug" is supported by KA-0005.
> 2. "Admin set a strict policy: 3 attempts, 24-hour lockout" is supported by KA-0005.
> 3. "Their own admin controls this setting" is supported by KA-0005.
> 4. "Admin can unlock the account right away" is supported by KA-0005.
> 5. The statement that the unlock steps aren't in the excerpt is accurate: KA-0005 says "see below" but the steps aren't included. This is not a product claim.
> 
> All claims are grounded.
> 
> Compared with the reference, the main point (not a bug; admin policy; admin can unlock) matches. The answer is missing secondary details: the configurable ranges (3–10 attempts, 15 minutes to 24 hours, Business/Enterprise) and the unlock menu path. Leaving out the path is honest because it wasn't retrieved, but it is still a missing useful detail. These are minor weaknesses, so correctness is 4.

## Q04. Every 6-digit code from my authenticator app is rejected, even when I type it fast.

### top-k 5: KA-0006#22, KA-0006#24, KA-0006#23, KA-0006#25, KA-0014#56

> The most likely cause is that **your phone's clock is off**. If it's more than about 60 seconds wrong, every code fails no matter how fast you type [KA-0006]. Another common cause is scanning an **old QR code**: each time the setup dialog opens it creates a new secret, so codes from an earlier attempt won't work [KA-0006].
> 
> To fix it:
> 
> 1. Turn on automatic date and time on your phone [KA-0006]:
>    - iOS: **Settings > General > Date & Time > Set Automatically**
>    - Android: **Settings > System > Date & time > Set time automatically**
>    - Google Authenticator on Android: **⋮ > Settings > Time correction for codes > Sync now**
> 2. In your authenticator app, delete any old *Lumora* entries [KA-0006].
> 3. In Lumora, cancel the setup dialog and start again at **Profile > Security > Two-factor authentication**, then scan the **new** QR code [KA-0006].
> 4. Enter the code that's showing now, not one that's about to expire [KA-0006].
> 
> If you can't use your device, sign in with a backup code. If you have none, a workspace Admin can reset 2FA from **Settings > Members > ⋯ > Reset 2FA** [KA-0006].

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer, checked against the retrieved excerpts:
> - The phone's clock is off; more than about 60 seconds wrong and every code fails. Supported by the KA-0006 Cause section. "No matter how fast you type" follows from that rule applied to the user's situation.
> - An old QR code is another cause; each setup dialog creates a new secret. Supported.
> - Resolution steps 1–4, including the iOS, Android and Google Authenticator paths. All supported verbatim.
> - Backup codes, and Admin reset via Settings > Members > ⋯ > Reset 2FA. Supported by the Lost device section.
> 
> Every claim is grounded and all citations point to the right article.
> 
> Compared with the reference, the answer gets the main point (clock skew of more than about 60 seconds) and the fix steps (automatic time, delete old entries, restart setup with the new QR code). It doesn't mention the 30-second TOTP window, which is a minor omission. Nothing contradicts the reference.

### top-k 3: KA-0006#22, KA-0006#24, KA-0006#23

> Since speed isn't the problem, the likeliest cause is that **your phone's clock is wrong**. If it is more than about 60 seconds off, every code fails [KA-0006]. Another possibility is that you scanned an **old QR code**: each time the setup dialog opens it creates a new secret, so codes from a previous attempt won't work [KA-0006].
> 
> To fix it:
> 
> 1. Turn on automatic date and time on your phone [KA-0006]:
>    - iOS: **Settings > General > Date & Time > Set Automatically**
>    - Android: **Settings > System > Date & time > Set time automatically**
>    - Google Authenticator on Android: **⋮ > Settings > Time correction for codes > Sync now**
> 2. In your authenticator app, delete any old *Lumora* entries [KA-0006].
> 3. In Lumora, cancel the setup dialog and start again at **Profile > Security > Two-factor authentication**. Scan the **new** QR code [KA-0006].
> 4. Enter the code that is showing now, not one that is about to expire [KA-0006].

Groundedness 5, correctness 5. Unsupported: none

> Claims: clock wrong >60s causes every code to fail (supported, Cause). Old QR code / new secret each time (supported). The answer treats clock error as the likeliest cause because fast typing rules out expiry; that follows reasonably from the user's statement and the excerpt. Resolution steps 1-4 match the excerpt exactly, including the menu paths. All claims are supported. Compared with the reference, the answer has the same main point (clock off by more than ~60s) and the same fix steps. It omits the 30-second TOTP window detail, which is minor.

## Q05. Our SAML login fails with 'Assertion expired'. What is the allowed clock skew?

### top-k 5: KA-0007#29, KA-0006#23, KA-0008#34, KA-0043#169, KA-0007#31

> The allowed clock skew is **3 minutes**. The "Assertion expired" error means the IdP server's clock is off. To fix it, correct NTP on the IdP so its time stays within 3 minutes [KA-0007].

Groundedness 5, correctness 5. Unsupported: none

> Checking each claim in the answer against the retrieved excerpts:
> 1. "Allowed clock skew is 3 minutes" is supported by the KA-0007 error table.
> 2. "Assertion expired" means the IdP server's clock is off. Supported by KA-0007.
> 3. "Fix NTP on the IdP" is supported by KA-0007.
> 4. "So its time stays within 3 minutes" follows directly from the stated skew.
> The citation to KA-0007 is correct.
> 
> The answer matches the reference on every point: 3 minutes as the allowed skew, the IdP clock as the cause, and fixing NTP as the action.

### top-k 3: KA-0007#29, KA-0006#23, KA-0008#34

> The allowed clock skew is **3 minutes** [KA-0007].
> 
> The `Assertion expired` error means the clock on your identity provider (IdP) server is off. To fix it, correct NTP (time sync) on the IdP so its clock is within 3 minutes [KA-0007].

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer:
> 1. The allowed clock skew is 3 minutes. KA-0007 states "Allowed skew is 3 minutes", so this is supported.
> 2. 'Assertion expired' means the IdP server's clock is off. KA-0007 gives this as the cause, so it is supported.
> 3. The fix is to correct NTP on the IdP so its clock is within 3 minutes. KA-0007 says "Fix NTP on the IdP", and "within 3 minutes" follows directly from the stated skew. Supported.
> 
> The citations are correct, and nothing is unsupported.
> 
> Compared with the reference, the answer has the same main point (3 minutes), the same cause and the same fix. Nothing contradicts it.

## Q06. After users log out of Okta, their open Lumora tabs keep working. Is this fixed yet?

### top-k 5: KA-0008#33, KA-0008#34, KA-0008#35, KA-0004#14, KA-0044#176

> **Not confirmed. The articles don't say whether the fix has shipped.** This is a known issue with two separate causes [KA-0008]:
> 
> 1. **No Single Logout URL configured.** If the SAML connection has no Single Logout URL, Lumora never learns about the Okta logout. The session stays active until it times out (12 hours by default) [KA-0008]. This is a configuration gap, not a bug.
> 2. **Offline cache not cleared.** Even with Single Logout set up, the web app's offline cache (service worker) isn't cleared on logout. This defect is being fixed in version 2026.11.1 [KA-0008].
> 
> **Workarounds until then** [KA-0008]:
> - Configure Single Logout in both Okta and Lumora (**Settings > Security > Single sign-on > Edit > Single Logout URL**). This ends the server-side session.
> - Shorten **Settings > Security > Session lifetime** to as little as 1 hour.
> - On shared or kiosk devices, turn on **Settings > Security > Disable offline cache**. Users lose offline access.
> - Have users also sign out in Lumora with **Profile > Sign out**, which clears the local cache.

Groundedness 4, correctness 4. Unsupported: The missing Single Logout URL is "a configuration gap, not a bug" (characterization not stated in excerpt)

> Claims checked against the retrieved text:
> - It is a known issue with two separate causes: supported by KA-0008 Cause.
> - With no Single Logout URL, Lumora never learns of the IdP logout, and the session lasts until timeout (12 hours by default): supported.
> - "This is a configuration gap, not a bug": an inference. The excerpt only calls #2 "the defect" and calls both items "problems." This is slightly broader framing than the text, but it is a reasonable reading.
> - The offline cache (service worker) is not cleared on logout, and this defect is being fixed in 2026.11.1: supported, and the wording keeps the excerpt's "being fixed."
> - All four workarounds, including the menu paths: supported by KA-0008 Workarounds.
> - "The articles don't say whether the fix has shipped": a statement about coverage, not a product claim. It is consistent with the excerpt's "being fixed."
> Applying "Okta" to the IdP follows from the question.
> 
> Compared with the reference: the main point is that the issue is open and a fix is planned for 2026.11.1, with the listed workarounds. The answer conveys that it is not confirmed fixed and is being fixed in 2026.11.1, and it lists all four workarounds. It misses the ENG-4471 ticket and the advice to link the case to it, which is a secondary detail. Its "not confirmed" framing is a little less direct than "open known issue," but it does not mislead.

### top-k 3: KA-0008#33, KA-0008#34, KA-0008#35

> **Not fully, as far as these articles say.** This is a known issue, and the articles don't say whether the fix has been released yet [KA-0008].
> 
> **Why it happens:**
> - If your SAML connection has no Single Logout URL, Lumora never learns about the Okta logout. The session stays active until it times out, which is 12 hours by default [KA-0008].
> - Even with Single Logout set up, the web app's offline cache isn't cleared on logout. This defect is being fixed in 2026.11.1 [KA-0008].
> 
> **Workarounds:**
> 1. Configure Single Logout in both Okta and Lumora (**Settings > Security > Single sign-on > Edit > Single Logout URL**). This ends the server-side session and should stop open tabs from working [KA-0008].
> 2. Shorten **Settings > Security > Session lifetime**, down to 1 hour if needed [KA-0008].
> 3. On shared or kiosk devices, turn on **Settings > Security > Disable offline cache**. Users lose offline access, but nothing is cached on the device [KA-0008].
> 4. Ask users to also sign out in Lumora with **Profile > Sign out**, which clears the local cache [KA-0008].

Groundedness 4, correctness 4. Unsupported: Configuring Single Logout "should stop open tabs from working"

> Claims checked against the retrieved excerpts:
> - Known issue, fix being worked on in 2026.11.1: supported (KA-0008 Cause).
> - "The articles don't say whether the fix has been released yet": a fair hedge, since the excerpt says "being fixed", which implies it is not released.
> - Without a Single Logout URL, Lumora never learns of the logout and the session lasts until timeout, 12 hours by default: supported.
> - The offline cache is not cleared on logout even with Single Logout set up: supported.
> - Workaround 1, the Single Logout menu path and "ends the server-side session": supported. The added "should stop open tabs from working" is an extrapolation the excerpt does not state.
> - Workaround 2, session lifetime down to 1 hour: supported.
> - Workaround 3, Disable offline cache: supported.
> - Workaround 4, Profile > Sign out clears the local cache: supported.
> - Calling the IdP "Okta" just applies the excerpt to the user's question, so it is fine.
> 
> Groundedness: one minor extrapolation, so 4.
> 
> Correctness: the reference's main point is that this is an open known issue with a fix planned for 2026.11.1. The answer conveys this, though the opening "Not fully" framing is a bit muddy. All four workarounds match the reference. The tracking ID ENG-4471 and the instruction to link the case to it are missing. That is a secondary detail, so 4.

## Q07. A user's role is Admin but every option they see is read-only. What should I check first?

### top-k 5: KA-0009#39, KA-0009#38, KA-0009#37, KA-0010#41, KA-0022#85

> Check the user's **seat type** first:
> 
> 1. Go to **Settings > Members** and find the user. If **Seat** says *Viewer*, change it to *Full*. This requires a free paid seat. [KA-0009]
> 2. Seat type takes priority over role, so a user on a Viewer seat is read-only everywhere even if their role says Admin. [KA-0009]
> 
> If the seat is already *Full*, check the remaining causes in this order:
> - **Wrong workspace:** they may be an Admin in only one of several workspaces. They can switch with the workspace picker in the top-left corner. [KA-0009]
> - **Past-due billing:** the workspace becomes read-only for everyone except Owners. [KA-0009]
> - **Stale session:** role changes apply on the next page load, so have them sign out and back in. [KA-0009]
> - **SCIM (Enterprise):** if roles sync from the IdP, change the user's group in the IdP rather than in Lumora. [KA-0009]

Groundedness 5, correctness 5. Unsupported: none

> Each claim in the answer, checked against the excerpts:
> 
> - "Check seat type first; in Settings > Members find the user; if Seat says Viewer change it to Full; requires a free paid seat": supported by KA-0009, step 1.
> - "Seat type takes priority over role; a Viewer seat is read-only everywhere even if the role says Admin": supported by the KA-0009 Roles table.
> - "Wrong workspace; they can switch with the workspace picker in the top-left corner": supported by step 2.
> - "Past-due billing makes the workspace read-only for everyone except Owners": supported by step 3.
> - "Stale session; role changes apply on the next page load; sign out and back in": supported by step 4.
> - "SCIM (Enterprise); change the user's group in the IdP instead of in Lumora": supported by step 5.
> 
> The answer leaves out that a Lumora-side change is overwritten at the next sync, but that omission doesn't change the meaning. Every claim is supported.
> 
> Against the reference: the answer gets the main point right (check seat type first; a Viewer seat overrides the Admin role; change it to Full in Settings > Members). It also covers all four follow-up checks the reference lists, in the same order. Nothing contradicts the reference.

### top-k 3: KA-0009#39, KA-0009#38, KA-0009#37

> **Check their seat type first.** In **Settings > Members**, find the user. If **Seat** says *Viewer*, change it to *Full*. This requires a free paid seat [KA-0009]. Seat type takes priority over role, so a user on a Viewer seat is read-only even if their role is Admin [KA-0009].
> 
> If the seat is already *Full*, check these next, in order [KA-0009]:
> 
> 1. **Wrong workspace:** they may be an Admin in a different workspace. They can switch using the workspace picker in the top-left corner.
> 2. **Billing lock:** if the subscription is past due, the workspace is read-only for everyone except Owners.
> 3. **Stale session:** role changes apply on the next page load, so have them sign out and back in.
> 4. **SCIM group mapping (Enterprise):** if roles come from the IdP, change the user's group there. Changes made in Lumora are overwritten at the next sync.

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> - Check seat type first in Settings > Members; if Viewer, change to Full; this needs a free paid seat. Supported by KA-0009 item 1.
> - Seat type takes priority over role, so a Viewer seat is read-only even with the Admin role. Supported by the Roles section.
> - Wrong workspace: the user may be Admin in a different workspace and can switch with the workspace picker in the top-left. Supported.
> - Billing lock: a past-due subscription makes the workspace read-only for everyone except Owners. Supported.
> - Stale session: role changes apply on the next page load, so sign out and back in. Supported.
> - SCIM (Enterprise): change the group in the IdP, because Lumora changes are overwritten at the next sync. Supported.
> Every claim is supported, so groundedness is 5.
> 
> Against the reference: the main point (seat type first, change Viewer to Full in Settings > Members) matches. The follow-up checks match the reference in the same order. Correctness is 5.

## Q08. Invitations show 'Pending — awaiting seat' and nobody gets an email. Why?

### top-k 5: KA-0010#42, KA-0010#40, KA-0010#43, KA-0010#41, KA-0011#46

> This happens when **every paid seat in your workspace is already in use**. The invites wait in *Pending — awaiting seat*, and no email is sent until a seat is available [KA-0010].
> 
> **To fix it,** either:
> - **Add seats** to your plan, or
> - **Free up a seat**, for example by removing or deactivating a user who no longer needs access [KA-0010].
> 
> If you have many users to deactivate or remove, you can do it in bulk with a CSV import. Go to **Settings > Members > Import** and set the `action` column to `deactivate` or `remove` [KA-0011].

Groundedness 4, correctness 5. Unsupported: Removing or deactivating a user frees up a seat (implied, not stated in excerpts)

> Claims:
> 1. Invites show 'Pending — awaiting seat' because every paid seat is in use. Supported by KA-0010, cause 4.
> 2. No email is sent "until a seat is available". KA-0010 says no email is sent; the "until" part is a mild inference.
> 3. Fix by adding seats or freeing one up. Supported.
> 4. Free a seat "by removing or deactivating a user". The excerpts don't say that deactivating or removing frees a seat. This is a reasonable elaboration, but slightly broader than the text.
> 5. Bulk deactivate or remove via CSV at Settings > Members > Import, with the `action` column set to deactivate or remove. Supported by KA-0011, though the excerpt doesn't say this frees seats.
> 
> The main answer is fully grounded. The only slip is the implication that deactivating or removing frees a seat, which is minor.
> 
> Correctness: the answer matches the reference's main point (all paid seats in use, so no email is sent) and its fix (add seats or free one up). Nothing contradicts the reference.

### top-k 3: KA-0010#42, KA-0010#40, KA-0010#43

> **All of your paid seats are in use.** When no seats are free, invitations stay in *Pending — awaiting seat* and no email is sent [KA-0010].
> 
> To fix it, either:
> - **Add more seats**, or
> - **Free up a seat** by removing someone who no longer needs access [KA-0010].
> 
> The articles don't say whether pending invites go out automatically once a seat becomes available.

Groundedness 5, correctness 5. Unsupported: none

> Claims: (1) All paid seats in use causes 'Pending — awaiting seat' and no email. Supported by KA-0010 item 4. (2) Fix by adding seats or freeing one up. Supported. The detail 'by removing someone who no longer needs access' is a slight elaboration of 'free one up' that follows naturally and doesn't change the meaning. (3) The note that the articles don't say whether pending invites send automatically is a statement about coverage, not a product claim, so it is neutral. The answer matches the reference's main point and fix exactly.

## Q09. What's the difference between deactivating and removing a user?

### top-k 5: KA-0011#47, KA-0011#45, KA-0031#122, KA-0011#44, KA-0011#48

> **Deactivating and removing both free the user's seat. The difference is what happens to their work and whether you can undo it:**
> 
> - **Deactivate:** Everything the user created stays assigned to them, and you can reverse it [KA-0011].
> - **Remove:** Their open tasks move to a person you choose, and you can't reverse it [KA-0011].
> 
> To do either for several users at once, go to **Settings > Members**. Tick the users, or filter and use **Select all matching**. Then choose **Deactivate** or **Remove** [KA-0011].

Groundedness 5, correctness 5. Unsupported: none

> Claims: 1) Both free the seat, which KA-0011 supports. 2) Deactivate keeps everything the user created assigned to them and can be reversed, which is supported. 3) Remove moves open tasks to a person you choose and can't be reversed, which is supported. 4) The bulk procedure (Settings > Members, tick users or filter and Select all matching, choose Deactivate or Remove) is supported by the member list excerpt. Every claim is grounded. The answer matches the reference fully. The extra procedure doesn't contradict anything.

### top-k 3: KA-0011#47, KA-0011#45, KA-0031#122

> Both free up the user's seat. They differ in what happens to the user's work and whether you can undo them:
> 
> - **Deactivate**: Everything the user created stays assigned to them, and you can reverse it [KA-0011].
> - **Remove**: Their open tasks move to a person you choose, and you can't reverse it [KA-0011].
> 
> To do either in bulk, go to **Settings > Members**. Tick the users, or filter and use **Select all matching**. Then choose **Deactivate** or **Remove** [KA-0011].

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer, checked against the excerpts:
> 1. Both actions free the seat. Supported by KA-0011.
> 2. Deactivate keeps everything the user created assigned to them and can be reversed. Supported by KA-0011.
> 3. Remove moves open tasks to a person you choose and can't be reversed. Supported by KA-0011.
> 4. The bulk procedure: Settings > Members, tick the users or filter and use Select all matching, then choose Deactivate or Remove. Supported by the KA-0011 member list section.
> 
> Every claim is supported and the citations are correct.
> 
> Compared with the reference, the answer matches it fully. The bulk steps are extra and don't contradict it.

## Q10. A customer updated their card and now sees a pending charge that isn't on any invoice. Do we refund it?

### top-k 5: KA-0012#49, KA-0012#50, KA-0014#57, KA-0013#54, KA-0013#53

> **No, there's nothing to refund.** A pending amount that appears after a card is added or updated is most likely a card **authorization hold**, not a charge. It should disappear within 3–7 business days [KA-0012].
> 
> To confirm:
> 1. Open the customer in the Billing Console and compare their card statement with **Invoices** and **Payments** [KA-0012].
> 2. If it's a small or matching amount marked *pending*, explain to the customer that it's a hold, not a charge [KA-0012].
> 
> You'd only refund if there are **two identical charges for the same invoice**. That's a true duplicate caused by a payment retry, and agents can refund it without approval [KA-0012].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the retrieved excerpts:
> 1. No refund; a pending amount after the card is added or updated is likely an authorization hold, not a charge, and disappears within 3–7 business days. Supported by the KA-0012 table row. The answer keeps the excerpt's hedge ("likely" / "most likely").
> 2. Open the customer in the Billing Console and compare the card statement with Invoices and Payments. Supported by KA-0012.
> 3. If it's a small or matching amount marked pending, explain it's a hold, not a charge. Supported by KA-0012.
> 4. Refund only if there are two identical charges for the same invoice, a true duplicate from a payment retry, which agents can refund without approval. Supported by both KA-0012 sections. The word "only" slightly narrows the excerpts, which also allow other refunds with approval over $500. In the context of this question it doesn't mislead.
> 
> All claims are grounded and citations are correct.
> 
> Compared with the reference: the answer matches the main point (no refund; it's an authorization hold that disappears within 3–7 business days) and nothing contradicts it.

### top-k 3: KA-0012#49, KA-0012#50, KA-0014#57

> **No, don't refund it.** A pending amount that shows up after a card is added or updated is a card **authorization hold**, not a charge, so there's nothing to refund [KA-0012].
> 
> - Tell the customer it's a temporary hold. It's usually small or matches the subscription amount, and it disappears from their statement within 3–7 business days [KA-0012].
> - To confirm, open the customer in the Billing Console and compare their card statement with **Invoices** and **Payments**. A hold won't match a payment on any invoice [KA-0012].
> - Refund only if you find two identical charges for the same invoice. That's a true duplicate from a payment retry [KA-0012].

Groundedness 4, correctness 5. Unsupported: Refund only if you find two identical charges for the same invoice (excerpt allows other refunds with approval)

> Claims checked against the excerpts:
> 1. A pending amount after a card is added or updated is an authorization hold, not a charge, so there is nothing to refund. KA-0012's table supports this, but it lists the hold only as the 'likely cause'. The answer states it as certain, dropping that hedge.
> 2. The hold is small or matches the amount and disappears within 3–7 business days. Supported. 'Matches the subscription amount' is slightly more specific than the excerpt's 'matching amount', but the meaning is the same.
> 3. Confirm by opening the customer in the Billing Console and comparing the statement with Invoices and Payments. Supported.
> 4. A hold won't match a payment on any invoice. This is a reasonable inference from the table and the question.
> 5. Refund only if you find two identical charges for the same invoice (a true duplicate from a payment retry). The duplicate row is supported. However, the excerpt also mentions other refunds over $500 that need Billing Lead approval, so 'only' is broader than the source.
> 
> Groundedness: the substance is supported, with minor slips: the dropped 'likely' hedge and the overbroad 'only'. Score 4.
> 
> Correctness: the answer matches the reference. Don't refund; it's an authorization hold that clears in 3–7 business days. Score 5.

## Q11. Can I refund a $700 true duplicate charge without approval?

### top-k 5: KA-0012#50, KA-0012#49, KA-0012#51, KA-0013#52, KA-0013#53

> Yes. Agents can refund true duplicates without approval, whatever the amount. The $500 Billing Lead approval rule applies only to other refunds [KA-0012].
> 
> To refund it:
> 1. In the Billing Console, open the duplicate **payment** (not the invoice) [KA-0012].
> 2. Click **Refund > Full** and choose the reason *Duplicate* [KA-0012].
> 3. Add a case comment with the refund ID [KA-0012].
> 
> The refund reaches the card in 5–10 business days, depending on the bank [KA-0012].
> 
> First make sure it's a true duplicate: two identical charges for the same invoice, caused by a payment retry [KA-0012].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the retrieved excerpts:
> - "Agents can refund true duplicates without approval": supported by KA-0012.
> - "whatever the amount": follows directly from the excerpt. Duplicates need no approval, and the $500 threshold is stated only for "any other refund".
> - "$500 Billing Lead approval applies only to other refunds": supported.
> - Refund steps (open the payment rather than the invoice, Refund > Full with reason Duplicate, add a case comment with the refund ID): supported.
> - "Refund reaches the card in 5–10 business days, depending on the bank": supported.
> - True duplicate definition (two identical charges for the same invoice, caused by a payment retry): supported by the table in KA-0012.
> 
> All claims are grounded.
> 
> Compared with the reference, the answer matches on every point: yes, no approval is needed, the $500 rule covers only other refunds, and the procedure is the same. Nothing contradicts the reference.

### top-k 3: KA-0012#50, KA-0012#49, KA-0012#51

> **Yes.** Agents can refund true duplicates without approval, whatever the amount. The Billing Lead approval rule applies only to *other* refunds over $500 [KA-0012].
> 
> First, confirm it's a true duplicate: two identical charges for the same invoice, caused by a payment retry [KA-0012]. Then:
> 
> 1. In the Billing Console, open the duplicate **payment** (not the invoice) [KA-0012].
> 2. Click **Refund > Full** and choose the reason *Duplicate* [KA-0012].
> 3. Add a case comment with the refund ID [KA-0012].
> 
> Let the customer know the refund takes 5–10 business days to reach their card, depending on their bank [KA-0012].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the retrieved excerpts:
> 1. Agents can refund true duplicates without approval: supported.
> 2. "whatever the amount": this follows directly from the unconditional statement plus the contrast with "any other refund over $500". It is a reasonable inference.
> 3. The Billing Lead approval applies only to other refunds over $500: supported.
> 4. A true duplicate is two identical charges for the same invoice, caused by a payment retry: supported by the table.
> 5. Steps (open the payment, not the invoice; Refund > Full with reason Duplicate; add a case comment with the refund ID): supported.
> 6. Refund reaches the card in 5–10 business days, depending on the bank: supported.
> 
> All claims are grounded and the citations are correct.
> 
> Against the reference, the answer gets the main point (yes, no approval needed), explains why the $500 rule doesn't apply, and gives the refund procedure. Nothing contradicts the reference.

## Q12. Billing history shows two invoices with the same number, one ending -V and one ending -R1. Will we be charged twice?

### top-k 5: KA-0013#52, KA-0013#53, KA-0012#51, KA-0012#49, KA-0012#50

> **No, you will only be charged once.** The invoice ending in `-V` is the original, now marked **Void**, and the one ending in `-R1` is the revised invoice with status **Paid** or **Open**. Only the revised (`-R1`) invoice is charged [KA-0013].
> 
> Lumora creates a revised invoice when billing details change after the invoice is issued, such as a new billing address, an added VAT/tax ID, or a changed PO number [KA-0013]. You can check both invoices' statuses in **Settings > Billing > Invoices** [KA-0013].

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer:
> 1. 'No, you will only be charged once': this follows from KA-0013, which says only the revised invoice is charged. Supported.
> 2. The -V invoice is the original with status Void: supported by KA-0013.
> 3. The -R1 invoice is the revision with status Paid or Open: supported by KA-0013.
> 4. Only the -R1 invoice is charged: supported by KA-0013.
> 5. A revision is created when billing details change, e.g. a new billing address, an added VAT/tax ID or a changed PO number: supported by KA-0013.
> 6. Both statuses can be checked in Settings > Billing > Invoices: supported by KA-0013.
> 
> Every claim is supported and the citations are correct, so groundedness is 5.
> 
> Against the reference: the main point is 'No, the -V invoice is the voided original, -R1 is the revision, and only the revision is charged.' The answer matches this exactly. It leaves out the reference's secondary advice for accounting (hide voided invoices or use Export statement). That advice was not in the retrieved excerpts, and the question did not ask about accounting, so this is only a small omission. Nothing in the answer contradicts the reference.
> 
> I considered scoring correctness 4 for the missing accounting tip, but it is secondary to the question asked, so correctness is 5.

### top-k 3: KA-0013#52, KA-0013#53, KA-0012#51

> No, you won't be charged twice. The invoice ending in `-V` is the original, and it has been voided. The one ending in `-R1` is the revised replacement, and only that one is charged [KA-0013].
> 
> You can confirm this in **Settings > Billing > Invoices**:
> - The `-V` invoice should show the status **Void** [KA-0013].
> - The `-R1` invoice should show **Paid** or **Open** [KA-0013].
> 
> Lumora creates a revised invoice when billing details change after the invoice is issued. Examples are a new billing address, an added VAT/tax ID, or a changed PO number [KA-0013]. Your accounting team should use the `-R1` invoice, since it's the only one that's charged [KA-0013].

Groundedness 5, correctness 4. Unsupported: none

> Claims checked against the excerpts:
> - Not charged twice; -V is the voided original; -R1 is the revision and only it is charged. Supported by KA-0013.
> - Path Settings > Billing > Invoices, with -V showing Void and -R1 showing Paid or Open. Supported.
> - Revisions happen when billing details change after issue (billing address, VAT/tax ID, PO number). Supported.
> - Accounting should use the -R1 invoice. Not stated outright, but it follows reasonably from "only the revised invoice is charged." Acceptable inference.
> 
> Against the reference: the main point (no double charge, -V void, -R1 charged) matches. The answer leaves out the reference's tip about hiding voided invoices or using Export statement for accounting. That is a secondary detail, and the excerpts didn't contain it. Its accounting advice (use -R1) is sensible and doesn't contradict the reference.

## Q13. A customer's payment failed 20 days ago. What can their users do in the workspace now?

### top-k 5: KA-0015#60, KA-0033#130, KA-0012#49, KA-0042#167, KA-0033#127

> At 20 days after the failed payment, the 14-day grace period has ended, so the workspace is **read-only** for everyone except Owners [KA-0015].
> 
> - **Regular users** can view content but can't make changes [KA-0015].
> - **Owners** can still reach billing to fix the payment [KA-0015].
> 
> If the payment isn't resolved by day 60, the workspace will be suspended. Data is then kept for 90 more days before it's deleted [KA-0015].

Groundedness 5, correctness 4. Unsupported: none

> Claims in the answer:
> 1. At day 20 the 14-day grace period has ended and the workspace is read-only for everyone except Owners. Supported by KA-0015 ("After day 14: read-only for everyone except Owners").
> 2. Regular users can view content but can't make changes. This follows directly from "read-only", so it is supported.
> 3. Owners can still reach billing to fix the payment. Supported by KA-0015; "to fix the payment" is a reasonable reading of why billing stays reachable.
> 4. If unresolved by day 60 the workspace is suspended, and data is kept 90 more days before deletion. Supported by KA-0015.
> 
> All claims are grounded and the citations are correct.
> 
> Compared with the reference, the main point matches: the workspace is read-only except for Owners, who can reach billing, and it is suspended after day 60. The answer leaves out the secondary detail that an Owner restores access by updating the payment method and clicking Retry payment. That step is not in the retrieved excerpts. Nothing in the answer contradicts the reference.

### top-k 3: KA-0015#60, KA-0033#130, KA-0012#49

> At 20 days, the workspace is past the 14-day grace period, so it is **read-only** for all users except Owners [KA-0015].
> 
> - **Regular users** can view the workspace but can't make changes [KA-0015].
> - **Owners** can still reach billing to fix the payment [KA-0015].
> 
> If payment still isn't resolved after day 60, the workspace is suspended. Data is kept for 90 more days and then deleted [KA-0015].

Groundedness 5, correctness 4. Unsupported: none

> Claims in the answer:
> 1. At day 20 the workspace is past the 14-day grace period and read-only for everyone except Owners. KA-0015 supports this: "After day 14: read-only for everyone except Owners." Applying that rule to day 20 is a direct inference.
> 2. Regular users can view the workspace but can't make changes. This is a direct paraphrase of "read-only." Supported.
> 3. Owners can still reach billing. Supported by KA-0015.
> 4. After day 60 the workspace is suspended, and data is kept for 90 more days, then deleted. Supported by KA-0015.
> 
> All claims are grounded, and nothing is unsupported.
> 
> Correctness: the main point matches the reference: read-only for everyone except Owners, who can reach billing, with suspension after day 60. The answer leaves out the reference's restore step (an Owner updates the payment method and clicks Retry payment). That step was not in the retrieved excerpts. It is a secondary detail that would help the user, so it costs one point.

## Q14. A bulk import took storage from 60% straight to 100% and no one got the 80% or 95% warning. Is that expected?

### top-k 5: KA-0016#64, KA-0016#65, KA-0036#143, KA-0042#168, KA-0011#46

> **Yes, this is a known gap.** If storage goes from below 80% to 100% in one day, for example after a large bulk import, only the 100% message appears [KA-0016]. The 80% and 95% warnings are skipped. A daily check to catch this is planned for 2026.11 [KA-0016].
> 
> At 100%:
> - **Blocked:** new uploads and new file versions [KA-0016].
> - **Still working:** everything else, including viewing and downloading existing files [KA-0016].
> - **Who is told:** everyone, through an error shown when uploading [KA-0016].
> 
> Admins can add more people to storage alerts under **Settings > Notifications > Workspace alerts > Storage** [KA-0016]. This won't fix the skipped warnings, but it widens who hears about the alerts that do fire.

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the retrieved excerpts:
> - "Known gap: from below 80% to 100% in one day, only the 100% message appears": supported by KA-0016.
> - "The 80% and 95% warnings are skipped": follows directly from the statement that only the 100% message appears.
> - "Daily check planned for 2026.11": supported, and the answer keeps the excerpt's "planned" wording.
> - "At 100%, new uploads and new file versions are blocked; viewing and downloading still work": supported by KA-0016.
> - "Everyone is told through an error shown when uploading": supported by the alerts table.
> - "Admins can add people under Settings > Notifications > Workspace alerts > Storage": supported.
> - "This won't fix the skipped warnings, but it widens who hears about the alerts that do fire": a reasonable inference from the excerpts, not a new product fact.
> 
> Every claim is grounded, so groundedness is 5.
> 
> Compared with the reference, the answer matches the main point (this is a known gap), the planned fix in 2026.11 and the 100% behavior. Nothing contradicts the reference, so correctness is 5.

### top-k 3: KA-0016#64, KA-0016#65, KA-0036#143

> Yes, that's expected. If storage goes from below 80% to 100% in one day, such as after a large bulk import, only the 100% message appears and the 80% and 95% warnings are skipped [KA-0016]. A daily check to catch this is planned for 2026.11 [KA-0016].
> 
> At 100%, new uploads and new file versions are blocked, but viewing and downloading existing files still work [KA-0016].
> 
> If you want more people to get storage alerts, an Admin can add them under **Settings > Notifications > Workspace alerts > Storage** [KA-0016].

Groundedness 5, correctness 5. Unsupported: none

> Claims: (1) Expected; jump from below 80% to 100% in one day shows only the 100% message, so the 80% and 95% warnings are skipped. Supported by the KA-0016 known gap. 'Skipped' follows directly from 'only the 100% message appears.' (2) A daily check is planned for 2026.11. Supported, and the answer keeps 'planned' rather than saying it is fixed. (3) At 100%, uploads and new versions are blocked, while viewing and downloading still work. Supported. (4) Admins can add people at Settings > Notifications > Workspace alerts > Storage. Supported. All claims are grounded. On correctness, the answer matches the reference's main point (known gap), the planned fix, and the 100% behaviour. The extras are consistent with the reference.

## Q15. On the Business plan, what's the biggest file I can upload in the browser, and is there a way to go bigger?

### top-k 5: KA-0017#68, KA-0017#67, KA-0017#69, KA-0016#66, KA-0021#83

> On the Business plan, the largest file you can upload in the browser (web or mobile) is **250 MB** [KA-0017]. Support can't raise this limit because it's tied to your plan [KA-0017].
> 
> Ways to work with bigger files:
> 
> 1. **Use the API.** Business supports resumable uploads up to **1 GB** via `POST /v2/files/uploads`, sent in 8 MB chunks [KA-0017].
> 2. **Link instead of uploading.** Use **Attach > From cloud storage** to attach a file from Google Drive, OneDrive, Dropbox, or Box. Linked files don't count against the size limit or your storage [KA-0017].
> 3. **Upgrade to Enterprise.** It allows 2 GB in the browser and 5 GB through the API [KA-0017].
> 4. **Compress or split the file**, for example into a ZIP archive [KA-0017].

Groundedness 5, correctness 5. Unsupported: none

> Claims: 250 MB web/mobile on Business (supported by the table). Support can't raise the limit because it is tied to the plan (supported). API resumable upload up to 1 GB via POST /v2/files/uploads in 8 MB chunks (supported). Link from cloud storage via Attach > From cloud storage, using Google Drive, OneDrive, Dropbox or Box, and linked files don't count against the limit or storage (supported). Enterprise allows 2 GB web and 5 GB API (supported). Compress or split, e.g. ZIP (supported). All citations are correct. Compared with the reference, the answer covers the main point (250 MB) and the key fact (1 GB via the API), plus the cloud linking and Enterprise upgrade options. Nothing contradicts the reference.

### top-k 3: KA-0017#68, KA-0017#67, KA-0017#69

> **In the browser, the Business plan's maximum upload is 250 MB** [KA-0017]. Support can't raise this limit because it's tied to the plan [KA-0017].
> 
> **Ways to go bigger:**
> 
> 1. **Use the API.** Business plans support resumable uploads up to 1 GB via `POST /v2/files/uploads`, sent in 8 MB chunks [KA-0017].
> 2. **Link instead of uploading.** Use **Attach > From cloud storage** to attach a file from Google Drive, OneDrive, Dropbox, or Box. Linked files don't count against the size limit or storage [KA-0017].
> 3. **Upgrade to Enterprise.** Browser uploads go up to 2 GB, and API resumable uploads up to 5 GB [KA-0017].
> 4. **Compress or split the file**, for example into a ZIP archive [KA-0017].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> - Business browser max is 250 MB: supported by the table (web and mobile column).
> - Support can't raise the limit because it's tied to the plan: supported.
> - API resumable uploads up to 1 GB on Business, via POST /v2/files/uploads in 8 MB chunks: supported by the table and the options list.
> - Link via Attach > From cloud storage (Google Drive, OneDrive, Dropbox, Box), and linked files don't count against the limit or storage: supported.
> - Upgrade to Enterprise gives 2 GB in the browser and 5 GB via API: supported by the table.
> - Compress or split, for example a ZIP: supported.
> All claims are grounded and all citations are correct.
> 
> Compared with the reference, the answer gets the main point (250 MB) and the key way to go bigger (the API, up to 1 GB). It also covers the other options the reference lists, linking from cloud storage and upgrading to Enterprise. Nothing contradicts the reference.

## Q16. We're on Team and our integration sends only about 80 requests a minute, but we still get 429 errors. Why?

### top-k 5: KA-0018#70, KA-0018#73, KA-0018#71, KA-0030#117, KA-0018#72

> **The 100-requests-per-minute Team limit is shared by your whole workspace, not given to each integration.** Every API token and installed integration counts against the same allowance [KA-0018]. So if other apps, such as the Salesforce connector, Zapier-style tools or a BI connector, are also making calls, together they can exceed 100 requests per minute even though yours sends only 80 [KA-0018].
> 
> Also check whether your integration calls the search endpoint (`/v2/search`). It has its own limit of 30 requests per minute on every plan [KA-0018].
> 
> **To find the cause:**
> - Go to **Settings > API > Usage**, which shows requests per token and per integration for the last 7 days. Usually one integration is using most of the allowance [KA-0018].
> 
> **To reduce 429 errors:**
> 1. Honor the `Retry-After` header and use exponential backoff with jitter [KA-0018].
> 2. Use webhooks instead of polling for changes [KA-0018].
> 3. Use batch endpoints (`POST /v2/tasks/batch`, up to 100 items) [KA-0018].
> 4. Request only the fields you need with `?fields=` [KA-0018].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> 1. The Team limit is 100/min, shared across the workspace by every token and integration. Supported by KA-0018.
> 2. Other apps (Salesforce connector, Zapier-style tools, BI connector) can push the combined total past 100. Supported.
> 3. Search endpoints have a separate 30/min limit on every plan. Supported.
> 4. Settings > API > Usage shows per-token and per-integration requests for the last 7 days, and usually one integration is using most of the allowance. Supported.
> 5. The four best practices (Retry-After with backoff and jitter, webhooks, batch endpoint up to 100 items, ?fields=). Supported. The webhooks point cites KA-0018, where the excerpt mentions it (it also references KA-0019), so the citation is fine.
> 
> Every claim is supported. Compared with the reference, the answer has the main point (the limit is shared per workspace) and the Usage page check. The search-limit note and best practices are extra but accurate and don't mislead.

### top-k 3: KA-0018#70, KA-0018#73, KA-0018#71

> **Why it happens**
> 
> The limit is likely shared. Rate limits apply per workspace per minute, and every API token and installed integration in the workspace draws from the same allowance [KA-0018]. On Team that allowance is 100 requests per minute [KA-0018]. So if other apps, such as a Salesforce connector, automation tools or a BI connector, send more than about 20 requests a minute between them, your integration's 80 will push the workspace over [KA-0018].
> 
> Also check whether your integration calls search. `/v2/search` has its own limit of 30 requests per minute on every plan [KA-0018].
> 
> **What to do**
> 
> 1. Go to **Settings > API > Usage**. It shows requests per token and per integration for the last 7 days, so you can see which integration is using most of the allowance [KA-0018].
> 2. Use the response headers to pace requests. `X-RateLimit-Remaining` shows how many requests are left in the current window, and `X-RateLimit-Reset` shows when the window resets [KA-0018].
> 3. When you get a 429, wait for the number of seconds in the `Retry-After` header before retrying [KA-0018].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> 1. Limits apply per workspace per minute and are shared by every API token and installed integration. Supported by KA-0018.
> 2. The Team allowance is 100 requests per minute. Supported by the table.
> 3. Other apps sending more than about 20 requests a minute would push the workspace over. This follows directly from the 100/min limit and the user's 80/min.
> 4. The example apps (Salesforce connector, automation tools, BI connector) are supported; "automation tools" paraphrases "Zapier-style tools".
> 5. `/v2/search` has a separate limit of 30 per minute on every plan. Supported.
> 6. Settings > API > Usage shows requests per token and per integration for the last 7 days. Supported.
> 7. `X-RateLimit-Remaining` and `X-RateLimit-Reset` work as described. Supported.
> 8. On a 429, wait the `Retry-After` seconds before retrying. This follows from the excerpt, which says a 429 comes with a `Retry-After` header in seconds.
> All claims are grounded.
> 
> Compared with the reference: the answer gives the main point (the 100/min limit is shared per workspace across all tokens and integrations, including other apps) and the action to check Settings > API > Usage. The extra notes on the search limit and the headers are accurate and do not mislead.

## Q17. Our webhook endpoint was disabled after an outage. How do we get the events we missed?

### top-k 5: KA-0019#76, KA-0019#74, KA-0019#75, KA-0019#77, KA-0018#72

> Fix the endpoint first, then click **Re-enable** and choose **Replay failed events**. This resends events from the last 72 hours [KA-0019].
> 
> Some context:
> - An endpoint is disabled after 24 hours of failed deliveries. Before that, Lumora retries each event 5 times over 24 hours with exponential backoff [KA-0019].
> - After re-enabling, you can confirm the endpoint works with **Send test event** on the endpoint page [KA-0019].
> 
> If the outage lasted longer than 72 hours, the articles don't say how to recover events older than that window.

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer:
> 1. Fix the endpoint, click Re-enable, choose Replay failed events, which resends events from the last 72 hours. Supported by KA-0019 (Re-enable section).
> 2. An endpoint is disabled after 24 hours of failed deliveries. Supported by KA-0019 (How webhooks work).
> 3. Before that, Lumora retries each event 5 times over 24 hours with exponential backoff. Supported by the same section; "each event" is a reasonable reading.
> 4. Send test event on the endpoint page can confirm the endpoint works. Supported by KA-0019 (Testing). Suggesting it after re-enabling is a reasonable application, not a new product fact.
> 5. The articles don't cover recovering events older than 72 hours. This is a note about coverage, not a product claim, and it is accurate.
> 
> Every claim is supported.
> 
> Compared with the reference, the main point matches exactly: fix the endpoint, Re-enable, Replay failed events, 72 hours. The extra context does not contradict the reference or mislead the user.

### top-k 3: KA-0019#76, KA-0019#74, KA-0019#75

> After fixing your endpoint, click **Re-enable** and choose **Replay failed events**. This resends events from the last 72 hours [KA-0019].
> 
> Lumora disables an endpoint after 24 hours of failed deliveries, during which it retries 5 times with exponential backoff [KA-0019]. If your outage lasted longer than 72 hours, the replay won't cover the oldest events. The articles don't explain how to recover events older than that.

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer, checked against <retrieved>:
> 1. "Fix the endpoint, click Re-enable, choose Replay failed events, which resends events from the last 72 hours." Supported verbatim by KA-0019.
> 2. "Lumora disables an endpoint after 24 hours of failed deliveries, retrying 5 times with exponential backoff." Supported by KA-0019, How webhooks work.
> 3. "If the outage lasted longer than 72 hours, the replay won't cover the oldest events." This follows directly from the 72-hour window.
> 4. "The articles don't explain how to recover older events." This is a statement about coverage, not a product claim, so it is neutral.
> All claims are grounded.
> 
> Comparison with the reference: the main point matches exactly (fix the endpoint, Re-enable, Replay failed events, 72-hour window). The extra details are accurate and do not mislead.

## Q18. Old links to the API docs with #section anchors now return 404. What's going on?

### top-k 5: KA-0020#79, KA-0020#81, KA-0020#80, KA-0044#176, KA-0020#78

> That's a known issue, tracked as DOC-311. The v1 documentation was retired on 2026-08-01, when the developer site moved to a new platform [KA-0020]. Old `/docs/api/...` links are supposed to redirect. Deep links to individual sections (anything with a `#anchor`) and links inside older community posts don't redirect, so they return 404 [KA-0020].
> 
> **Workaround:** Replace `/docs/api/` with `/v2/reference/` in the URL, or search the developer site [KA-0020]. The current v2 API reference is at `https://developers.lumora.example/v2/reference` [KA-0020].
> 
> **Reporting it:** Send us the page URL and the broken link, and we'll log it against DOC-311. Broken-link fixes ship weekly [KA-0020].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> 1. Known issue DOC-311: supported by KA-0020.
> 2. v1 docs retired 2026-08-01 when the developer site moved: supported.
> 3. Old /docs/api/ links should redirect, but #anchor deep links and links in older community posts don't: supported. That these return 404 follows from the section heading "Why do some links return 404?".
> 4. Workaround of replacing /docs/api/ with /v2/reference/ or searching the developer site: supported.
> 5. v2 reference URL: supported.
> 6. Reporting by sending the page URL and broken link, logged against DOC-311, with fixes shipping weekly: supported. The excerpt is an internal instruction to agents ("Ask for the page URL…"), and the answer reframes it as a customer-facing invitation. This is a reasonable adaptation, not a new fact.
> 
> Compared with the reference, the answer has the main point (v1 retired, anchors don't redirect, DOC-311) and the workaround. Nothing contradicts the reference.

### top-k 3: KA-0020#79, KA-0020#81, KA-0020#80

> This is a known issue (DOC-311). The v1 documentation was retired on 2026-08-01, when the developer site moved to a new platform [KA-0020]. Old `/docs/api/...` links should redirect, but deep links to individual sections (anything with `#anchor`) and links in older community posts don't [KA-0020].
> 
> **Workaround:** Replace `/docs/api/` with `/v2/reference/` in the URL, or search the developer site [KA-0020].
> 
> **Reporting a broken link:** Share the page URL and the broken link so it can be logged against DOC-311. Broken-link fixes ship weekly [KA-0020].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> 1. Known issue DOC-311: supported.
> 2. v1 docs retired 2026-08-01 when the developer site moved to a new platform: supported.
> 3. Old /docs/api links should redirect, but #anchor deep links and links in older community posts don't: supported.
> 4. Workaround of replacing /docs/api/ with /v2/reference/ or searching the developer site: supported.
> 5. Reporting by sharing the page URL and broken link, logged against DOC-311: supported. The excerpt is phrased as agent instructions ("Ask for the page URL..."), and the answer reframes it for the customer. That changes the audience, not the facts.
> 6. Broken-link fixes ship weekly: supported.
> 
> Every claim is grounded. The answer matches the reference on the main point (the retirement date and the anchor redirect issue DOC-311) and on the workaround. The reporting section is extra but consistent with the reference.

## Q19. Exporting a 120,000-row table to CSV downloads an empty file.

### top-k 5: KA-0021#83, KA-0021#84, KA-0021#82, KA-0043#171, KA-0011#46

> The likely cause is that 120,000 rows is over the 50,000-row limit for an immediate download. Exports that large run in the background, but older browser bookmarks still trigger the immediate download, which returns an empty file [KA-0021].
> 
> **Fix:**
> 1. Choose **Export > CSV (email me when ready)** instead of plain **Export > CSV** [KA-0021].
> 2. You'll get an email with a download link that works for 7 days. Each export can include up to 1,000,000 rows, so 120,000 is fine [KA-0021].
> 
> **If the file is still empty or missing rows:**
> - Save the view (**Save view**) and export from the saved view, so the export uses the same filters you see on screen [KA-0021].
> - Check your project role. Columns you aren't allowed to see are left out, and if every selected column is restricted, the file is empty [KA-0021].
> - Fields marked *Sensitive* are removed unless you have the **Export sensitive data** permission [KA-0021].
> - If Excel shows a blank column, open the file with **Data > From Text/CSV**, or use **Export > CSV (Excel compatible)** [KA-0021].
> 
> If none of this helps, collect the report URL, the time of export, the browser, and a HAR file, then escalate to Reports Engineering [KA-0021].

Groundedness 5, correctness 5. Unsupported: none

> Claims: 120,000 rows exceeds the 50,000-row threshold, so the export runs in the background, and older bookmarks trigger an immediate download that returns an empty file. Supported by KA-0021. The answer calls 50,000 a "limit for an immediate download", a slight framing, but it follows directly from the excerpt. Use Export > CSV (email me when ready): supported. Link valid for 7 days: supported. The answer says "you'll get an email"; the excerpt says "email me when ready" and that they'll receive a link, so this is a reasonable inference. Max 1,000,000 rows, so 120,000 is fine: follows from the stated rule. Save view and export from the saved view: supported. Field permissions, where all restricted columns give an empty file: supported. Sensitive fields: supported. Excel tips: supported. Escalation with report URL, export time, browser and HAR file: supported. All claims are grounded. Compared with the reference, the answer matches the main point and the key facts (background export, email option, 7 days, 1M max). The extra troubleshooting does not contradict the reference.

### top-k 3: KA-0021#83, KA-0021#84, KA-0021#82

> The export is too large for an immediate download. Exports over **50,000 rows** run in the background, and older browser bookmarks still trigger the immediate download, which returns an empty file [KA-0021].
> 
> **To fix it:**
> 1. Choose **Export > CSV (email me when ready)** [KA-0021].
> 2. Use the download link you receive by email. It stays valid for 7 days [KA-0021].
> 
> 120,000 rows is within the 1,000,000-row maximum per export [KA-0021].
> 
> **If the file is still empty:**
> - **Restricted columns:** columns you aren't allowed to see are left out, and if every selected column is restricted, the file is empty. Check your project role (KA-0009) [KA-0021].
> - **Sensitive fields:** these are removed unless you have the **Export sensitive data** permission (KA-0022) [KA-0021].
> - **Escalation:** collect the report URL, the time of export, the browser, and a HAR file (KA-0003), then escalate to Reports Engineering [KA-0021].

Groundedness 5, correctness 5. Unsupported: none

> Claims: too large for immediate download, >50,000 rows run in background, older bookmarks trigger immediate download returning empty file — supported. Choose Export > CSV (email me when ready) — supported. Link via email valid 7 days — excerpt says 'They'll receive a download link valid for 7 days'; 'by email' is implied by the option name, fine. 120,000 within 1,000,000 max — follows from the excerpt. Restricted columns and the project role check — supported. Sensitive fields and the permission — supported. Escalation steps — supported. Every claim is grounded. The main point and key facts match the reference: the background threshold, the email option, the 7-day link and the 1,000,000-row maximum. The extra troubleshooting steps don't contradict the reference.

## Q20. A customer got a scheduled export on 2026-09-10 that contained Sensitive fields. How should I handle it?

### top-k 5: KA-0022#87, KA-0022#86, KA-0022#85, KA-0045#179, KA-0042#168

> Treat this as a possible data exposure and set priority to at least **High** [KA-0022]. Since the export was scheduled and received before 2026-09-16, it matches known issue ENG-4388 [KA-0022]. That issue affected releases 2026.08.1 to 2026.09.1 and was fixed in 2026.09.2, released 2026-09-16 [KA-0022]. In those releases, scheduled exports kept including sensitive fields after the creator lost **Export sensitive data**, or after the schedule was handed to another owner [KA-0022].
> 
> Steps:
> 
> 1. Ask the customer for the export file name, the report or schedule name, and the date it was received. **Don't** ask them to attach the file [KA-0022].
> 2. Escalate to the **Security & Privacy** queue. They decide whether the customer must be formally notified under the DPA [KA-0022].
> 3. Recommend that the customer:
>    - delete any copies of the export,
>    - review the schedule's recipients, and
>    - check who holds **Export sensitive data** under **Settings > Roles** [KA-0022].
> 
> You don't need to escalate to Reports Engineering as a regression. That step applies only to exports received after the fix [KA-0022].

Groundedness 5, correctness 5. Unsupported: none

> Checking each claim in the answer against the retrieved excerpts:
> - "Treat it as a possible data exposure, priority at least High": supported by KA-0022.
> - "Scheduled and received before 2026-09-16, so it matches ENG-4388": follows from step 2 applied to the question's date (2026-09-10). Supported.
> - "Affected releases 2026.08.1 to 2026.09.1, fixed in 2026.09.2, released 2026-09-16": supported by the known-issue table.
> - Description of the bug (sensitive fields kept after the creator lost the permission, or after the schedule was handed to another owner): supported.
> - Step 1 (ask for file name, report or schedule name and date; don't ask for the file): supported.
> - Step 2 (escalate to Security & Privacy, who decide on DPA notification): supported.
> - Step 3 (delete copies, review recipients, check Settings > Roles): supported.
> - "No Reports Engineering escalation needed, since that applies only after the fix": follows from step 5. Supported.
> 
> The answer drops "in every case" from the Security & Privacy step, but it still says to escalate, so this doesn't change the meaning. All claims are grounded.
> 
> Against the reference: the answer matches ENG-4388 with its releases, fix version and date, and covers High priority, not asking for the file, and escalating to Security & Privacy. It omits that manual and API exports were unaffected, but that detail is irrelevant here because the export was scheduled. It fully matches the reference.

### top-k 3: KA-0022#87, KA-0022#86, KA-0022#85

> This matches known issue ENG-4388. The export was scheduled and received before the 2026-09-16 fix [KA-0022]. Treat it as a possible data exposure and set priority to at least **High** [KA-0022].
> 
> 1. **Get details:** Ask for the export file name, the report or schedule name, and the date it was received. Don't ask them to attach the file [KA-0022].
> 2. **Confirm the match:** ENG-4388 affected only **scheduled** exports in releases 2026.08.1 to 2026.09.1, and was fixed in 2026.09.2 on 2026-09-16 [KA-0022]. The bug kept sensitive fields in scheduled exports after the creator lost **Export sensitive data**, or after the schedule moved to another owner [KA-0022].
> 3. **Escalate to Security & Privacy:** This is required in every case. They decide whether the customer must be formally notified under the DPA [KA-0022].
> 4. **Advise the customer** to [KA-0022]:
>    - delete any copies of the export
>    - review the schedule's recipients
>    - check who holds **Export sensitive data** under **Settings > Roles**
> 
> The date is before the fix, so you don't need to escalate to Reports Engineering as a regression [KA-0022].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the retrieved excerpts:
> - The export matches ENG-4388 because it was scheduled and dated before 2026-09-16. Supported: this applies step 2 to the question's facts (2026-09-10 is before 2026-09-16).
> - Treat it as a possible data exposure with priority at least High. Supported.
> - Ask for the file name, the report or schedule name and the date received, and don't ask for the file. Supported.
> - Affected releases 2026.08.1 to 2026.09.1, fixed in 2026.09.2 on 2026-09-16, scheduled exports only. Supported by the known-issue table.
> - Bug description (sensitive fields kept after the creator lost the permission, or after an owner change). Supported.
> - Escalate to Security & Privacy in every case; they decide on DPA notification. Supported.
> - Advise the customer to delete copies, review recipients and check Export sensitive data under Settings > Roles. Supported.
> - No Reports Engineering escalation is needed because the date is before the fix. Follows directly from step 5, which applies only to dates after the fix.
> 
> Every claim is grounded.
> 
> Correctness: the answer matches the reference on all points: the ENG-4388 match, the release and fix details, possible data exposure, High priority, not asking for the file, and escalation to Security & Privacy. Nothing contradicts the reference.

## Q21. Can scheduled reports be delivered straight to an Amazon S3 bucket?

### top-k 5: KA-0024#93, KA-0024#92, KA-0024#95, KA-0042#168, KA-0043#172

> Yes, but S3 delivery is currently in **beta** (since 2026.10.1) and is only on **Business plans and above** [KA-0024].
> 
> To set it up:
> 1. An Owner turns on the beta under **Settings > Labs > Scheduled exports to cloud storage** [KA-0024].
> 2. Create an integration connection to an S3 bucket, using an IAM role ARN [KA-0024].
> 3. Open a saved report, click **Schedule**, and choose the frequency, time and timezone [KA-0024].
> 4. Pick a format (CSV, XLSX or PDF), choose S3 as the destination, and click **Save** [KA-0024].
> 
> Files are named `<report>_<YYYY-MM-DD>.<ext>` [KA-0024]. You can send beta feedback through the in-app **Labs feedback** form [KA-0024].

Groundedness 5, correctness 4. Unsupported: none

> Claims checked against the retrieved excerpts:
> - Yes, S3 delivery is in beta since 2026.10.1 on Business+. Supported by the KA-0024 destinations table.
> - An Owner enables it under Settings > Labs > Scheduled exports to cloud storage. Supported.
> - S3 needs an integration connection with a bucket and an IAM role ARN. Supported.
> - Open a saved report, click Schedule, and choose frequency, time and timezone. Supported.
> - Format is CSV, XLSX or PDF; choose the destination and click Save. Supported. Choosing S3 as the destination follows directly from the excerpts.
> - File naming pattern and the Labs feedback form. Both supported.
> 
> Every claim is supported, so groundedness is 5.
> 
> Compared with the reference, the answer matches the main point: yes, in beta since 2026.10.1, on Business and above, with the Owner enabling it in Labs and an IAM role ARN needed for S3. It leaves out the internal guidance to link feature-request cases to FR-118 and close them as Resolved – Available in beta. That guidance only applies to feature-request cases, so it is a minor secondary omission for an answer addressed to the user.

### top-k 3: KA-0024#93, KA-0024#92, KA-0024#95

> **Yes, but it's currently a beta feature.** Scheduled reports can go to cloud storage, including Amazon S3, on Business plans and above. This has been in **beta** since version 2026.10.1 [KA-0024].
> 
> **To set it up:**
> 1. An Owner turns on the beta under **Settings > Labs > Scheduled exports to cloud storage** [KA-0024].
> 2. Connect the destination with an S3 bucket and an IAM role ARN [KA-0024].
> 3. Open a saved report, click **Schedule**, and choose the frequency, time, timezone, and format (CSV, XLSX or PDF). Then pick the S3 destination and click **Save** [KA-0024].
> 
> Files are named `<report>_<YYYY-MM-DD>.<ext>` [KA-0024]. The schedule runs with the schedule owner's permissions [KA-0024]. You can send feedback on the beta through the in-app **Labs feedback** form [KA-0024].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> - Yes, S3 is a beta destination on Business+, in beta since 2026.10.1: supported.
> - An Owner enables it under Settings > Labs > Scheduled exports to cloud storage: supported.
> - The S3 connection needs a bucket with an IAM role ARN: supported.
> - Schedule steps (open a saved report, click Schedule, choose frequency, time, timezone and format CSV/XLSX/PDF, pick the destination, Save): supported.
> - File naming pattern `<report>_<YYYY-MM-DD>.<ext>`: supported.
> - The schedule runs with the owner's permissions: supported.
> - Feedback goes through the in-app Labs feedback form: supported.
> 
> Every claim is grounded, and all citations point to the right article.
> 
> Against the reference, the main point (yes, beta since 2026.10.1, Business+, Owner enables it in Labs, S3 needs an IAM role ARN) is fully matched. The answer omits the internal feature-request handling (link FR-118, close as Resolved – Available in beta). That guidance is for agents and is secondary for this user's question. Nothing contradicts the reference.

## Q22. A scheduled report set to New York time back in July runs at the wrong hour. How do we fix it?

### top-k 5: KA-0025#98, KA-0025#97, KA-0025#96, KA-0026#101, KA-0024#94

> This is probably the known defect: schedules created before release 2026.08.2 saved the timezone as UTC, whatever timezone was chosen. The schedule shows New York when you open it, but it actually runs in UTC [KA-0025][KA-0024].
> 
> **To fix it:**
> 1. Open the schedule and check its **Timezone** field [KA-0025].
> 2. Edit the schedule, change any setting, change it back, then click **Save**. Saving rewrites the stored timezone [KA-0025].
> 
> Once it's fixed, the report will run at New York time. It also follows daylight saving, so a 09:00 New York schedule stays at 09:00 when the clocks change [KA-0025].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> - Schedules created before 2026.08.2 saved the timezone as UTC whatever was chosen: supported by KA-0025 and KA-0024.
> - The schedule shows the correct timezone when opened but runs in UTC: supported by KA-0025.
> - Open the schedule and check its Timezone field: supported by KA-0025, step 1.
> - Edit the schedule, change any setting and change it back, then Save, which rewrites the stored timezone: supported by KA-0025, step 2.
> - After the fix the report runs at New York time: follows directly from the fix rewriting the stored timezone.
> - Schedules follow daylight saving, so a 09:00 New York schedule stays at 09:00: supported by KA-0025, step 3.
> 
> The word "probably" is a reasonable hedge. The question says July but doesn't confirm the schedule predates release 2026.08.2.
> 
> Compared with the reference, the answer has the same main point: the pre-2026.08.2 UTC defect and the edit/change/revert/Save fix. Nothing contradicts the reference.

### top-k 3: KA-0025#98, KA-0025#97, KA-0025#96

> This is most likely a known defect that was fixed in release 2026.08.2 [KA-0025]:
> 
> - **Cause:** Schedules created before that release saved their timezone as UTC, whatever timezone was chosen. When you open the schedule it shows the correct timezone, but it actually runs in UTC [KA-0025].
> - **Fix:**
>   1. Open and edit the schedule.
>   2. Change any setting, then change it back.
>   3. Click **Save**. Saving rewrites the stored timezone [KA-0025].
> 
> If it still runs at the wrong hour, check its **Timezone** field [KA-0025]. Daylight saving time isn't the cause, because schedules follow local time in their timezone. A 09:00 New York schedule stays at 09:00 after the clocks change [KA-0025].
> 
> To keep the report consistent for everyone, you can also set **Settings > Timezone > Fixed** on the report itself (for example, *America/New_York*). All viewers, exports and schedules will then use that timezone [KA-0025].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> - The known defect was fixed in 2026.08.2. Supported.
> - Schedules created before that release saved the timezone as UTC, whatever was chosen. Supported.
> - The schedule shows the right timezone but runs in UTC. Supported.
> - Fix: edit the schedule, change a setting and change it back, then Save, which rewrites the stored timezone. Supported.
> - Check the Timezone field. Supported. The excerpt lists this as step 1, and the answer moves it to a later fallback, but that is not a factual error.
> - DST isn't the cause because schedules follow local time; a 09:00 New York schedule stays at 09:00. Supported.
> - Settings > Timezone > Fixed makes all viewers, exports and schedules use that timezone. Supported.
> 
> The answer hedges with "most likely." The question says the schedule was created in July, and the excerpts don't say when 2026.08.2 shipped, so the hedge is appropriate.
> 
> Compared with the reference, the answer has the main cause and fix right and contradicts nothing.

## Q23. One dashboard widget still shows July revenue while the others are current.

### top-k 5: KA-0026#100, KA-0026#101, KA-0026#102, KA-0035#137, KA-0025#99

> The most likely cause is that the widget's date filter is fixed to July (for example *1 Jul – 31 Jul*) instead of a relative range [KA-0026].
> 
> 1. **Fix the date range (most common cause):** Edit the widget, go to **Filters > Date**, and choose a relative option such as **This month** or **Last 30 days** [KA-0026].
> 2. **Check for a paused snapshot:** If the source report uses **Save as snapshot**, the widget shows the last snapshot. Snapshots pause when the report owner is deactivated. Open the source report and check **Last refreshed**, then assign a new owner or switch to live data [KA-0026].
> 3. **Check the connector:** If the revenue comes from an external source, such as a billing system, check **Settings > Integrations > [connector] > Sync log** [KA-0026].
> 4. **Refresh the cache:** Widgets are cached for up to 15 minutes. Click **⋯ > Refresh**. If the widget is still out of date after refreshing, the cache isn't the problem [KA-0026].
> 5. **Check the source report:** If the dashboard was duplicated, the widget may still point to the original report. Check **Edit widget > Source** [KA-0026].
> 
> If none of these fix it, escalate to Reports Engineering. Include the dashboard URL, the widget name, the expected value, and the value shown [KA-0026].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against KA-0026:
> - Most likely cause is a date filter fixed to July rather than a relative range: supported (cause 1, 'most common cause'; the 1 Jul – 31 Jul example).
> - Edit widget > Filters > Date, choose This month or Last 30 days: supported.
> - Paused snapshot: Save as snapshot shows the last snapshot, snapshots pause when the owner is deactivated, check Last refreshed, assign a new owner or switch to live data: supported.
> - Connector: check Settings > Integrations > [connector] > Sync log for external sources such as a billing system: supported.
> - Cache: widgets are cached up to 15 minutes, use ⋯ > Refresh, and still stale after refresh means it isn't the cache: supported.
> - Duplicated dashboard: widget points to the original report, check Edit widget > Source: supported.
> - Escalate to Reports Engineering with the dashboard URL, widget name, expected value and shown value: supported.
> Every claim is supported and the citations are correct.
> 
> Compared with the reference: the main point (fixed date filter; switch to a relative range under Filters > Date) matches, and all the secondary checks the reference lists are covered. Nothing contradicts the reference.

### top-k 3: KA-0026#100, KA-0026#101, KA-0026#102

> This is most likely a **fixed date range**, the most common cause. The widget's filter is set to absolute dates (for example *1 Jul – 31 Jul*) instead of a relative range [KA-0026].
> 
> **Fix:** Edit the widget, go to **Filters > Date**, and choose a relative option such as **This month** or **Last 30 days** [KA-0026].
> 
> If the date filter is already relative, check these in order:
> 1. **Cache:** Click **⋯ > Refresh** on the widget. Widgets are cached for up to 15 minutes, so if it's still out of date after refreshing, the cache isn't the problem [KA-0026].
> 2. **Paused snapshot:** If the source report uses **Save as snapshot**, open it and check **Last refreshed**. Snapshots pause when the report owner is deactivated. Assign a new owner or switch to live data [KA-0026].
> 3. **Connector stopped syncing:** If the revenue comes from an external source such as a billing system, check **Settings > Integrations > [connector] > Sync log** [KA-0026].
> 4. **Wrong source report:** If the dashboard was duplicated, its widgets still point to the original report. Check **Edit widget > Source** [KA-0026].
> 
> If none of these apply, escalate to Reports Engineering. Include the dashboard URL, the widget name, the expected value, and the value shown [KA-0026].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the retrieved excerpts:
> - A fixed date range is the most likely and most common cause, with the filter set to absolute dates like 1 Jul – 31 Jul: supported.
> - Fix via Filters > Date by choosing This month or Last 30 days: supported.
> - Cache is up to 15 minutes, use ⋯ > Refresh, and a widget still stale after refreshing isn't a cache problem: supported.
> - Paused snapshot: Save as snapshot, check Last refreshed, snapshots pause when the owner is deactivated, assign a new owner or switch to live data: supported.
> - Connector sync log path: supported.
> - Duplicated dashboard widgets point to the original report, check Edit widget > Source: supported.
> - Escalation to Reports Engineering with the listed details: supported.
> 
> The answer reorders the checks ("check these in order", with cache first), whereas the excerpt lists them differently. This is a mild framing choice and not a factual claim that contradicts the excerpt. All claims are grounded.
> 
> Compared with the reference, the main point matches: fixed dates, fixed by choosing a relative range. The answer also covers all the secondary checks the reference lists.

## Q24. The browser freezes when I filter a table with 200,000 rows.

### top-k 5: KA-0028#108, KA-0028#111, KA-0028#109, KA-0028#110, KA-0021#83

> A table that size is more than the browser handles well. Table views load up to 100,000 rows into the browser by default, and above that, filtering in the browser uses a lot of memory and CPU, especially with formula columns [KA-0028].
> 
> To fix it:
> 
> 1. **Turn on server-side filtering (main fix).** Go to **View settings > Performance > Filter on server**. Filters and sorts then run on Lumora's servers, and only 500 rows at a time are loaded [KA-0028].
> 2. **Filter on indexed fields.** These filter much faster: Status, Assignee, Created date, Due date, Project, and any custom field with **Indexed** ticked (**Settings > Fields > Edit**). Business plans include up to 20 indexed custom fields, Enterprise up to 100 [KA-0028].
> 3. **Use saved views** with the filters already set, so the full table never loads [KA-0028].
> 4. **Hide formula columns** you don't need in that view [KA-0028].
> 5. **Archive old rows.** Moving completed items older than 12 months to an archive table can make the main table much smaller [KA-0028].
> 
> From release 2026.11, server-side filtering turns on automatically above 50,000 rows [KA-0028].
> 
> If it still freezes with server-side filtering on, collect a HAR file and a browser performance profile and escalate to Frontend Engineering [KA-0028].

Groundedness 5, correctness 5. Unsupported: none

> I checked each claim in the answer against the KA-0028 excerpts:
> - Table views load up to 100,000 rows by default, and filtering above that uses a lot of memory and CPU, especially with formula columns. Supported by "Why it happens".
> - Server-side filtering via View settings > Performance > Filter on server, with only 500 rows loaded, described as the main fix. Supported.
> - Indexed fields list, Settings > Fields > Edit, and the 20 (Business) / 100 (Enterprise) limits. Supported.
> - Saved views, hiding formula columns, and archiving rows older than 12 months. Supported.
> - Server-side filtering turns on automatically above 50,000 rows from release 2026.11. Supported.
> - Escalation with a HAR file and performance profile. Supported.
> 
> One small framing point: the opening line "more than the browser handles well" is a reasonable application of the excerpt to a 200,000-row table, not a new claim. Every claim is grounded.
> 
> Against the reference, the answer covers the main fix (server-side filtering with the exact menu path and the 500-row page), indexed fields, saved views, formula columns and the 2026.11 change. Nothing contradicts the reference.

### top-k 3: KA-0028#108, KA-0028#111, KA-0028#109

> Large tables are a known cause of this. By default, table views load up to 100,000 rows into the browser so quick filters respond immediately. Above that size, filtering in the browser uses a lot of memory and CPU, especially with formula columns [KA-0028]. A freeze or a "Page unresponsive" message is the typical symptom [KA-0028].
> 
> What the articles cover:
> - **From release 2026.11**, server-side filtering turns on automatically for tables above 50,000 rows, so your 200,000-row table should use it [KA-0028].
> - **If the freezing continues with server-side filtering on**, collect a HAR file and a browser performance profile and escalate to Frontend Engineering [KA-0028].
> 
> The articles don't explain how to turn on server-side filtering manually on earlier releases or give other workarounds, so I can't advise on those.

Groundedness 5, correctness 3. Unsupported: none

> Claims in the answer, checked against the excerpts:
> - Default table views load up to 100,000 rows into the browser, and above that filtering uses a lot of memory and CPU, especially with formula columns. Supported by the "Why it happens" excerpt.
> - Freezing or a "Page unresponsive" message is the typical symptom. Supported by the "Symptoms" excerpt.
> - From release 2026.11, server-side filtering turns on automatically above 50,000 rows. Supported by the "Notes" excerpt. The conclusion "so your 200,000-row table should use it" applies the stated rule to the question, but it assumes the user is on 2026.11 or later. The answer does hedge with "should", and the release is stated in the bold header, so this is acceptable.
> - If freezing continues with server-side filtering on, collect a HAR file and a performance profile and escalate. Supported.
> - The excerpts don't explain manual enabling or other workarounds. True; this is a statement about coverage, not a product claim.
> 
> Groundedness: every claim is supported, so 5.
> 
> Correctness: the reference's main point is to turn on server-side filtering manually (View settings > Performance > Filter on server). Its other workarounds are filtering on indexed fields, using saved views and hiding formula columns. The answer does not give the manual enable path or these workarounds; it honestly says the excerpts don't cover them. It does mention server-side filtering and the automatic behaviour from 2026.11, which is in the reference. So the main action is only partly conveyed: the user learns that server-side filtering exists but not how to turn it on. That leaves an important fact missing, so 3 rather than 2.

## Q25. The Salesforce connector disconnects like clockwork every 12 hours.

### top-k 5: KA-0031#121, KA-0031#122, KA-0031#123, KA-0018#70, KA-0035#137

> A disconnect on a fixed schedule like every 12 hours usually comes from Salesforce's **refresh token policy**, which is the most common cause of this problem [KA-0031]. If the policy is set to "Expire refresh token after X hours", the connector disconnects on that schedule [KA-0031].
> 
> **To fix it:**
> 1. In Salesforce Setup, go to **Connected Apps OAuth Usage > Lumora Workspace > Manage > Edit Policies** [KA-0031].
> 2. Set **Refresh Token Policy** to *Refresh token is valid until revoked* [KA-0031].
> 3. In Lumora, go to **Settings > Integrations > Salesforce > Reconnect**, signed in as the integration user. Your field mappings are kept [KA-0031].
> 
> If it still disconnects after that, check the other causes in KA-0031: a password change or deactivation of the connecting user, IP restrictions, the Salesforce API limit, a sandbox refresh, or too many tokens for one user [KA-0031].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the retrieved excerpts:
> 1. A disconnect on a fixed schedule usually comes from the refresh token policy, the most common cause. Supported by KA-0031: "This is the most common cause" and "disconnects on that schedule."
> 2. If the policy is set to "Expire refresh token after X hours", the connector disconnects on that schedule. Supported.
> 3. Menu path Connected Apps OAuth Usage > Lumora Workspace > Manage > Edit Policies. Supported, matches the excerpt exactly.
> 4. Set the policy to "Refresh token is valid until revoked". Supported.
> 5. Reconnect via Settings > Integrations > Salesforce > Reconnect as the integration user, and field mappings are kept. Supported.
> 6. List of other causes (password change or deactivation, IP restrictions, API limit, sandbox refresh, too many tokens). Supported.
> 
> All claims are grounded and there are no unsupported claims.
> 
> Compared with the reference, the answer has the same main point: the refresh token policy expires the token, and the fix is to set it to valid until revoked via the same Setup path. The extra reconnect step and fallback causes are consistent with the reference and do not mislead.

### top-k 3: KA-0031#121, KA-0031#122, KA-0031#123

> A disconnect every 12 hours almost certainly comes from Salesforce's **Refresh Token Policy**. If it's set to "Expire refresh token after X hours", the connector disconnects on that schedule. This is the most common cause [KA-0031].
> 
> **Fix:**
> 1. In Salesforce Setup, go to **Connected Apps OAuth Usage > Lumora Workspace > Manage > Edit Policies** [KA-0031].
> 2. Set **Refresh Token Policy** to *Refresh token is valid until revoked* [KA-0031].
> 3. In Lumora, go to **Settings > Integrations > Salesforce > Reconnect**, signed in as the integration user. Your field mappings are kept [KA-0031].
> 
> If it still disconnects after that, check the other listed causes, such as the daily API limit or more than 5 refresh tokens for the same user and connected app [KA-0031].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> 1. The Refresh Token Policy is the cause of a 12-hour disconnect: supported. KA-0031 says that if the policy is set to "Expire refresh token after X hours", the connector disconnects on that schedule. Applying this to a fixed 12-hour pattern follows directly; "almost certainly" is a reasonable inference.
> 2. It is the most common cause: supported.
> 3. The Setup path "Connected Apps OAuth Usage > Lumora Workspace > Manage > Edit Policies": supported.
> 4. Setting the policy to "Refresh token is valid until revoked": supported.
> 5. Reconnect through Settings > Integrations > Salesforce > Reconnect as the integration user, with field mappings kept: supported.
> 6. Other causes such as the daily API limit, and the limit of 5 refresh tokens per user per connected app: supported.
> Every claim is grounded.
> 
> Against the reference: the main point (an expiring refresh token policy, fixed by setting it to valid until revoked, via the correct path) matches. The reconnect step and the other causes are extra but consistent with the reference.

## Q26. A payment form's transaction log has no entries at all. What does that mean?

### top-k 5: KA-0033#129, KA-0033#131, KA-0033#127, KA-0033#130, KA-0033#128

> If the transaction log has no entries at all, the form isn't reaching the payment step [KA-0033]. To fix it, check the conditional logic on the payment field [KA-0033].

Groundedness 5, correctness 4. Unsupported: none

> The answer makes two claims. (1) "No entries means the form isn't reaching the payment step." The KA-0033 table supports this. (2) "Check the conditional logic on the payment field." The same table supports this. Both claims are grounded. Compared with the reference, the main point (the form never reaches the payment step) and the fix (check the payment field's conditional logic) both match. The answer leaves out that payment failures should be set to Urgent. That is a secondary detail and arguably less relevant to a question about what an empty log means, but the reference includes it.

### top-k 3: KA-0033#129, KA-0033#131, KA-0033#127

> If the transaction log (**Settings > Payments > Transaction log**) has no entries at all, the form isn't reaching the payment step [KA-0033].
> 
> **Fix:** Check the conditional logic on the payment field [KA-0033].
> 
> Because failed payments mean the customer is losing revenue, set the case to **Urgent** [KA-0033].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts: 1) The transaction log is at Settings > Payments > Transaction log. Supported. 2) No entries at all means the form isn't reaching the payment step. Supported by the table. 3) The fix is to check the payment field's conditional logic. Supported. 4) Failed payments mean the customer is losing revenue, so set the case to Urgent. Supported by the Priority section. All citations are correct. Compared with the reference, the answer matches every point: the form never reaches the payment step, the fix is to check the conditional logic, and the case should be Urgent.

## Q27. I click Delete on a custom field and nothing happens.

### top-k 5: KA-0035#136, KA-0035#138, KA-0035#139, KA-0035#140, KA-0035#137

> This usually means something still uses the field, and a field can't be deleted while it's in use [KA-0035]. The references can come from:
> 
> - Automation rule conditions or actions
> - Report filters, columns or groupings, and dashboard widgets
> - Form questions mapped to the field
> - Formula fields that refer to it
> - Integration field mappings (for example, the Salesforce connector)
> - Required-field rules on a project [KA-0035]
> 
> It can look like nothing happens because of a known bug (ENG-4502): the message listing these references sometimes closes straight away. A fix is due in 2026.11.1 [KA-0035].
> 
> **To delete the field:**
> 1. In **Settings > Fields**, open the field and go to the **Usage** tab. It lists every reference with a link [KA-0035].
> 2. Remove or change each reference: edit the automation, report or form, or remap the integration field [KA-0035].
> 3. Go back to the field and click **Delete** again [KA-0035].
> 
> **If the field is used in many places,** you can choose **Archive field** instead. It disappears from forms, views and pickers, but past values and references are kept, and you can restore it at any time [KA-0035].
> 
> After you delete a field, you can restore it with its values for 30 days under **Settings > Fields > Deleted** [KA-0035].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the retrieved excerpts:
> 1. A field can't be deleted while something still uses it, with the list of six reference types. Supported by KA-0035 Cause.
> 2. Known bug ENG-4502: the message sometimes closes straight away, with a fix due in 2026.11.1. Supported, and the answer keeps "due" rather than saying "fixed".
> 3. Resolution steps: Usage tab, remove each reference, delete again. Supported.
> 4. Archive field: disappears from forms, views and pickers, keeps values and references, can be restored any time. Supported.
> 5. Deleted fields can be restored with their values for 30 days under Settings > Fields > Deleted. Supported.
> "Usually means" is a mild hedge and doesn't add a product claim. Every claim is grounded.
> 
> Against the reference: the answer covers the cause, the defect and its fix version, the Usage tab steps, and archiving as an alternative. It matches fully.

### top-k 3: KA-0035#136, KA-0035#138, KA-0035#139

> This is a known issue: clicking **Delete** on a custom field in **Settings > Fields** may do nothing, or show "This field can't be deleted." [KA-0035]
> 
> To fix it:
> 1. In **Settings > Fields**, open the field and go to the **Usage** tab. It lists every reference to the field, with links. [KA-0035]
> 2. Remove or change each reference: edit the automation, report or form, or remap the integration field. [KA-0035]
> 3. Go back to the field and click **Delete** again. [KA-0035]
> 
> **Alternative:** If the field is used in many places, choose **Archive field**. It disappears from forms, views and pickers, but past values and references are kept, and you can restore it at any time. [KA-0035]

Groundedness 4, correctness 4. Unsupported: This is a known issue

> Claims in the answer, checked against the excerpts:
> - Clicking Delete in Settings > Fields may do nothing or show "This field can't be deleted." Supported by the KA-0035 Symptoms excerpt.
> - "This is a known issue." The excerpts describe the symptom in a KB article but never call it a known issue or defect. This is slightly broader framing than the text supports, though it doesn't change the substance.
> - Resolution steps: open the Usage tab, remove or change each reference, then delete again. Supported nearly verbatim.
> - Archive field alternative, including what it hides, what it keeps and that it can be restored. Supported.
> Groundedness is 4 because of the one framing slip.
> 
> Compared with the reference:
> - The answer gives the right fix: use the Usage tab, remove references, delete again, or archive the field instead.
> - It never says outright that the cause is the field still being referenced. That is only implied by the steps.
> - It omits the defect (ENG-4502) where the message listing references closes immediately, and the planned fix in 2026.11.1.
> The main action is correct, but the explanation of the cause is thin and the defect detail is missing. Correctness is 4.

## Q28. A scheduled automation rule updates 200 tasks. How many runs does that use?

### top-k 5: KA-0036#142, KA-0036#144, KA-0036#141, KA-0036#143, KA-0001#1

> It uses **200 runs**: a scheduled rule counts one run for each task it updates [KA-0036].
> 
> For comparison, a rule that triggers once counts as 1 run no matter how many actions it takes. Runs where the conditions aren't met don't count at all [KA-0036].
> 
> Each scheduled rule can process up to 5,000 items per run. You can check how many runs you've used under **Settings > Automations > Usage** [KA-0036].

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer:
> 1. A scheduled rule that updates 200 tasks uses 200 runs, one per task. Supported by KA-0036.
> 2. A rule that triggers once counts as 1 run no matter how many actions it takes. Supported by KA-0036.
> 3. Runs where the conditions aren't met don't count. Supported by KA-0036.
> 4. Each scheduled rule can process up to 5,000 items per run. Supported by KA-0036 (Other limits).
> 5. Usage can be checked under Settings > Automations > Usage. Supported by KA-0036.
> 
> The excerpt itself mixes 'run' terminology (200 runs versus 5,000 items per run). The answer repeats both statements accurately, so this is not a grounding problem.
> 
> Compared with the reference (200 runs, one per task), the answer matches exactly, and the extra statements don't contradict it.

### top-k 3: KA-0036#142, KA-0036#144, KA-0036#141

> That uses **200 runs**: a scheduled rule counts one run for each task it updates [KA-0036].
> 
> One exception: if a rule's conditions aren't met, that run doesn't count [KA-0036]. You can check your usage under **Settings > Automations > Usage** [KA-0036].

Groundedness 5, correctness 5. Unsupported: none

> Claims: 200 runs, one per task — supported. Runs where conditions aren't met don't count — supported. Usage under Settings > Automations > Usage — supported. All cited correctly. Matches reference exactly.

## Q29. My daily recurring task keeps showing up on Saturdays and Sundays.

### top-k 5: KA-0037#145, KA-0037#146, KA-0037#147, KA-0025#96, KA-0023#90

> This is expected: a **Daily** recurrence includes weekends [KA-0037].
> 
> **To skip weekends:**
> 1. Open the task, go to **Repeat**, and choose **Every weekday (Mon–Fri)** instead of **Daily** [KA-0037].
> 2. If your working week is different (for example Sunday to Thursday), an Admin sets it under **Settings > Workspace > Working days**. Then choose **Repeat > Every working day** [KA-0037].
> 3. To skip public holidays as well, add a holiday calendar under **Settings > Workspace > Holidays** and tick **Skip holidays** on the recurrence [KA-0037].
> 
> **If a task still appears on a weekend:** there was a known defect where an *Every weekday* recurrence created before a daylight saving change could produce one weekend task. It was fixed in 2026.09.3. After the fix, open each affected recurrence and **Save** it again to recalculate the schedule [KA-0037].
> 
> **To remove weekend tasks already created:** filter the project by **Created by: Recurrence** and **Due date: is weekend**, then select and delete them. Deleting one occurrence doesn't affect the rest of the series [KA-0037].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> 1. "Daily includes weekends, expected." Supported by KA-0037 (item 1).
> 2. "Repeat > Every weekday (Mon–Fri) instead of Daily." Supported (item 1).
> 3. "Admin sets Settings > Workspace > Working days, then Repeat > Every working day." Supported (item 2).
> 4. "Add a holiday calendar under Settings > Workspace > Holidays and tick Skip holidays." Supported (item 3).
> 5. "Known defect: Every weekday recurrences created before a daylight saving change could produce one weekend task; fixed in 2026.09.3; re-save each affected recurrence." Supported (item 4). The answer keeps the "fixed" status and the "could produce" hedge from the excerpt.
> 6. "Clean-up filter (Created by: Recurrence, Due date: is weekend); deleting one occurrence doesn't affect the series." Supported by the clean-up excerpt.
> 
> Every claim is supported and all citations point to KA-0037.
> 
> Against the reference: the main point (Daily includes weekends; switch to Every weekday or set working days and use Every working day) matches. The holiday, defect and clean-up details are extra, consistent with the reference and not misleading.

### top-k 3: KA-0037#145, KA-0037#146, KA-0037#147

> This is expected: a **Daily** recurrence includes weekends [KA-0037].
> 
> **To stop weekend tasks:**
> 1. Open the task, go to **Repeat**, and choose **Every weekday (Mon–Fri)** instead of **Daily** [KA-0037].
> 2. If your team works a different week (for example Sunday to Thursday), an Admin can set **Settings > Workspace > Working days**. Then choose **Repeat > Every working day** [KA-0037].
> 3. To skip public holidays too, add a holiday calendar under **Settings > Workspace > Holidays** and tick **Skip holidays** on the recurrence [KA-0037].
> 
> **If you already use "Every weekday" and still get a weekend task:** a known defect affected recurrences created before a daylight saving change. It was fixed in 2026.09.3. After updating, open each affected recurrence and **Save** it again to recalculate the schedule [KA-0037].
> 
> **To remove weekend tasks already created:** filter the project by **Created by: Recurrence** and **Due date: is weekend**, select the tasks, and delete them. Deleting one occurrence doesn't affect the rest of the series [KA-0037].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> - "Daily" includes weekends and this is expected: supported (KA-0037, item 1).
> - Choose Repeat > Every weekday (Mon–Fri) instead of Daily: supported (item 1).
> - For a different working week (e.g. Sunday to Thursday), an Admin sets Settings > Workspace > Working days, then the user chooses Repeat > Every working day: supported (item 2).
> - To skip public holidays, add a holiday calendar under Settings > Workspace > Holidays and tick Skip holidays: supported (item 3).
> - A known defect fixed in 2026.09.3 affected Every weekday recurrences created before a daylight saving change; open each affected recurrence and Save it again to recalculate: supported (item 4). The excerpt says such recurrences "could produce one task on the weekend". The answer's "still get a weekend task" fits that wording. "After updating" is a reasonable paraphrase of "after the fix".
> - Clean-up via the filters Created by: Recurrence and Due date: is weekend, and deleting one occurrence doesn't affect the rest of the series: supported (clean-up section).
> All citations point to KA-0037, which is correct.
> 
> Correctness: the reference's main point is that Daily includes weekends, so the user should switch to Every weekday or set up custom working days and use Every working day. The answer covers both. The extra items (holidays, the defect, clean-up) are accurate and don't contradict the reference.

## Q30. A user on iOS app version 2.3.2 says the app still crashes on launch. Is that the known 2.3.1 issue?

### top-k 5: KA-0040#159, KA-0040#157, KA-0040#156, KA-0040#155, KA-0040#158

> No, that isn't the known 2.3.1 issue. The known crash affects version **2.3.1** [KA-0040], and if a user still sees a crash on launch with 2.3.2 or later, that article doesn't apply [KA-0040].
> 
> **Next steps:**
> 1. Ask the user for:
>    - the app version
>    - the iOS version
>    - the crash log, found in **Settings > Privacy & Security > Analytics & Improvements > Analytics Data** (entries starting with `Lumora`) [KA-0040]
> 2. Escalate to Mobile Engineering [KA-0040].
> 
> In the meantime, the article suggests the mobile web version at `https://app.lumora.example` in Safari as a workaround for the 2.3.1 issue [KA-0040]. It doesn't say whether that works for crashes on 2.3.2.

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> 1. "Not the known 2.3.1 issue": supported. The Agent notes say the article doesn't apply to 2.3.2 or later.
> 2. "The known crash affects 2.3.1": supported by Symptoms.
> 3. "Ask for the app version, the iOS version and the crash log, with that menu path and the 'Lumora' entries": supported verbatim by the Agent notes.
> 4. "Escalate to Mobile Engineering": supported.
> 5. "The mobile web workaround is for the 2.3.1 issue, and the excerpts don't say whether it helps on 2.3.2": supported, and the answer flags the limit accurately.
> All claims are supported.
> 
> Compared with the reference: the main point matches (No, the article doesn't apply; collect the version, iOS version and crash log, then escalate). The answer omits the MOB-982 ID and doesn't say outright that 2.3.2 fixed the bug, but those are minor details. The workaround mention is properly hedged and does not mislead.

### top-k 3: KA-0040#159, KA-0040#157, KA-0040#156

> No. The known launch crash only affects version 2.3.1. If a user still sees a crash on launch with 2.3.2 or later, that article doesn't apply [KA-0040].
> 
> Instead:
> 1. Ask for the app version, the iOS version, and the crash log [KA-0040].
> 2. To find the crash log, have the user go to **Settings > Privacy & Security > Analytics & Improvements > Analytics Data** and look for entries starting with `Lumora` [KA-0040].
> 3. Escalate to Mobile Engineering [KA-0040].

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer:
> 1. "No. The known launch crash only affects version 2.3.1." Supported. The article title says the crash is in 2.3.1, the cause section ties it to the 2.3.1 migration, and the agent notes say the article doesn't apply to 2.3.2 or later.
> 2. "If a user still sees a crash on launch with 2.3.2 or later, that article doesn't apply." Supported, stated directly in the agent notes.
> 3. "Ask for the app version, the iOS version, and the crash log." Supported.
> 4. The crash log path (Settings > Privacy & Security > Analytics & Improvements > Analytics Data) and "entries starting with `Lumora`". Supported; the path and the prefix match the excerpt exactly.
> 5. "Escalate to Mobile Engineering." Supported.
> 
> Every claim is grounded and the citations are correct.
> 
> Compared with the reference: the answer gets the main point right (no, it isn't the known issue, because the article doesn't apply to 2.3.2+) and gives the same next steps: collect the version, iOS version and crash log, then escalate to Mobile Engineering. It leaves out the ticket ID MOB-982 and doesn't explicitly say "fixed in 2.3.2", but it conveys the same meaning. These are minor omissions.

## Q31. On iPad Safari in landscape, the sidebar covers the board and the toolbar is cut off. When will it be fixed, and how should I close the case?

### top-k 5: KA-0041#161, KA-0041#163, KA-0041#164, KA-0041#160, KA-0041#162

> This is a known issue with the web app on tablets in landscape, and the fix is planned for release **2026.11.2** (ticket FE-1290) [KA-0041]. It happens because screens 1024–1366 px wide get the desktop width but still use the touch layout, and the two clash [KA-0041].
> 
> **Handling the case:** Don't close it. Link it to **FE-1290** so the customer is notified when the fix ships, and set the status to **Pending Release** [KA-0041].
> 
> **Workarounds for the customer until then:**
> 1. Use the native *Lumora for iPad* app (recommended) [KA-0041].
> 2. In Safari, tap **aA > Request Desktop Website** to load the full desktop layout (touch targets are smaller) [KA-0041].
> 3. Collapse the sidebar with the **«** button. It stays collapsed for the session [KA-0041].
> 4. Use portrait orientation [KA-0041].

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer, checked against the excerpts:
> 1. It is a known issue with the web app on tablets in landscape: supported by Symptoms.
> 2. The fix is planned for release 2026.11.2, ticket FE-1290: supported by Status, and the answer keeps the word "planned".
> 3. The cause is that 1024–1366 px screens get desktop width but still use the touch layout, and the two clash: supported by Cause.
> 4. Don't close the case; link it to FE-1290 so the customer is notified, and set status to Pending Release: supported by Agent notes.
> 5. Workarounds: native iPad app (recommended), aA > Request Desktop Website with smaller touch targets, collapse the sidebar with « for the session, and portrait orientation: all supported by Workarounds.
> 
> Every claim is supported.
> 
> Compared with the reference, the answer covers all of it: open issue FE-1290, fix planned for 2026.11.2, the native app recommendation plus the other workarounds, and linking the case and setting Pending Release instead of Closed. Nothing contradicts the reference.

### top-k 3: KA-0041#161, KA-0041#163, KA-0041#164

> **There's no fix date yet.** This is a known issue with the web app in tablet browsers in landscape. The sidebar overlaps the board and the toolbar is cut off [KA-0041]. The article doesn't say when the fix will ship.
> 
> **How to handle the case:**
> - Link it to **FE-1290** so the customer is notified when the fix ships [KA-0041].
> - Set the status to **Pending Release**, not Closed [KA-0041].
> 
> **Workarounds for the customer in the meantime:**
> 1. Use the native *Lumora for iPad* app. This is the recommended option [KA-0041].
> 2. In Safari, tap **aA > Request Desktop Website** to load the full desktop layout, which has smaller touch targets [KA-0041].
> 3. Collapse the sidebar with the **«** button. It stays collapsed for the session [KA-0041].
> 4. Switch to portrait orientation [KA-0041].

Groundedness 3, correctness 3. Unsupported: There's no fix date yet.

> Claims in the answer, checked against <retrieved>:
> - "There's no fix date yet." Unsupported. The excerpts are silent on a fix date, which is not the same as there being none. The answer's own later line ("The article doesn't say when the fix will ship") is a fair coverage statement, but the bold headline asserts a product fact.
> - It is a known issue in tablet browsers in landscape, with the sidebar overlapping and the toolbar cut off. Supported by KA-0041 Symptoms.
> - Link the case to FE-1290 so the customer is notified when the fix ships. Supported by Agent notes.
> - Set the status to Pending Release, not Closed. Supported by Agent notes.
> - The four workarounds: native app (recommended), aA > Request Desktop Website with smaller touch targets, collapse the sidebar with the « button (stays collapsed for the session), and portrait orientation. All supported by Workarounds.
> 
> Groundedness: one unsupported claim, and it sits on half of the user's question (when will it be fixed). The case-handling half stands on its own and is fully supported. This lands at 3.
> 
> Correctness: the reference says the fix is planned for 2026.11.2. The answer's headline says there is no fix date, which contradicts the reference and would mislead the user. The case handling (link to FE-1290, Pending Release, not Closed) and the workarounds match the reference. The main point is partly right but an important fact is wrong, so 3.

## Q32. A Business customer bulk-edited a project by mistake 45 days ago. Can we restore it from backup?

### top-k 5: KA-0042#167, KA-0042#165, KA-0042#168, KA-0042#166, KA-0037#147

> **No, a backup restore won't work here.** Backups for Business plans are kept for 30 days [KA-0042], so no backup exists from before an edit made 45 days ago. Restore requests only cover data still within the backup window [KA-0042].
> 
> **What may still help:**
> 
> - **Revert field changes on each task:** Field changes on a task can be reverted from the task's **Activity** tab using **Revert**, with no time limit [KA-0042]. If the bulk edit changed task fields, the customer can undo it this way, one task at a time.
> - **Use the customer's own exports:** If the customer set up scheduled reports or used the bulk export API (`POST /v2/exports`), an older export may hold the earlier data [KA-0042].
> 
> The articles don't cover any other way to recover data past the 30-day backup window.

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer, checked against the excerpts:
> 1. "Business backups are kept for 30 days": supported by the Backup policy excerpt (Starter, Team, Business: 30 days).
> 2. "No backup exists from before an edit made 45 days ago": follows directly from the 30-day retention.
> 3. "Restore requests only cover data still within the backup window": supported. The restore excerpt mentions "still within the backup window", and restores can only come from backups that exist.
> 4. "Field changes on a task can be reverted from the Activity tab using Revert, with no time limit": supported by the table row "Field changes on a task | Activity tab, then Revert | Unlimited".
> 5. "One task at a time": a reasonable reading of the per-task Revert, but no excerpt states it. It is a minor inference.
> 6. Scheduled reports or the bulk export API `POST /v2/exports` may hold the earlier data: supported by the Customer-side backups excerpt. The wording is conditional ("if the customer set up"), which is fine.
> 7. The closing line saying the articles don't cover other recovery routes is a coverage statement, not a product claim.
> 
> All substantive claims are grounded. The "one task at a time" remark is a slight extrapolation that doesn't change the meaning.
> 
> Against the reference: the answer matches its main point (no, 45 days is outside the 30-day Business window) and its secondary point (Activity tab revert). It leaves out the parenthetical that Enterprise keeps 90 days, which doesn't matter here because the customer is on Business. The export suggestion doesn't contradict the reference. Correctness is fully met.

### top-k 3: KA-0042#167, KA-0042#165, KA-0042#168

> **No. A 45-day-old point in time is outside the Business plan's backup window.**
> 
> - Business backups are kept for **30 days**. Only Enterprise keeps them for 90 days [KA-0042].
> - Restores for mistaken bulk edits are only possible within that backup window [KA-0042].
> 
> The only other option is if the customer made their own backups, through scheduled reports or the bulk export API (`POST /v2/exports`). They could recover the data from those [KA-0042].

Groundedness 3, correctness 4. Unsupported: The only other option is if the customer made their own backups

> Claims in the answer:
> 1. "Business backups are kept for 30 days; only Enterprise keeps them for 90 days." This is supported by KA-0042 (Backup policy).
> 2. "A 45-day-old point is outside the Business backup window." This follows directly from the 30-day retention rule applied to the question.
> 3. "Restores for mistaken bulk edits are only possible within that backup window." This follows from KA-0042: requests cover data "still within the backup window", and retention is 30 days.
> 4. "Customers can make their own backups via scheduled reports or the bulk export API (`POST /v2/exports`)." This is supported by the Customer-side backups section.
> 5. "The only other option is if the customer made their own backups." The excerpts do not say this is the only alternative, so the exclusivity is unsupported. It is a secondary claim.
> 
> Comparison with the reference: the main point (No, because Business retention is 30 days and Enterprise keeps 90) matches. The answer misses that field changes on individual tasks can still be reverted from the Activity tab. Worse, it calls customer exports "the only other option", which mildly contradicts the reference and could steer the user away from the Activity-tab route. The main point is correct, so this is a secondary imprecision.

## Q33. Can a workspace Owner delete audit log entries, and how long does Enterprise keep them?

### top-k 5: KA-0043#170, KA-0042#165, KA-0042#167, KA-0044#174, KA-0001#1

> No. Audit log entries can't be edited or deleted by anyone, including workspace Owners [KA-0043].
> 
> Enterprise keeps audit log entries for 7 years, and they can also be streamed out [KA-0043][KA-0001]. Business keeps them for 1 year, viewable in the app [KA-0043].

Groundedness 5, correctness 5. Unsupported: none

> Claims: (1) Entries can't be edited or deleted by anyone, including Owners — KA-0043 supports this. "By anyone" is a slight generalization, but the excerpt's meaning is effectively the same. (2) Enterprise keeps entries 7 years and can stream them out — KA-0043 and KA-0001 support this. (3) Business keeps them 1 year, viewable in the app — KA-0043 supports this. Every claim is supported. The answer matches the reference on both points (no deletion; 7 years for Enterprise) and adds the Business detail, which the reference also includes.

### top-k 3: KA-0043#170, KA-0042#165, KA-0042#167

> No. Audit log entries can't be edited or deleted by anyone, including workspace Owners [KA-0043].
> 
> On Enterprise, audit log entries are kept for **7 years** and can also be streamed out [KA-0043]. For comparison, Business keeps them for 1 year, viewable in the app [KA-0043].

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the retrieved excerpts:
> 1. Audit log entries can't be edited or deleted by anyone, including Owners. Supported by KA-0043.
> 2. Enterprise keeps entries for 7 years and they can be streamed out. Supported by KA-0043.
> 3. Business keeps them for 1 year, viewable in the app. Supported by KA-0043.
> 
> Every claim is supported. Compared with the reference, the answer matches fully: Owners cannot delete entries, Enterprise keeps them 7 years, and the Business comparison (1 year) is also correct.

## Q34. Can our Enterprise workspace use our root domain example.com as its custom domain?

### top-k 5: KA-0044#175, KA-0044#174, KA-0044#176, KA-0044#177, KA-0047#186

> No. Custom domains support only subdomains, such as `work.example.com`, not apex domains like `example.com` [KA-0044].
> 
> To use a subdomain instead:
> 
> 1. Go to **Settings > Workspace > Custom domain** and enter the subdomain [KA-0044].
> 2. In your DNS, create a **CNAME** record: `work.example.com → custom.lumora.example` [KA-0044].
> 3. Click **Verify**. DNS changes can take up to 24 hours but usually take minutes [KA-0044].
> 4. Lumora handles the TLS certificate automatically. If your domain has **CAA** records, add `letsencrypt.org` [KA-0044].

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer, checked against the excerpts:
> 1. "No, only subdomains are supported, not apex domains." KA-0044 Setup step 1 says this. Supported.
> 2. The menu path Settings > Workspace > Custom domain. Supported.
> 3. A CNAME from work.example.com to custom.lumora.example. Supported.
> 4. Click Verify; DNS changes can take up to 24 hours but usually take minutes. Supported.
> 5. Lumora handles TLS automatically, and letsencrypt.org should be added if CAA records exist. Supported ("issues and renews" is paraphrased as "handles").
> 
> Every claim is grounded, so there are no unsupported claims.
> 
> Compared with the reference: the main point (No, apex domains aren't supported; use a subdomain) matches. The CNAME instruction the reference mentions is also included. Nothing contradicts the reference.

### top-k 3: KA-0044#175, KA-0044#174, KA-0044#176

> No. Custom domains support only subdomains, such as `work.example.com`, not apex (root) domains like `example.com` [KA-0044].
> 
> To use a subdomain instead:
> 1. Go to **Settings > Workspace > Custom domain** and enter the subdomain [KA-0044].
> 2. In your DNS, create a **CNAME** record pointing it to `custom.lumora.example` [KA-0044].
> 3. Click **Verify**. DNS changes usually take minutes but can take up to 24 hours [KA-0044].

Groundedness 5, correctness 5. Unsupported: none

> Every claim in the answer is backed by the retrieved excerpts. 1. "Only subdomains are supported, not apex domains like example.com" is stated directly in KA-0044 Setup. 2. The menu path Settings > Workspace > Custom domain matches the excerpt. 3. Creating a CNAME to custom.lumora.example matches. 4. Clicking Verify, with DNS changes usually taking minutes but up to 24 hours, matches. The citations are correct. Compared with the reference, the answer gets the main point right (no, only subdomains are supported) and includes the CNAME step. Nothing in it contradicts the reference.

## Q35. Is Lumora available in Italian?

### top-k 5: KA-0045#179, KA-0044#174, KA-0008#32, KA-0027#105, KA-0027#103

> Not yet. Lumora is currently available in English, Spanish, Portuguese (BR), French, German, Japanese and Dutch [KA-0045]. Italian (along with Polish) is planned for the first half of 2027 [KA-0045].
> 
> Once it's available, users can switch languages under **Profile > Preferences > Language** [KA-0045].

Groundedness 5, correctness 5. Unsupported: none

> Claims: (1) Not yet available in Italian — supported by KA-0045. (2) The current languages are English, Spanish, Portuguese (BR), French, German, Japanese and Dutch — supported. (3) Italian and Polish are planned for the first half of 2027 — supported, and the answer keeps the word "planned". (4) Users switch languages under Profile > Preferences > Language — supported. All citations are correct. Compared with the reference, the main point (not yet; planned for H1 2027) and the current language list both match. The reference adds "don't promise a date". The answer says "planned" rather than promising, so it doesn't contradict that. "Once it's available" implies it will become available, but this is consistent with "planned" and is a minor point.

### top-k 3: KA-0045#179, KA-0044#174, KA-0008#32

> **Not yet.** Italian (and Polish) are planned for the first half of 2027 [KA-0045].
> 
> The app is currently available in English, Spanish, Portuguese (BR), French, German, Japanese and Dutch. Users can choose one under **Profile > Preferences > Language** [KA-0045].

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer:
> 1. Italian is not yet available. Supported: KA-0045 lists the current languages and Italian is not among them.
> 2. Italian and Polish are planned for the first half of 2027. Supported by KA-0045, which also uses the word "planned".
> 3. The current languages are English, Spanish, Portuguese (BR), French, German, Japanese and Dutch. Supported by KA-0045.
> 4. Users choose a language under Profile > Preferences > Language. Supported by KA-0045.
> All citations point to the correct article. Every claim is supported.
> 
> Compared with the reference: the main point matches (not yet; planned for H1 2027), and the list of current languages matches. The reference also tells the agent not to promise a date. The answer keeps the "planned" wording and makes no firm promise, so nothing contradicts the reference. It omits the FR-077 request ID, which is a minor detail and not a real weakness.

## Q36. How much does the Business plan cost per user per month?

### top-k 5: KA-0001#1, KA-0036#141, KA-0036#143, KA-0018#70, KA-0001#2

> The knowledge base articles don't include pricing, so I can't say how much the Business plan costs per user per month.
> 
> They do describe what the Business plan includes. For example:
> - 1 TB of storage per workspace [KA-0001]
> - 250 MB maximum file upload on the web [KA-0001]
> - 300 API requests per minute per workspace [KA-0001]
> - 250 active automation rules and 250,000 automation runs per month [KA-0001]
> - SSO (SAML / OIDC) and 1 year of audit log retention [KA-0001]

Groundedness 5, correctness 4. Unsupported: none

> Claims: no pricing in excerpts (non-product claim, true). Business: 1 TB storage (supported), 250 MB upload (supported), 300 API rpm (supported), 250 active rules and 250,000 runs (supported), SSO yes and 1 year audit log (supported). All are supported by KA-0001. Correctness: the reference says the KB has no pricing. The answer declines and gives no figure, which matches. It doesn't suggest the pricing page or account team, a minor omission. The related facts are allowed.

### top-k 3: KA-0001#1, KA-0036#141, KA-0036#143

> The articles provided don't include Business plan pricing, so I can't say what it costs per user per month.
> 
> They do cover what the Business plan includes:
> - 1 TB storage per workspace, 250 MB max web upload, and 300 API requests per minute [KA-0001].
> - 250 active automation rules and 250,000 automation runs per month [KA-0001].
> - SSO (SAML / OIDC) and 1 year of audit log retention [KA-0001].
> - Up to 25 actions per automation rule [KA-0036].
> 
> For pricing, please check Lumora's pricing page or contact the sales or billing team.

Groundedness 5, correctness 5. Unsupported: none

> The answer says the excerpts don't include pricing. That is not a product claim, and it is accurate. Each listed Business plan fact checks out against the excerpts:
> - 1 TB storage, 250 MB max web upload and 300 API requests per minute match the Business column of KA-0001.
> - 250 active rules and 250,000 runs per month match KA-0001.
> - SSO Yes and 1 year audit log retention match KA-0001.
> - 25 actions per rule matches KA-0036.
> The closing advice to check the pricing page or contact sales or billing is generic and neutral. Every claim is supported.
> 
> The reference says the knowledge base has no prices and the answer should say so and point to the pricing page or account team. The answer does exactly this without guessing, and the related facts it adds are allowed.

## Q37. Does Lumora have a two-way sync with Microsoft Outlook calendars?

### top-k 5: KA-0032#124, KA-0032#125, KA-0030#118, KA-0032#126, KA-0027#104

> **The articles don't say whether Lumora syncs with Microsoft Outlook calendars.** They only describe the Google Calendar two-way sync.
> 
> For comparison, here is how the Google Calendar sync works:
> - Each user connects their own Google account under **Profile > Integrations > Google Calendar** [KA-0032].
> - Tasks with a due date and time, and Lumora events, are written to one chosen Google calendar (by default a new calendar called *Lumora*) [KA-0032].
> - Events from the Google calendars you tick appear in your Lumora calendar view [KA-0032].
> 
> To find out about Outlook support, you'll need to check with Lumora support or the Integrations team.

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> 1. "The articles don't say whether Lumora syncs with Outlook." This is a statement about coverage, not a product claim, so it doesn't affect groundedness.
> 2. Users connect under Profile > Integrations > Google Calendar. Supported by KA-0032.
> 3. Tasks with a due date and time, and Lumora events, are written to one chosen calendar, by default *Lumora*. Supported by KA-0032.
> 4. Events from ticked Google calendars appear in the Lumora calendar view. Supported by KA-0032.
> 5. "Check with Lumora support or the Integrations team." Generic advice, so neutral.
> 
> Every product claim is supported.
> 
> Correctness: the reference says the knowledge base doesn't cover Outlook and only Google Calendar sync is documented. The answer says exactly that. It presents the Google details as a comparison and does not suggest Outlook works the same way, so it doesn't guess.

### top-k 3: KA-0032#124, KA-0032#125, KA-0030#118

> The articles provided don't say whether Lumora has a two-way sync with Microsoft Outlook calendars. They only describe Google Calendar two-way sync:
> 
> - Each user connects their own Google account under **Profile > Integrations > Google Calendar** [KA-0032].
> - Tasks with a due date and time, and Lumora events, are written to a chosen Google calendar. Events from the Google calendars you tick appear on your Lumora calendar view [KA-0032].
> 
> For Outlook support, please check with Lumora support or look for an article on that integration.

Groundedness 5, correctness 5. Unsupported: none

> Claims: (1) The articles don't cover Outlook sync. This is a statement about coverage, not a product claim, and it is accurate. (2) Users connect their own Google account under Profile > Integrations > Google Calendar. KA-0032 supports this. (3) Tasks with a due date and time, and Lumora events, are written to a chosen Google calendar. KA-0032 supports this. (4) Events from ticked Google calendars appear on the Lumora calendar view. KA-0032 supports this. (5) The suggestion to check with support is generic advice and neutral. Every product claim is supported. On correctness, the reference says the knowledge base doesn't cover Outlook, and the answer says it can't answer without guessing. It mentions related Google facts but does not suggest Outlook works the same way, which matches the reference.

## Q38. Can we choose to keep our workspace data in an EU data center?

### top-k 5: KA-0042#165, KA-0042#167, KA-0047#186, KA-0044#174, KA-0015#60

> The provided articles don't say whether you can choose an EU data center for your workspace data. The only location detail is that Lumora stores encrypted backups in a separate region from production [KA-0042]. Please contact Lumora Support or your account manager to ask about data residency options.

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer:
> 1. The articles don't cover choosing an EU data center. This is a statement about coverage, not a product claim, and it is accurate: none of the excerpts mention data residency.
> 2. Lumora stores encrypted backups in a separate region from production [KA-0042]. Supported: KA-0042 says encrypted snapshots are taken "in a separate region from production."
> 3. Contact Support or your account manager about data residency. This is generic advice with no product facts, so it is neutral.
> 
> Every claim is supported, so groundedness is 5.
> 
> Correctness: the reference says data residency is not in the knowledge base and that regions appear only in passing, such as the separate backup region. The answer says it can't answer, does not guess, and mentions the related backup-region fact. That matches the reference, so correctness is 5.

### top-k 3: KA-0042#165, KA-0042#167, KA-0047#186

> The articles provided don't say whether you can choose to store your workspace data in an EU data center. The only location detail is that backup snapshots are kept in a separate region from production [KA-0042]. It doesn't say which regions are used or whether customers can pick one.
> 
> For a definite answer on data residency options, please check with Lumora Support or your account team.

Groundedness 5, correctness 5. Unsupported: none

> Claims: (1) The articles don't cover EU data center choice: this is a statement about the excerpts, not a product claim. (2) Backup snapshots are kept in a separate region from production: KA-0042 supports this. (3) The excerpts don't say which regions are used or whether customers can pick one: accurate. (4) Contact Support or the account team: generic, neutral. Every claim is grounded. The reference says data residency isn't covered and the answer should say so. The assistant did that without guessing and mentioned a related fact, so it matches the reference.

## Q39. Will Lumora sign a HIPAA Business Associate Agreement?

### top-k 5: KA-0043#173, KA-0007#28, KA-0002#5, KA-0006#23, KA-0004#14

> **The knowledge base doesn't say whether Lumora will sign a HIPAA Business Associate Agreement (BAA).** None of the provided articles mention HIPAA or BAAs.
> 
> The closest related information is that customers can download the following from the Trust Center at `trust.lumora.example` after signing an NDA [KA-0043]:
> - SOC 2 Type II report
> - ISO 27001 report
> - Data Processing Agreement (DPA)
> 
> A DPA isn't the same thing as a HIPAA BAA, so please escalate the BAA question to the appropriate team for a definitive answer.

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer:
> - The knowledge base doesn't cover HIPAA or BAAs. This is a statement about the excerpts' coverage, not a product claim, and it is accurate.
> - SOC 2 Type II, ISO 27001 and the DPA can be downloaded from the Trust Center at trust.lumora.example after signing an NDA. KA-0043 states this.
> - "A DPA isn't the same thing as a HIPAA BAA." This is general knowledge rather than a Lumora product fact. It is a mild extrapolation, but it makes no claim about Lumora's offerings, so it is effectively neutral.
> - "Escalate to the appropriate team." This is generic advice and states no product facts.
> 
> Comparison with the reference: the reference says the knowledge base doesn't cover this and that the answer shouldn't claim HIPAA support either way. The answer correctly declines to answer, mentions the related documents from KA-0043, and makes no claim about HIPAA support.

### top-k 3: KA-0043#173, KA-0007#28, KA-0002#5

> The provided articles don't say whether Lumora will sign a HIPAA Business Associate Agreement (BAA), so I can't confirm it either way.
> 
> The only compliance documents they mention are SOC 2 Type II and ISO 27001 reports and a DPA. Customers can download these from the Trust Center at `trust.lumora.example` after signing an NDA [KA-0043]. To get an answer about a BAA, please ask Lumora directly, for example through a support case or your account contact.

Groundedness 5, correctness 5. Unsupported: none

> Claims: (1) The articles don't say whether Lumora signs a BAA. This is a statement about coverage, so it is neutral. (2) The only compliance documents mentioned are SOC 2 Type II, ISO 27001 and the DPA. KA-0043 supports this. (3) Customers download them from the Trust Center at trust.lumora.example after signing an NDA. KA-0043 supports this. (4) Advice to ask via a support case or account contact. This is generic advice and neutral. Every claim is supported. The answer matches the reference: it declines to make any HIPAA claim and mentions the related documents.

## Q40. Does the Android app version 2.3.1 also crash on launch?

### top-k 5: KA-0040#159, KA-0040#156, KA-0040#157, KA-0040#158, KA-0040#155

> The knowledge base doesn't say whether the Android app is affected. The only article on this crash covers the **iOS** app.
> 
> What the article does say about the iOS issue:
> - It affects iOS app version 2.3.1 on iOS 17 and 18, and only for users who had offline mode turned on [KA-0040].
> - A database migration in 2.3.1 failed on devices that already had offline data stored [KA-0040].
> - The fix is to update to 2.3.2 or later [KA-0040].
> 
> For an Android crash report, I can't confirm whether this is the same issue. Collecting the app version, OS version, and crash details and escalating would be a reasonable next step, but the articles don't describe an Android-specific process.

Groundedness 5, correctness 5. Unsupported: none

> Claims checked against the excerpts:
> - "KB doesn't say whether Android is affected; the only article covers iOS." This is a coverage statement, not a product claim, and it fits the excerpts: KA-0040 is iOS-only.
> - "Affects 2.3.1 on iOS 17 and 18, only with offline mode on." Supported by the Symptoms section.
> - "A database migration failed on devices with offline data." Supported by the Cause section.
> - "Update to 2.3.2 or later." Supported by the Resolution section.
> - "Collect version, OS version and crash details and escalate." This is generic advice, and the answer explicitly says the articles don't describe an Android process. It is neutral.
> 
> Every claim is grounded.
> 
> Compared with the reference: the reference says the question isn't answered by the KB and the answer shouldn't extend the iOS issue to Android. The assistant says exactly that and adds related iOS facts, which the rubric allows. It matches the reference's main point.

### top-k 3: KA-0040#159, KA-0040#156, KA-0040#157

> The knowledge base doesn't say whether the Android app is affected; the only article on this crash covers the **iOS** app. In iOS version 2.3.1, a database migration failed on devices that already had offline data stored, so the app crashed every time it started [KA-0040]. The fix for iOS is to update to 2.3.2 or later [KA-0040].
> 
> For an Android crash, please contact support with your app version and device details so they can look into it.

Groundedness 5, correctness 5. Unsupported: none

> Claims in the answer:
> 1. The knowledge base doesn't say whether Android is affected, and the only article covers iOS. This is a statement about coverage, not a product claim. It is accurate: KA-0040 is titled iOS only.
> 2. In iOS 2.3.1, a database migration failed on devices that already had offline data, so the app crashed every time it started. Supported by the Cause section.
> 3. The iOS fix is to update to 2.3.2 or later. Supported by Resolution step 1.
> 4. The advice to contact support with app version and device details is generic and states no product facts, so it is neutral.
> 
> All claims are supported.
> 
> Compared with the reference: the reference says the knowledge base doesn't cover Android and the iOS article shouldn't be extended to it. The answer says it can't answer for Android and does not extend the iOS issue. The related iOS facts it adds are allowed.

