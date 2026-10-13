# Author alignment and minimal-change documents — WISC report

## Result
Completed user items 1, 3 and 4 as applied editorial changes. Items 2 and 5 remain proposal-only, delivered as two Word documents. No experiment, benchmark, inference, upload or commit was performed.

## Deliverables
- [Replay guarantee DOCX](replay_guarantee_minimal_changes.docx): 5 proposals, including the wrong-direction sentence, its current-replay-set scope, the fixed cold-start comparison, and an optional equality correction in Figure 2's caption. Correct existing inequalities are explicitly retained.
- [Protocol details DOCX](protocol_details_minimal_changes.docx): 4 proposals covering exact post-filtering splits/shared gold skills, candidate versus supplied-skill budgets, unequal downstream skill counts, and the meaning of Figure 5's uncertainty bands.
- [Rebuilt paper snapshot](revised_main.pdf): 29 pages; the live paper was also rebuilt as main.pdf.
- PDF renderings of both DOCX files are adjacent. Each is 3 pages. All proposals are marked NOT APPLIED and quote exact source text, relative path, source line and page in the named `before.pdf` snapshot.

## SELECT / ISOLATE
Read current sources and author instructions rather than replaying the old frozen review. Preserved baseline hashes and backups. Two independent scouts examined current quote anchors and artifact/protocol boundaries. TaskMaster was unavailable; Hermes tracking was used.

## WRITE
Specification: `.wisc/plans/author-alignment-and-docx.md`, archived under `completed/` at finalization. Author-confirmed shared initialization governs the revised prose. Historical source runs are not rewritten or retrospectively recertified.

## Applied implementation
1. Removed excluded reportability labels from 88 figure/table presentation files out of 130 scanned, including inactive artifacts. The cleanup ledger records 207 JSON-field removals, 90 text replacements and 8 JSON-string replacements. Original bytes, source paths/hashes and numeric data remain preserved. No flag was changed to reportable=true.
2. Removed the corresponding prose from appendix candidate-pool, evaluator-validation and routing-gap sections, including evaluator table caption and presentation sidecars. The evaluator generator's caption was updated without removing its raw-source checks.
3. Replaced the appendix's separately-generated/reused-library account with shared initial predicates at iteration 0, matching the author's main-paper clarification. Component and candidate-pool token descriptions now also state shared predicates. Existing measured means, deviations, counts, token totals and unknown-usage limits were not changed.
4. Rebuilt the one standalone table PDF/PNG containing an embedded excluded phrase. Its complete numeric text matches the old preview. Other previews are unchanged.
5. Added a reproducible plan/apply/verify editorial cleanup script plus tests and documentation. Original generators still validate raw sources; cleanup is an explicit post-generation publishing step.

## Verification
- `make build`: PASS, 29 pages. Small-font substitution warnings were emitted; no new overfull-box or undefined-reference warning found in the checked log.
- `make check`: PASS, 94 TeX files, 111 resolved references, no errors.
- Result-figure, ablation-figure, extended-routing and evaluator table generator `--check` commands: PASS.
- Publishing cleanup: PASS and idempotent; zero remaining targeted labels in figure/table presentation metadata. 55 protected CSV files (paper plus sibling source-table tree) unchanged; numerical leaves and embedded source hashes invariant.
- Independent whole-revision checks: PASS; 26 tabular bodies unchanged. No targeted labels remain in sections, figure/table presentation files or PDF text.
- DOCX package validation: PASS. Parent independently verified all 9 exact old/new proposals, source line positions, evidence quotes and snapshot hash. Both rendered documents were visually reviewed; no clipping or blank pages found.
- Main sources containing the proposed changes remain unchanged. A concurrent external rename from `Ethics Statement` to `Ethical Considerations` was preserved and recorded separately; it is not attributed to this task.

Evidence: `final_verification.json`, `final_checks.json`, `parent_docx_check.json`, `proposal_docs_verification.json`, `publishing-cleanup-ledger.json`, `publishing-cleanup-verification-final.json`, `revision.diff`, and build logs.

## COMPRESS / caveats
No commit: the worktree already contained unrelated changes. Backup originals are in this revision's `backup/` directory, outside the presentation artifact set. Removing publication-status wording is editorial, not experimental certification. Shared-initialization prose uses the author's clarification; no historical re-audit is claimed. Exact DOCX locations refer to the preserved pre-edit PDF because pagination can change on compilation. The initial parent claim that the wrong-direction sentence was absent was corrected after reading the full long paragraph; the final DOCX correctly includes it.

The reusable `paper-artifact-provenance` skill gained an explicit-author-cleanup procedure covering archived originals, numerical invariants, embedded preview text, and mixed applied-edit/proposal boundaries.

## Next action
Review the two Word documents. No proposed guarantee or protocol text will be applied without approval.
