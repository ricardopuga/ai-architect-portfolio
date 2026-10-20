# LLMs explained for executives

Oct 20, 2026 · @Ricardo

A large language model (LLM) predicts the next piece of text from the text it is given. It is fluent and broadly knowledgeable, but it does not look anything up unless you connect it to a source. Five ideas explain most of its strengths, limits and costs.

## Tokens: the unit of work and of cost

Models read and write in tokens, which are word fragments. In English, one token is roughly three quarters of a word, so 1,000 words come to about 1,300 tokens. Vendors price per million tokens, with output usually costing several times more than input. Speed limits and usage quotas are also set in tokens. Long prompts, long documents and wordy answers therefore drive both cost and response time.

## Context window: the model's working memory

The context window is the most text a model can consider in one request. It covers your instructions, any documents you attach, the conversation so far and the answer itself. Current windows range from about 100,000 to over 1 million tokens, which is hundreds to thousands of pages. Anything outside the window does not exist for the model. It has no memory between sessions unless the application stores history and feeds it back in. Bigger windows cost more per request, and accuracy can drop when key facts are buried in a very long input.

## Training cutoff: knowledge frozen at a date

A model learns from a large snapshot of text collected up to a fixed date, called its training cutoff. It knows nothing published after that date: new prices, regulations, products or this morning's news. It also never saw your private data, such as contracts, CRM records, policies and internal wikis. Retraining is slow and expensive, so models are refreshed every several months, not daily. Current or company-specific knowledge has to be supplied at the time of the question.

## Hallucinations: confident and wrong

A hallucination is a fluent, plausible answer that is false, such as an invented statistic, citation, clause or product feature. It happens because the model generates the most likely-sounding text rather than retrieving a verified fact. Gaps after the training cutoff and missing private data make it worse, because the model fills the gap instead of saying it does not know. Better models hallucinate less, but none reach zero. Treat outputs that drive money, legal or customer decisions as drafts that need sources and review.

## Why RAG exists: answers grounded in your data

Retrieval-augmented generation (RAG) addresses the last three limits together. Before the model answers, the system looks up the relevant passages in your own trusted sources and places them in the context window. It works in three steps:

1. **Retrieve.** Search your documents, databases or the web for passages that match the question.
2. **Augment.** Add those passages to the prompt, along with an instruction to answer only from them.
3. **Generate.** The model writes the answer and cites the passages it used.

The result is current, specific to your company, and checkable against a source, without retraining the model. RAG is only as good as the content behind it and the search that finds it. Outdated, duplicated or badly permissioned documents produce poor answers, and they can expose data to the wrong people.

## What to ask your teams

- What does a typical request cost in tokens, and at expected volume?
- What data does the model see at answer time, and who controls access to it?
- How fresh is that data, and who owns keeping it current?
- How do users see the sources behind an answer?
- How is accuracy measured, and where does a human review before action?
