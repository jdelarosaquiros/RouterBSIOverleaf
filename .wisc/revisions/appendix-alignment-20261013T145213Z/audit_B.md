# Appendix alignment audit B

## Outcome

Audited **18 assigned TeX files**: 9 subsections, three section wrappers, 6 standalone table leaves, and the embedded settings table. Proposed **5 exact replacements in 3 files**; 15 files require no edit. No manuscript, source-data, generator, or experiment files were written. No build, experiment, model call, or web access was performed.

The proposals remove one legacy-temperature configuration sentence, one artifact-verification sentence, and three repository-local `in-tree` qualifiers. All numeric tokens and useful methodological/uncertainty limits are preserved.

## Scope and authoritative anchors

- Root: `/workspace/storage/healthcare_workspace/project_skill_selection/RouterBSIPaper`.
- Baseline: `/workspace/storage/healthcare_workspace/project_skill_selection/RouterBSIPaper/.wisc/revisions/appendix-alignment-20261013T145213Z/before`; all assigned files matched this snapshot when checked.
- Read `main_context.txt` in full (abstract through limitations plus other active main sections), active `main.tex` and appendix includes.
- Read all eight active main figure/table captions, including resolved `description.text` inputs: introduction predicate example; related-work method overview; main average routing table; average retention; downstream average; component-ablation nDCG@1; token usage; backbone comparison.
- Evaluator validation is active **H.1**, not D.5. Parent reports 31 active subsections / 49 active appendix TeX files globally; this audit covers only its 18 assigned files.
- Read two relevant generator sources without execution to understand table column/format semantics; no additional code or run discovery undertaken.

## Required-useful caveats versus removable narration

**Keep:** non-blinded first adjudication; AI-not-human validation; class imbalance and always-False comparator; provisional reference; deduplication and occurrence weighting; stratified blinded second pass, exclusions and ambiguous cases; no direct approved-True check; nonrepresentative sample; single-run comparisons and same-seed repetitions; population SD versus uncertainty of a mean; no significance tests; set-F1 versus ranked cutoffs; task/retriever aggregation order; own-pool retention and SkillDAG expansion; no-MBR retaining proposal history; timeout/retry/cache/concurrency and actual evaluation rules.

**Remove:** only code-path/legacy-field narrative, checksum/journal/request verification assurances, and repository-local `in-tree` phrasing as listed below. Unprinted generated-file comments need not be cleaned.

## Unresolved; do not force false alignment

1. Unresolved main-text contradiction: sections/experiments.tex Baselines calls retrievers trained on the training split, whereas Implementation Details calls them training-free. Do not invent retriever training or alter the appendix to force agreement.
2. Unresolved main/implementation mismatch: sections/experiments.tex specifies binary label plus retrieval score, whereas sections/appendix/procedure_routing.tex describes lexicographic label/score/order ranking. Do not claim equivalence for arbitrary raw scores; reciprocal-rank SkillSight is the stated special case. Resolution belongs outside this audit group.
3. Blocked, outside group: the actual main ablation caption (figs/mbr_replay_test_ndcg@1_std/description.text) claims the same initial predicates. Parent-provided evidence distinguishes the saved initial predicate libraries across runs, whereas the requested wording describes shared initialization. No new equality claim or source alteration is proposed; preserve repetition/seed uncertainty and require author/evidence reconciliation.
4. Main retention wording is broader than the appendix: retain the own-method Recall@50 denominator and expanded SkillDAG-pool distinction.
5. Full Coverage is named but not explicitly defined in the metrics prose. Optional self-containment improvement only; no unverified new metric definition is proposed.

## Per-file coverage and exact proposals

### `sections/appendix/evaluator_validation.tex`

**Status:** EDIT

**Headings/leaves:** Predicate-Evaluator Validation

**Main anchors:** Limitations: fixed predicate-checker instructions and checking errors; Experiments: Evaluation Metrics; Method: predicate-based skill routing

EDIT: delete only the checksum/journal/request-payload verification sentence. This active subsection is H.1, not D.5. KEEP the named adjudicator, observed saved Boolean/non-blinding, predicate-satisfaction rather than relevance target, unique-review versus occurrence weighting, class imbalance, provisional-reference recall, always-False comparison, stratified second-pass design, previous-sample exclusion, blinded assessment, ambiguous/likely-incorrect outcomes, AI-not-human status, lack of True checks, and nonrepresentative-sample limits. These qualifications are necessary to prevent 97.10% agreement being presented as human accuracy.

**Replacement 1** (JSON strings preserve leading spaces exactly):

Old:
```json
" Source checksums, journal-record hashes, request payloads, and occurrence-weighted counts were verified before tabulation."
```
New:
```json
""
```
Reason: This is artifact-verification narration. The separate deduplication and occurrence-weighting sentences already preserve the scientifically necessary denominator semantics.

### `sections/appendix/evaluator_validation_table.tex`

**Status:** RETAIN

**Headings/leaves:** Table leaf: evaluator_validation_table

**Main anchors:** Limitations: predicate checker errors; Experiments: task-instance averaging

RETAIN: all six dataset rows plus pooled row and numeric cells. The caption correctly says model-adjudicated agreement, not human-validated accuracy; this caveat is required. The unprinted generated-file comment is not manuscript prose and need not be removed.

**Proposed edits:** none.

### `sections/appendix/implementation.tex`

**Status:** RETAIN

**Headings/leaves:** Implementation and Configuration

**Main anchors:** Experiments: Implementation Details; Method: MBR Update Selection with Bounded Replay and Held-Out Validation

RETAIN: active section wrapper includes Shared Configuration, Requests/Caching/Reproducibility, Controlled Method Variants, and Retrieval/Evaluation Software. All four children audited; no printed provenance narration.

**Proposed edits:** none.

### `sections/appendix/implementation_runtime.tex`

**Status:** EDIT

**Headings/leaves:** Requests, Caching, and Reproducibility

**Main anchors:** Experiments: Implementation Details (proposal temperature 1; evaluation temperature 0); Method: sequential recursive updates; Limitations: computational cost

EDIT: remove only the legacy-field/request-wrapper implementation-history sentence. KEEP request schema, effective temperatures, model-specific reasoning parameters, timeouts, retry exhaustion, overflow behavior, concurrency without task-order changes, cache semantics, and initial-library/prompt binding: these describe reproducibility-relevant behavior, not artifact-quality assurances.

**Replacement 1** (JSON strings preserve leading spaces exactly):

Old:
```json
" In the active proposal branch, the request wrapper sets temperature one explicitly; a legacy proposal-temperature configuration field does not override this branch."
```
New:
```json
""
```
Reason: The immediately preceding sentence already gives the effective temperature. Legacy configuration precedence is code-history narration, not needed to interpret the experiment.

### `sections/appendix/implementation_settings.tex`

**Status:** RETAIN

**Headings/leaves:** Shared Configuration; Embedded table: Default RouterBSI optimization settings (tab:appendix-settings)

**Main anchors:** Experiments: Implementation Details (SkillSight, Qwen3.5-4B, 50 candidates, downstream k=5, temperatures, 10 iterations); Method: bounded replay N, generated candidates M_p, predicate limit l

RETAIN: shared settings, embedded table, unchanged-predicate option, character rather than token limit, current-inclusive replay bound, and distinct retrieval/downstream budgets are useful methodology. Preserve every setting and numeric value. Single-predicate validation specialization is explained by the referenced appendix; do not substitute a different objective.

**Proposed edits:** none.

**Unresolved:**
- Unresolved main-text contradiction: sections/experiments.tex Baselines calls retrievers trained on the training split, whereas Implementation Details calls them training-free. Do not invent retriever training or alter the appendix to force agreement.

### `sections/appendix/implementation_software.tex`

**Status:** EDIT

**Headings/leaves:** Retrieval and Evaluation Software; Retrieval and reranking.; Task evaluation.; Examples and split construction.

**Main anchors:** Experiments: Baselines and Implementation Details; Experiments: Evaluation Metrics and Benchmarks and Skill Corpus

EDIT: neutralize three repository-local "in-tree" qualifiers. KEEP tokenizer, model, scoring, rank-score exposure, reranker input truncation, precision, task-specific evaluation rules/tolerances, resource limits, ToolQA demonstrations, and split solver details. These are useful operational methodology, not removable provenance. All three paragraphs explicitly covered: Retrieval and reranking; Task evaluation; Examples and split construction.

**Replacement 1** (JSON strings preserve leading spaces exactly):

Old:
```json
"The in-tree SRA BM25 implementation"
```
New:
```json
"The SRA BM25 implementation"
```
Reason: Remove repository-local positioning while retaining the specific retrieval implementation.

**Replacement 2** (JSON strings preserve leading spaces exactly):

Old:
```json
"We use the in-tree SRA task evaluators"
```
New:
```json
"We use the SRA task evaluators"
```
Reason: Remove repository-local positioning; preserve benchmark-specific scoring rules.

**Replacement 3** (JSON strings preserve leading spaces exactly):

Old:
```json
"ToolQA's in-tree ReAct prompt"
```
New:
```json
"ToolQA's ReAct prompt"
```
Reason: Remove repository-local positioning; preserve fixed demonstration counts, order, and inference path.

**Unresolved:**
- Unresolved main-text contradiction: sections/experiments.tex Baselines calls retrievers trained on the training split, whereas Implementation Details calls them training-free. Do not invent retriever training or alter the appendix to force agreement.
- Unresolved main/implementation mismatch: sections/experiments.tex specifies binary label plus retrieval score, whereas sections/appendix/procedure_routing.tex describes lexicographic label/score/order ranking. Do not claim equivalence for arbitrary raw scores; reciprocal-rank SkillSight is the stated special case. Resolution belongs outside this audit group.

### `sections/appendix/implementation_variants.tex`

**Status:** RETAIN

**Headings/leaves:** Controlled Method Variants

**Main anchors:** Ablations: Impact of MBR based on Replay and Held-out Validation Gate; Ablations: Performance and Token Usage Tradeoff; Method: bounded replay and held-out gate

RETAIN: capacity and candidate-budget settings; no-gate rollback semantics; no-MBR still uses historical context; replay-F1 zero-denominator convention and distinction from Boolean error; single-predicate validation equivalence. These prevent the ablations being misread as removing all history or changing the default loss.

**Proposed edits:** none.

**Unresolved:**
- Blocked, outside group: the actual main ablation caption (figs/mbr_replay_test_ndcg@1_std/description.text) claims the same initial predicates. Parent-provided evidence distinguishes the saved initial predicate libraries across runs, whereas the requested wording describes shared initialization. No new equality claim or source alteration is proposed; preserve repetition/seed uncertainty and require author/evidence reconciliation.

### `sections/appendix/retention.tex`

**Status:** RETAIN

**Headings/leaves:** Retention Under a Skill-Budget Constraint

**Main anchors:** Results: Required Skill Retention; Abstract and Introduction: 90.5% top-5 retention; Main figure fig:average_recall_degradation

RETAIN: active wrapper for Coverage and Retention and Results Across Routing Budgets; both included table leaves audited.

**Proposed edits:** none.

### `sections/appendix/retention_definition.tex`

**Status:** RETAIN

**Headings/leaves:** Coverage and Retention

**Main anchors:** Experiments: Evaluation Metrics (Ret@k); Results: Required Skill Retention; Main figure fig:average_recall_degradation (retention mean across retrievers)

RETAIN: ratio of task-mean recalls, then equal averaging of three retriever-specific ratios. Each method has its own Recall@50 denominator, including SkillDAG expanded ranking. Preserve the distinction from averaging task-level ratios and from end-to-end recall. These are essential estimand/candidate-pool qualifications that make the compressed main wording interpretable.

**Proposed edits:** none.

**Unresolved:**
- Main results and figure describe retention from an initial top-50 retrieval pool too broadly. The appendix correctly qualifies SkillDAG normalization as its own expanded pool. Do not erase this qualification or claim all methods share the same denominator; any remaining main wording change is outside appendix-only scope.

### `sections/appendix/retention_mean_table.tex`

**Status:** RETAIN

**Headings/leaves:** Table leaf: retention_mean_table

**Main anchors:** Abstract/Introduction and Results: 90.5% top-5 retention; Main figure fig:average_recall_degradation

RETAIN: mean retention table, all methods/cutoffs, percentages and caption. Equal average of three task-mean-recall ratios is the correct stated estimand; do not replace it with pooled occurrence retention or a ratio of retriever means.

**Proposed edits:** none.

### `sections/appendix/retention_results.tex`

**Status:** RETAIN

**Headings/leaves:** Results Across Routing Budgets

**Main anchors:** Results: Required Skill Retention; Abstract/Introduction: RouterBSI 90.5% retention; Main figure fig:average_recall_degradation

RETAIN: RouterBSI 90.5%/94.6% and SkillRouter 83.9%/87.9% comparisons, SkillDAG coverage-versus-ordering boundary, and fixed-ranking-prefix interpretation. The statement that updater reruns are not required explains what varying k measures and is useful methodology, not removable process history.

**Proposed edits:** none.

### `sections/appendix/retention_table.tex`

**Status:** RETAIN

**Headings/leaves:** Table leaf: retention_table

**Main anchors:** Results: Required Skill Retention (coverage and SkillDAG expansion); Main figure fig:average_recall_degradation

RETAIN: all per-retriever coverage and retention rows, including initialization. Preserve Recall@50 as a fractional coverage score versus percentage retention, and Ret@50=100. No printed provenance or code-quality commentary; the own-pool definition in Coverage and Retention must remain.

**Proposed edits:** none.

### `sections/appendix/routing.tex`

**Status:** RETAIN

**Headings/leaves:** Extended Skill-Routing Results

**Main anchors:** Results: Skill Routing Performance; Experiments: Evaluation Metrics

RETAIN: active wrapper for Ranking and Selection Metrics and Results by Benchmark and Retriever, with three table leaves audited.

**Proposed edits:** none.

### `sections/appendix/routing_metrics.tex`

**Status:** RETAIN

**Headings/leaves:** Ranking and Selection Metrics; Statistical reporting.

**Main anchors:** Experiments: Evaluation Metrics (per-task averages); Experiments: Baselines/Implementation Details (strict versus top-k routing); Main table tab:skill_routing_performance_average (task-weighted 748-task scores; equal retriever means); Main ablation figure fig:mbr_replay_test_ndcg@1_std (three-run variation)

RETAIN: nDCG/recall/F1 definitions, ranked-versus-selected distinction, task weighting, and retriever averaging. Statistical reporting is required-useful uncertainty, not process narration: single evaluations, non-seed repetitions, common replay seed, population SD rather than SE/CI, absent run-to-run estimates and absent significance tests must remain. Do not rewrite set-level F1 as fixed-cutoff F1 merely because the main overview uses F1@k.

**Proposed edits:** none.

**Unresolved:**
- Unresolved main/implementation mismatch: sections/experiments.tex specifies binary label plus retrieval score, whereas sections/appendix/procedure_routing.tex describes lexicographic label/score/order ranking. Do not claim equivalence for arbitrary raw scores; reciprocal-rank SkillSight is the stated special case. Resolution belongs outside this audit group.
- Blocked, outside group: the actual main ablation caption (figs/mbr_replay_test_ndcg@1_std/description.text) claims the same initial predicates. Parent-provided evidence distinguishes the saved initial predicate libraries across runs, whereas the requested wording describes shared initialization. No new equality claim or source alteration is proposed; preserve repetition/seed uncertainty and require author/evidence reconciliation.
- The table leaves include FC@5/FC@10, named Full Coverage in their captions, without an explicit definition in this metrics subsection. A definition could improve self-containment, but is not required provenance cleanup; no new metric implementation is asserted or replacement proposed here.

### `sections/appendix/routing_results.tex`

**Status:** RETAIN

**Headings/leaves:** Results by Benchmark and Retriever

**Main anchors:** Results: Skill Routing Performance (TheoremQA and MedCalc-Bench exceptions); Main table tab:skill_routing_performance_average

RETAIN: benchmark/retriever decomposition, exact illustrative endpoints, TheoremQA SkillRouter advantage and Vector MedCalc-Bench boundary. These qualify the aggregate claim and should not be removed as negative results. All three included routing tables explicitly covered.

**Proposed edits:** none.

### `sections/appendix/routing_table_1.tex`

**Status:** RETAIN

**Headings/leaves:** Table leaf: routing_table_1

**Main anchors:** Results: Skill Routing Performance; Main table tab:skill_routing_performance_average; Experiments: Evaluation Metrics

RETAIN: TheoremQA and LogicBench table leaf, all BM25/Vector/SkillSight groups and seven methods per group. Preserve every numeric cell, bold/underline marker, metric abbreviation and set-level-F1 caption. No printed provenance or code-quality commentary. These are per-retriever detail, not duplicate estimates of an independently repeated experiment.

**Proposed edits:** none.

### `sections/appendix/routing_table_2.tex`

**Status:** RETAIN

**Headings/leaves:** Table leaf: routing_table_2

**Main anchors:** Results: Skill Routing Performance; Main table tab:skill_routing_performance_average; Experiments: Evaluation Metrics

RETAIN: ToolQA and MedCalc-Bench table leaf, all BM25/Vector/SkillSight groups and seven methods per group. Preserve every numeric cell, bold/underline marker, metric abbreviation and set-level-F1 caption. No printed provenance or code-quality commentary. These are per-retriever detail, not duplicate estimates of an independently repeated experiment.

**Proposed edits:** none.

### `sections/appendix/routing_table_3.tex`

**Status:** RETAIN

**Headings/leaves:** Table leaf: routing_table_3

**Main anchors:** Results: Skill Routing Performance; Main table tab:skill_routing_performance_average; Experiments: Evaluation Metrics

RETAIN: CHAMP and BigCodeBench table leaf, all BM25/Vector/SkillSight groups and seven methods per group. Preserve every numeric cell, bold/underline marker, metric abbreviation and set-level-F1 caption. No printed provenance or code-quality commentary. These are per-retriever detail, not duplicate estimates of an independently repeated experiment.

**Proposed edits:** none.

## Verification

- Coverage compared programmatically against the four assigned filename globs; no omitted files or duplicate entries.
- Every proposed old span occurs exactly once in its current target; proposed edits were simulated in memory only.
- Numeric-token sequences before/after each simulated proposal are identical.
- All assigned current files equal the revision-local `before` snapshot at audit time.
- Initial Git status was blocked by dubious ownership; a command-local `git -c safe.directory=...` read succeeded without changing configuration. The worktree already contained extensive edits and untracked appendix files; none were reset or adopted as this audit's changes.
- Audit files are recommendations, not experimental certification. Full frozen-source reconstruction and builds were not run.

### Source digests for proposal application

| File | SHA-256 | Edits |
|---|---|---:|
| `sections/appendix/evaluator_validation.tex` | `2c036d2843065388c8d35f6362e3720d2734c9aecbcb8b7e52e23dcdeb5a29da` | 1 |
| `sections/appendix/evaluator_validation_table.tex` | `31a5585e6246ac12226de5bd252163a6d2ff03b4d449744a40a593e0da1d40ef` | 0 |
| `sections/appendix/implementation.tex` | `863cd01286323b051211f565029a44df6ca632ee482d495023b33f17d2864414` | 0 |
| `sections/appendix/implementation_runtime.tex` | `b1c3356393ee07cd36143c13c090e898e90d45470831096232b1e0fdc50e41b4` | 1 |
| `sections/appendix/implementation_settings.tex` | `4eede10c210234b328b3945d39b27fdf595b1cc22b42ae9d4c777d6b1009b745` | 0 |
| `sections/appendix/implementation_software.tex` | `fcab2c3a61efd32ecb751b013be10654c614ebd814e9896e23cbc36ffe7784a6` | 3 |
| `sections/appendix/implementation_variants.tex` | `464f33cd4f0fd84a96995c2e8b32c80fc712f95480c665e4f142359b3f4f9b90` | 0 |
| `sections/appendix/retention.tex` | `7bcea3c4509f1a3143721c2817915c14dffeb29b293cf7a1c2937afa8fbcdce2` | 0 |
| `sections/appendix/retention_definition.tex` | `3fa8cadb1954a96d26326e0ea5f597f2e41b354bc47541f49d6c55e1840c4953` | 0 |
| `sections/appendix/retention_mean_table.tex` | `bf988aaf5dc14cae2a99af205946c703b185540161a53ece99451bcefaec028f` | 0 |
| `sections/appendix/retention_results.tex` | `5af619bcc09f4e6ad52240cd5d9c82e61cc2e210cf815f6cc048931580c8152e` | 0 |
| `sections/appendix/retention_table.tex` | `00c26db2750321eaeb62e9b287ecfb709087757a31a75666c769c5469d968a0d` | 0 |
| `sections/appendix/routing.tex` | `fa1cbda925fb6ec705ce35aa156ab0644bf6f53d5aadc31453d693cdb4d50f26` | 0 |
| `sections/appendix/routing_metrics.tex` | `5ec95a52aafb534513aaee191c04c098cbd7a407884d6749af637685b9af6e34` | 0 |
| `sections/appendix/routing_results.tex` | `b506203d2b1e1a70953a0371e41ac70e10205ac290eb3c71a79499dd0a6621f5` | 0 |
| `sections/appendix/routing_table_1.tex` | `460d17d55197399ca6d22199e65634efe7a5fe23a5724deede29d40e4a942ffc` | 0 |
| `sections/appendix/routing_table_2.tex` | `8bf12480674c0f50d01a84b932245a8c5483b9228439e641abb5b6eb4e6d661d` | 0 |
| `sections/appendix/routing_table_3.tex` | `5e246c010a0a6fde1a67d68da4186dae2b036dec830bd3284061b377ddd80b7e` | 0 |
