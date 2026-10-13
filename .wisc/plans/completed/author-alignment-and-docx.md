# Task: Author-requested alignment and minimal-change DOCX proposals

## Scope
Implement user items 1, 3, 4: remove reportability/provenance warning language from manuscript and paper-facing figure/table artifacts; align appendix to main-paper protocol using author's explicit shared-initialization correction. Produce two DOCX proposal-only documents for items 2 and 5 (replay guarantees and essential protocol details). Do not apply those proposed main-text changes.

## Boundaries
- Current live paper is authoritative, not prior frozen review. Baseline and backups: `.wisc/revisions/author-alignment-20261013/`.
- Main methods/results/ablation govern narrative; shared initialization is author-confirmed, not independently re-certified historical evidence.
- Remove presentation metadata/wording, never mark an unaudited experiment reportable=true or change historical logs, source CSVs, task records, result numbers or checksums to simulate validation.
- Preserve original provenance in revision-local backups outside the paper/artifact presentation set; no changes to BayesGSI experimental archives.
- Preserve meaningful scientific scope (e.g. model agreement is not human accuracy; unknown token counts remain unknown). Shared predicates do not by themselves certify identical token logging.
- Only user-authorized alignment edits; gate/replay changes and protocol promotions are proposals only.

## Files
Current sections/appendix files, figure/table metadata/captions and directly related generators when needed for regeneration consistency. Two DOCX files and verification evidence under revision directory. Build outputs from make build.

## Validation
Exact replacements with drift guards; source hashes/data numeric invariance; paper make check and build; PDF inspection; DOCX package/readback and LibreOffice rendering; exact quotes with source lines and snapshot page locations. Record any contradictory archive evidence without rewriting historical artifacts.

## Tracking
TaskMaster unavailable; Hermes todo list tracks phases/items. Existing dirty worktree preserved; no commit unless separately requested.
