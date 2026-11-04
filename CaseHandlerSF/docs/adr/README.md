# Architecture decision records

Each record explains one decision: the problem, the options, what was chosen and why, and when to revisit it. Records are not rewritten when a decision changes; a new record replaces the old one and links back to it.

| # | Decision | Status |
|---|---|---|
| [0001](0001-vector-store-pgvector.md) | Store Knowledge base embeddings in Postgres with pgvector | Accepted |
| [0002](0002-model-choice.md) | Use Claude Opus 5.5 for every generation step, with effort as the cost lever | Accepted, follow-up open |
| [0003](0003-human-approval-for-writes.md) | A person approves every write the AI makes to Salesforce | Accepted |

For how the parts fit together, see the [architecture diagrams](../architecture.md).
