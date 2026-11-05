# Prompting, RAG, fine-tuning or agents: when to use what

Four ways to put a language model to work. They are not rivals; most real systems combine two or three. Start at the top and move down only when the simpler approach has been tried and measured, because each step down adds cost, build time and things that can go wrong.

| | Prompting | RAG | Fine-tuning | Agents |
|---|---|---|---|---|
| **What it changes** | The instructions | What the model can see at answer time | How the model behaves by default | What the model can do, step by step |
| **Use it when** | The task is clear and the input holds everything needed | The answer depends on your documents, or on facts newer than the model | You need a consistent style or format at high volume, and prompting with examples isn't enough | The task takes several steps that can't be fixed in advance |
| **Don't use it for** | Facts the model doesn't have | Changing tone or format | Teaching facts; they go stale and can't be cited | Anything a fixed sequence of steps can do |
| **Typical effort** | Hours to days | Weeks | Weeks, plus labelled data and retraining | Weeks, plus testing and guardrails |
| **Main risk** | Edge cases the instructions don't cover | Bad search gives confident, wrong answers | Locked to one model version; costly to update | Wrong actions, not just wrong words |

## Prompting: start here

Write clear instructions, give a few examples, and define the output format. It is enough for most summarising, classifying, extracting and rewriting.

**Enterprise example:** turning long support Case histories into a three-line handover note (issue, actions taken, next step) when a Case changes hands. In this repository, a prompt with a fixed list of categories put 20 of 20 sample Cases in the expected category (against draft labels still to be checked by hand), with no other technique needed.

## RAG (retrieval-augmented generation): when the answer lives in your documents

Before the model answers, search your own sources and put the best passages in front of it, with an instruction to answer only from them and cite each one. The model needs no retraining, the content can change daily, and every claim can be checked.

**Enterprise example:** a support assistant that answers from the company's Knowledge articles and cites the article behind each fact, so the agent can verify it before replying. Quality depends mostly on search: in this repository's tests, cutting retrieval from five passages to three dropped the passage with the answer on 3 of 40 questions, and two of those answers stated something false.

## Fine-tuning: when behaviour, not knowledge, is the problem

Train a model further on hundreds or thousands of examples of the exact output you want. It changes the model's habits (tone, format, labelling) and can let a smaller, cheaper model do a narrow job well. It does not keep facts current, and every new base model means training again.

**Enterprise example:** a bank coding millions of transaction descriptions a month into its own ledger categories, where a small model fine-tuned on past coding decisions is cheaper and more consistent than a large model with a long prompt. Try prompting with examples, and RAG over past decisions, first; fine-tune only if they fall short on a measured test.

## Agents: when the steps depend on what the model finds

Give the model tools (look up a record, search, draft, update) and let it decide which to call and when to stop. Use one when the path can't be scripted in advance. Keep a person in charge of any action that is hard to undo, and enforce that in code rather than in the prompt.

**Enterprise example:** a support agent that reads a Case, searches the Knowledge base, drafts a reply and posts it to the customer after a support agent approves the exact text. In this repository's 10-run review, the agent handled a missing Case, an out-of-scope Case and two writes correctly, and the approval step stopped a reply on a Case that was already closed.

## Before choosing, ask

1. Could a clear prompt with three examples do it? Test that first.
2. Does the answer depend on information the model can't know? Add RAG.
3. Is the output right but inconsistent, at a volume where cost matters? Consider fine-tuning.
4. Does the task need several steps whose order depends on results? Build an agent, and decide which actions need a person's approval.
5. How will you measure it? Write the test set before choosing; without one, none of these choices can be defended.
