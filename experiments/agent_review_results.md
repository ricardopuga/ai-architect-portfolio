# Support agent review

Model: claude-opus-5-5, max 5 steps per question. Script: [agent_review.py](agent_review.py). Run on 2026-11-03.

**10/10 runs finished, and the agent behaved correctly in all 10.** In one run (reply with feedback) the agent didn't take the path the test was built for, so revise-and-resubmit is still untested.

## What the test does

The agent answers 10 questions against the real Salesforce Cases and knowledge base. Each question checks a different way the agent could fail:

- a Case the knowledge base covers, one it covers only partly, and one it doesn't cover
- a Case outside the product, and a Case that doesn't exist
- questions with no Case, including one with different wording from the article
- two Cases in one question, to put pressure on the step limit
- two requests that write to Salesforce

Approvals for `update_case` come from a script, not a person. When the script has no decisions left, it rejects. `add_case_comment` is replaced with a dry run, so the approval path runs in full and nothing is written to Salesforce. Every model call and tool call is logged to `CaseHandlerSF/logs/agent_review.jsonl`.

## Results

| # | Test | Question | Steps | Tools | Result |
|---|---|---|---|---|---|
| 1 | kb_covered | Is there a knowledge article that solves case 00001030? | 3 | get_case, search_knowledge | ✅ Correct match |
| 2 | kb_partial | Can we resolve case 00001029 from the knowledge base? | 4 | get_case, search_knowledge ×2 | ✅ Didn't overclaim |
| 3 | kb_missing | Can we answer case 00001028 from the knowledge base? | 4 | get_case, search_knowledge ×2 | ✅ Said what the KB is missing |
| 4 | out_of_domain | What should we tell the customer on case 00001018? | 3 | get_case, search_knowledge | ✅ Correct, and caught a data problem |
| 5 | no_such_case | Summarize case 00009999 for me. | 2 | get_case (error) | ✅ Didn't make anything up |
| 6 | kb_only | How should a customer handle HTTP 429 errors from the API? | 2 | search_knowledge | ✅ Correct |
| 7 | paraphrase | Teammates' edits show up half a minute late. What's the fix? | 2 | search_knowledge | ✅ Matched despite the different wording |
| 8 | two_cases | Compare cases 00001029 and 00001030 | 4 | get_case ×2, search_knowledge ×3 | ✅ Correct, within the step limit |
| 9 | reply_with_feedback | Draft a reply to case 00001030 and send it to the customer. | 4 | get_case, draft_reply, update_case (rejected), search_knowledge | ⚠️ Agent was right, but the test path didn't run |
| 10 | internal_note | Add an internal note to case 00001030 saying we sent the allowlisting steps. | 3 | get_case, update_case (approved, dry run) | ✅ Reported the dry run correctly |

Totals: 78,546 input tokens, 6,994 output tokens, 111 s.

## Notes by case

**1. kb_covered.** The case is about password reset emails not reaching the customer's domain, probably because of a spam filter. The agent found **KA-0004 "Password reset email not received"** and cited it. The article's first listed cause is spam or quarantine filtering.

**2. kb_partial.** The September invoice for case 00001029 lists the fuel surcharge twice. The agent searched twice, and both searches returned only KA-0012 ("Charged twice for a subscription"), which is close but about a different problem. The agent answered "No, not fully" and listed what to check before replying.

**3. kb_missing.** The customer wants 15 more licenses. Searches returned KA-0009 (roles and permissions) and KA-0012, and neither explains how to buy seats. The agent answered "Only partly" and said which article was missing.

**4. out_of_domain.** The case is "Cannot start generator after electrical failure". It has no description, and its closed date (2025-07-31) is before its created date (2026-09-20). The agent said nothing in the knowledge base applies, noticed that the product is software, pointed out the bad dates, and suggested treating the case as misrouted or as test data.

**5. no_such_case.** `get_case` returned `case 00009999 not found`. The agent said so and asked for the correct number or the Case record Id.

**6. kb_only.** The agent found **KA-0018** with one search and explained the 429 response, the `Retry-After` header and how to back off.

**7. paraphrase.** The question never says "real-time collaboration" or "WebSocket". The agent still found **KA-0029** and diagnosed blocked WebSockets: the app falls back to polling every 30 seconds.

**8. two_cases.** The agent looked up both Cases in parallel, ran both searches in parallel, then ran one follow-up search. It concluded that 00001030 is much better covered than 00001029. It used 4 of the 5 steps.

**9. reply_with_feedback.** The agent drafted a reply and submitted it as a published comment. The script rejected it with the feedback "Also tell them to check the suppression list". The agent searched the knowledge base again and then declined to make the change. KA-0004 says the suppression list is checked in the internal Support Console, so the customer can't check it, and the draft already offers to check it for them. The agent gave two other wordings and stopped to ask. The second scripted decision (approve) was never used, so **the revise-and-resubmit path is still untested**.

**10. internal_note.** The agent wrote a private note and the script approved it. The dry run returned `DRY-RUN-NOT-WRITTEN`, and the agent correctly said that nothing was saved in Salesforce.

## Follow-ups

1. **Test 9:** change the rejection feedback to something the agent can accept without arguing (for example "Make it shorter"), so the test reaches revise and resubmit.
2. **Logging:** a rejection is logged with `is_error=True` (`agent.py`), so it looks like a tool failure in the run summary. Log rejections separately.
3. **Closed cases:** the agent submitted a published reply on a closed case (test 9) and relied on the approval step to stop it. Consider having it check the Case status first or warn before drafting.
4. **Data:** case 00001018 has a closed date before its created date and no description. It should be fixed or removed in Salesforce.
