# Audit C — appendix ablations, errors, trajectory, downstream tables

## Scope and outcome
- Read the complete main context, all main-referenced caption sources relevant to these comparisons, all 14 assigned files, and the baseline copies. Assigned files match the baseline. No manuscript edits, experiments, builds, or external lookup were performed.
- Seven exact, minimal replacements are supplied in `audit_C.json`: measured-policy terminology, one iteration-label correction, provenance-only adjective/comment cleanup, and a plural table reference. No numeric values, evidence, initialization claims, or scientifically useful qualification is changed.
- Keep token coverage/unknown usage, single-run versus three-run distinction, retrospective/causal scope, nonstandard FP/FN definitions, and rounded-variance precision explanation. Do not add mandatory caveats.

## Unresolved — do not falsely harmonize
- **Initialization:** leave the existing shared-initialization sentence untouched. Parent reports requested shared-initialization wording conflicts with differences in the inspected saved predicate libraries; protected main Figure 5 caption also claims shared initialization. No proposed initialization edit.
- **Backbone ceiling:** the protected main claims an unovercomeable plateau; the appendix establishes measured finite-backbone endpoints only. Do not invent an irreducible ceiling or suppress measured evidence.
- **Printed SD precision:** Only-MBR initial nDCG@1 is SD 0.001 in the endpoint table versus 0.000 in the trajectory table. Retain the trajectory's explicit rounded-variance reconstruction explanation; do not alter cells.

## Per-file coverage

### `sections/appendix/ablations.tex`
- Covered: Ablations and Sensitivity Analyses.
- Covered complete wrapper and all four input children. Order is components, cost/capacity, candidate pool, backbones. This supports the main ablations; candidate-pool and capacity sensitivity are useful additional detail.
- Action: retain.

### `sections/appendix/ablation_components.tex`
- Covered: Replay and Held-Out Gate.
- Covered configuration definition, endpoint table/caption, initialization/trajectory paragraph, gate rule, and admission-count paragraph. Endpoint means support main ordering and gains. Preserve task-weighted test means, three-run population SD, selected-set F1 versus ranking metrics, strict improvement over initialization, rollback on ties/absent support, and possible worsening relative to previous policy. The admission counts sum to 12,390; these are decisions rather than distinct skills. No scientific qualification is merely artifact clutter.
- Action: retain; initialization blocked.

### `sections/appendix/ablation_cost_capacity.tex`
- Covered: Token Accounting and Replay Capacity.
- Covered accounting paragraph, single-run component table/caption, replay-capacity paragraph, and sensitivity table/caption. Main cost figure is a single-run comparison, not the three-run component means. Keep known-token scope, unavailable-usage counts, retry/cache treatment, phase definitions, and per-class capacity interpretation. Preserve all initialization wording unchanged. Sensitivity is metric-dependent and does not conflict with the main method.
- Action: minimal terminology cleanup.
- Replacement 1: Describe the measured policy and split directly, without snapshot/artifact terminology; retain sample size and all results.
```text
OLD: Quality is measured on the final-test snapshot over 748 tasks.
NEW: Quality is measured for the final policy on the test set of 748 tasks.
```

### `sections/appendix/ablation_candidate_pool.tex`
- Covered: Candidate-Pool Size and Token Usage.
- Covered candidate-versus-selected-budget definition, task-instance aggregation, all three measured endpoints, and token-accounting/comparison scope. K=10/25/50 is a sensitivity study around the default top-50 pool, not a contradiction. Keep known tokens versus full/per-query costs and the absence of a controlled budget-matched comparison. Do not alter initialization claims.
- Action: minimal terminology cleanup.
- Replacement 1: Replace artifact-oriented snapshot terminology while preserving the measured endpoint and task count.
```text
OLD: quality is measured on the final-test snapshot over 748 tasks.
NEW: quality is measured for the final policy on the test set of 748 tasks.
```

### `sections/appendix/ablation_backbones.tex`
- Covered: Backbone Comparison.
- Covered full paragraph, all initial/final/reference rows, caption, and within-stage ranking marks. Main and appendix agree on all displayed nDCG@1 endpoints, improvement of every backbone, and nonmonotonic final performance. The appendix 99.64% and main 99.6% have compatible display precision; do not recompute from rounded endpoint cells. Keep single-run/748-task/ten-iteration scope.
- Action: retain measured endpoint; flag protected-main overclaim.

### `sections/appendix/trajectory_table.tex`
- Covered: Table tab:app-ablation-trajectory.
- Covered all eleven iteration rows and caption. Iteration 10 matches component endpoint means; intermediate values are nonmonotonic. Retain test-versus-validation distinction and rounded-variance reconstruction because it explains printed SD precision. Keep generated-file maintenance comment: it is nonrendered and helps prevent unsafe cell editing.
- Action: minimal iteration terminology correction.
- Replacement 1: The gate accepts per-skill updates, not entire iterations. This avoids suggesting every iteration is globally accepted or improves quality.
```text
OLD: Test nDCG@1 at initialization and each accepted iteration, averaged over three runs.
NEW: Test nDCG@1 at initialization and each optimization iteration, averaged over three runs.
```

### `sections/appendix/error_analysis.tex`
- Covered: Error Analysis and Additional Downstream Outcomes.
- Covered all six input children and ordering: evaluator validation, counts, ranking gap, examples, conditional downstream disagreements, complete downstream results. Wrapper requires no change. Evaluator-validation source and table were also read for cross-context; their detailed edits belong to the separate evaluator audit.
- Action: retain.

### `sections/appendix/error_counts.tex`
- Covered: False Positives and False Negatives.
- Covered both set definitions, full confusion-count table/caption, error-direction paragraph, retrospective attribution definitions, and complete attribution table/caption. Explicit nonstandard FP/FN definitions are essential because numeric column labels use the authors' convention; do not silently standardize them. Preserve candidate rejection versus retrieval miss, pooled observations versus distinct tasks, and retrospective interpretation versus checker-generated explanation. Error shares reproduce 62.24% and 79.81%; attribution counts sum to 331. No change needed.
- Action: retain.

### `sections/appendix/error_routing_gap.tex`
- Covered: Why RouterBSI Trails SkillRouter on Two Datasets; Required-skill nonactivation.; Predicate design versus checker judgments.; Implications for refinement..
- Covered introduction, matched-ranking table/caption, Required-skill nonactivation, Predicate design versus checker judgments and attribution table, examples, and Implications for refinement. The diagnostic matches the main dataset exceptions and expands them without claiming downstream causality. Preserve task/retriever denominators, gross versus net loss, uncertainty in semantic assessments, and untested human-edit/training interventions. Late changes and restrictive-versus-checker distinctions are useful evidence, not artifact-quality caveats.
- Action: remove provenance-only wording/comments.
- Replacement 1: Nonrendered evidence-path inventory is workflow provenance, not scientific exposition; no results or interpretation removed.
```text
OLD: % Evidence: ../.wisc/verification/routerbsi-exception-investigation/
% analysis.json, independent_verification.json, theoremqa/summary.json,
% medcalc/summary.json, and trajectory_spotcheck.json.

NEW: 
```
- Replacement 2: Remove the archive/provenance adjective while retaining the scientifically important observational-versus-interventional distinction.
```text
OLD: These are retrospective archived-run diagnostics, not new intervention results.
NEW: These are retrospective diagnostics, not new intervention results.
```

### `sections/appendix/error_examples.tex`
- Covered: Representative Predicate Decisions; False-negative judgment (nonrequired skill accepted).; False-positive judgment (required skill rejected).; Restrictive predicate.; Medical-calculator judgment..
- Covered Representative Predicate Decisions and all four paragraphs: nonrequired business skill accepted for Newton-Raphson, required de Broglie skill rejected, restrictive P/E predicate, and calcium-correction judgment. Preserve quoted predicates, saved Boolean observations, nonstandard labels explained in preceding subsection, and explicit excerpt qualification. These are useful distinct scientific examples, not documentation of code-artifact quality. No changes proposed.
- Action: retain.

### `sections/appendix/error_downstream.tex`
- Covered: Routing Errors Within Downstream Disagreements.
- Covered cohort definition, every conditional-table row and caption, extra-selection-share paragraph, and required-skill-coverage/comparator paragraph. It distinguishes actual supplied top-five skills from predicate decisions and routing correctness from downstream success. Keep noncausal interpretation, one-gold/five-supplied context, and conditioned/pooled denominators. Conditional shares reproduce 94.68% and 93.75%.
- Action: remove provenance-only adjective.
- Replacement 1: The archive adjective contributes nothing to the denominator or interpretation; retain all explanatory limitations.
```text
OLD: These archived extra-selection shares
NEW: These extra-selection shares
```

### `sections/appendix/error_downstream_results.tex`
- Covered: Complete Downstream Results.
- Covered subsection prose, strict/top-five/direct/oracle definitions, mean-versus-benchmark distinction, and both table inputs. Definitions agree with main; two tables follow, so singular introduction is stale.
- Action: minimal table-reference cleanup.
- Replacement 1: Two tables follow; update only singular/plural wording.
```text
OLD: The following table reports downstream task-success rates by benchmark and retriever,
NEW: The following tables report downstream task-success rates by benchmark and retriever,
```

### `sections/appendix/downstream_mean_table.tex`
- Covered: Table tab:app-downstream-mean.
- Covered every method/reference row, column-ranking marks, and full caption. All 21 retriever-level method values exactly match the Average cells in downstream_table.tex. Equal-retriever means over each 748-task pooled rate match main caption aggregation. SkillDAG leads, RouterBSI top-five exceeds strict on the mean, and direct/oracle remain retriever-independent. Do not replace printed means or main relative ratios using calculations from already-rounded cells.
- Action: retain.

### `sections/appendix/downstream_table.tex`
- Covered: Table tab:app-downstream.
- Covered reference conditions, BM25, Vector, and SkillSight blocks (all benchmark rows and Average cells), ranking emphasis, and caption. Benchmark-specific reversals of aggregate rankings are useful breakdowns, not conflicts. Average is task pooled rather than an equal-dataset mean. No numbers or highlighting changes warranted. Main already supplies the SkillDAG ten-skill versus RouterBSI five-skill protocol; no new mandatory caveat is added.
- Action: retain.

## Verification
- Programmatic coverage check: all 14 assigned paths and their section/subsection/paragraph headings are represented; table-only files are represented by table labels.
- Every proposed old span occurs exactly once in its baseline-identical target; all replacements preserve numeric-token sequences. All 21 downstream retriever-level summary values match the detailed table averages. Checked error-share denominators and admission/attribution totals.
- Existing repository was already dirty. Initial read-only git status encountered the safe-directory guard; command-scoped `git -c safe.directory=...` succeeded without changing git configuration. Only these two audit artifacts were written.
