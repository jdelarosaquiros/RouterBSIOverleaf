# Appendix-only alignment and scientific-prose cleanup

## Scope and authority
Author explicitly authorizes local appendix revisions and a complete subsection audit. Main source (abstract through limitations plus ethics/acknowledgment), entrypoint, bibliography, figures/captions, tables outside appendix and experimental results are immutable. No publication, commit or model experiments. Venue/stage remains unknown; this is an unsubmitted local draft, not a portal revision. No new experimental results.

## Evidence boundary
User requests saying Both Enabled uses the same initialization in all three runs. Inspected manifest-linked predicate libraries instead differ across those runs. Do not strengthen the existing common-initialization claim or silently rewrite evidence; mark it unresolved pending actual historical run binding. Consistency with the main text is not sufficient grounds to fabricate experimental details. Preserve useful scientific limitations, denominators, uncertainty and data scope. Remove process/provenance/artifact-quality narration only when it does not support subsection interpretation. Preserve raw prompts and numeric tables.

## SELECT / ISOLATE
Read main.tex and all active main sections/captions and all appendix subsections. Snapshot current 334 protected files under `.wisc/revisions/appendix-alignment-20261013T145213Z/before/`; record hashes in before.json. Three independent audit scouts cover separate subsection groups. Parent reconciles recommendations, including unresolved main-side errors that cannot truthfully be fixed in appendix only. TaskMaster tools unavailable; Hermes todo and JSON inventory supply tracking.

## Files allowed to change
`sections/appendix/*.tex` only, supported by exact old/new edits and per-subsection checks. Supporting WISC audit/spec/build artifacts may be written under `.wisc/`. Original main.pdf will not be replaced; build a review PDF in an isolated copy to honor appendix-only scope.

## Implementation
1. Read each changed file before editing and compare with snapshot.
2. Apply approved safe changes in a dedicated implementation agent with exact replacement allowlist.
3. Preserve all values, equations, prompt examples and citations unless a specifically justified nonnumeric text correction is documented.
4. Reject conflicting concurrent edits rather than overwriting.
5. Compile an isolated copy with repository Makefile; do not regenerate result assets.
6. Check final diff, exact main/asset hashes, full subsection coverage, labels/citations/build logs and rendered edited pages.

## Deliverables
Per-subsection audit JSON/Markdown (including unchanged and blocked), exact task diff, revision report separating edits from unresolved factual mismatches, isolated built PDF and build verification. Full appendix-main alignment cannot be claimed while evidence-backed contradictions remain under the frozen-main constraint.

## Completed execution
- All 49 active appendix TeX files / 31 subsections audited in three independent groups and parent reconciliation.
- Applied 18 exact prose/caption replacements in 13 appendix files; initialization claim not strengthened.
- Clean isolated baseline and revised builds pass; revised PDF is 30 pages and first eight pages render pixel-identically.
- `make check`: 96 TeX files, 113 resolved references, no errors. No overfull or undefined-reference warnings; existing font substitutions remain.
- Original main sources, figure assets/captions, numeric values, equations, prompt blocks, citations and root main.pdf unchanged.
- Five unresolved groups (initialization, replay membership/support, ranking scope, split description, retriever-training contradiction) documented in APPENDIX_AUDIT.md and REVISION_REPORT.json.
- Visual inspection covers all appendix pages 11–30. No task-introduced clipping/overlap detected.
- No commit, experiment, result regeneration or upload. Source edits complete; factual full-alignment objective remains blocked as documented.
- Reusable appendix-only audit guidance added to latex-paper-drafting skill; author-specific task scope is not stored as a global preference.
