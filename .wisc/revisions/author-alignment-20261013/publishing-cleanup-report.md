# Figure/table publishing cleanup — verified result

## Applied scope

- Scanned all 130 presentation files beneath `figs/` and `tables/` (`.json`, `.text`, `.tex`, `.md`, `.txt`).
- Changed 88 files: 72 figure files and 16 table files; 31 JSON, 44 `.text`, 13 TeX.
- Recorded 207 JSON-field deletions, 8 JSON-string replacements and 90 text-line changes in `publishing-cleanup-ledger.json`.
- Archived all 88 original files byte-for-byte under `backup/publishing-cleanup/<sha256>/<relative-path>`. Parent baseline and existing backups were not overwritten.
- Remaining reportability/analysis-only/noncanonical/diagnostic-only/publication-validity/provisional flags in the 130-file presentation scope: **0**.

## Preservation and verification

- 55 protected CSVs are byte-identical (40 paper-local and 15 sibling `BayesGSI/tables` sources).
- All 7,435 numeric JSON leaves in changed JSON files retained their values and paths. 29,579 retained JSON leaves are unchanged; 674 embedded SHA256 occurrences in changed files are unchanged.
- All TeX tabular bodies are byte-identical; text numeric tokens are invariant except the explicitly removed audit-reason configuration setting `=1`, whose complete text is archived and logged.
- Source/run identities, source hashes, scientific uncertainty, confidence-interval qualifications, mixed run families, candidate-pool scope, unavailable checkpoints and known-only token-accounting limits are preserved.
- Three offline regression tests passed, including five drift/unknown-wording/archive subcases, idempotence, CSV mutation rejection and the parent's narrow preview-refresh exception.
- Independent leaf-level ledger replay and source-code hash verification passed; 12 relevant raw generator/test files remain identical to the parent baseline. `git diff --check -- figs tables scripts/publishing_cleanup.py scripts/test_publishing_cleanup.py scripts/README_publishing_cleanup.md` passed.
- Cleanup application and no-op/idempotence verification passed. Evidence: `publishing-cleanup-verification.json`, `publishing-cleanup-independent-verification.json`.

## Regeneration and boundaries

Use `scripts/publishing_cleanup.py` after any raw generator, following `scripts/README_publishing_cleanup.md`. The tool makes a hash-bound, immutable review plan before archival/writes and refuses unknown flag wording or drift. The source generators and validation tests were not weakened.

The earlier `publishing-cleanup-pre-preview-policy-plan.json` is an unapplied planning snapshot retained when the parent requested a preview verification exception. The applied/current ledger is `publishing-cleanup-ledger.json`.

No manuscript sections, Makefile, DOCX, numeric CSVs, raw experiments, previews or builds were modified/run by this subtask. Existing embedded output/snapshot hashes deliberately remain the original generator bindings; **the ledger's after_sha256 values bind the cleaned presentation**, not the older embedded output hashes. No scientific re-certification was performed.

Parent-owned pending rendering: `tables/retrieval_and_reranking_performance/preview.pdf` and `preview.png` still require the parent's caption refresh; these are the only intentional mutable preview exceptions. Use `verify --allow-preview-refresh` after that refresh; the output records their actual hash changes, and every other artifact remains bound. At subtask verification time both previews were still unchanged.

Item 4 follow-up scan found no explicit different-initial-predicate claim in this artifact presentation scope. Existing known-only/incomplete token-cost caveats and external/shared-initialization accounting boundaries remain; shared initial predicates are not treated as proof of identical token logging. Main/appendix alignment stays with the parent.
