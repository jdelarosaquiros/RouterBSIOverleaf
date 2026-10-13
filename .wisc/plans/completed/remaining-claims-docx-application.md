# Apply remaining claims DOCX revisions

## Scope
Apply exactly the three Proposed replacement passages from `.temp/RouterBSI_remaining_claims_revisions.docx` to the live manuscript. No additional scientific/style corrections, source-data changes, figure/caption edits, or commits of inherited edits.

## Targets
- `sections/results.tex`: proposal 02 retention sentence and proposal 03 SkillDAG sentence.
- `sections/ablations.tex`: proposal 08 backbone paragraph tail.

## Decisions
Author-provided proposed passages take precedence over explanatory Reasons. Preserve “significantly”, plateau claim, “overcomed”, whitespace and punctuation exactly as supplied. Proposal 03 Previous text says “has”; live manuscript says “covered”; uniquely match that full live sentence and replace with the proposed passage. Three unique targets verified. DOCX has no tracked changes or Office Math.

## Implementation and validation
Exact replacement pairs and baseline snapshots: `.temp/remaining_claims_application/replacements.json`, `before/`, `baseline.json`. Delegate bounded application/read-only context review; use patch only for the two manuscript files. Parent independently reconstructs expected outputs from snapshots and compares bytes, confirms unrelated source/assets remain unchanged, runs `make rebuild` and `make check`, inspects final log and rendered affected pages. Save a task-only diff and verification report. Archive this plan upon completion; no commit requested. TaskMaster unavailable: use Hermes todo.
