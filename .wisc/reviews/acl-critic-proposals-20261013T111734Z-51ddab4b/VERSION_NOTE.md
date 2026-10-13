# Version boundary and concurrent changes

The critique is bound to the PDF captured at review start, not to an assumed stable live worktree.

| Snapshot | SHA256 | Pages |
|---|---|---:|
| `reviewed_main.pdf` (review input) | `51ddab4b827e211879ecf8c936083ea5fa2a03f6b34a32d230f98b90f5910d6b` | 28 |
| `observed_later_main.pdf` (later read-only observation) | `0401ac8acbac22ecefdd7b50d0582895aaa105ea094fa5e23cd42a569b0a27c7` | 28 |
| `final_observed_main.pdf` (final read-only observation) | `856f39f7bf11594ee8689eff8a0b4bced019b8ce3cc59405693b259a356e4e6b` | 28 |

The live `main.pdf` and build/figure files changed after the baseline snapshot. This workflow did not invoke a manuscript build or edit those files. The producing process was not identified. Do not attribute the changes to the user or another specific agent without evidence.

## Effect on findings

- **ISSUE-001:** the original PDF misinterprets 94.68%/93.75% as required-skill predicate-rejection rates. The later PDF removes that sentence and the narrow-predicate explanation. `sections/results.tex` already lacked these sentences when its baseline hash was captured, so the original PDF was not fully synchronized with that source even at review start. **Do not reapply the deletion.** The critique records the frozen-version error; an optional accurate summary remains a proposal only. The residual speculation about more training/human editing should still be scoped as untested.
- **ISSUE-014 / Figure 3:** the later live render has changed tick labels. Recheck the current render before applying a figure proposal; measurements of the frozen render are not automatically current.
- The later Conclusion changes its opening wording and removes the explicit caveat that stronger routing does not consistently produce the best downstream performance. Preserve/reinstate an accurate caveat in any approved revision; do not overwrite newer prose wholesale.
- Text flow and page anchors shift in the later PDF. All issue page numbers and verbatim quotes in `REVIEW_JSON.json` refer to `reviewed_main.pdf`.

## Scope of verification

`protected_before.json` contains 351 baseline file hashes (paper files plus supplied prompts/requirements; `.wisc` and unrelated `.temp` material excluded). The final check records changed and unchanged baseline paths in `verification.json`; live updates continued through finalization, including `main.tex`, Figure 5 rendering assets and `sections/appendix/error_analysis.tex`. The named snapshot `final_observed_main.pdf` is an observation at 11:42:46 UTC, not a claim that the live PDF stopped changing. At that observation, `final_live_observation.json` found the false percentage attribution absent and the other 14 anchors present; presence alone does not certify surrounding findings. Later PDFs were not substituted into this review. It must **not** report the whole manuscript tree as unchanged when external differences exist. The review/proposal artifacts and immutable input PDF can be verified independently despite live drift.

`live_pdf_text_diff.txt` is a diagnostic normalized text comparison, not an executable patch. It includes layout/extraction-order changes and is not a replacement for visual verification.

Before any implementation: obtain user approval, capture the current source/PDF pair, resolve which version is authoritative, remap anchors, and skip already-resolved changes. No manuscript change is authorized by this review.
