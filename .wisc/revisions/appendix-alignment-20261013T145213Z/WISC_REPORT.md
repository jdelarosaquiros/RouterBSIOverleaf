# WISC execution report — appendix alignment

## Outcome
Audited all **31 active appendix subsections** and **49 TeX files**. Applied **18 exact prose/caption replacements in 13 appendix source files**. Main sources, main captions/figures, bibliography, numeric results and original `main.pdf` are unchanged. The edits are local, unsubmitted changes, not a claim of venue compliance.

**Full factual alignment remains incomplete.** The requested shared-initialization sentence was not added because inspected saved libraries differ across the Both Enabled runs; their historical binding to Figure 5 remains unresolved. This is a manuscript-versus-artifact issue, not a main-versus-appendix contradiction. The existing disputed sentence is unchanged. The other unresolved items are replay definition/support, ranking-rule scope, global versus per-dataset splits, and the main paper's incompatible retriever-training statements. See the [complete subsection audit](APPENDIX_AUDIT.md).

## Changes
- Removed checksum/journal-verification assertions, legacy temperature-field commentary, a credential-archive aside, irrelevant archive qualifiers and repository-relative wording.
- Renamed Artifact Coverage and Reuse to Dataset Coverage and Reuse; preserved language, privacy, licensing and safety content.
- Corrected the appendix/main cross-reference, iteration acceptance terminology and plural downstream-table reference.
- Replaced saved-snapshot language with measured-policy terminology, retaining all task counts and results.
- Preserved useful token-coverage, uncertainty, evaluator-adjudication, data-scope and observational-versus-causal qualifications.

## Verification
- Clean baseline and revised isolated builds passed; revised PDF has 30 pages.
- First eight pages render pixel-identically to the clean pre-edit baseline.
- No changes outside appendix sources among 334 protected files.
- Numeric tokens, table bodies, display equations, quoted prompt blocks and citations preserved in every edited file.
- Build has no fatal errors, undefined references or overfull boxes; existing small-font substitution warnings remain.
- Existing repository check passed in the revised build. All modified appendix regions and their following transitions were visually checked in contact sheets.

## WISC record
- SELECT: live main text/captions, complete appendix include tree and dirty working-tree baseline.
- ISOLATE: three independent audits plus parent reconciliation; no artifact/model runs.
- WRITE: `.wisc/plans/appendix-alignment-20261013T145213Z.md` and exact replacement allowlist.
- IMPLEMENT: edits restricted to `sections/appendix/*.tex`; isolated `make build` and `make check`.
- COMPRESS: audit, diff, revision/verification JSON and this report. No commit; unrelated existing changes remain untouched. TaskMaster tools unavailable; Hermes task checklist used.

## Deliverables
- [Revised review PDF](build_after/main.pdf) — isolated build; original `main.pdf` not overwritten.
- [Every-subsection audit](APPENDIX_AUDIT.md)
- [Exact appendix-only diff](appendix_only.diff)
- [Revision report](REVISION_REPORT.json)
- [Verification](verification.json)

## Next decision
Resolve the disputed historical initialization binding and allow corrections to the frozen main claims where necessary. No benchmark rerun, figure regeneration, commit or upload was authorized or performed.
