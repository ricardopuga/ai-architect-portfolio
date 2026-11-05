# Own RAG vs Amazon Bedrock Managed Knowledge Base

I rebuilt the Lumora support assistant on Amazon Bedrock's managed option, a Managed Knowledge Base (KB), and compared it with my own build test set (`rag_test_questions.csv`): 40 questions, 5 of which the articles can't answer. Run date: 2026-11-05. How to set up the KB: `BEDROCK_KB_SETUP.md`.

## The three arms

Every arm answers the same 40 questions. They differ in **who searches the articles** and **who writes the answer**.

### 1. My own build

- **Search:** my code finds the 5 best pieces of the articles. It looks them up in my Postgres database by meaning and by keywords, and a small model picks the best 5.
- **Answer:** Claude writes the answer, with my prompt: "use only these articles, cite each fact".
- **Code that runs:** `hybrid_search.py` for the search, `rag_answer.py` for the answer.
- **In this comparison:** the numbers are my saved week 10 results (`topk_results.md`, produced by `topk_test.py`).

### 2. Bedrock search + my prompt

- **Search:** AWS finds the 5 best pieces from its own copy of the articles. I gave it the files with no settings.
- **Answer:** Claude with my prompt, exactly as in arm 1.
- **Code that runs:** `bedrock_kb_eval.py` asks AWS for the 5 pieces (`Bedrock.retrieve`). The answer step is the same `rag_answer.py` code as arm 1. My own search code isn't used.
- **Why:** only the search changes from arm 1, so any difference in the scores comes from AWS's search. It's like testing two engines in the same car with the same driver.

### 3. Bedrock does everything (agentic)

- **Search:** AWS searches, and can search again if it thinks something is missing.
- **Answer:** AWS's own model writes it. My prompt and Claude aren't used.
- **Code that runs:** `bedrock_kb_eval.py` sends the question to AWS and reads back the answer (`Bedrock.agentic`). Nothing of mine is in the loop.
- **Why:** it shows what you get from the fully managed product with no work at all.

### How the answers were scored

Each answer gets two scores from 1 to 5, using the week 10 judge rules (`prompts/rag_answer_judge_v1.md`):
- **Groundedness:** is every claim backed by the pieces of the articles that arm found?
- **Correctness:** does it match the expected answer?

A 4 or 5 is a pass.

To avoid paying for the Anthropic API, I (Claude, in a chat session) did the Claude steps for the two Bedrock arms by hand. For arm 2, I wrote the answers following `rag_answer.py`'s rules, seeing only the question and the 5 pieces, not the expected answer. Then I scored every answer of arms 2 and 3. My answers and scores are saved in `bedrock_kb_manual.json`, and `bedrock_kb_eval.py --manual` builds `bedrock_kb_results.md` from them. With an Anthropic API key, the same script does these steps through the API instead.

## Comparison

| | My build | Bedrock search + my prompt | Bedrock does everything |
|---|---|---|---|
| Right article found, of 35 answerable | 35 | 35 | 35 |
| Right article ranked 1st | 35 | 35 | 35 |
| Key facts found by the search, of 59 | 57 | **59** | **59** |
| Grounded answers, of 40 | 40 | 40 | 37 |
| Correct answers, of 40 | 40 | 40 | 39 |
| The 5 unanswerable questions handled right | 5 | 5 | 4 |
| Average scores, grounded / correct | 4.95 / 4.85 | 4.97 / 4.95 | 4.60 / 4.88 |
| Text sent to the answer model per question | 2,400 characters | 5,300 | 11,700 |
| Time per question | not measured | 0.6 s to search | 7.3 s to search and answer |

Every answer with its scores and reasons is in `bedrock_kb_results.md`.

**AWS's search is at least as good as mine.** With zero tuning it found every key fact, including the two that my build misses: how to unlock a user (Q03) and the ticket number ENG-4471 (Q06). The likely reason is that its pieces are about twice the size of mine, so a fix usually sits in the same piece as the problem it fixes. The downside is that twice as much text goes to Claude for each answer.

**AWS's own answers are accurate but sometimes say more than the articles do.** That's the problem my week 10 report warned about, where "the articles don't say" turns into a statement of fact:

1. **Q40 "Does the Android app 2.3.1 also crash?"** It answers "No — … not Android". The article only covers iOS, so nobody knows. An agent would tell the customer Android is fine.
2. **Q32 "Can we restore a project bulk-edited 45 days ago?"** It says undoing the changes from the task's Activity tab "likely won't help". The article says field changes can be undone with no time limit, which is the one thing that does help.
3. **Q08** says the "copy invite link" workaround doesn't apply. The article doesn't say that.

My prompt's rule "use only facts from the articles" keeps arms 1 and 2 from doing this. Arm 3 has no such rule, and I can't add one.

## Cost

Bedrock prices are from the [AWS pricing page](https://aws.amazon.com/bedrock/pricing/). Claude Opus 5.5 costs $4 per million tokens (pieces of words) it reads and $20 per million it writes. Token counts are estimates: characters ÷ 4, plus about 300 tokens per written answer.

| Per question | My build | Bedrock search + my prompt | Bedrock does everything |
|---|---|---|---|
| Search | $0 (my own servers) | $0.001 | $0.004, plus $0.001 per search it makes (1.2 on average) |
| Claude writing the answer | about $0.009 | about $0.013 | $0, included |
| **Total** | **about $0.009 + servers** | **about $0.014** | **about $0.005** |
| For 10,000 questions a month | about $90 + servers | about $140 | about $52 |

- **Fixed costs.** Bedrock charges $5 per GB of articles per month. Our 47 articles are 188 KB, a fraction of a cent. Reading, chunking and indexing the articles is free.
- **My build** costs nothing on a laptop. In production it needs a database server and a server for the two small models, running all month. I haven't priced those.
- **"Bedrock does everything" is the cheapest**, because the answer is included in AWS's price. That's only worth it if its answers can be trusted, and the three examples above show they can't always.
- **Bedrock search + my prompt** costs about 40% more than my build per answer, because its bigger pieces mean Claude reads more.

## Effort

| | My build | Bedrock |
|---|---|---|
| Search code to write | 353 lines in 5 files, plus a database in Docker | None. One call to AWS |
| Time to a working search | About 4 days (30 Oct – 2 Nov), including two experiments | About half a day. AWS needed under 3 minutes; the rest was finding the right settings |
| To keep running | Database, two small models, re-processing when articles change | A file bucket and the KB. Re-sync when articles change |
| What I can tune | How articles are cut, how search is mixed, the reranker, how many pieces | Mainly how many pieces come back |

The half-day went on things the documentation didn't warn about. They're listed in `BEDROCK_KB_SETUP.md`: Paris isn't supported, a missing Python package, a different search setting, and a different shape for the agentic call.

## How far to trust this

- **Two different graders.** My build was scored in week 10 by the judge through the API. The Bedrock arms were scored by me in a chat session with the same rules: the same rubric, but not the same grader.
- **I scored my own answers.** I wrote arm 2's answers (blind) and then scored them. Read its perfect score with that in mind.
- **The test is too easy.** Every arm finds the right article every time, so it can't tell a good search from a great one.
- **One scored run per arm.** The search results were the same in two runs. AWS's own answers change between runs, but Q40 said "No" both times.

## Recommendation

**Use Bedrock for the search and keep my prompt and Claude for the answers (arm 2).** It removes all the search code and servers, finds at least as much as my build, and keeps the rule that stops answers from claiming more than the articles say. It costs about 40% more per answer; sending 4 pieces instead of 5 would win some of that back. I wouldn't use AWS's own answers (arm 3) with customers without a safety filter and a harder test first.
