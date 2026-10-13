# Task: RouterBSI three-run test nDCG@1 trajectory

## What / authorized scope
Update only figs/routerbsi_test_ndcg@1_std as an independent single-method plot of test performance of the evolving predicates across run_1, run_2 and run_3 of project_skill_selection/.wisc/results/GatedRouter/sra_full_skillsight_f1_i10_l400_qwen3.5_4b. Cold start, iterations 1–10, and saved Final evaluation. No inference, training, raw-run changes, manuscript integration or prose revisions. TaskMaster tools unavailable; Hermes todo tracks WISC. No commit requested; leave ready for review.

## Starting point
The target is a copied four-condition ablation folder with stale sibling artifact IDs, wrapper includes, tests, data, provenance and readability report. Main manuscript does not reference this target. Prior figure bytes and all 344 paper-file hashes are in .wisc/verification/routerbsi-three-run-trajectory/.

## Key decisions
- Interpret uncertainty as across-run SD of task-averaged test nDCG@1 of the predicate policies, not numeric SD of predicate strings/counts or dispersion across tasks/checkpoints.
- Use raw saved ranked_ids and required_ids; with verified nonempty binary gold, nDCG@1 equals top-ranked relevance (Hit@1). 748 equally weighted tasks per run/checkpoint, then arithmetic mean and population SD (ddof=0) across three runs, consistent with existing plot convention. Explicitly not a paired baseline CI or significance test.
- Exact matrix: 3 runs × (cold start + 1..10 accepted-policy tests + Final snapshot) = 36 evaluations. Final is categorical and may coincide numerically with iteration 10; never manufacture a different endpoint.
- Validate exact test membership/gold across all files, unique tasks, completion metadata, stored available Hit@1/MRR@10 crosschecks; missing stored Hit@1 in run_3 is allowed only because complete predictions permit exact derivation.
- Bind policies to predictions via candidate_statements and saved initial/accepted/final conditions where feasible; preserve policy hashes, prediction hashes and status in provenance.
- Retain source noncanonical/non-reportable status. Concise caption describes mean/band/checkpoints; technical provenance states full caveats.
- Correct ARTIFACT, all output identities/includes/label to routerbsi_test_ndcg@1_std; remove ablation series and claims of common initial predicates.
- Single green RouterBSI mean line plus shaded ±1 population SD. Legible 8–9pt labels at single-column width; display Cold start and Final clearly. No arbitrary clipping of bands.

## Files to change
Target generate.py, test_generate.py, selected_data.csv, selection_manifest.json, preview.pdf/png, description.text, provenance.text, table.tex, readability_manifest.json. Add per_run_data.csv for full precision supporting values. Any verification scripts/outputs stay in .wisc/verification/routerbsi-three-run-trajectory.

## Validation
- Independent scout recomputation of all 36 evaluations and 12 means/SDs.
- Focused tests for exact run/checkpoint matrix, statistics, invalid/missing/duplicate evidence failure, artist lines/bands and output identity/hash closure.
- Run standalone generator and tests; syntax check.
- Compile actual target table.tex in isolated ACL preview (not main.pdf); visually inspect exported figure and wrapper.
- Verify raw consumed hashes, unrelated paper and sibling hashes unchanged; explicitly record concurrent drift rather than revert.
- Save completed WISC report and concise endpoint summary.
