---
name: lecture-notes-from-transcript
description: Turn raw lecture transcripts into formal course notes that preserve the instructor's teaching sequence, example evolution, and technical reasoning. Use when creating or substantially expanding notes from classroom transcripts; do not use for verbatim transcription or generic topic summaries without a lecture source.
---

# Lecture Transcript to Notes

Produce a self-contained note that is easier to review and search than the transcript while still feeling structurally faithful to the class.

## Core method

Treat the lecture as a guided argument, not as a bag of facts. Recover its pedagogical spine before writing:

- the problem or motivating question;
- the first, often manual or incomplete approach;
- the failure, limitation, or counterexample that motivates a change;
- each refinement introduced by the instructor;
- the final technique, its boundary conditions, and the lesson drawn from it.

Use that progression as the note's main structure. Prefer headings that follow topic transitions in the lecture over an encyclopedia-style taxonomy imposed afterward.

## Workflow

1. Read the complete transcript, the target note, repository instructions, and nearby notes that establish course style. Search for existing notes on the same concepts when this affects links or duplication.
2. Outline the lecture spine before editing. Capture demonstrations, deliberately broken examples, audience questions that change the explanation, and transitions to the next concept.
3. Merge with the target note. Preserve useful existing material; reposition supplementary material after the classroom narrative or label it as a supplement when it was not taught in the lecture.
4. Rewrite oral speech as formal notes: remove greetings, repetition, false starts, and dialogue framing while preserving the reasoning that made each refinement necessary.
5. Reconstruct code, formulas, commands, and data structures accurately. Keep the evolution of important examples instead of showing only the final version when the intermediate failure teaches the concept.
6. Where a visual would materially clarify a relationship, process, architecture, comparison, or failure mode, insert an inline, multi-line fenced `image-prompt` block at that exact point in the note. The block is a temporary placeholder, not a detached list of image suggestions. Write a usable generation prompt that states the visual's purpose, required elements and relationships, relevant constraints, and any facts that must not be invented. Prefer a small number of high-value prompts; use Mermaid or Excalidraw instead when exact labels, arrows, or editable structure matter more than a raster illustration.
7. Verify the finished artifact in proportion to its contents: Markdown structure, code fences, heading continuity, formulas, relative links, whitespace, and repository diff. Syntax-check executable code blocks; treat `image-prompt` blocks as intentionally non-executable placeholders, and exclude only other examples that are deliberately invalid (identifying why they are invalid).

## Writing decisions

- Explain what a concept is, why it appears at that point in the lecture, how control or data flows through it, and where it fails or stops applying.
- Convert useful classroom questions into direct explanations. Omit questions that merely repeat material or do not change the final understanding.
- Preserve terminology, example names, and the instructor's order when they carry teaching value. Compress repeated runs or repeated spoken descriptions into one representative example and a concise conclusion.
- Distinguish “this test passed” from “the implementation is correct,” and make analogous evidence-versus-conclusion distinctions in other subjects.
- Do not fabricate missing lecture content, outputs, citations, version details, or transitions. If the transcript is damaged or incomplete, preserve only what can be recovered confidently and mark material gaps when they matter.
- Add outside knowledge only when it prevents a technical misunderstanding or makes an example usable. Keep it brief, clearly separate it from the lecture's claims, and verify unstable facts when required.

## Code and command examples

- Prefer minimal, complete examples that preserve the classroom variable names and progression.
- Explain deliberately faulty code before correcting it; do not silently replace the teaching example with the final answer.
- When a snippet is intentionally syntactically invalid, say so explicitly and exclude it from the expected-success syntax check.
- Treat examples that depend on networks, third-party services, package versions, or operating systems as environment-dependent. State prerequisites or instability instead of claiming they were executed when they were not.

## Inline image prompts

- Place the prompt immediately after the paragraph or section it explains, with blank lines around the fenced block:

  ````markdown
  ```image-prompt
  绘制一张……
  ```
  ````

- The prompt should preserve the lecture's claims and terminology. Do not introduce components, causal relationships, numbers, or conclusions that are absent from the transcript or clearly marked supplementary material.
- When the user later generates the asset, replace the whole block with a repository-relative image link such as `![架构图](assets/主题/架构图.png)`. Do not leave the prompt as a second, redundant copy beside the finished image.
- Keep prompts in the note while the visual is pending so the intended placement and rationale remain visible; do not collect them only at the end of the note.

## Completion criteria

The final note should let a learner recover both the technical content and the reason the lecture introduced it in that order. It should contain no conversational shell, no unsupported expansion presented as classroom fact, and no loss of useful existing material unrelated to a deliberate correction.
