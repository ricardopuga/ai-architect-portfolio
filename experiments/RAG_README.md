# Answering questions from a Knowledge base (RAG), step by step

This folder has a small, working **RAG** system: *retrieval-augmented generation*. In plain words:

1. Someone asks a question.
2. We **search** our help articles for the few pieces of text most likely to contain the answer.
3. We give those pieces to Claude and ask it to **answer using only them**, citing which article each fact came from.

Claude doesn't need to "know" anything about our product. It reads the right text at the moment it answers, and the citations let a person check every claim.

Everything here was built in order, one step at a time. This file explains each step, what each file does, and what we learned.

---

## The process, in order

### Step 1: Create the Knowledge base

We needed help articles to search. We wrote **47 made-up support articles** for a fictional product called *Lumora Workspace*. Each one answers one or more of the 50 sample Cases in `CaseHandlerSF/data/sample_cases.csv`.

| File | What it does |
|---|---|
| `CaseHandlerSF/data/knowledge/articles/KA-*.md` | One article per file. The top of each file lists its ID, title, type and the Cases it answers |
| `CaseHandlerSF/data/knowledge/build_knowledge.py` | Turns the articles into files the other scripts read |
| `CaseHandlerSF/data/knowledge/knowledge.jsonl` | All articles, one per line. **This is what the scripts below read** |
| `CaseHandlerSF/data/knowledge/knowledge_articles.csv` | The same articles, shaped for a Salesforce Knowledge import |
| `CaseHandlerSF/data/knowledge/case_article_map.csv` | Which article answers which Case (the "answer key" for tests) |

### Step 2: Cut the articles into chunks

Search works better on small, focused pieces than on whole articles. Cutting text into pieces is called **chunking**. We tried two ways:

- **Fixed-size:** cut every 100 words, wherever that lands, even mid-sentence.
- **Heading-based:** one piece per section (`## Heading`). Each piece starts with *"Article title > Section heading"*, so it always says what it's about.

| File | What it does |
|---|---|
| `chunker.py` | The two chunking functions |
| `chunking_test.py` | Asks 23 questions and checks which way of chunking finds the answer more often |

**Result:** heading-based found the answer in the top 3 pieces for 21 of 23 questions, fixed-size for 20 of 23. Fixed-size sometimes cut a fact away from what it was about. In one case, a table row about SAML ended up in a piece with no mention of SAML. **We use heading-based chunks from here on.**

### Step 3: Turn chunks into embeddings and store them in Postgres

An **embedding** is a list of numbers (384 of them here) that captures what a piece of text means. Texts with similar meanings get similar numbers. That's how search can match *"half a minute late"* with *"30 seconds"*.

We store each chunk and its embedding in **Postgres** with **pgvector** (an add-on that lets Postgres store and compare these lists of numbers). Postgres runs in **Docker**, so there's nothing to install on your Mac except Docker itself.

| File | What it does |
|---|---|
| `compose.yaml` | Starts Postgres with pgvector in Docker |
| `embed_to_pgvector.py` | Chunks the 47 articles (186 chunks), embeds them, and saves them in a `chunks` table |
| `search_pgvector.py` | Type a question, get the 3 closest chunks. Good for trying out search on its own |

The embedding model, `BAAI/bge-small-en-v1.5`, is small and runs on your laptop, so embedding costs nothing.

### Step 4: Retrieve, then generate (with citations)

Now the full loop. We find the 5 best chunks, put them in the prompt labelled with their article IDs, and ask Claude to answer **only** from them, citing like `[KA-0029]`. The script then checks that every cited ID was really one of the 5 chunks.

| File | What it does |
|---|---|
| `rag_answer.py` | **The main script.** Question in, answer with citations out |

**What we learned:** Claude's answer was accurate and fully cited, but it was missing the actual fix, because the "Fix" section of the article was never retrieved. **The answer can only be as good as what the search finds.** When the fix was missing, Claude said so instead of making one up, which is exactly what we asked for.

### Step 5: Better search with keywords (BM25) and a reranker

Vector search is good at meaning but can miss exact terms like `test_mode_key_in_live` or `ENG-4388`. So we added:

- **Keyword search (BM25):** scores chunks by matching words, and rare words count more. No model, just counting.
- **Hybrid search:** runs vector *and* keyword search and merges the two lists. A chunk that's fairly high in both lists beats one that's high in only one.
- **Reranker:** takes the top 20 hybrid results, and a small model reads the question and each chunk *together* to pick the best 5. It's slower than comparing embeddings, but better at judging "does this actually answer the question?".

| File | What it does |
|---|---|
| `hybrid_search.py` | The search methods: vector, keyword (BM25, written by hand), hybrid, and hybrid + rerank |
| `compare_retrieval.py` | Runs 10 questions through 3 search methods, has Claude answer each, and scores the results |
| `retrieval_comparison.md` | The results, with every answer side by side |

**Result (10 questions):**

| Method | Fact found by search | Fact in Claude's answer |
|---|---|---|
| Vector only | 9 / 10 | 9 / 10 |
| Hybrid (vector + keywords) | 10 / 10 | 10 / 10 |
| Hybrid + rerank | 10 / 10 | 10 / 10 |

The question that separated them was *"Teammates' edits show up half a minute late. How do we fix it?"*. Vector search alone ranked the Fix section 15th, and keyword search alone ranked it 18th. Merged, it came 4th, and the reranker moved it to 2nd. Hybrid + rerank also gave the most complete answer. **`rag_answer.py` now uses hybrid + rerank.**

Be careful with these numbers: 10 questions is a small test, and 9 of them were easy for every method. A bigger, harder set of questions is the natural next step.

---

## How to run it yourself

Run these in a terminal (in VS Code: **Terminal → New Terminal**), from the project folder. Docker Desktop must be open.

```bash
# 1. Start the database
docker compose -f experiments/compose.yaml up -d

# 2. Load the chunks into it (run again whenever the articles change)
uv run experiments/embed_to_pgvector.py

# 3. Ask a question (needs an Anthropic API key)
export ANTHROPIC_API_KEY=sk-ant-...
uv run experiments/rag_answer.py "Why do my teammates' edits show up late?"

# Optional: see exactly what Claude receives
uv run experiments/rag_answer.py "How do I set up SSO?" --show-prompt

# Stop the database when you're done (your data is kept)
docker compose -f experiments/compose.yaml down
```

To look inside the database: `docker compose -f experiments/compose.yaml exec db psql -U postgres -d knowledge`, then for example `SELECT article_number, left(content, 60) FROM chunks LIMIT 5;`. Type `\q` to leave.

## Words used in this file

| Word | Meaning |
|---|---|
| **RAG** | Retrieval-augmented generation: search first, then let the LLM answer from what was found |
| **Chunk** | A small piece of an article |
| **Embedding** | A list of numbers that represents a text's meaning |
| **pgvector** | An add-on that lets Postgres store embeddings and find the closest ones |
| **BM25** | A classic keyword-scoring formula. Matching rare words count more |
| **Hybrid search** | Combining vector search and keyword search |
| **Reranker** | A model that reorders search results by reading the question and each result together |
| **Citation** | The article ID after a fact, like `[KA-0029]`, so a person can check it |

## Notes

- The database password (`postgres`) is for local experiments only.
- With an API key, `rag_answer.py` makes one Claude call per question, and `compare_retrieval.py` makes 30.
