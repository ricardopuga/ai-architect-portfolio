# Retrieval hit rate

35 answerable questions from rag_test_questions.csv, top 5 chunks each. A hit means a chunk from the right article is in the top 5. MRR@5 is the average of 1 / rank of the first hit (0 for a miss).

| Method | Hit@5 | Hit@1 | MRR@5 |
|---|---|---|---|
| vector | 35/35 (100%) | 33/35 (94%) | 0.97 |
| keyword (BM25) | 35/35 (100%) | 34/35 (97%) | 0.98 |
| hybrid (vector + BM25) | 35/35 (100%) | 34/35 (97%) | 0.99 |
| hybrid + rerank | 35/35 (100%) | 35/35 (100%) | 1.00 |

## Hit@5 by question kind

| Kind | Questions | vector | keyword (BM25) | hybrid (vector + BM25) | hybrid + rerank |
|---|---|---|---|---|---|
| fact | 13 | 13/13 | 13/13 | 13/13 | 13/13 |
| multi-article | 2 | 2/2 | 2/2 | 2/2 | 2/2 |
| paraphrase | 7 | 7/7 | 7/7 | 7/7 | 7/7 |
| reasoning | 7 | 7/7 | 7/7 | 7/7 | 7/7 |
| version-date | 6 | 6/6 | 6/6 | 6/6 | 6/6 |

## Misses

None.

## Rank of the first hit per question

| # | Kind | Question | Source | vector | keyword (BM25) | hybrid (vector + BM25) | hybrid + rerank |
|---|---|---|---|---|---|---|---|
| Q01 | fact | What is the first-response target for a High priority case on the Business plan? | KA-0002 | 1 | 1 | 1 | 1 |
| Q02 | reasoning | A user in a workspace that requires SSO says the password reset email never arrives. Why? | KA-0004 | 1 | 1 | 1 | 1 |
| Q03 | paraphrase | Someone got locked out for a whole day after only three wrong passwords. Is that a bug? | KA-0005 | 1 | 1 | 1 | 1 |
| Q04 | paraphrase | Every 6-digit code from my authenticator app is rejected, even when I type it fast. | KA-0006 | 1 | 1 | 1 | 1 |
| Q05 | fact | Our SAML login fails with 'Assertion expired'. What is the allowed clock skew? | KA-0007 | 1 | 1 | 1 | 1 |
| Q06 | version-date | After users log out of Okta, their open Lumora tabs keep working. Is this fixed yet? | KA-0008 | 1 | 1 | 1 | 1 |
| Q07 | fact | A user's role is Admin but every option they see is read-only. What should I check first? | KA-0009 | 1 | 1 | 1 | 1 |
| Q08 | fact | Invitations show 'Pending — awaiting seat' and nobody gets an email. Why? | KA-0010 | 1 | 1 | 1 | 1 |
| Q09 | fact | What's the difference between deactivating and removing a user? | KA-0011 | 1 | 1 | 1 | 1 |
| Q10 | reasoning | A customer updated their card and now sees a pending charge that isn't on any invoice. Do we refund it? | KA-0012 | 1 | 1 | 1 | 1 |
| Q11 | reasoning | Can I refund a $700 true duplicate charge without approval? | KA-0012 | 1 | 1 | 1 | 1 |
| Q12 | fact | Billing history shows two invoices with the same number, one ending -V and one ending -R1. Will we be charged twice? | KA-0013 | 2 | 1 | 2 | 1 |
| Q13 | reasoning | A customer's payment failed 20 days ago. What can their users do in the workspace now? | KA-0015 | 1 | 3 | 1 | 1 |
| Q14 | version-date | A bulk import took storage from 60% straight to 100% and no one got the 80% or 95% warning. Is that expected? | KA-0016 | 1 | 1 | 1 | 1 |
| Q15 | multi-article | On the Business plan, what's the biggest file I can upload in the browser, and is there a way to go bigger? | KA-0017, KA-0001 | 1 | 1 | 1 | 1 |
| Q16 | reasoning | We're on Team and our integration sends only about 80 requests a minute, but we still get 429 errors. Why? | KA-0018 | 1 | 1 | 1 | 1 |
| Q17 | fact | Our webhook endpoint was disabled after an outage. How do we get the events we missed? | KA-0019 | 1 | 1 | 1 | 1 |
| Q18 | fact | Old links to the API docs with #section anchors now return 404. What's going on? | KA-0020 | 1 | 1 | 1 | 1 |
| Q19 | paraphrase | Exporting a 120,000-row table to CSV downloads an empty file. | KA-0021 | 1 | 1 | 1 | 1 |
| Q20 | version-date | A customer got a scheduled export on 2026-09-10 that contained Sensitive fields. How should I handle it? | KA-0022 | 1 | 1 | 1 | 1 |
| Q21 | multi-article | Can scheduled reports be delivered straight to an Amazon S3 bucket? | KA-0024, KA-0045 | 1 | 1 | 1 | 1 |
| Q22 | version-date | A scheduled report set to New York time back in July runs at the wrong hour. How do we fix it? | KA-0025, KA-0024 | 1 | 1 | 1 | 1 |
| Q23 | paraphrase | One dashboard widget still shows July revenue while the others are current. | KA-0026 | 1 | 1 | 1 | 1 |
| Q24 | paraphrase | The browser freezes when I filter a table with 200,000 rows. | KA-0028 | 1 | 1 | 1 | 1 |
| Q25 | reasoning | The Salesforce connector disconnects like clockwork every 12 hours. | KA-0031 | 1 | 1 | 1 | 1 |
| Q26 | fact | A payment form's transaction log has no entries at all. What does that mean? | KA-0033 | 1 | 1 | 1 | 1 |
| Q27 | paraphrase | I click Delete on a custom field and nothing happens. | KA-0035 | 1 | 1 | 1 | 1 |
| Q28 | fact | A scheduled automation rule updates 200 tasks. How many runs does that use? | KA-0036 | 1 | 1 | 1 | 1 |
| Q29 | paraphrase | My daily recurring task keeps showing up on Saturdays and Sundays. | KA-0037 | 1 | 1 | 1 | 1 |
| Q30 | version-date | A user on iOS app version 2.3.2 says the app still crashes on launch. Is that the known 2.3.1 issue? | KA-0040 | 1 | 1 | 1 | 1 |
| Q31 | version-date | On iPad Safari in landscape, the sidebar covers the board and the toolbar is cut off. When will it be fixed, and how should I close the case? | KA-0041 | 1 | 1 | 1 | 1 |
| Q32 | reasoning | A Business customer bulk-edited a project by mistake 45 days ago. Can we restore it from backup? | KA-0042 | 1 | 1 | 1 | 1 |
| Q33 | fact | Can a workspace Owner delete audit log entries, and how long does Enterprise keep them? | KA-0043 | 1 | 1 | 1 | 1 |
| Q34 | fact | Can our Enterprise workspace use our root domain example.com as its custom domain? | KA-0044 | 1 | 1 | 1 | 1 |
| Q35 | fact | Is Lumora available in Italian? | KA-0045 | 3 | 1 | 1 | 1 |
