# Task: Complete appendix tables for active result and ablation figures

## Scope
Audit five active numerical figures: average_retention_degradation; downstream_average; mbr_replay_test_ndcg@1_std; performance_token_usage; routing_performance_across_llms_init. Introduction routing and method diagrams are conceptual, excluded. Unused archived figures excluded. Preserve main prose (including author DOCX edits), figure assets, source data, and existing unrelated appendix text.

## Findings and changes
- Retention: existing mean table covers four cutoffs, caption states Ret@50=100. Make all five plotted cutoffs explicit; match mean of per-retriever recall ratios, not ratio of means.
- Downstream: detailed benchmark/retriever table exists, but mean-across-retrievers plotted bars do not. Add compact table with per-retriever pooled rates and equal-weight retriever mean, plus Direct and Oracle references; retain detailed table.
- Component trajectory: existing eleven-checkpoint table has means only. Add population SD below each mean for all 44 points; derive exactly as figure sqrt(stored variance), not alternate raw-run recalculation. Keep endpoints separate.
- Token cost: existing table already covers all four x/y pairs; verify and add figure link, no duplicate.
- Backbone: existing table has six initial/final model rows but lacks SkillSight reference. Add baseline row from same selected_data.csv and link to figure.

## Implementation
Read frozen selection manifests and CSVs, independently cross-check authoritative CSV rows; generate reproducible additions with script under scripts/. Existing completed tables remain intact except stated coverage completions. Keep scientific prose free of code paths/provenance disclaimers, preserve caveats in audit report. Use existing table style, three decimals for quality/SD (needed to retain small uncertainties) and mean above SD. Correct only table-specific metric/aggregation explanations when necessary.

## Verification
Persist JSON coverage matrix with exact points, source hashes, table mapping/counts. Compare all numerical figure values to table cells at display precision and recover underlying aggregation. Build current main.pdf, run repository check, inspect changed-table PDF pages. Hash-preserve main prose, source inputs and figures. No training, inference, experiments, commits, or unrelated corrections. TaskMaster unavailable; use Hermes todo. Parent owns final build and verification after worker stops writing.
