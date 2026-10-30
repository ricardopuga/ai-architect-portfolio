"""Build machine-readable files from the Knowledge articles in ./articles.

Writes, next to this script:
  knowledge.jsonl         one article per line (for embeddings / RAG experiments)
  knowledge_articles.csv  Title, UrlName, Summary, Body, ... (for a Salesforce Knowledge import)
  case_article_map.csv    case_id -> article_number ground truth (for retrieval evals)

Usage:
    python CaseHandlerSF/data/knowledge/build_knowledge.py

Standard library only. Front matter is parsed with a small subset of YAML:
scalar values and inline lists like [a, b].
"""

import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
ARTICLES = HERE / "articles"


def parse_value(raw: str):
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        return [item.strip() for item in raw[1:-1].split(",") if item.strip()]
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        return raw[1:-1]
    return raw


def parse_article(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    _, front, body = text.split("---\n", 2)
    meta = {}
    for line in front.strip().splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = parse_value(value)
    meta["body"] = body.strip()
    return meta


def main() -> None:
    articles = [parse_article(p) for p in sorted(ARTICLES.glob("KA-*.md"))]

    with open(HERE / "knowledge.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(a, ensure_ascii=False) + "\n" for a in articles)

    with open(HERE / "knowledge_articles.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "ArticleNumber__c",
                "Title",
                "UrlName",
                "Summary",
                "Body__c",
                "ArticleType__c",
                "Category__c",
                "Plans__c",
                "Language",
            ]
        )
        for a in articles:
            writer.writerow(
                [
                    a["article_number"],
                    a["title"],
                    a["url_name"],
                    a["summary"],
                    a["body"],
                    a["article_type"],
                    a["category"],
                    ";".join(a["plans"]),
                    "en_US",
                ]
            )

    with open(HERE / "case_article_map.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["case_id", "article_number"])
        pairs = sorted(
            (c, a["article_number"]) for a in articles for c in a["related_cases"]
        )
        writer.writerows(pairs)

    print(f"{len(articles)} articles, {len(pairs)} case->article links")


if __name__ == "__main__":
    main()
