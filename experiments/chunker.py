"""Two simple ways to cut an article into smaller pieces ("chunks").

Why chunk at all? A search system turns each piece of text into numbers
(an "embedding") and compares them to the question. Smaller, focused pieces
match questions better than a whole article, and they're cheaper to hand to an LLM.
"""


def fixed_size_chunks(text, size=100, overlap=20):
    """Strategy 1: cut every `size` words, ignoring the article's structure.

    Each chunk repeats the last `overlap` words of the one before it, so a
    sentence cut at the edge still appears whole in one of the two chunks.
    """
    words = text.split()
    step = size - overlap  # how far to move forward each time
    chunks = []
    for start in range(0, len(words), step):
        chunks.append(" ".join(words[start:start + size]))
        if start + size >= len(words):  # reached the end of the article
            break
    return chunks


def heading_chunks(text, title):
    """Strategy 2: one chunk per section, cutting wherever a "## " heading starts.

    Each chunk begins with "article title > section heading", so even a short
    section says what it's about.
    """
    chunks = []
    heading = ""
    lines = []
    for line in text.splitlines():
        if line.startswith("## "):  # a new section starts here
            if lines:
                chunks.append(f"{title} > {heading}\n" + "\n".join(lines).strip())
            heading = line[3:]  # the heading text without the "## "
            lines = []
        else:
            lines.append(line)
    if lines:  # don't forget the last section
        chunks.append(f"{title} > {heading}\n" + "\n".join(lines).strip())
    return chunks
