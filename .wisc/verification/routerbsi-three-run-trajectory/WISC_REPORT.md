# WISC execution report: RouterBSI three-run trajectory

## Purpose and scope
Refresh `figs/routerbsi_test_ndcg@1_std` to show the mean and standard deviation of test nDCG@1 for the evolving RouterBSI predicate policies, from each run's cold start through the final evaluation, using the specified three archived runs. This authorization applies to the named figure, not the prior review's other proposed revisions.

## SELECT
Loaded WISC, publication-figure-iteration, gatedrouter-run-analysis and paper-artifact-provenance guidance; workspace AGENTS.md; target generator/tests/caption/wrapper/manifests; selected raw run schemas and native metric definition. No relevant .wisc/rules found. TaskMaster unavailable; Hermes todo used.

## ISOLATE
Independent scout audited all 36 evaluation files and all policy/ledger links. Identical 748 task IDs, task hashes, gold labels and realized candidate order across all three runs and every checkpoint. The last accepted policy/predictions exactly match saved Final in every run. Source run 1 has a different recorded source/prepared binding than runs 2/3; original noncanonical status is preserved. Three runs share one configured seed but have distinct initial predicate policies; this is not a three-seed experiment.

Parent separately reconciled all 11 shared checkpoint means and population variances with the old Both Enabled series to its six-decimal stored precision. Independent raw endpoint check is recorded in parent_endpoint_check.json. Scout evidence: scout.json.

## WRITE
Contract: `../../plans/completed/routerbsi-three-run-trajectory.md`. Original figure backed up in figure_before/. Protected snapshot covers 344 original paper files and 180 selected raw-source files.

## Implementation intent and limits
Replace the stale copied four-condition ablation with one RouterBSI mean line and population-SD band. Retain green styling, readable single-column type, exact raw-input provenance and full precision. Correct every copied target ID/path. Include cold start, iterations 1–10 and categorical Final; disclose Final duplicates iteration 10. Do not integrate an inactive figure into main.tex. No manuscript prose edits, model calls, training, benchmark reruns, commits or uploads.

The band is descriptive across-run SD (ddof=0), not a confidence interval or paired baseline comparison. This scoped update does not resolve the broader review request for paired comparison-level uncertainty. All three sources explicitly remain completed_noncanonical and reportable=false.

## Verified implementation
Updated generate.py, test_generate.py, table.tex, description.text, provenance.text, selected_data.csv, selection_manifest.json, readability_manifest.json and preview.pdf/png. Added per_run_data.csv. The generator now reads raw saved rankings and predicate policies from exactly the requested run_1/run_2/run_3, validates membership/gold/conditions/ledger links, derives nDCG@1, then computes the three-run mean and population SD. All output references bind to routerbsi_test_ndcg@1_std, not the sibling ablation.

## Verification results
- `python -B figs/routerbsi_test_ndcg@1_std/test_generate.py -v`: **6 tests passed** in the parent's recorded run (33.234 seconds). Tests cover raw matrix/statistics, malformed and missing evidence, policy tampering, hash drift, plotted coordinates/band vertices and byte-reproducible generation. See tests.log.
- `verify_numeric.py`: **12/12 means and SDs, 36/36 per-run values** match the independent scout. Generator, output and consumed-input hashes pass. See numeric_verification.json.
- `verify_scope.py`: **180 raw source files unchanged**, no unrelated changes among **344 preexisting paper files**, main.pdf unchanged; only the ten authorized preexisting target files changed, with one new per-run CSV. See parent_preservation.json.
- System TeX standalone wrapper build succeeded (1 page), using `/usr/bin` tools because the earlier PATH's conda TeX lacks needed packages. No main manuscript build. See latex-build.log and wrapper.pdf/png.
- PNG and actual ACL wrapper visually inspected: one green mean line, one SD band, clear Cold start/1–10/Final labels, no clipped/overlapping labels. PDF is 218×154 points with minimum 8-point text. Figure source/image hashes were verified after generation.
- Old Both Enabled data reconcile exactly at all 11 shared checkpoints to the old CSV's six-decimal precision; new SD avoids rounded-variance error. See previous_series_reconciliation.json.
- An initial parent numeric check ran before publication and failed on absent per_run_data.csv; it was rerun after generation and passed. No fallback or invented data was used.

## Results
| Endpoint | Mean test nDCG@1 | Population SD across 3 runs |
|---|---:|---:|
| Cold start | 0.5213903743315508 | 0.008241195191134986 |
| Final | 0.7237076648841354 | 0.013472563687906398 |

## COMPRESS / current state
Complete and ready for review. The implementation worker was stopped after parent tests, rendering, numeric and preservation verification completed, preventing unnecessary late edits; this report records the verified result directly rather than relying on a child success claim. No commit requested or created. TaskMaster unavailable; Hermes checklist completed. No follow-up is needed for the requested artifact. The inactive figure was not integrated into the manuscript, and the broader paired-baseline uncertainty issue remains outside this scope.

## Final conclusion
The named standalone figure now displays raw-source-verified three-run mean ± one population SD from cold start through final. No inference or benchmark reruns were needed, and manuscript/source/sibling bytes were preserved.
