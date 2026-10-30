---
article_number: KA-0017
title: File upload size limits and how to upload large files
url_name: file-upload-size-limits
article_type: FAQ
category: Files & Storage
plans: [Starter, Team, Business, Enterprise]
last_reviewed: 2026-10-05
related_cases: [CASE-1036]
summary: Upload size limits by plan (50 MB, 250 MB or 2 GB) and the options for files above them.
---

## What is the maximum file size?

| Plan | Web and mobile upload | API resumable upload |
|---|---|---|
| Starter | 50 MB | n/a |
| Team | 50 MB | 50 MB |
| Business | 250 MB | 1 GB |
| Enterprise | 2 GB | 5 GB |

Form file fields have their own limit, set by the form author (no more than the plan limit).

## Can Support raise the limit for us?

No. The limit is tied to the plan. Options:

1. **Upgrade** to Business (250 MB) or Enterprise (2 GB).
2. **Link instead of uploading.** Attach a file from a connected cloud drive (Google Drive, OneDrive, Dropbox, Box) using **Attach > From cloud storage**. Linked files don't count against storage or the size limit.
3. **Use the API** for resumable uploads on Business and Enterprise (`POST /v2/files/uploads`, sent in 8 MB chunks).
4. **Compress or split** the file (for example a ZIP archive of the images).

## Upload fails below the limit

- A corporate proxy or firewall may cap request size. Ask IT to allow `uploads.lumora.example`.
- Executable files (`.exe`, `.bat`, `.sh`, `.msi`) are blocked on every plan.
- Check that the workspace hasn't hit its storage limit (KA-0016).
