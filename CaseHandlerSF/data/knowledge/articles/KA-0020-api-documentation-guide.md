---
article_number: KA-0020
title: Finding API documentation, code examples and reporting doc problems
url_name: api-documentation-guide
article_type: FAQ
category: API & Integrations
plans: [Team, Business, Enterprise]
last_reviewed: 2026-10-10
related_cases: [CASE-1026, CASE-1048]
summary: Where the current (v2) API reference and examples live, why some old links return 404, and how to request missing examples.
---

## Where are the docs?

- **API reference (v2, current):** `https://developers.lumora.example/v2/reference`
- **Guides and recipes:** `https://developers.lumora.example/guides`
- **OpenAPI spec:** `https://developers.lumora.example/v2/openapi.json`. Customers can import it into Postman or Insomnia to get a working example of every endpoint.
- **SDKs:** official Python and JavaScript SDKs, each with an `examples/` folder.

## Why do some links return 404?

The v1 documentation was retired on **2026-08-01**, when the developer site moved to a new platform. Old `/docs/api/...` links should redirect, but some deep links to individual sections (anything with `#anchor`) and links inside older community posts don't. That is known issue DOC-311.

Workaround: replace `/docs/api/` with `/v2/reference/` in the URL, or search the developer site.

## Missing examples

Every reference page has a **Was this page helpful? > Suggest an improvement** link that creates a ticket for the Developer Docs team. When a customer asks for examples:

1. Point them to the OpenAPI spec and the SDK `examples/` folder for now.
2. Log the request with the endpoint names on internal ticket DOC-REQ. Developer Docs prioritize by how many requests each endpoint gets.
3. Close the case as **Resolved – Documentation request logged** and share the ticket number.

## Reporting a broken link

Ask for the page URL and the broken link. Log it against DOC-311. Fixes for broken links ship weekly.
