# Verification plan

- Target is an inactive copied artifact; make its IDs/includes self-contained and keep the manuscript/sibling untouched.
- Parent independently computed endpoints from all 748 raw test rows per run. Expected cold-start mean/population SD: 0.5213903743315508 / 0.008241195191134986. Final: 0.7237076648841354 / 0.013472563687906398.
- Checkpoint scout independently validates all 36 evaluation files and 12 aggregated points; implementation must reconcile against this file, not trust old selected_data.csv.
- The native GatedRouter/src/gatedrouter/src/metrics.py:6–13,23–24,44–68 confirms binary nDCG@1 equals top-1 relevance (Hit@1), with zero for empty ideal. Our source requires nonempty required_ids for every task anyway.
- Preserve population SD convention (ddof=0) from original figure. This is descriptive between-run variability, not taskwise variability or paired baseline uncertainty; do not mark the broader critique solved.
- Compile wrapper.tex from RouterBSIPaper cwd with output directed here; do not run the paper Makefile or overwrite main.pdf.
- Final preservation reads paper_before.json, excludes only exact authorized target folder and temp/workflow dirs already excluded at baseline; records unrelated concurrent drift explicitly.
