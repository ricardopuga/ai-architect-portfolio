# Own RAG vs Bedrock Managed Knowledge Base

Week 10 test set, 40 questions, top 5 chunks. Run date: 2026-11-05. The kb answers and every grade were written by Claude Opus 5.5 in a Claude Code chat session, not through the API: the kb answers first, blind (question and chunks only, no reference answers), following rag_answer.py's system prompt; then the grades, following prompts/rag_answer_judge_v1.md. Every answer is scored against the chunks its own arm retrieved; 4 or 5 is a pass.

| Measure | Bedrock KB Retrieve + our prompt | Bedrock agentic, managed answer |
|---|---|---|
| Right article in the chunks (35 answerable) | 35/35 (100%) | 35/35 (100%) |
| Right article ranked 1st | 35/35 (100%) | 35/35 (100%) |
| MRR | 1.00 | 1.00 |
| Key facts present in the chunks | 59/59 (100%) | 59/59 (100%) |
| Questions with every key fact in the chunks | 35/35 (100%) | 35/35 (100%) |
| Chunks per question (mean) | 5.0 | 11.1 |
| Context per question (characters, mean) | 5,263 | 11,719 |
| Retrieval latency, median (s) | 0.60 | 7.25 |
| Groundedness pass, all 40 | 40/40 (100%) | 37/40 (92%) |
| Correctness pass, all 40 | 40/40 (100%) | 39/40 (98%) |
| Groundedness pass, 35 answerable | 35/35 (100%) | 33/35 (94%) |
| Correctness pass, 35 answerable | 35/35 (100%) | 35/35 (100%) |
| Groundedness pass, 5 unanswerable | 5/5 (100%) | 4/5 (80%) |
| Correctness pass, 5 unanswerable | 5/5 (100%) | 4/5 (80%) |
| Mean groundedness / correctness | 4.97 / 4.95 | 4.60 / 4.88 |

## Per question

| # | Kind | kb | agentic |
|---|---|---|---|
| Q01 | fact | rank 1, facts 1/1, G5 C5 | rank 1, facts 1/1, G5 C5 |
| Q02 | reasoning | rank 1, facts 3/3, G5 C5 | rank 1, facts 3/3, G5 C5 |
| Q03 | paraphrase | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G5 C5 |
| Q04 | paraphrase | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G5 C5 |
| Q05 | fact | rank 1, facts 1/1, G5 C5 | rank 1, facts 1/1, G5 C5 |
| Q06 | version-date | rank 1, facts 3/3, G5 C5 | rank 1, facts 3/3, G5 C5 |
| Q07 | fact | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G4 C5 |
| Q08 | fact | rank 1, facts 1/1, G5 C5 | rank 1, facts 1/1, G3 C4 |
| Q09 | fact | rank 1, facts 1/1, G5 C5 | rank 1, facts 1/1, G5 C5 |
| Q10 | reasoning | rank 1, facts 1/1, G5 C5 | rank 1, facts 1/1, G4 C5 |
| Q11 | reasoning | rank 1, facts 1/1, G5 C5 | rank 1, facts 1/1, G5 C5 |
| Q12 | fact | rank 1, facts 3/3, G5 C5 | rank 1, facts 3/3, G5 C5 |
| Q13 | reasoning | rank 1, facts 1/1, G5 C5 | rank 1, facts 1/1, G5 C5 |
| Q14 | version-date | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G4 C5 |
| Q15 | multi-article | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G4 C5 |
| Q16 | reasoning | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G4 C5 |
| Q17 | fact | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G5 C5 |
| Q18 | fact | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G4 C5 |
| Q19 | paraphrase | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G4 C5 |
| Q20 | version-date | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G5 C5 |
| Q21 | multi-article | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G4 C5 |
| Q22 | version-date | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G5 C5 |
| Q23 | paraphrase | rank 1, facts 1/1, G5 C5 | rank 1, facts 1/1, G5 C5 |
| Q24 | paraphrase | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G5 C5 |
| Q25 | reasoning | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G5 C5 |
| Q26 | fact | rank 1, facts 1/1, G5 C4 | rank 1, facts 1/1, G5 C5 |
| Q27 | paraphrase | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G5 C5 |
| Q28 | fact | rank 1, facts 1/1, G5 C5 | rank 1, facts 1/1, G4 C5 |
| Q29 | paraphrase | rank 1, facts 1/1, G5 C5 | rank 1, facts 1/1, G5 C5 |
| Q30 | version-date | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G5 C5 |
| Q31 | version-date | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G5 C5 |
| Q32 | reasoning | rank 1, facts 1/1, G4 C5 | rank 1, facts 1/1, G3 C4 |
| Q33 | fact | rank 1, facts 2/2, G5 C5 | rank 1, facts 2/2, G4 C5 |
| Q34 | fact | rank 1, facts 1/1, G5 C5 | rank 1, facts 1/1, G5 C5 |
| Q35 | fact | rank 1, facts 1/1, G5 C5 | rank 1, facts 1/1, G5 C5 |
| Q36 | unanswerable | rank –, facts 0/0, G5 C4 | rank –, facts 0/0, G5 C5 |
| Q37 | unanswerable | rank –, facts 0/0, G5 C5 | rank –, facts 0/0, G5 C5 |
| Q38 | unanswerable | rank –, facts 0/0, G5 C5 | rank –, facts 0/0, G5 C5 |
| Q39 | unanswerable | rank –, facts 0/0, G5 C5 | rank –, facts 0/0, G5 C5 |
| Q40 | unanswerable | rank –, facts 0/0, G5 C5 | rank –, facts 0/0, G3 C2 |

## Q01. What is the first-response target for a High priority case on the Business plan?

### Bedrock KB Retrieve + our prompt: KA-0002, KA-0002, KA-0045, KA-0033, KA-0018

> On the Business plan, the first-response target for a High priority case is 4 hours [KA-0002].

Groundedness 5, correctness 5. Unsupported: none

> One claim, 4 hours for High on Business, straight from KA-0002's table. Matches the reference's main point; the Enterprise figure is a secondary detail.

### Bedrock agentic, managed answer: KA-0002, KA-0002, KA-0045, KA-0033, KA-0018, KA-0022, KA-0042, KA-0045, KA-0001, KA-0027

> The first-response target for a **High** priority case on the **Business** plan is **4 hours**.

Groundedness 5, correctness 5. Unsupported: none

> 4 hours for High on Business, from KA-0002. Matches the reference.

## Q02. A user in a workspace that requires SSO says the password reset email never arrives. Why?

### Bedrock KB Retrieve + our prompt: KA-0004, KA-0004, KA-0010, KA-0010, KA-0008

> Because the workspace enforces SSO. When SSO is required, Lumora does not send password reset emails, since the password is managed by the identity provider [KA-0004]. The user should sign in with **Continue with SSO** and reset their password through their company IdP [KA-0004].

Groundedness 5, correctness 5. Unsupported: none

> Both claims (no reset email when SSO is required because the IdP manages the password; sign in with Continue with SSO and reset through the IdP) are in KA-0004. Matches the reference.

### Bedrock agentic, managed answer: KA-0004, KA-0004, KA-0010, KA-0010, KA-0008, KA-0007, KA-0007, KA-0009, KA-0007, KA-0005

> If the workspace requires SSO, that's actually the expected behavior — Lumora does **not** send password reset emails in that case, because the password is managed by the company's identity provider (IdP), not by Lumora.
> 
> ## What to tell the user
> 
> - The password for this workspace isn't stored in Lumora, so there's no "reset" email to send once SSO is required.
> - The user should go to the sign-in page and click **Continue with SSO**, then reset or recover their password through their company's identity provider (e.g., Okta, Microsoft Entra ID, Google Workspace) instead of through Lumora.
> 
> ## If they still can't sign in
> 
> - Confirm with the user's IT team that their IdP account is active and not locked.
> - If the issue turns out *not* to be SSO-related (e.g., the workspace doesn't actually enforce SSO for this user, or they have a legacy password-based account), the other usual causes of missing reset emails are worth checking: spam/quarantine filtering of `no-reply@mail.lumora.example`, the address being on Lumora's suppression list after a bounce, a typo or plus-addressing mismatch on the account email, or hitting the rate limit of 3 reset emails per address per hour.
> - An Admin can also try sending a reset link manually from **Settings > Members > ⋯ > Send password reset** — but note this will have no effect for a genuinely SSO-enforced user, since no reset email is generated for such accounts.
> - If none of this resolves it, escalate to the Messaging team with the user's email address and the UTC time of the attempt.

Groundedness 5, correctness 5. Unsupported: none

> Main claims from KA-0004; IdP examples (Okta, Entra ID, Google Workspace) from KA-0007; the other reset-email causes, the admin reset link, the Messaging escalation are all in KA-0004. 'Confirm the IdP account is active' is generic advice. The note that an admin-sent reset has no effect under SSO follows from 'Lumora does not send reset emails'. Matches the reference.

## Q03. Someone got locked out for a whole day after only three wrong passwords. Is that a bug?

### Bedrock KB Retrieve + our prompt: KA-0005, KA-0004, KA-0005, KA-0031, KA-0004

> No, that's not a bug. It means the workspace admin has set a strict sign-in policy: 3 failed attempts and a 24-hour lockout [KA-0005]. On Business and Enterprise, admins can set failed attempts from 3 to 10 and lockout from 15 minutes to 24 hours [KA-0005]. Explain that their own admin controls this, and that the admin can unlock the account right away: **Settings > Members**, select the user, then **⋯ > Unlock account**; the user can sign in immediately [KA-0005]. Support agents can also unlock the user from the Support Console after confirming the request with a workspace Admin [KA-0005].

Groundedness 5, correctness 5. Unsupported: none

> Not a bug, strict admin policy (3 attempts, 24 hours), ranges 3–10 and 15 min–24 h on Business/Enterprise, unlock path, Support Console unlock: all in KA-0005. Matches the reference including the unlock path.

### Bedrock agentic, managed answer: KA-0005, KA-0004, KA-0005, KA-0031, KA-0004, KA-0008, KA-0006, KA-0007, KA-0006, KA-0007

> No, that's not a bug — it's expected behavior resulting from your workspace's security settings. On the Business and Enterprise plans, a workspace Owner or Admin can configure the **Failed attempts before lockout** (range: 3–10 attempts) and **Lockout duration** (range: 15 minutes–24 hours) under **Settings > Security > Sign-in policy**. In this case, the workspace admin had set a strict policy of 3 failed attempts triggering a 24-hour lockout, which is why the user got locked out after just three wrong tries for a full day.
> 
> To resolve it immediately, a workspace Admin can unlock the account right away:
> - Go to **Settings > Members**, select the user, then click **⋯ > Unlock account**. The user will be able to sign in immediately.
> - Support agents can also unlock a user from the Support Console after confirming the request with a workspace Admin.
> 
> If this strict policy is unintended, the admin can adjust the **Failed attempts before lockout** and **Lockout duration** settings to be less restrictive via the same **Sign-in policy** page. Note that the default settings are 5 failed attempts and a 15-minute lockout, so 3 attempts/24 hours reflects a deliberately stricter configuration rather than a system default or malfunction.

Groundedness 5, correctness 5. Unsupported: none

> Ranges, Settings > Security > Sign-in policy, the strict 3/24h policy, unlock path, Support Console unlock and the defaults (5 attempts, 15 minutes) are all in KA-0005. Matches the reference.

## Q04. Every 6-digit code from my authenticator app is rejected, even when I type it fast.

### Bedrock KB Retrieve + our prompt: KA-0006, KA-0006, KA-0033, KA-0027, KA-0004

> The most likely cause is the phone's clock: Lumora uses time-based codes (TOTP, 30-second window), and if the phone's clock is more than about 60 seconds off, every code fails [KA-0006]. To fix it [KA-0006]:
> 1. Turn on automatic date and time on the phone (iOS: **Settings > General > Date & Time > Set Automatically**; Android: **Settings > System > Date & time > Set time automatically**). Google Authenticator on Android also has **⋮ > Settings > Time correction for codes > Sync now**.
> 2. Delete any old *Lumora* entries in the authenticator app.
> 3. In Lumora, cancel the setup dialog and start again at **Profile > Security > Two-factor authentication**, scanning the new QR code.
> 4. Enter the code that is currently showing.

Groundedness 5, correctness 5. Unsupported: none

> Clock more than ~60 s off with TOTP 30-second window, automatic date and time paths, delete old entries, restart setup with the new QR, enter the current code: all in KA-0006. Matches the reference.

### Bedrock agentic, managed answer: KA-0006, KA-0006, KA-0033, KA-0027, KA-0004, KA-0014, KA-0033, KA-0004, KA-0018, KA-0019

> This is a classic symptom of the authenticator app's clock being out of sync — Lumora's two-factor authentication uses time-based one-time passwords (TOTP) with a 30-second window and only one window of tolerance on either side, so if your phone's clock is off by more than about 60 seconds, every code will be rejected regardless of how fast you type it.
> 
> Here's how to fix it:
> 
> 1. **Turn on automatic date/time on your phone:**
>    - iOS: **Settings > General > Date & Time > Set Automatically**
>    - Android: **Settings > System > Date & time > Set time automatically**
>    - If you use Google Authenticator on Android, also go to **⋮ > Settings > Time correction for codes > Sync now** 
> 2. **Delete any old "Lumora" entries** in your authenticator app, since each time you open the 2FA setup dialog it generates a *new* secret — a code tied to an old QR code will never work.
> 3. In Lumora, cancel the setup dialog and restart it from **Profile > Security > Two-factor authentication**, scanning the **new** QR code.
> 4. Make sure you enter the code that is **currently showing**, not one about to expire.
> 
> If you're locked out and have no backup codes, you can sign in with a backup code if you have one; otherwise a workspace Admin can reset 2FA for you from **Settings > Members > ⋯ > Reset 2FA**. Support can only reset 2FA after verifying your identity through the account recovery procedure.

Groundedness 5, correctness 5. Unsupported: none

> TOTP details, all four steps, and the lost-device advice (backup codes, Admin Reset 2FA, Support identity check) are in KA-0006. The lost-device sentence is clumsily worded but supported. Matches the reference.

## Q05. Our SAML login fails with 'Assertion expired'. What is the allowed clock skew?

### Bedrock KB Retrieve + our prompt: KA-0007, KA-0007, KA-0007, KA-0008, KA-0008

> The allowed clock skew is 3 minutes [KA-0007]. `Assertion expired` means the IdP server's clock is off, so fix NTP on the IdP [KA-0007].

Groundedness 5, correctness 5. Unsupported: none

> 3 minutes and fix NTP on the IdP are in KA-0007's error table. Matches the reference.

### Bedrock agentic, managed answer: KA-0007, KA-0007, KA-0007, KA-0008, KA-0008, KA-0006, KA-0005, KA-0043, KA-0001, KA-0004

> The "Assertion expired" error in SAML login occurs when the identity provider's (IdP) server clock is out of sync. Lumora allows a clock skew tolerance of **3 minutes**. To fix this, correct the NTP (time sync) settings on the IdP server.

Groundedness 5, correctness 5. Unsupported: none

> IdP clock off, 3 minutes, fix NTP: KA-0007. Matches the reference.

## Q06. After users log out of Okta, their open Lumora tabs keep working. Is this fixed yet?

### Bedrock KB Retrieve + our prompt: KA-0008, KA-0008, KA-0040, KA-0003, KA-0007

> Not yet. This is an open known issue, engineering ticket ENG-4471, with a fix planned for release 2026.11.1 [KA-0008]. It has two causes: if the SAML connection has no Single Logout URL, Lumora never hears about the IdP logout, and even with Single Logout the web app's offline cache isn't cleared on logout [KA-0008]. Workarounds [KA-0008]:
> - Configure Single Logout in both the IdP and Lumora (**Settings > Security > Single sign-on > Edit > Single Logout URL**), which ends the server-side session.
> - Shorten **Settings > Security > Session lifetime** (down to 1 hour).
> - On shared devices, turn on **Settings > Security > Disable offline cache**.
> - Have users also sign out with **Profile > Sign out** in Lumora.
> Link the case to ENG-4471 so the customer is notified when the fix ships [KA-0008].

Groundedness 5, correctness 5. Unsupported: none

> Open, ENG-4471, fix planned for 2026.11.1, the two causes, all four workarounds and linking the case are in KA-0008. Matches the reference fully.

### Bedrock agentic, managed answer: KA-0008, KA-0008, KA-0040, KA-0003, KA-0007, KA-0004, KA-0029, KA-0033, KA-0040, KA-0044

> This is a known, currently **open** issue (KA-0008: "Known issue: SSO logout does not fully end the Lumora session"), not yet fixed — a fix is planned for release **2026.11.1** via engineering ticket ENG-4471.
> 
> ## Why it happens
> There are two separate problems causing already-open tabs to keep working after an IdP (e.g., Okta) logout:
> - If the SAML connection has no **Single Logout URL** configured, Lumora never finds out about the Okta logout, so the session simply runs until it times out on its own (12 hours by default).
> - Even when Single Logout *is* configured so the server-side session properly ends, the web app's offline cache (service worker) isn't cleared on logout — this is the specific defect targeted for the 2026.11.1 fix.
> 
> ## Workarounds available now
> - Configure Single Logout in **both** Okta and Lumora (**Settings > Security > Single sign-on > Edit > Single Logout URL**) — this ends the server-side session.
> - Shorten **Settings > Security > Session lifetime** to as little as 1 hour.
> - On shared/kiosk devices, turn on **Settings > Security > Disable offline cache** so nothing is cached locally (users lose offline access).
> - Have users also sign out via **Profile > Sign out** inside Lumora in addition to logging out of Okta — this clears the local cache.
> 
> ## Customer messaging note
> You can tell customers that the server-side session *is* properly ended once Single Logout is configured — the remaining risk is just data cached in the browser on that device. It's worth linking their case to ENG-4471 so they're notified automatically when the fix ships.

Groundedness 5, correctness 5. Unsupported: none

> Open, ENG-4471, 2026.11.1, both causes with the 12-hour default, all four workarounds and the customer messaging are in KA-0008. Matches the reference fully.

## Q07. A user's role is Admin but every option they see is read-only. What should I check first?

### Bedrock KB Retrieve + our prompt: KA-0009, KA-0009, KA-0011, KA-0021, KA-0010

> Check their seat type first. Seat type takes priority over role: a user on a Viewer seat is read-only even if their role says Admin [KA-0009]. In **Settings > Members**, find the user; if **Seat** says *Viewer*, change it to *Full*, which needs a free paid seat [KA-0009].

Groundedness 5, correctness 5. Unsupported: none

> Seat type over role, Viewer seat read-only even as Admin, change to Full in Settings > Members (needs a free paid seat): all in KA-0009. The question asks what to check first, which is the reference's main point; the later checks are secondary.

### Bedrock agentic, managed answer: KA-0009, KA-0009, KA-0011, KA-0021, KA-0010, KA-0004, KA-0011, KA-0009, KA-0043, KA-0022

> When a user's role shows **Admin** but everything they see is read-only, work through these checks in order:
> 
> 1. **Seat type (check this first).** Seat type takes priority over role — a user on a **Viewer seat** is read-only everywhere even if their role says Admin. Go to **Settings > Members**, find the user, and if **Seat** says *Viewer*, change it to *Full* (this requires a free paid seat).
> 2. **Wrong workspace.** The user may belong to several workspaces and only be an Admin in one of them. Have them switch workspaces using the picker in the top-left corner.
> 3. **Billing lock.** If the subscription is past due, the entire workspace becomes read-only for everyone except Owners.
> 4. **Stale session.** Role changes only take effect the next time the page loads — ask the user to sign out and back in.
> 5. **SCIM group mapping (Enterprise only).** If roles are managed through the IdP via SCIM, any role change made directly in Lumora gets overwritten at the next sync. In that case, the group-to-role mapping needs to be changed in the IdP instead.
> 
> Since **seat type overrides role**, the Viewer seat check is almost always the culprit and the right place to start.

Groundedness 4, correctness 5. Unsupported: the Viewer seat check is almost always the culprit

> All five checks, in order, are in KA-0009. The closing line that the seat is 'almost always the culprit' is not stated (the article only says to check in order): wording broader than the excerpt, a minor slip. Main point and the follow-up checks match the reference.

## Q08. Invitations show 'Pending — awaiting seat' and nobody gets an email. Why?

### Bedrock KB Retrieve + our prompt: KA-0010, KA-0010, KA-0004, KA-0039, KA-0002

> Because the workspace has no seats left. When every paid seat is in use, invites wait in *Pending — awaiting seat* and no email is sent [KA-0010]. Add seats or free one up [KA-0010].

Groundedness 5, correctness 5. Unsupported: none

> No seats left, invites wait in Pending — awaiting seat with no email, add or free a seat: KA-0010. Matches the reference.

### Bedrock agentic, managed answer: KA-0010, KA-0010, KA-0004, KA-0039, KA-0002, KA-0004, KA-0011, KA-0002, KA-0039, KA-0015

> This happens because **all of the paid seats on your workspace are currently in use**. When there are no seats left, new invitations are created in a *Pending — awaiting seat* state, and Lumora deliberately does **not** send the invitation email until a seat becomes available.
> 
> ## How to fix it
> 
> - **Add more seats** to your plan, or
> - **Free up an existing seat** — for example by deactivating or removing a user who no longer needs access — which will let the pending invite(s) send automatically.
> 
> Once a seat is available, the invite moves out of "Pending — awaiting seat" and the invitation email goes out.
> 
> ## If you need access right away
> 
> If you can't wait for a seat to free up, this specific "awaiting seat" state isn't one where a direct invite link workaround applies the same way as other delivery issues (domain restrictions, spam quarantine, suppression lists) — the invite literally won't be sent until a seat exists. The fastest resolution is to add a seat or deactivate/reassign an unused one.
> 
> ## Other possible causes (if seats are *not* the issue)
> 
> If you check and seats are actually available, but invites still don't arrive, the other common causes are:
> 
> | Cause | What happens | Fix |
> |---|---|---|
> | Domain restriction | Blocks invites to other domains silently, no error shown | Add the domain in Settings > Security > Allowed email domains, or invite as Guest |
> | Spam/quarantine | Mail gateway blocks emails from `invites@mail.lumora.example` | Ask IT to allowlist `mail.lumora.example` |
> | Suppression list | A prior bounce suppressed the address | Check "Email deliverability" on the pending invite and remove the suppression |
> | SSO with JIT provisioning | No invite needed — users just sign in via SSO | No action needed |
> 
> If this is affecting **every** workspace (not just one), check the status page for an email delivery incident, and if none is listed, this should be escalated as Urgent to the Messaging team.

Groundedness 3, correctness 4. Unsupported: freeing a seat lets the pending invites send automatically / the email goes out once a seat is available; the direct invite link workaround doesn't apply to the 'awaiting seat' state

> Main cause (all paid seats in use, no email sent, add or free a seat) and the other-causes table are in KA-0010. Two secondary claims aren't in the excerpts: that invites send automatically once a seat frees up, and that the Copy invite link workaround doesn't apply here (KA-0010 gives that workaround for pending invites without such a restriction). Main point right; the workaround claim could steer an agent away from a documented option.

## Q09. What's the difference between deactivating and removing a user?

### Bedrock KB Retrieve + our prompt: KA-0011, KA-0011, KA-0031, KA-0043, KA-0031

> - **Deactivate** frees the seat and keeps everything the user created assigned to them. You can reverse it [KA-0011].
> - **Remove** frees the seat and moves their open tasks to the person you choose. You can't reverse it [KA-0011].

Groundedness 5, correctness 5. Unsupported: none

> Both definitions are quoted from KA-0011. Matches the reference.

### Bedrock agentic, managed answer: KA-0011, KA-0011, KA-0031, KA-0043, KA-0031, KA-0009, KA-0005, KA-0037, KA-0024, KA-0004

> Deactivating and removing a user both free up their seat, but they differ in what happens to the user's content and whether the action can be undone:
> 
> | Aspect | Deactivate | Remove |
> |---|---|---|
> | Seat | Freed up | Freed up |
> | User's created content (projects, tasks, etc.) | Stays assigned to them | N/A — their open tasks are moved to a person you choose |
> | Reversible? | Yes, you can reverse it | No, this action can't be reversed |
> 
> In short, **deactivating** is the safer, reversible option that keeps everything the user created assigned to them (useful if you might need to restore access later), while **removing** is permanent and requires you to reassign the user's open tasks to someone else.
> 
> Both actions can be performed individually from **Settings > Members**, in bulk by selecting multiple rows in the member list, or via CSV import using the `deactivate` or `remove` action values.

Groundedness 5, correctness 5. Unsupported: none

> Seat, content and reversibility from KA-0011; doing it in bulk or by CSV with deactivate/remove also in KA-0011. Matches the reference.

## Q10. A customer updated their card and now sees a pending charge that isn't on any invoice. Do we refund it?

### Bedrock KB Retrieve + our prompt: KA-0012, KA-0012, KA-0013, KA-0013, KA-0015

> No. A pending charge that appears when a card is added or updated, and isn't on an invoice, is most likely a card **authorization hold**; it disappears within 3–7 business days [KA-0012]. Explain that it's a hold, not a charge, so there is nothing to refund [KA-0012].

Groundedness 5, correctness 5. Unsupported: none

> Authorization hold when the card is added or updated, gone within 3–7 business days, explain it's a hold, nothing to refund: KA-0012. Matches the reference.

### Bedrock agentic, managed answer: KA-0012, KA-0012, KA-0013, KA-0013, KA-0015, KA-0033, KA-0015, KA-0014, KA-0033, KA-0042

> No refund is needed in this case. When a customer adds or updates a card, Lumora's payment processor places a temporary **authorization hold** on the card to verify it — this shows up as a small or matching "pending" charge that has no invoice because it's not an actual charge, just a hold.
> 
> Here's how to confirm and respond:
> 
> - **Check the amount and status**: compare what the customer sees on their card statement against **Invoices** and **Payments** in the Billing Console.
> - **Confirm it's a hold**: if it's a small or matching pending amount with no corresponding invoice, it's an authorization hold, not a real charge.
> - **What happens next**: these holds typically disappear on their own within **3–7 business days**.
> - **What to tell the customer**: explain that it's just a hold from the bank verifying the card, nothing has actually been charged, and there is nothing to refund.
> 
> If instead you find it's a *real* charge — for example, a second full charge tied to its own invoice (could mean a second workspace) or two identical charges against the same invoice (a true duplicate from a payment retry) — those are handled differently: a second workspace charge should be confirmed with the customer (with an option to merge/cancel), while a true duplicate charge should be refunded via **Billing Console > open the duplicate payment > Refund > Full**, reason "Duplicate". But for a standard pending authorization hold after a card update, no refund action is required since no money has actually moved.

Groundedness 4, correctness 5. Unsupported: the payment processor places the hold to verify the card / a hold from the bank verifying the card

> Authorization hold on card add/update, 3–7 business days, nothing to refund, and the other cases (second workspace, true duplicate refund steps) are in KA-0012. Attributing the hold to 'Lumora's payment processor' 'to verify the card' is a little broader than the excerpt, which only says a hold is taken when the card is added or updated. Matches the reference.

## Q11. Can I refund a $700 true duplicate charge without approval?

### Bedrock KB Retrieve + our prompt: KA-0012, KA-0012, KA-0013, KA-0015, KA-0013

> Yes. Agents can refund true duplicates without approval, whatever the amount; the rule that refunds over $500 need a Billing Lead's approval applies to other refunds [KA-0012]. To refund it [KA-0012]:
> 1. In the Billing Console, open the duplicate **payment** (not the invoice).
> 2. Click **Refund > Full**, reason *Duplicate*.
> 3. Add a case comment with the refund ID.
> The refund reaches the card in 5–10 business days, depending on the bank [KA-0012].

Groundedness 5, correctness 5. Unsupported: none

> Duplicates refundable without approval, the $500 rule for other refunds, refund steps and timing: all in KA-0012. Matches the reference, including refunding the payment not the invoice.

### Bedrock agentic, managed answer: KA-0012, KA-0012, KA-0013, KA-0015, KA-0013, KA-0015, KA-0045, KA-0033, KA-0042, KA-0026

> Yes. According to Lumora's duplicate-charge policy, agents can refund a **true duplicate** charge without needing approval, regardless of the amount. The $500-approval threshold only applies to *other* refund types (i.e., refunds that are not true duplicates) when the amount exceeds $500 — that case requires sign-off from a Billing Lead.
> 
> To process the refund:
> 1. In the **Billing Console**, open the duplicate **payment** (not the invoice).
> 2. Click **Refund > Full**, and select the reason **Duplicate**.
> 3. The refund will reach the card in 5–10 business days, depending on the bank.
> 4. Add a case comment with the refund ID.
> 
> So for your $700 true duplicate charge, you can go ahead and issue the full refund directly without approval.

Groundedness 5, correctness 5. Unsupported: none

> Same facts as KA-0012: duplicates need no approval, the $500 rule applies to other refunds, refund steps and timing. Matches the reference.

## Q12. Billing history shows two invoices with the same number, one ending -V and one ending -R1. Will we be charged twice?

### Bedrock KB Retrieve + our prompt: KA-0013, KA-0013, KA-0012, KA-0012, KA-0014

> No. The invoice ending `-V` is the voided original, and the one with the same base number ending `-R1` is its revision; only the revised invoice is charged [KA-0013]. Lumora creates a revision when billing details change after the invoice is issued, such as a new billing address, a VAT/tax ID or a PO number [KA-0013]. For a clean record, turn on **Settings > Billing > Hide voided invoices**, or use **Export statement** for a CSV with only valid invoices and credit notes [KA-0013].

Groundedness 5, correctness 5. Unsupported: none

> -V voided, -R1 revision, only the revision charged, why revisions happen, Hide voided invoices and Export statement: KA-0013. Matches the reference.

### Bedrock agentic, managed answer: KA-0013, KA-0013, KA-0012, KA-0012, KA-0014, KA-0014, KA-0015, KA-0015, KA-0043, KA-0036

> No, you won't be charged twice. This is expected behavior, not a billing error.
> 
> ## Why you see two invoices
> 
> Lumora creates a **revised invoice** whenever billing details change after an invoice is first issued — for example, a new billing address, an added VAT/tax ID, or a change to the PO number.
> 
> | Invoice | Suffix | Status | Charged? |
> |---|---|---|---|
> | Original | `-V` | **Void** | No — it's cancelled |
> | Revision | `-R1` | **Paid** or **Open** | Yes — this is the one you're billed for |
> 
> So the `-V` invoice is the voided original, and the `-R1` invoice with the same base number is its replacement. **Only the `-R1` (revised) invoice is actually charged**.
> 
> ## For your accounting records
> 
> If you'd like a cleaner record without voided invoices cluttering the list:
> 
> - Turn on **Settings > Billing > Hide voided invoices** to filter them out of the invoice list.
> - Use **Export statement** to download a CSV containing only valid invoices and credit notes.
> - If you've already sent the voided invoice to an ERP system and need it formally removed, Lumora's Billing team can issue a credit note — this requires escalating to the Billing queue.
> 
> If what you're actually seeing is two *separate* charges (rather than a void/revision pair), that's usually either a proration charge for seats added mid-cycle, or two workspaces sharing the same billing contact — let me know if that's the case and I can walk through how to distinguish those instead.

Groundedness 5, correctness 5. Unsupported: none

> -V/-R1, statuses, revision reasons, Hide voided invoices, Export statement, credit note via the Billing queue, proration and two-workspace alternatives: all in KA-0013. Matches the reference.

## Q13. A customer's payment failed 20 days ago. What can their users do in the workspace now?

### Bedrock KB Retrieve + our prompt: KA-0015, KA-0033, KA-0033, KA-0033, KA-0002

> At 20 days they're past the 14-day grace period, so the workspace is **read-only** for everyone except Owners, who can still reach billing [KA-0015]. To restore access, an Owner updates the payment method under **Settings > Billing > Payment method** and clicks **Retry payment**; access comes back within a minute of a successful charge [KA-0015]. If nothing is done, the workspace is suspended after day 60 [KA-0015].

Groundedness 5, correctness 5. Unsupported: none

> Past the 14-day grace period, read-only except Owners who can reach billing, Retry payment restores access within a minute, suspension after day 60: KA-0015. Matches the reference.

### Bedrock agentic, managed answer: KA-0015, KA-0033, KA-0033, KA-0033, KA-0002, KA-0042, KA-0015, KA-0012, KA-0042, KA-0012

> Since payment failed 20 days ago, the workspace is now past the 14-day grace period but hasn't yet hit the 60-day suspension mark, so it's in the **read-only** stage.
> 
> ## Current State of the Workspace
> 
> - The workspace is **read-only for everyone except Owners** — regular users and Admins can view data but cannot make changes.
> - **Owners** retain the ability to reach billing and can still access **Settings > Billing > Payment method** to fix the issue.
> - Data is still fully intact at this point — nothing is suspended or deleted yet. Suspension (with data retained for 90 more days before deletion) only happens after **day 60** of failed payment.
> 
> ## How to Restore Full Access
> 
> An Owner needs to:
> 1. Go to **Settings > Billing > Payment method** and update the payment method.
> 2. Click **Retry payment**.
> 
> Access is restored for all users within a minute of a successful charge.
> 
> ## If There's a Concern About Missed Warnings
> 
> If the customer says they never got any payment-failure notifications, check:
> - The **billing contacts** list — renewal and failure emails only go to Owners and designated billing contacts, not all Admins/members.
> - Email suppression status (see KA-0004).
> 
> If warranted, agents can also grant a **one-time, 7-day courtesy extension** (once per 12 months) via the Billing Console under **Subscription > Extend grace**, which would temporarily restore full access while the customer sorts out payment.

Groundedness 5, correctness 5. Unsupported: none

> Read-only except Owners, suspension after day 60 with 90 more days of data, Retry payment, billing-contacts-only emails (KA-0015 extra chunk), suppression check, 7-day courtesy extension: all in KA-0015. 'Temporarily restore full access' follows from the grace period meaning everything works. Matches the reference.

## Q14. A bulk import took storage from 60% straight to 100% and no one got the 80% or 95% warning. Is that expected?

### Bedrock KB Retrieve + our prompt: KA-0016, KA-0016, KA-0011, KA-0030, KA-0015

> Yes, it's a known gap: if storage goes from below 80% to 100% in one day, for example after a large bulk import, only the 100% message appears. A daily check that catches this is planned for 2026.11 [KA-0016]. At 100%, new uploads and new file versions are blocked, but viewing and downloading existing files keeps working [KA-0016]. To free space: empty the trash, keep fewer file versions (**Settings > Files > Version history**) and use **Usage > Storage > Largest files**; to add capacity, upgrade or buy 100 GB storage packs [KA-0016].

Groundedness 5, correctness 5. Unsupported: none

> Known gap, daily check planned for 2026.11, what's blocked at 100%, ways to free space and add capacity: KA-0016. Matches the reference.

### Bedrock agentic, managed answer: KA-0016, KA-0016, KA-0011, KA-0030, KA-0015, KA-0036, KA-0042, KA-0022, KA-0001, KA-0011

> Yes, that's a known gap in the current system — not a bug specific to your workspace. According to Lumora's storage alert documentation:
> 
> - Alerts are normally sent at **80%** (to Owners and billing contacts), **95%** (to Owners, billing contacts and Admins), and **100%** (to everyone, shown as an error when uploading).
> - However, there's a **documented known gap**: if storage usage jumps from below 80% straight to 100% in a single day — exactly the scenario you describe with a large bulk import — only the 100% message is triggered. The 80% and 95% thresholds get skipped because the checks don't catch rapid, large jumps within the same check interval.
> - A fix (a daily check designed to catch this kind of jump) is planned for release in **2026.11**.
> 
> So in short: missing the 80%/95% warnings after a big bulk import is expected behavior given the current known limitation, not a malfunction. At 100%, new uploads and new file versions are blocked, but viewing and downloading existing files continues to work normally. If you need to free up space in the meantime, you can empty the trash, limit file version history, identify large files under Usage > Storage > Largest files, or remove unneeded archived projects — or upgrade the plan / buy additional storage packs.

Groundedness 4, correctness 5. Unsupported: the 80%/95% thresholds are skipped because the checks don't catch rapid jumps within the same check interval

> Thresholds and recipients, the known gap, the 2026.11 daily check, what's blocked at 100% and the free-space steps are in KA-0016. The explanation of the mechanism ('within the same check interval') isn't stated; it's a gloss on 'a daily check that catches this is planned', so a minor broadening. Matches the reference.

## Q15. On the Business plan, what's the biggest file I can upload in the browser, and is there a way to go bigger?

### Bedrock KB Retrieve + our prompt: KA-0017, KA-0017, KA-0001, KA-0001, KA-0021

> On Business the browser (web) upload limit is 250 MB [KA-0017][KA-0001]. Support can't raise it, because it's tied to the plan, but there are options [KA-0017]:
> - **Use the API** for resumable uploads, up to 1 GB on Business (`POST /v2/files/uploads`, in 8 MB chunks).
> - **Link instead of uploading** with **Attach > From cloud storage** (Google Drive, OneDrive, Dropbox, Box); linked files don't count against storage or the size limit.
> - **Upgrade** to Enterprise (2 GB).
> - **Compress or split** the file.

Groundedness 5, correctness 5. Unsupported: none

> 250 MB web limit (KA-0017, KA-0001); API resumable upload up to 1 GB in 8 MB chunks, cloud links, Enterprise 2 GB, compress/split, Support can't raise it: KA-0017. Matches the reference.

### Bedrock agentic, managed answer: KA-0017, KA-0017, KA-0001, KA-0001, KA-0021, KA-0016, KA-0016, KA-0028, KA-0028, KA-0003

> On the **Business** plan, the maximum file size you can upload via the web (browser) or mobile app is **250 MB**.
> 
> If you need to go bigger than that, you have a few options:
> 
> - **Use the API for resumable uploads** – Business plan supports resumable uploads via the API (`POST /v2/files/uploads`, sent in 8 MB chunks) up to **1 GB**.
> - **Link instead of uploading** – Attach a file from a connected cloud drive (Google Drive, OneDrive, Dropbox, Box) using **Attach > From cloud storage**. Linked files don't count against storage or the size limit, so there's effectively no size cap this way.
> - **Compress or split the file** – e.g., zip up a folder of images to get under the limit.
> - **Upgrade to Enterprise** – which raises the web/mobile upload limit to **2 GB** and the API resumable upload limit to **5 GB**.
> 
> Note that Support cannot manually raise the upload limit — it's tied to the plan, so upgrading or using one of the workarounds above are the only ways to go bigger.

Groundedness 4, correctness 5. Unsupported: linking from cloud storage means there's effectively no size cap

> 250 MB, API resumable 1 GB in 8 MB chunks, cloud links not counting against the limit, compress/split, Enterprise 2 GB web and 5 GB API, Support can't raise it: KA-0017. 'Effectively no size cap' goes slightly beyond 'don't count against storage or the size limit'. Matches the reference.

## Q16. We're on Team and our integration sends only about 80 requests a minute, but we still get 429 errors. Why?

### Bedrock KB Retrieve + our prompt: KA-0018, KA-0030, KA-0018, KA-0030, KA-0029

> The Team limit of 100 requests per minute (burst 20) is counted per workspace and shared by every API token and installed integration in it, so other apps such as the Salesforce connector, Zapier-style tools or a BI connector use the same allowance [KA-0018]. Search endpoints (`/v2/search`) also have a separate limit of 30 per minute [KA-0018]. Check **Settings > API > Usage**, which shows requests per token and per integration for the last 7 days; usually one integration is using most of the allowance [KA-0018]. Honor `Retry-After` with exponential backoff, and use webhooks, batch endpoints and `?fields=` to cut requests [KA-0018].

Groundedness 5, correctness 5. Unsupported: none

> 100/min with burst 20 per workspace, shared by all tokens and integrations, search limit, Settings > API > Usage, best practices: KA-0018. Matches the reference.

### Bedrock agentic, managed answer: KA-0018, KA-0030, KA-0018, KA-0030, KA-0029, KA-0019, KA-0029, KA-0020, KA-0016, KA-0027

> Even though your own integration sends about 80 requests a minute—under the Team plan's 100/minute limit—the limit isn't per integration, it's **per workspace, shared by every API token and installed integration** in that workspace. So you can still hit 429 errors if other apps or tokens in the same workspace (e.g., a Salesforce connector, Zapier-style tool, or BI connector) are also making calls and pushing the combined total over the limit.
> 
> A few other things that can contribute:
> 
> - **Search endpoints** (`/v2/search`) have their own separate limit of 30 requests/minute on every plan, regardless of your overall workspace allowance.
> - The Team plan allows **100 requests/minute with a burst of 20**, so a short spike above the steady 80/min (even from your own integration) could trigger a 429 if it coincides with other traffic.
> 
> ## How to confirm and fix it
> 
> 1. Check the response headers on your calls: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `X-RateLimit-Reset` tell you the workspace's allowance and how much is left in the current window.
> 2. Go to **Settings > API > Usage** to see requests per token and per integration over the last 7 days — this usually reveals that one integration (possibly not yours) is consuming most of the shared allowance.
> 3. When you do get a 429, honor the `Retry-After` header and use exponential backoff with jitter.
> 4. Where possible, switch from polling to **webhooks**, use the batch endpoint (`POST /v2/tasks/batch`, up to 100 items), and request only the fields you need with `?fields=` to reduce the number of calls.
> 
> If after checking Usage you confirm your integration truly is the only consumer and you're still getting throttled below 100/min, that would be worth escalating as a support case, since Enterprise customers can also request a higher limit through their CSM (not available by default on Team).

Groundedness 4, correctness 5. Unsupported: a short spike above 80/min could trigger a 429 if it coincides with other traffic (reading of 'burst 20')

> Shared per-workspace limit, search limit, headers, Usage page, Retry-After, webhooks, batch, ?fields= and the Enterprise CSM note are in KA-0018. The excerpt gives a burst figure but doesn't explain it, so the spike explanation is the answer's own interpretation; minor. Matches the reference's main point.

## Q17. Our webhook endpoint was disabled after an outage. How do we get the events we missed?

### Bedrock KB Retrieve + our prompt: KA-0019, KA-0019, KA-0019, KA-0033, KA-0043

> Fix the endpoint, then click **Re-enable** and choose **Replay failed events**, which resends events from the last 72 hours [KA-0019]. (An endpoint is disabled after 24 hours of failed deliveries [KA-0019].)

Groundedness 5, correctness 5. Unsupported: none

> Re-enable, Replay failed events, 72 hours, disabled after 24 hours of failures: KA-0019. Matches the reference.

### Bedrock agentic, managed answer: KA-0019, KA-0019, KA-0019, KA-0033, KA-0043, KA-0043, KA-0033, KA-0018, KA-0002, KA-0002

> To recover events missed while your webhook endpoint was disabled, follow these steps:
> 
> 1. **Fix the underlying issue first.** Your endpoint was disabled because it returned non-2xx responses (or took longer than 10 seconds) for 5 retry attempts over a 24-hour period of exponential backoff — once that window elapsed with continued failures, Lumora disabled the endpoint.
> 2. **Re-enable the endpoint.** Go to the endpoint page and click **Re-enable**.
> 3. **Replay the missed events.** When re-enabling, choose **Replay failed events** — this resends events from the last **72 hours**.
> 
> ## Important limitation
> Only events from the **last 72 hours** can be replayed this way. If the outage caused failures further back than that, those events cannot be recovered through this replay mechanism, based on the available documentation.
> 
> ## Before re-enabling, make sure the fix addresses the root cause
> Common causes of endpoint failures worth checking:
> - Your code doesn't handle the verification `challenge` request correctly.
> - Your signature check is validating against *parsed and re-serialized* JSON instead of the **raw request body**.
> - Your handler does slow processing before responding — best practice is to respond `200` immediately and process the event asynchronously in the background.
> 
> Once you've confirmed the endpoint is fixed (e.g., via **Send test event**), click **Re-enable** and select **Replay failed events** to get the last 72 hours of missed events resent.

Groundedness 5, correctness 5. Unsupported: none

> Disable rule (non-2xx or >10 s, 5 retries over 24 hours), Re-enable, Replay failed events for 72 hours, the common endpoint failure causes and Send test event: KA-0019. The 72-hour limitation is hedged ('based on the available documentation'). Matches the reference.

## Q18. Old links to the API docs with #section anchors now return 404. What's going on?

### Bedrock KB Retrieve + our prompt: KA-0020, KA-0020, KA-0019, KA-0018, KA-0018

> The v1 documentation was retired on 2026-08-01, when the developer site moved to a new platform. Old `/docs/api/...` links should redirect, but deep links to sections (with `#anchor`) don't; this is known issue DOC-311 [KA-0020]. Workaround: replace `/docs/api/` with `/v2/reference/` in the URL, or search the developer site [KA-0020]. Report broken links by logging the page URL and the link against DOC-311 [KA-0020].

Groundedness 5, correctness 5. Unsupported: none

> v1 retired 2026-08-01, anchor links don't redirect, DOC-311, URL workaround, reporting against DOC-311: KA-0020. Keeps the 'should redirect' hedge. Matches the reference.

### Bedrock agentic, managed answer: KA-0020, KA-0020, KA-0019, KA-0018, KA-0018, KA-0030, KA-0044, KA-0030, KA-0019, KA-0005

> This is a known issue. The v1 API documentation was retired on **2026-08-01** when the developer site moved to a new platform. Most old `/docs/api/...` links redirect automatically to the new v2 docs, but **deep links to individual sections (anything with a `#anchor`)** — as well as links inside older community posts — don't redirect properly and return a 404.
> 
> This is tracked internally as known issue **DOC-311**.
> 
> **Workaround:** Replace `/docs/api/` with `/v2/reference/` in the broken URL, or just search the developer site directly to find the current page. The current locations are:
> - API reference (v2): `https://developers.lumora.example/v2/reference`
> - Guides and recipes: `https://developers.lumora.example/guides`
> - OpenAPI spec: `https://developers.lumora.example/v2/openapi.json` 
> 
> If you want to report a specific broken link, provide the page URL and the broken link so it can be logged against DOC-311 — fixes for broken links ship weekly.

Groundedness 4, correctness 5. Unsupported: most old /docs/api/ links redirect automatically

> Retirement date, anchor links and community posts not redirecting, DOC-311, the URL workaround, the current doc URLs and weekly fixes are in KA-0020. The excerpt says old links 'should redirect'; the answer drops that hedge. Matches the reference.

## Q19. Exporting a 120,000-row table to CSV downloads an empty file.

### Bedrock KB Retrieve + our prompt: KA-0021, KA-0021, KA-0028, KA-0011, KA-0028

> Exports over 50,000 rows run in the background, but older browser bookmarks still trigger the immediate download, which returns an empty file [KA-0021]. Ask the user to choose **Export > CSV (email me when ready)**; they'll get a download link valid for 7 days (maximum 1,000,000 rows per export) [KA-0021].

Groundedness 5, correctness 5. Unsupported: none

> Over 50,000 rows runs in the background, old bookmarks trigger the empty immediate download, Export > CSV (email me when ready), 7-day link, 1,000,000 max: KA-0021. Matches the reference.

### Bedrock agentic, managed answer: KA-0021, KA-0021, KA-0028, KA-0011, KA-0028, KA-0011, KA-0022, KA-0022, KA-0043, KA-0013

> This is a known behavior described in Lumora's troubleshooting guide for empty or incomplete CSV exports (KA-0021).
> 
> ## Why this happens
> 
> Your table has 120,000 rows, which is **over the 50,000-row threshold** for immediate downloads. Exports above that size are meant to run in the background, but if you triggered the export from an older bookmarked link or an outdated UI state, it can still attempt an immediate download — which returns an empty file instead.
> 
> ## How to fix it
> 
> 1. **Use the background export option.** Instead of a direct download, choose **Export > CSV (email me when ready)**. You'll receive a download link by email, valid for **7 days**. The maximum export size is **1,000,000 rows**, so your 120,000-row table is well within range.
> 2. **Double-check filters.** If the on-screen view has a temporary filter not applied to the export (or vice versa), rows can be missing. Save the view first (**Save view**) and then export from that saved view to keep the results consistent.
> 3. **Check field-level permissions.** If columns in the export are restricted by your project role, they're excluded — and if *every* selected column is restricted, the resulting file will be completely empty. Verify your project role under **Settings**.
> 4. **Check for Sensitive fields.** Any field marked *Sensitive* is stripped from exports unless you have the **Export sensitive data** permission.
> 5. **Rule out an Excel display issue.** If the file isn't actually empty but just *looks* blank when opened by double-clicking in Excel, use **Data > From Text/CSV** in Excel, or export using **CSV (Excel compatible)**, which adds a byte-order mark for proper encoding detection.
> 
> ## If it's still empty
> 
> If none of the above resolves it, escalate to Reports Engineering with the following details:
> - The report URL
> - The exact time of the export attempt
> - The browser used
> - A HAR file capturing the export request
> 
> Start with option 1 (the background/email export) since 120,000 rows exceeds the immediate-download limit — that's the most likely cause here.

Groundedness 4, correctness 5. Unsupported: an 'outdated UI state' can trigger the immediate download

> The 50,000-row cause, the email export, the other causes and the escalation details are in KA-0021. 'Outdated UI state' is added to the excerpt's 'older browser bookmarks', and 'verify your project role under Settings' adds a vague location; minor. Leads with the right cause. Matches the reference.

## Q20. A customer got a scheduled export on 2026-09-10 that contained Sensitive fields. How should I handle it?

### Bedrock KB Retrieve + our prompt: KA-0022, KA-0022, KA-0022, KA-0024, KA-0021

> Treat it as a possible data exposure and set the priority to at least **High** [KA-0022]. A scheduled export received on 2026-09-10 is before the fix (2026.09.2, released 2026-09-16), so it matches known issue ENG-4388 (affected releases 2026.08.1 to 2026.09.1, scheduled exports only) [KA-0022]. Then [KA-0022]:
> 1. Ask for the export file name, the report or schedule name and the date received. Don't ask them to attach the file.
> 2. Escalate to the **Security & Privacy** queue; they decide whether the customer must be formally notified under the DPA.
> 3. Recommend the customer delete any copies, review the schedule's recipients, and check who holds **Export sensitive data** under **Settings > Roles**.

Groundedness 5, correctness 5. Unsupported: none

> Possible data exposure at least High, date before the 2026-09-16 fix so it matches ENG-4388 with the affected releases and scope, the steps and Security & Privacy escalation: KA-0022. Matches the reference fully.

### Bedrock agentic, managed answer: KA-0022, KA-0022, KA-0022, KA-0024, KA-0021, KA-0024, KA-0043, KA-0021, KA-0002, KA-0042

> This matches the known issue **ENG-4388**, where scheduled exports kept including Sensitive fields even after the creator lost the **Export sensitive data** permission or the schedule changed owners. Since the export was received on **2026-09-10**, this falls within the affected window (2026.08.1 to 2026.09.1, fixed in 2026.09.2 released 2026-09-16), so it matches this known defect.
> 
> Here's how to handle it:
> 
> ## Treat it as a possible data exposure
> Set the case priority to at least **High**.
> 
> ## Steps to take
> - Ask the customer for the export file name, the report/schedule name, and the date it was received — but **don't** ask them to attach the file.
> - Confirm the date: since 2026-09-10 is before the 2026-09-16 fix release and the export was scheduled, this matches known issue ENG-4388.
> - **Escalate to the Security & Privacy queue** in every case — they will decide whether the customer must be formally notified under the DPA.
> - Recommend the customer:
>   - Delete any copies of the export file.
>   - Review the schedule's recipients.
>   - Check who currently holds the **Export sensitive data** permission under **Settings > Roles**.
> 
> ## Why this happened
> The underlying bug: scheduled exports created by a user with **Export sensitive data** kept including sensitive fields even after the creator lost that permission, or when the schedule was handed off to another owner. This affected **scheduled exports only** — manual and API exports were not affected.
> 
> ## Note
> If a similar report comes in dated *after* 2026-09-16 (the fix date), that would instead need escalation to Reports Engineering as a possible regression, referencing ENG-4388 — but that doesn't apply here since this case is clearly within the affected window.

Groundedness 5, correctness 5. Unsupported: none

> ENG-4388 cause, window, fix date, scope, priority, the steps, Security & Privacy escalation and the regression note: all in KA-0022. Matches the reference fully.

## Q21. Can scheduled reports be delivered straight to an Amazon S3 bucket?

### Bedrock KB Retrieve + our prompt: KA-0024, KA-0024, KA-0043, KA-0025, KA-0022

> Yes, as a beta. Cloud storage destinations (Amazon S3, Google Drive, SharePoint) are available on Business and above, in beta since 2026.10.1 [KA-0024]. An Owner turns it on under **Settings > Labs > Scheduled exports to cloud storage**; an S3 destination needs an integration connection with the bucket and an IAM role ARN, and files are named `<report>_<YYYY-MM-DD>.<ext>` [KA-0024]. If the customer asked for this as a feature request, tell them about the beta, link the case to FR-118 and close it as **Resolved – Available in beta** [KA-0024].

Groundedness 5, correctness 5. Unsupported: none

> Beta since 2026.10.1 on Business+, Owner enables under Settings > Labs, S3 bucket with IAM role ARN, file naming, FR-118 handling: KA-0024. Matches the reference fully.

### Bedrock agentic, managed answer: KA-0024, KA-0024, KA-0043, KA-0025, KA-0022, KA-0025, KA-0042, KA-0022, KA-0022, KA-0023

> Yes — scheduled reports can be delivered directly to an Amazon S3 bucket, but this is currently a **Beta** feature (available since release 2026.10.1), available on **Business and higher** plans.
> 
> ## How it works
> - Cloud storage destinations (Amazon S3, Google Drive, SharePoint) are an option alongside the generally available Email and Slack/Microsoft Teams delivery options.
> - A workspace **Owner** must enable it under **Settings > Labs > Scheduled exports to cloud storage**.
> - For S3 specifically, you'll need to set up an integration connection with an **S3 bucket and an IAM role ARN**.
> - Delivered files are named using the pattern `<report>_<YYYY-MM-DD>.<ext>`.
> - Any feedback on the beta can be submitted via the in-app **Labs feedback** form.
> 
> ## If a customer requests this as a feature
> If a customer asks for this capability, let them know it's available in beta, link their case to feature request **FR-118**, and you can close it as **Resolved – Available in beta**.
> 
> Note: this is separate from audit log streaming to S3 (used for security/compliance event streaming on Enterprise plans), which is a different, already generally available feature.

Groundedness 4, correctness 5. Unsupported: audit log streaming to S3 is 'already generally available'

> Beta status, plans, the Email/Slack GA options, Owner enablement, S3 bucket with IAM role ARN, naming, Labs feedback and FR-118 handling are in KA-0024. The closing note about audit log streaming to S3 on Enterprise is in KA-0043, but calling it 'generally available' isn't stated; minor. Matches the reference fully.

## Q22. A scheduled report set to New York time back in July runs at the wrong hour. How do we fix it?

### Bedrock KB Retrieve + our prompt: KA-0025, KA-0025, KA-0024, KA-0024, KA-0023

> This matches a known defect, fixed in 2026.08.2: schedules created before that release saved the timezone as UTC whatever was chosen, so the schedule shows the right timezone but runs in UTC [KA-0025]. **Fix:** edit the schedule, change any setting and change it back, then **Save**; saving rewrites the stored timezone [KA-0025].

Groundedness 5, correctness 5. Unsupported: none

> Pre-2026.08.2 schedules saved as UTC, shows the right timezone but runs in UTC, edit-change-back-save fix: KA-0025. Matches the reference.

### Bedrock agentic, managed answer: KA-0025, KA-0025, KA-0024, KA-0024, KA-0023, KA-0026, KA-0022, KA-0037, KA-0042, KA-0022

> This matches a known defect affecting scheduled reports created before a certain release.
> 
> ## Why this happens
> Schedules created **before release 2026.08.2** had a bug where the timezone was saved internally as **UTC**, no matter what timezone was actually selected (e.g., *America/New_York*). Since your schedule was set up back in July — before that fix shipped — it would show "New York" in its settings but actually run on UTC time, which explains why it's firing at the wrong hour.
> 
> Note that this is *not* a daylight-saving issue: schedules follow local time for their timezone, so a 09:00 New York schedule stays at 09:00 even after clocks change. The wrong-hour symptom you're seeing is specifically the pre-2026.08.2 UTC-save defect.
> 
> ## How to fix it
> 1. Open the schedule and confirm its **Timezone** field (it will likely still show *America/New_York*, but is actually running in UTC).
> 2. Edit the schedule: change any setting, then change it back.
> 3. Click **Save** — this rewrites the stored timezone correctly, after which it will run at the intended New York hour.
> 
> No need to recreate the schedule from scratch; the edit-and-resave step resolves it for any schedule created before the 2026.08.2 fix.

Groundedness 5, correctness 5. Unsupported: none

> The pre-2026.08.2 UTC defect, the DST note, and the open-check-edit-save fix are in KA-0025. Ruling out DST follows from the stated DST behaviour. Matches the reference.

## Q23. One dashboard widget still shows July revenue while the others are current.

### Bedrock KB Retrieve + our prompt: KA-0026, KA-0026, KA-0025, KA-0025, KA-0033

> The most common cause is a fixed date range: the widget's filter is set to absolute dates (for example *1 Jul – 31 Jul*) instead of a relative range [KA-0026]. Edit the widget, go to **Filters > Date**, and choose a relative option such as **This month** or **Last 30 days** [KA-0026]. If that isn't it, check whether the source report is a paused snapshot (**Last refreshed**), whether a data connector stopped syncing, refresh the widget's cache (**⋯ > Refresh**), and check **Edit widget > Source** in case it points to the wrong report [KA-0026].

Groundedness 5, correctness 5. Unsupported: none

> Fixed date range as the most common cause with the Filters > Date fix, then snapshot, connector, cache refresh and source report checks: KA-0026. Matches the reference; the 15-minute cache duration is a minor omission.

### Bedrock agentic, managed answer: KA-0026, KA-0026, KA-0025, KA-0025, KA-0033, KA-0035, KA-0029, KA-0033, KA-0045, KA-0046

> This is a known issue covered in our knowledge base article on stale dashboard widgets. Here are the likely causes, in order of how common they are, with fixes:
> 
> ## Why one widget is stuck on July data
> 
> - **Fixed date range (most common cause).** The widget's filter may be set to an absolute date range (e.g., *1 Jul – 31 Jul*) instead of a relative one. **Fix:** Edit the widget → **Filters > Date** → change it to a relative option like **This month** or **Last 30 days**.
> - **Source report is a paused snapshot.** If the widget pulls from a report using **Save as snapshot**, it will keep showing the last snapshot taken. Snapshots pause automatically if the report owner's account is deactivated. **Fix:** Open the source report and check **Last refreshed**; if it's paused, assign a new owner or switch the report to live data.
> - **Data connector stopped syncing.** If the revenue figure comes from an external billing system via a connector, the sync may have failed. **Fix:** Check **Settings > Integrations > [connector] > Sync log** for errors.
> - **Cache.** Widgets cache for up to 15 minutes. **Fix:** Click **⋯ > Refresh** on the widget — but if it's still showing July data after refreshing, caching isn't the real cause.
> - **Wrong source report after duplicating a dashboard.** If this dashboard was copied from another one, the widget may still be pointing at the *original* report instead of the new one. **Fix:** Check **Edit widget > Source** to confirm it points to the right report.
> 
> ## If none of these fix it
> 
> Escalate to Reports Engineering with the dashboard URL, the widget's name, the value you expected to see, and the value currently shown.
> 
> Would you like help walking through any of these steps, for example checking the widget's filter settings or the connector sync log?

Groundedness 5, correctness 5. Unsupported: none

> All five causes with their fixes, the 15-minute cache and the escalation details are in KA-0026. Matches the reference fully.

## Q24. The browser freezes when I filter a table with 200,000 rows.

### Bedrock KB Retrieve + our prompt: KA-0028, KA-0028, KA-0021, KA-0041, KA-0027

> Table views load up to 100,000 rows into the browser by default, and above that, filtering in the browser uses a lot of memory and CPU [KA-0028]. The main fix is to turn on server-side filtering: in the view, go to **View settings > Performance > Filter on server**, so filters run on Lumora's servers and only 500 rows are loaded at a time [KA-0028]. Also [KA-0028]:
> - Filter on indexed fields (Status, Assignee, dates, Project, or custom fields marked **Indexed**).
> - Use saved views with the filters already set.
> - Hide formula columns you don't need, and archive old rows.
> If it continues with server-side filtering on, collect a HAR file and a browser performance profile and escalate to Frontend Engineering [KA-0028].

Groundedness 5, correctness 5. Unsupported: none

> Why it happens, Filter on server path with 500-row pages, indexed fields, saved views, formula columns, archiving, escalation: KA-0028. Matches the reference's main point and key facts; the 2026.11 auto-on note is left out.

### Bedrock agentic, managed answer: KA-0028, KA-0028, KA-0021, KA-0041, KA-0027, KA-0019, KA-0027, KA-0019, KA-0029, KA-0003

> This is a known performance issue with very large tables in Lumora. With 200,000 rows you're well above the default 100,000-row browser-side load limit, so filtering/sorting becomes slow and can freeze the tab.
> 
> ## Why it happens
> By default, table views load up to 100,000 rows directly into the browser so quick filters feel instant. Beyond that, in-browser filtering consumes a lot of memory and CPU — especially if the view has formula columns — which is why a 200,000-row table struggles.
> 
> ## How to fix it
> - **Turn on server-side filtering** (the main fix): go to **View settings > Performance > Filter on server**. Filters and sorts then run on Lumora's servers, and only one page of results (500 rows) loads into the browser at a time.
> - **Filter on indexed fields.** Status, Assignee, Created date, Due date, Project, and any custom field with **Indexed** ticked (**Settings > Fields > Edit**) filter much faster. Business plans get up to 20 indexed custom fields, Enterprise up to 100.
> - **Use saved views** with filters already applied, so the full table never has to load.
> - **Hide formula columns** you don't need in that particular view.
> - **Archive old rows** — moving completed items older than 12 months to an archive table can shrink the main table significantly.
> 
> ## Good to know
> Starting with release **2026.11**, server-side filtering will turn on automatically for any table above 50,000 rows, so this should become less of an issue going forward.
> 
> If you turn on server-side filtering and the freezing continues, the next step is to collect a HAR file and a browser performance profile so it can be escalated to Frontend Engineering. Let me know if you'd like help capturing that HAR file or walking through the server-side filtering setting.

Groundedness 5, correctness 5. Unsupported: none

> Cause, Filter on server with 500-row pages, indexed fields with plan counts, saved views, formula columns, archiving, the 2026.11 auto-on note, escalation: KA-0028. Matches the reference fully.

## Q25. The Salesforce connector disconnects like clockwork every 12 hours.

### Bedrock KB Retrieve + our prompt: KA-0031, KA-0031, KA-0030, KA-0030, KA-0008

> A regular schedule points to the most common cause: the Salesforce **Refresh Token Policy**. If it's set to "Expire refresh token after X hours", the connector disconnects on that schedule [KA-0031]. In Salesforce Setup, go to **Connected Apps OAuth Usage > Lumora Workspace > Manage > Edit Policies** and set **Refresh Token Policy** to *Refresh token is valid until revoked* [KA-0031]. Then reconnect under **Settings > Integrations > Salesforce > Reconnect**, signed in as the integration user; field mappings are kept [KA-0031].

Groundedness 5, correctness 5. Unsupported: none

> Refresh Token Policy as the cause of scheduled disconnects, the Salesforce Setup path, 'valid until revoked', reconnect steps: KA-0031. Matches the reference.

### Bedrock agentic, managed answer: KA-0031, KA-0031, KA-0030, KA-0030, KA-0008, KA-0008, KA-0027, KA-0035, KA-0018, KA-0026

> A disconnect that happens on a precise, regular schedule (like every 12 hours) is the classic signature of the **Refresh Token Policy** setting in Salesforce — this is the most common cause of recurring Salesforce connector disconnects in Lumora.
> 
> ## What's happening
> 
> In Salesforce, the Connected App for Lumora Workspace has a **Refresh Token Policy**. If it's configured to "Expire refresh token after X hours" instead of "Refresh token is valid until revoked," Salesforce will force the connector to disconnect on that exact schedule — in your case, every 12 hours.
> 
> ## How to fix it
> 
> 1. In Salesforce, go to **Setup > Connected Apps OAuth Usage > Lumora Workspace > Manage > Edit Policies**.
> 2. Find **Refresh Token Policy** and change it to **"Refresh token is valid until revoked"**.
> 3. Save the change — this should stop the recurring disconnects going forward.
> 
> ## Other things to rule out if the above doesn't fully resolve it
> 
> - **Connecting user issues**: The connector runs as whichever Salesforce user authorized it. If that user's password changes or they get deactivated, the connection breaks — use a dedicated **integration user** whose password never expires.
> - **IP restrictions**: If Salesforce's **Permitted Users** setting requires pre-authorization or IP relaxation is set to enforce restrictions, you'll need to allowlist Lumora's outbound IPs (listed at `https://lumora.example/ips`) on the integration user's profile, or relax IP restrictions for the Lumora connected app.
> - **API limits**: If the org hits its daily Salesforce API limit, calls get rejected and Lumora shows this as a disconnect — check **Setup > Company Information > API Requests, Last 24 Hours**.
> - **Sandbox refresh**: Refreshing a Salesforce sandbox wipes all OAuth grants, requiring reconnection.
> - **Too many tokens**: Salesforce allows only 5 refresh tokens per user per connected app — authorizing more silently revokes the oldest one, so avoid sharing one integration user across multiple Lumora workspaces.
> 
> ## To reconnect
> 
> Go to **Settings > Integrations > Salesforce > Reconnect**, signed in as the integration user — your field mappings will be preserved.
> 
> Given the exact 12-hour regularity you're describing, I'd check the Refresh Token Policy first, as that's by far the most likely culprit for a clockwork-timed disconnect.

Groundedness 5, correctness 5. Unsupported: none

> Refresh Token Policy cause and fix path, the other five causes, reconnect steps: KA-0031. Matches the reference.

## Q26. A payment form's transaction log has no entries at all. What does that mean?

### Bedrock KB Retrieve + our prompt: KA-0033, KA-0033, KA-0033, KA-0043, KA-0043

> It means the form never reaches the payment step. Check the payment field's conditional logic [KA-0033].

Groundedness 5, correctness 4. Unsupported: none

> Form doesn't reach the payment step; check conditional logic: KA-0033. Main point right; it leaves out that failed payments are handled as Urgent, which the reference includes.

### Bedrock agentic, managed answer: KA-0033, KA-0033, KA-0033, KA-0043, KA-0043, KA-0021, KA-0034, KA-0034, KA-0042, KA-0003

> If the **Transaction log** (found at **Settings > Payments > Transaction log** on the form) has no entries at all, it means the form never reaches the payment step in the first place. In other words, the payment gateway isn't even being attempted/called — the submission flow is stopping before it gets to the payment field.
> 
> The recommended fix is to check the payment field's **conditional logic** on the form, since misconfigured conditions can prevent respondents from ever reaching the payment step.
> 
> This is different from the other logged errors (like `authentication_failed`, `webhook_signature_invalid`, `currency_not_supported`, etc.), which indicate the form *did* reach the payment step but the gateway rejected or failed the attempt. Since failed/incomplete payments mean lost revenue for the customer, this type of issue should be treated as **Urgent**.

Groundedness 5, correctness 5. Unsupported: none

> Transaction log path, never reaches the payment step, conditional logic, contrast with logged errors, Urgent because of lost revenue: KA-0033. Matches the reference fully.

## Q27. I click Delete on a custom field and nothing happens.

### Bedrock KB Retrieve + our prompt: KA-0035, KA-0035, KA-0042, KA-0042, KA-0022

> A custom field can't be deleted while anything still uses it: automation rules, report filters/columns or dashboard widgets, form questions, formula fields, integration field mappings or required-field rules [KA-0035]. It looks like nothing happens because of a known UI defect (ENG-4502): the message listing those references sometimes closes straight away; a fix is due in 2026.11.1 [KA-0035]. To fix it [KA-0035]:
> 1. In **Settings > Fields**, open the field and go to the **Usage** tab, which lists every reference.
> 2. Remove or change each reference.
> 3. Click **Delete** again.
> If it's used in many places, choose **Archive field** instead [KA-0035].

Groundedness 5, correctness 5. Unsupported: none

> What blocks deletion, ENG-4502 with the 2026.11.1 fix, Usage tab, remove references, delete again, Archive field: KA-0035. Matches the reference fully.

### Bedrock agentic, managed answer: KA-0035, KA-0035, KA-0042, KA-0042, KA-0022, KA-0028, KA-0028, KA-0034, KA-0044, KA-0044

> This is a known behavior, not a bug on Lumora's end (though there's a related UI glitch) — a custom field can't be deleted while anything is still using it. 
> 
> ## Why this happens
> 
> A field is blocked from deletion if it's referenced by any of the following:
> - Automation rule conditions or actions
> - Report filters, columns, groupings, or dashboard widgets
> - Form questions mapped to the field
> - Formula fields that refer to it
> - Integration field mappings (e.g., the Salesforce connector)
> - Required-field rules on a project 
> 
> **Note on the "nothing happens" symptom:** There's a known UI defect (ENG-4502) where the message listing these references closes immediately, making it look like clicking Delete did nothing at all. A fix is due in release 2026.11.1.
> 
> ## How to fix it
> 
> 1. Go to **Settings > Fields**, open the field, and click the **Usage** tab — it lists every place the field is referenced, with a link to each.
> 2. Remove or change each reference: edit the automation, report, or form, or remap the integration field.
> 3. Go back to the field and click **Delete** again.
> 
> ## Alternative: Archive instead of delete
> 
> If the field is used in many places and removing all references isn't practical, you can click **Archive field** instead. This hides it from forms, views, and pickers while keeping past values and references intact — and it can be restored at any time.
> 
> ## If you still delete it
> 
> Deleted custom fields (and their values) can be restored for 30 days via **Settings > Fields > Deleted**.

Groundedness 5, correctness 5. Unsupported: none

> Blocking references, ENG-4502 and 2026.11.1, Usage tab steps, Archive field, 30-day restore of deleted fields: KA-0035. Matches the reference fully.

## Q28. A scheduled automation rule updates 200 tasks. How many runs does that use?

### Bedrock KB Retrieve + our prompt: KA-0036, KA-0036, KA-0001, KA-0001, KA-0024

> 200 runs: a scheduled rule that updates 200 tasks counts as one run per task [KA-0036].

Groundedness 5, correctness 5. Unsupported: none

> 200 runs, one per task: KA-0036. Matches the reference.

### Bedrock agentic, managed answer: KA-0036, KA-0036, KA-0001, KA-0001, KA-0024, KA-0037, KA-0027, KA-0024, KA-0018, KA-0023

> A scheduled rule that updates 200 tasks counts as **200 runs** — one run per task it updates. This is because a run is counted per task affected, not per rule trigger, for scheduled rules that act on multiple items.

Groundedness 4, correctness 5. Unsupported: a run is counted per task affected, not per rule trigger, for scheduled rules

> 200 runs, one per task, is in KA-0036. The added explanation over-generalises: the article defines a run as one rule triggering once, and gives the 200-task scheduled rule as an example, not a separate counting rule. Minor. Matches the reference.

## Q29. My daily recurring task keeps showing up on Saturdays and Sundays.

### Bedrock KB Retrieve + our prompt: KA-0037, KA-0037, KA-0025, KA-0032, KA-0029

> "Daily" includes weekends, so this is expected. In the task, go to **Repeat** and choose **Every weekday (Mon–Fri)** instead of **Daily** [KA-0037]. For a different working week, an Admin sets **Settings > Workspace > Working days**, then choose **Repeat > Every working day** [KA-0037]. To remove the weekend tasks already created, filter the project by **Created by: Recurrence** and **Due date: is weekend**, select them and delete them [KA-0037].

Groundedness 5, correctness 5. Unsupported: none

> Daily includes weekends, Every weekday, working days with Every working day, cleanup filter: KA-0037. Matches the reference.

### Bedrock agentic, managed answer: KA-0037, KA-0037, KA-0025, KA-0032, KA-0029, KA-0024, KA-0025, KA-0016, KA-0042, KA-0032

> This is expected behavior if your task's recurrence is set to **"Daily"** — that setting includes weekends by design.
> 
> ## How to fix it
> 
> - **Skip weekends:** Open the task and go to **Repeat**, then choose **Every weekday (Mon–Fri)** instead of **Daily**.
> - **Non-standard work week** (e.g., Sunday–Thursday): An Admin can set this under **Settings > Workspace > Working days**, then choose **Repeat > Every working day** on the task.
> - **Also skip public holidays:** Add a holiday calendar under **Settings > Workspace > Holidays**, and tick **Skip holidays** on the recurrence.
> 
> ## A known defect to check for
> 
> If your recurrence is already set to **Every weekday** but a weekend task still slipped through, this may be related to a now-fixed defect: recurrences created *before* a daylight saving time change could generate one extra task on the weekend, because the next date was calculated in UTC. This was fixed in version **2026.09.3**. If you're on a version at or after that fix and still see this, simply **open the affected recurrence and click Save again** — this forces the schedule to recalculate correctly.
> 
> ## Cleaning up tasks already created by mistake
> 
> To remove any weekend tasks that were created in error:
> 1. Filter the project by **Created by: Recurrence** and **Due date: is weekend**.
> 2. Select the unwanted tasks and delete them.
> 
> Note that deleting these individual occurrences will not affect the rest of the recurring series.

Groundedness 5, correctness 5. Unsupported: none

> Daily includes weekends, Every weekday, working days, holidays, the 2026.09.3 DST defect with the re-save fix, and the cleanup filter: KA-0037. Matches the reference.

## Q30. A user on iOS app version 2.3.2 says the app still crashes on launch. Is that the known 2.3.1 issue?

### Bedrock KB Retrieve + our prompt: KA-0040, KA-0040, KA-0008, KA-0041, KA-0041

> No. The 2.3.1 launch crash was resolved in iOS 2.3.2, so if a user still reports a crash on launch with 2.3.2 or later, that article doesn't apply [KA-0040]. Ask for the app version, the iOS version and the crash log (**Settings > Privacy & Security > Analytics & Improvements > Analytics Data**, entries starting with `Lumora`), then escalate to Mobile Engineering [KA-0040].

Groundedness 5, correctness 5. Unsupported: none

> Resolved in 2.3.2, article doesn't apply on 2.3.2+, collect version, iOS version and crash log path, escalate to Mobile Engineering: KA-0040. Matches the reference.

### Bedrock agentic, managed answer: KA-0040, KA-0040, KA-0008, KA-0041, KA-0041, KA-0002, KA-0027, KA-0002, KA-0008, KA-0027

> No — this does not match the known issue described in KA-0040. That known issue affected **iOS version 2.3.1** only (iOS 17 and 18 devices with offline mode turned on), where a database migration failed on devices with existing offline data, causing the app to crash right after the splash screen. It was fixed in version **2.3.2**, released 2026-07-15.
> 
> Since your user is already on 2.3.2 or later, the article explicitly states this known issue does not apply to them. Per the agent notes, the next steps are to:
> 
> - Collect the exact app version and iOS version.
> - Get the crash log from **Settings > Privacy & Security > Analytics & Improvements > Analytics Data** (entries starting with "Lumora").
> - Escalate the case to Mobile Engineering as a new/different issue, since it isn't covered by the 2.3.1 fix.
> 
> If the crash is affecting all users in production with no workaround, this would likely qualify as **Urgent** priority per support guidelines.

Groundedness 5, correctness 5. Unsupported: none

> 2.3.1 scope and cause, fixed in 2.3.2 on 2026-07-15, article doesn't apply, the three agent steps: KA-0040. The Urgent note matches KA-0002's example (mobile app crashing on launch for all users). Matches the reference.

## Q31. On iPad Safari in landscape, the sidebar covers the board and the toolbar is cut off. When will it be fixed, and how should I close the case?

### Bedrock KB Retrieve + our prompt: KA-0041, KA-0041, KA-0003, KA-0040, KA-0040

> This is an open known issue, ticket FE-1290, with a fix planned for release 2026.11.2 [KA-0041]. Until then, the workarounds are [KA-0041]:
> - Use the native *Lumora for iPad* app (recommended).
> - In Safari, tap **aA > Request Desktop Website**.
> - Collapse the sidebar with the **«** button.
> - Use portrait orientation.
> Don't close the case: link it to FE-1290 so the customer is notified when the fix ships, and set the status to **Pending Release**, not Closed [KA-0041].

Groundedness 5, correctness 5. Unsupported: none

> Open, FE-1290, 2026.11.2, the four workarounds, link to FE-1290 and set Pending Release not Closed: KA-0041. Matches the reference fully.

### Bedrock agentic, managed answer: KA-0041, KA-0041, KA-0003, KA-0040, KA-0040, KA-0045, KA-0045, KA-0020, KA-0029, KA-0008

> This is a known issue (KA-0041) affecting the Lumora web app on tablets — including Safari on iPad — in **landscape** orientation: the left sidebar overlaps the board instead of pushing it across, and the top toolbar is cut off so filter/share buttons can't be reached (pinch zoom makes it worse).
> 
> ## When it will be fixed
> It's currently **Open**, tracked under ticket **FE-1290**, with a fix planned for release **2026.11.2**.
> 
> ## Workarounds to offer the customer
> - **Use the native iPad app** — *Lumora for iPad* has a proper tablet layout and is the recommended option.
> - In Safari, tap **aA > Request Desktop Website** to load the full desktop layout (touch targets will be smaller).
> - **Collapse the sidebar** with the **«** button — it stays collapsed for the session.
> - Switch to **portrait orientation**, which isn't affected.
> 
> ## How to close the case
> Do **not** close it — link the case to **FE-1290** so the customer is automatically notified when the fix ships, and set the case status to **Pending Release** rather than Closed.

Groundedness 5, correctness 5. Unsupported: none

> Symptoms, Open/FE-1290/2026.11.2, the four workarounds and the Pending Release instruction: KA-0041. Matches the reference fully.

## Q32. A Business customer bulk-edited a project by mistake 45 days ago. Can we restore it from backup?

### Bedrock KB Retrieve + our prompt: KA-0042, KA-0042, KA-0016, KA-0043, KA-0037

> Not from backup: on Business, backups are kept for 30 days, so 45 days ago is outside the backup window [KA-0042]. However, field changes on a task can be reverted with no time limit, from the task's **Activity** tab, then **Revert** [KA-0042], so the bulk edit can still be undone that way.

Groundedness 4, correctness 5. Unsupported: the bulk edit can still be undone that way (implies the whole edit, though revert is per task)

> 30-day Business backup retention so 45 days is outside the window, and Activity > Revert with no time limit, are in KA-0042. 'The bulk edit can still be undone that way' is slightly broader than the excerpt, which describes reverting field changes on a task, one task at a time. Main point and the revert route match the reference.

### Bedrock agentic, managed answer: KA-0042, KA-0042, KA-0016, KA-0043, KA-0037, KA-0045, KA-0045, KA-0001, KA-0002, KA-0011

> No — on the Business plan, backup snapshots are retained for only **30 days**, and this bulk-edit happened 45 days ago, which is outside that window. So the data is no longer recoverable from backup.
> 
> Some additional context:
> - Backups are intended for disaster recovery (restoring a whole workspace or project), not as a browsable archive, and on Business/Starter/Team plans the retention is 30 days (Enterprise gets 90 days).
> - If this had been caught within 30 days, a workspace **Owner** could have requested a restore in writing on the case, specifying the project/workspace name and the exact point in time to restore to. Restores are always done into a **new copy** of the project (never overwriting live data), with a target turnaround of 2 business days for Business (1 day for Enterprise), and no charge for Business/Enterprise customers.
> - Other self-service recovery options also only cover limited windows and likely won't help here if 45 days have passed: Trash covers deleted items for 30 days, deleted custom fields are recoverable for 30 days, and field changes on a task can be reverted from the Activity tab with no time limit — but that only works for individual field changes, not a full bulk-edit rollback.
> 
> Going forward, you might suggest the customer set up their own regular exports via scheduled reports or the bulk export API, so they have independent backups they can restore from in the future.

Groundedness 3, correctness 4. Unsupported: Activity-tab revert only works for individual field changes, not a full bulk-edit rollback, and likely won't help here

> 30-day Business retention vs 45 days, Enterprise 90 days, the restore process and the self-service windows are in KA-0042. The excerpt says field changes on a task can be reverted with no time limit; the claim that this 'likely won't help' and isn't a way to roll back the bulk edit isn't in the excerpts, and it steers the agent away from the one route that works. Main point (no backup restore) is right.

## Q33. Can a workspace Owner delete audit log entries, and how long does Enterprise keep them?

### Bedrock KB Retrieve + our prompt: KA-0043, KA-0043, KA-0042, KA-0001, KA-0042

> No. Audit log entries can't be edited or deleted, including by Owners [KA-0043]. Enterprise keeps them for 7 years, and they can also be streamed out to a SIEM [KA-0043].

Groundedness 5, correctness 5. Unsupported: none

> Entries can't be edited or deleted including by Owners, Enterprise 7 years, streaming: KA-0043. Matches the reference; Business's 1 year is a secondary omission.

### Bedrock agentic, managed answer: KA-0043, KA-0043, KA-0042, KA-0001, KA-0042, KA-0009, KA-0015, KA-0047, KA-0016, KA-0005

> No. Audit log entries **cannot be edited or deleted by anyone, including Owners**. On the **Enterprise** plan, audit log entries are retained for **7 years**, and they can also be streamed out to an external system (e.g., Splunk HEC, Datadog, Amazon S3, or a generic HTTPS endpoint) for longer-term storage. By comparison, the **Business** plan retains audit logs for only 1 year, viewable in the app.

Groundedness 4, correctness 5. Unsupported: entries can be streamed out 'for longer-term storage'

> No deletion including Owners, Enterprise 7 years, the streaming destinations and Business 1 year are in KA-0043. The purpose 'for longer-term storage' isn't stated; minor. Matches the reference fully.

## Q34. Can our Enterprise workspace use our root domain example.com as its custom domain?

### Bedrock KB Retrieve + our prompt: KA-0044, KA-0001, KA-0044, KA-0007, KA-0047

> No. Only subdomains are supported as custom domains, not apex domains like `example.com` [KA-0044]. Use a subdomain such as `work.example.com`: enter it under **Settings > Workspace > Custom domain** and create a CNAME record `work.example.com → custom.lumora.example` [KA-0044].

Groundedness 5, correctness 5. Unsupported: none

> Subdomains only, not apex domains, the custom domain setting and CNAME target: KA-0044. Matches the reference.

### Bedrock agentic, managed answer: KA-0044, KA-0001, KA-0044, KA-0007, KA-0047, KA-0010, KA-0047, KA-0001, KA-0039, KA-0010

> No — Lumora's custom domain feature only supports **subdomains**, not apex/root domains. So you cannot use `example.com` itself as your workspace's custom domain; you would need to use something like `work.example.com` instead.
> 
> Here's how it works on Enterprise:
> - Go to **Settings > Workspace > Custom domain** and enter a subdomain, e.g., `work.example.com`.
> - In your DNS, create a **CNAME** record: `work.example.com → custom.lumora.example`.
> - Click **Verify** — DNS propagation can take up to 24 hours, though it's usually much faster.
> - Lumora automatically issues and renews the TLS certificate. If your domain has **CAA** records, you'll need to add `letsencrypt.org` to them.
> - Once verified, the status shows **Active** and your old `lumora.example` address will redirect to the new custom domain.
> 
> A couple of related notes if you proceed with a subdomain:
> - If you also use SAML SSO, you'll need to update your Identity Provider's Entity ID and ACS URL to the new domain — Lumora accepts both old and new addresses for 14 days during the transition.
> - Webhook and API URLs do **not** change; the API stays on `api.lumora.example`.
> 
> Custom domains are an Enterprise-only feature — other plans use the `<subdomain>.lumora.example` format.

Groundedness 5, correctness 5. Unsupported: none

> Subdomains only, setup steps, CAA, Active redirect, SSO 14-day overlap, API URLs unchanged, Enterprise-only: KA-0044. Matches the reference.

## Q35. Is Lumora available in Italian?

### Bedrock KB Retrieve + our prompt: KA-0045, KA-0044, KA-0041, KA-0008, KA-0034

> Not yet. The app is available in English, Spanish, Portuguese (BR), French, German, Japanese and Dutch; Italian and Polish are planned for the first half of 2027 (feature request FR-077) [KA-0045]. Users choose their language under **Profile > Preferences > Language** [KA-0045].

Groundedness 5, correctness 5. Unsupported: none

> Current languages, Italian and Polish planned for H1 2027 under FR-077, language setting: KA-0045. Gives the timing the article says to tell customers, without promising more. Matches the reference.

### Bedrock agentic, managed answer: KA-0045, KA-0044, KA-0041, KA-0008, KA-0034, KA-0045, KA-0040, KA-0044, KA-0011, KA-0027

> Not yet. Lumora currently supports English, Spanish, Portuguese (BR), French, German, Japanese, and Dutch. Italian (along with Polish) is planned for addition in the first half of 2027. Once available, users will be able to select it under **Profile > Preferences > Language**.

Groundedness 5, correctness 5. Unsupported: none

> Current languages, Italian and Polish planned for H1 2027, language setting: KA-0045. Matches the reference.

## Q36. How much does the Business plan cost per user per month?

### Bedrock KB Retrieve + our prompt: KA-0001, KA-0001, KA-0036, KA-0018, KA-0002

> The articles I have don't include pricing. They list each plan's limits, such as storage, upload size, API rate and automations [KA-0001], but not what the Business plan costs per user per month.

Groundedness 5, correctness 4. Unsupported: none

> Says the articles list limits (KA-0001) but no prices; correct refusal with no figure invented. The reference also asks the answer to point to the pricing page or account team, which it doesn't.

### Bedrock agentic, managed answer: KA-0001, KA-0001, KA-0036, KA-0018, KA-0002, KA-0042, KA-0011, KA-0042, KA-0017, KA-0012, KA-0011, KA-0002, KA-0045, KA-0009, KA-0047, KA-0047, KA-0009, KA-0015

> I couldn't find a specific per-user, per-month price for the Business plan in the knowledge base I have access to. The available documentation (plan limits, support channels, automation limits, API rate limits, billing troubleshooting, etc.) covers feature/usage limits by plan but does not list pricing figures for Starter, Team, Business, or Enterprise plans.
> 
> If you need the exact Business plan price, I'd recommend checking Lumora's pricing page or the Billing Console, or let me know if you'd like me to look into a related billing topic (like proration, seat changes, or invoices) instead.

Groundedness 5, correctness 5. Unsupported: none

> Says no pricing figures are in the articles and suggests the pricing page. 'Or the Billing Console' is generic advice. Correct refusal with a pointer, as the reference asks.

## Q37. Does Lumora have a two-way sync with Microsoft Outlook calendars?

### Bedrock KB Retrieve + our prompt: KA-0032, KA-0032, KA-0030, KA-0030, KA-0027

> The articles I have don't answer this. They only describe the two-way sync with **Google Calendar** [KA-0032]; they don't mention Microsoft Outlook calendars.

Groundedness 5, correctness 5. Unsupported: none

> Says the articles only describe Google Calendar sync (KA-0032) and don't mention Outlook. Doesn't assume either way. Correct refusal.

### Bedrock agentic, managed answer: KA-0032, KA-0032, KA-0030, KA-0030, KA-0027, KA-0006, KA-0027, KA-0040, KA-0007, KA-0009, KA-0031, KA-0033, KA-0011, KA-0018, KA-0029, KA-0020

> Based on the knowledge base I have access to, I found no mention of a Microsoft Outlook calendar integration for Lumora. The only two-way calendar sync documented is with **Google Calendar**:
> 
> - Each user connects their own Google account under **Profile > Integrations > Google Calendar**.
> - **Lumora → Google:** tasks with a due date/time and Lumora events are written to a dedicated calendar (by default called *Lumora*).
> - **Google → Lumora:** events from selected Google calendars appear on the user's Lumora calendar view.
> - Changes typically sync within about 2 minutes.
> 
> There is no corresponding article or reference describing a native Outlook (Microsoft 365/Exchange) calendar sync in the support knowledge base. If you need Outlook compatibility, it's possible this isn't currently supported, or it may require a different method (e.g., subscribing to an iCal feed, if one exists) — I don't have documentation confirming either possibility. I'd recommend checking directly with Lumora support or the Integrations team to confirm whether Outlook support exists or is planned, since my search didn't surface any article on it.

Groundedness 5, correctness 5. Unsupported: none

> Google Calendar details are from KA-0032. Says Outlook isn't documented; the iCal idea is explicitly hedged as undocumented. Doesn't claim either way. Correct refusal.

## Q38. Can we choose to keep our workspace data in an EU data center?

### Bedrock KB Retrieve + our prompt: KA-0042, KA-0047, KA-0001, KA-0042, KA-0015

> The articles I have don't cover choosing where workspace data is hosted. The only related detail is that backups are stored in a separate region from production [KA-0042].

Groundedness 5, correctness 5. Unsupported: none

> Says data residency isn't covered; the only regional detail, backups in a separate region (KA-0042), is supported. Correct refusal.

### Bedrock agentic, managed answer: KA-0042, KA-0047, KA-0001, KA-0042, KA-0015, KA-0002, KA-0047, KA-0001, KA-0044, KA-0024, KA-0027, KA-0002, KA-0022, KA-0043, KA-0025, KA-0045, KA-0014, KA-0025, KA-0040, KA-0040, KA-0038, KA-0007, KA-0008, KA-0043, KA-0005, KA-0022, KA-0033, KA-0044, KA-0007

> I couldn't find any article in the Lumora knowledge base describing a feature to choose or select a specific data center region (such as the EU) for storing your workspace data. The available documentation covers backup/restore policies, plan limits, audit logs, security policies, and sharing projects across workspaces, but none of them mention customer-selectable data residency or region pinning — backups are simply described as being kept "in a separate region from production" without naming or offering a choice of locations.
> 
> Given this, I can't confirm that EU-only data residency is offered as a self-service or configurable option. If this is a compliance requirement for your organization, I'd recommend raising it directly with Lumora Support (or your Customer Success Manager if you're on Enterprise) referencing data residency/GDPR requirements — they may have an enterprise-level accommodation not documented in this help center, or can point you to the DPA and compliance documents available at the Trust Center (`trust.lumora.example`).
> 
> Would you like me to search for anything else, such as the Data Processing Agreement details or compliance certifications (SOC 2, ISO 27001)?

Groundedness 5, correctness 5. Unsupported: none

> Says no selectable data residency is documented; the separate-region backup detail (KA-0042) and Trust Center/DPA (KA-0043) are supported; the possible enterprise accommodation is hedged. Correct refusal.

## Q39. Will Lumora sign a HIPAA Business Associate Agreement?

### Bedrock KB Retrieve + our prompt: KA-0043, KA-0007, KA-0004, KA-0007, KA-0006

> The articles I have don't mention HIPAA or a Business Associate Agreement. The compliance documents they list are the SOC 2 Type II and ISO 27001 reports and the DPA, available from the Trust Center at `trust.lumora.example` after signing an NDA [KA-0043].

Groundedness 5, correctness 5. Unsupported: none

> Says HIPAA/BAA isn't mentioned; lists the SOC 2, ISO 27001 and DPA documents from KA-0043. No claim either way. Correct refusal.

### Bedrock agentic, managed answer: KA-0043, KA-0007, KA-0004, KA-0007, KA-0006, KA-0042, KA-0008, KA-0004, KA-0033, KA-0045, KA-0043, KA-0022, KA-0035, KA-0001, KA-0022, KA-0002, KA-0025, KA-0045, KA-0005, KA-0009, KA-0009

> I couldn't find any information in the knowledge base indicating that Lumora offers or signs a HIPAA Business Associate Agreement (BAA). The compliance documentation that is mentioned covers SOC 2 Type II and ISO 27001 reports, plus a Data Processing Agreement (DPA) — these are available to download from the Trust Center (`trust.lumora.example`) after signing an NDA. There is no mention of HIPAA compliance or a BAA anywhere in the available articles.
> 
> If HIPAA/BAA support is a hard requirement for your use case, I'd recommend reaching out directly to Lumora's sales or support team to confirm current compliance offerings, since this isn't something I can verify from the knowledge base alone.

Groundedness 5, correctness 5. Unsupported: none

> Says HIPAA/BAA isn't mentioned; SOC 2, ISO 27001, DPA and the Trust Center are in KA-0043. No claim either way. Correct refusal.

## Q40. Does the Android app version 2.3.1 also crash on launch?

### Bedrock KB Retrieve + our prompt: KA-0040, KA-0040, KA-0002, KA-0002, KA-0041

> The articles I have don't say. The known launch crash in version 2.3.1 is documented for the **iOS** app (iOS 17 and 18, with offline mode on, fixed in iOS 2.3.2) [KA-0040]; there is nothing about the Android app.

Groundedness 5, correctness 5. Unsupported: none

> Says the articles don't say; the 2.3.1 crash is documented for iOS (KA-0040) and nothing covers Android. Doesn't extend it to Android or deny it. Correct refusal.

### Bedrock agentic, managed answer: KA-0040, KA-0040, KA-0002, KA-0002, KA-0041, KA-0027, KA-0041, KA-0046, KA-0003, KA-0006

> No — the known launch-crash issue in version 2.3.1 was specific to **iOS**, not Android. 
> 
> According to the knowledge base article KA-0040, Lumora for **iOS** 2.3.1 crashed on launch, but only for users who had offline mode turned on; the crash was caused by a database migration that failed on devices with existing offline data. This was fixed in **iOS** 2.3.2, released 2026-07-15. There is no mention of this crash affecting the Android app, so Android 2.3.1 is not documented as having this launch-crash issue.
> 
> If a customer is reporting an actual crash on launch with the Android app, that would not be covered by this known issue, and per the agent notes for the iOS article, you'd want to collect the app version, OS version, and crash log, then escalate to Mobile Engineering.

Groundedness 3, correctness 2. Unsupported: 'No' — the 2.3.1 launch crash is 'not Android' / Android 2.3.1 doesn't crash

> The iOS facts and agent notes are from KA-0040, and the body correctly says Android 'is not documented'. But the answer opens with 'No — … specific to iOS, not Android', answering a question the articles can't answer: the excerpt is scoped to iOS and says nothing about Android. The reference says the answer should not extend the article to Android either way. An agent reading the first line would tell the customer Android is unaffected.

