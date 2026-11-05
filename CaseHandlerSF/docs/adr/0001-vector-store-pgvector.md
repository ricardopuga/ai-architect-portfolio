# ADR 0001: Store Knowledge base embeddings in Postgres with pgvector

- **Status:** Accepted
- **Recorded:** 2026-11-04
- **Applies to:** the Knowledge base container and the MCP server's `search_knowledge` and `draft_reply` tools ([architecture](../architecture.md))

## Context

The assistant answers support questions from 47 Knowledge articles, cut into 186 heading-based chunks. Each chunk needs a 384-number embedding (`BAAI/bge-small-en-v1.5`, run locally) and must be searchable by meaning and by exact terms such as error codes (`test_mode_key_in_live`) and ticket numbers (`ENG-4388`).

What mattered:

- **Retrieval quality**, measured, not assumed. The answer can only be as good as what search finds.
- **Hybrid search.** Vector search alone missed a fix that keyword search and the merged list found ([retrieval comparison](../../../experiments/retrieval_comparison.md)).
- **Few moving parts.** One developer, local Docker, no budget for a managed service.
- **A path to production** without rewriting the search code.

## Decision

Store chunks, metadata and embeddings in one Postgres table (`chunks`) using the pgvector extension, running in Docker (`pgvector/pgvector:pg17`).

Search is hybrid: pgvector does the vector half (cosine distance), BM25 keyword scoring runs in memory in Python, the two lists are merged with Reciprocal Rank Fusion, and a local cross-encoder reranks the top 20 down to 5 ([knowledge.py](../../src/casehandlersf/knowledge.py)).

## Options considered

| Option | For | Against |
|---|---|---|
| **Postgres + pgvector** (chosen) | One store for text, metadata and vectors, queried with SQL. Runs locally in Docker; managed Postgres with pgvector is available from the major clouds. Joins and filters (by article, product, permission) are plain SQL | No built-in BM25; keyword scoring has to live elsewhere. Needs an index tuned by hand at larger sizes |
| Dedicated vector database (managed or self-hosted) | Built for vector search at scale; some include hybrid search and filtering | Another service to run, secure and pay for. Text and metadata either duplicated or split across two stores. Nothing at 186 chunks needs it |
| In-memory only (numpy or FAISS in the app) | Fastest to build, nothing to run | Rebuilt on every start, not shared between processes, nothing to query or inspect |

## Evidence

On a 40-question test set (35 answerable, 5 deliberately not) ([RAG eval report](../../../experiments/RAG_EVAL_REPORT.md)):

| Retrieval method | Right article in top 5 | Right article ranked 1st |
|---|---|---|
| Vector only (pgvector) | 35/35 | 33/35 |
| BM25 only | 35/35 | 34/35 |
| Hybrid | 35/35 | 34/35 |
| Hybrid + rerank (chosen) | 35/35 | 35/35 |

End to end at top-k 5, answers passed groundedness and correctness 40/40, and all 5 unanswerable questions were refused. The report's caveat applies here too: the questions were written after reading the articles, so these numbers flatter the system.

## Consequences

- **Good:** one store to back up and inspect (`psql`), SQL filters available when the Knowledge base gains permissions or product tags, and a standard managed-Postgres path to production.
- **Bad:** BM25 lives in the MCP server, which loads **every chunk into memory** on first search. That is fine for hundreds of chunks and wrong for hundreds of thousands.
- **Bad:** there is no vector index. Every query scans all 186 rows. Add an HNSW index before the table grows into the tens of thousands.
- **Risk:** the embedding model name is set in two places, [`embed_to_pgvector.py`](../../../experiments/embed_to_pgvector.py) and [`knowledge.py`](../../src/casehandlersf/knowledge.py). If they drift apart, search quietly gets worse with no error.
- **Debt:** the database and its loader live under `experiments/`, although the MCP server depends on them at runtime.

## Revisit when

- The Knowledge base passes about 50,000 chunks, or BM25 start-up time becomes noticeable. Move keyword search into Postgres (full-text search) or a search engine, and add an HNSW index.
- Articles move to Salesforce Knowledge. Then re-evaluate keeping a copy in Postgres against searching in Salesforce directly.
- A harder test set shows retrieval misses that a different store, not a different query, would fix.
