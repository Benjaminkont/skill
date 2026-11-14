---
name: bulk-rename-codex-chats
description: Preview and batch rename Codex task titles by project, recency, keyword, explicit mapping, or naming template. Use when a user asks to rename or standardize multiple Codex chats; do not use for renaming projects or editing conversation content.
---

# Batch Rename Codex Chats

Rename multiple Codex task titles while preserving task content, project membership, archive state, and git state.

## Resolve the target set

1. Resolve a named project with the Codex project listing. Prefer an exact label match; if labels collide, use the saved path and ask only when the intended project remains ambiguous.
2. Combine ordinary and pinned Codex tasks, then sort the combined set by actual `updatedAt` descending. Pin position must not affect a request for the "latest N" tasks.
3. Filter by the resolved project ID, requested keywords, count, and time direction. Include archived tasks only when the user explicitly requests them.
4. Select user-created Codex tasks only. Exclude ChatGPT conversations, approval or guardian records, and other internal tasks. Never silently broaden the selection when fewer than the requested count are available.

Use the app's task listing as the primary source. If its global result window cannot cover the requested project count, inspect locally available Codex task metadata read-only to finish discovery. Inspect the current schema before querying it, restrict results to visible user tasks, and never write to or migrate the local database.

## Derive titles

- Honor an explicit old-title-to-new-title mapping exactly.
- Otherwise use the existing title, summary, first user request, relevant completed result, and linked local note title as evidence. Read only enough task history and local context to identify the outcome.
- Follow the user's template exactly, including separators and numbering. For course work, prefer the course's established name and the formal chapter or lecture title.
- If evidence is insufficient, leave the item unchanged and mark it for review instead of inventing a title.
- Detect duplicate proposed titles before mutation. Disambiguate with a meaningful course, unit, topic, or outcome qualifier and show that choice in the preview; do not append hidden or arbitrary sequence numbers.

## Preview and authorization

When any new title is inferred by Codex, present a complete preview containing the old and proposed titles and make no changes in that turn. Wait for explicit confirmation of that preview.

The preview may be skipped only when the user supplies the complete exact mapping and explicitly asks to apply it. A request for a preview, proposal, inspection, or explanation never authorizes mutation.

## Apply changes

- Rename tasks only through the Codex task-title API. Never update the local database directly.
- Submit bounded batches of at most 10 renames at a time and retain the requested mapping for verification.
- If one rename fails, read its current title before retrying. Retry that exact idempotent title assignment at most once, then stop retrying it and report the failure.
- Do not change task content, archive state, pinning, project membership, sidebar placement, or repository files as part of this workflow.

## Verify and report

After mutation, independently read every targeted task's current title and compare it with the approved mapping. A successful write response alone is not verification.

Report the requested, matched, failed, unchanged, and skipped counts. List every mismatch or unavailable task with its old, expected, and observed title when available. The counts must reconcile to the number of targeted tasks.
