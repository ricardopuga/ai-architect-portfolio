# /// script
# requires-python = ">=3.10"
# dependencies = ["anthropic", "fastembed", "psycopg[binary]", "pgvector", "numpy"]
# ///
"""Answer a question from the Knowledge base, with citations (retrieve, then generate).

Steps:
  1. Retrieve: find the 5 best chunks with hybrid search + rerank
     (vector search in Postgres plus keyword search, then a reranker; see hybrid_search.py).
  2. Generate: give those chunks to Claude and ask it to answer using only them,
     citing the article ID (like [KA-0029]) after each fact.
  3. Check: make sure every cited ID was actually one of the 5 chunks.

Needs the database running with chunks loaded (see embed_to_pgvector.py) and
an API key:
    export ANTHROPIC_API_KEY=sk-ant-...
    uv run experiments/rag_answer.py "Why do my teammates' edits show up late?"

Add --show-prompt to print the exact prompt sent to Claude.
"""

import os
import re
import sys

import anthropic

from hybrid_search import Searcher

MODEL = "claude-opus-5-5"
TOP_K = 5

SYSTEM_PROMPT = """You answer support questions for Lumora Workspace using only the \
knowledge base articles provided in the user's message.

- Use only facts from the articles. If they don't answer the question, say so plainly \
instead of guessing.
- After each fact, cite the article it came from in square brackets, like [KA-0029].
- Keep the answer short: a few sentences, or a short list of steps."""


def retrieve(question):
    """Step 1: return the TOP_K best chunks as (article_number, title, content).
    Hybrid + rerank won the comparison in compare_retrieval.py."""
    chunks = Searcher().hybrid_rerank(question, k=TOP_K)
    return [(c["article_number"], c["title"], c["content"]) for c in chunks]


def build_prompt(question, chunks):
    """Put the chunks in the prompt, each labelled with its article ID."""
    articles = "\n\n".join(
        f'<article id="{number}">\n{content}\n</article>' for number, _, content in chunks
    )
    return f"{articles}\n\nQuestion: {question}"


def generate(prompt):
    """Step 2: ask Claude to answer from the chunks."""
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        # Answering from 5 short chunks needs little reasoning.
        output_config={"effort": "low"},
        messages=[{"role": "user", "content": prompt}],
        # If a safety check declines, retry on Anthropic's recommended fallback model.
        betas=["server-side-fallback-2026-07-01"],
        extra_body={"fallbacks": "default"},
    )
    if response.stop_reason == "refusal":
        return "[Claude declined to answer]"
    return "".join(block.text for block in response.content if block.type == "text").strip()


def main():
    show_prompt = "--show-prompt" in sys.argv
    question = " ".join(a for a in sys.argv[1:] if a != "--show-prompt") or \
        "Why do my teammates' edits show up half a minute late?"

    chunks = retrieve(question)
    print(f"Question: {question}\n\nRetrieved chunks:")
    for number, title, content in chunks:
        heading = content.splitlines()[0]
        print(f"  {number}  {heading}")

    prompt = build_prompt(question, chunks)
    if show_prompt:
        print(f"\n--- prompt sent to Claude ---\n{prompt}\n--- end of prompt ---")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\nNo API key found, so Claude wasn't called. Set one and run again:")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        return

    answer = generate(prompt)
    print(f"\nAnswer:\n{answer}")

    # Step 3: every citation should point to a chunk we actually gave Claude.
    cited = set(re.findall(r"KA-\d{4}", answer))
    given = {number for number, _, _ in chunks}
    titles = {number: title for number, title, _ in chunks}
    print("\nSources:")
    for number in sorted(cited & given):
        print(f"  {number}  {titles[number]}")
    if cited - given:
        print(f"  Warning: cited articles that weren't retrieved: {sorted(cited - given)}")
    if not cited:
        print("  (no citations in the answer)")


if __name__ == "__main__":
    main()
