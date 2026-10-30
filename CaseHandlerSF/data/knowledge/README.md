# Synthetic Knowledge base: Lumora Workspace

47 made-up support Knowledge articles for **Lumora Workspace**, a fictional cloud work-management product (projects, tasks, forms, reports, automations). The articles are written to answer the Cases in [`../sample_cases.csv`](../sample_cases.csv). Every one of the 50 Cases has at least one matching article. All names, URLs (`*.lumora.example`) and ticket numbers are invented.

## Layout

| Path | What |
|---|---|
| `articles/KA-*.md` | One article per file, with YAML front matter (`article_number`, `title`, `url_name`, `article_type`, `category`, `plans`, `last_reviewed`, `related_cases`, `summary`) |
| `build_knowledge.py` | Builds the three files below from `articles/` |
| `knowledge.jsonl` | One article per line, for embedding and RAG experiments |
| `knowledge_articles.csv` | Flat export shaped for a Salesforce Knowledge import (map the `__c` columns to your article fields) |
| `case_article_map.csv` | Ground truth `case_id → article_number` for retrieval evaluation |

Rebuild after editing an article:

```bash
python CaseHandlerSF/data/knowledge/build_knowledge.py
```

## Mix

Troubleshooting 20 · How-to 9 · FAQ 6 · Reference 5 · Known Issue 4 · Policy 3. Articles are 180–320 words each.

Plan limits appear in more than one article on purpose (KA-0001 is the reference copy), so you can test whether answers stay consistent. Some articles contain release-dependent facts ("fixed in 2026.09.2") and resolved known issues, so you can test whether a model handles dates and versions correctly.
