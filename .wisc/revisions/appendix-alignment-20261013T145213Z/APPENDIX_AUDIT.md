# Appendix alignment audit

## Scope
All active appendix subsection files and their table/wrapper inputs were checked against the frozen main paper. Edits remove process narration and improve cross-references without changing experimental values. Full scientific alignment is **not certified**: the unresolved items below require evidence or main-text authorization.

## Every subsection
| Appendix | Subsection | Result | Unresolved |
|---|---|---|---|
| A.1 | Initialization and Online Routing | unresolved alignment | RANK |
| A.2 | Bounded Replay Construction | unresolved alignment | REPLAY |
| A.3 | Candidate Admission and Minimum-Risk Selection | unresolved alignment | REPLAY |
| A.4 | Held-Out Gate and Partial Rollback | reviewed unchanged | None identified in this source audit |
| A.5 | Optimization Procedure | edited with unresolved alignment | REPLAY |
| B.1 | Initial Predicate Generation | edited | None identified in this source audit |
| B.2 | Replacement Proposals | reviewed unchanged | None identified in this source audit |
| B.3 | Boolean Predicate Evaluation | reviewed unchanged | None identified in this source audit |
| B.4 | A Complete Replay Decision | reviewed unchanged | None identified in this source audit |
| C.1 | Task Filtering and Split Construction | edited with unresolved alignment | SPLIT |
| C.2 | Required-Skill Labels and Task Types | reviewed unchanged | None identified in this source audit |
| C.3 | Shared Skill Corpus and Data Access | reviewed unchanged | None identified in this source audit |
| C.4 | Dataset Coverage and Reuse | edited | None identified in this source audit |
| D.1 | Shared Configuration | unresolved alignment | REPLAY |
| D.2 | Requests, Caching, and Reproducibility | edited | None identified in this source audit |
| D.3 | Controlled Method Variants | unresolved alignment | REPLAY |
| D.4 | Retrieval and Evaluation Software | edited with unresolved alignment | TRAIN |
| E.1 | Ranking and Selection Metrics | reviewed unchanged | None identified in this source audit |
| E.2 | Results by Benchmark and Retriever | reviewed unchanged | None identified in this source audit |
| F.1 | Coverage and Retention | reviewed unchanged | None identified in this source audit |
| F.2 | Results Across Routing Budgets | reviewed unchanged | None identified in this source audit |
| G.1 | Replay and Held-Out Gate | unresolved alignment | INIT |
| G.2 | Token Accounting and Replay Capacity | edited with unresolved alignment | REPLAY |
| G.3 | Candidate-Pool Size and Token Usage | edited | None identified in this source audit |
| G.4 | Backbone Comparison | reviewed unchanged | None identified in this source audit |
| H.1 | Predicate-Evaluator Validation | edited | None identified in this source audit |
| H.2 | False Positives and False Negatives | reviewed unchanged | None identified in this source audit |
| H.3 | Why RouterBSI Trails SkillRouter on Two Datasets | edited | None identified in this source audit |
| H.4 | Representative Predicate Decisions | reviewed unchanged | None identified in this source audit |
| H.5 | Routing Errors Within Downstream Disagreements | edited | None identified in this source audit |
| H.6 | Complete Downstream Results | edited | None identified in this source audit |

## Unresolved factual alignment

### INIT — evidence conflict
**Locations:** G.1; Figure 5 caption; sections/ablations.tex
The main caption and appendix agree textually on shared initialization. The separate artifact audit found different saved initial predicate libraries across the three Both Enabled runs, while the other configurations reuse the first run's library. Their historical binding to Figure 5 remains unresolved. The existing manuscript sentence is unchanged.
**Needed:** Immutable historical initialization bindings demonstrating that different runs produced Figure 5, or authorization for a truthful correction of the main caption and appendix.

### REPLAY — definition mismatch
**Locations:** A.2, A.3, A.5, D.1, D.3, G.2; Section 4.2 replay-set equation and replay description
Main defines the scoring set as two historical buckets, each bounded by N. Appendix includes the current task as well, with up to 2N+1 distinct tasks. Main also describes error over tasks retrieving the skill, while appendix history construction does not state that retrieval restriction. No scored task or bound was removed to force textual agreement.
**Needed:** Clarify the intended experimental definition and authorize any necessary main-text correction; no new run is automatically required.

### RANK — general rule mismatch
**Locations:** A.1; Sections 5.4 and 5.5 label-plus-retrieval-score rule
Appendix specifies selected-first lexicographic ranking. It explains equivalence to additive labels for SkillSight reciprocal-rank scores, but arbitrary raw-score addition is not generally equivalent across retrievers.
**Needed:** Confirm per-retriever scoring transformations or authorize a main-rule clarification.

### SPLIT — allocation-description mismatch
**Locations:** C.1; Section 5.1 per-dataset 70/15/15 statement
Appendix reports a constrained global 3491/748/748 allocation and non-70/15/15 per-dataset final counts. Numeric counts and coverage constraints were preserved.
**Needed:** Clarify target versus final per-dataset ratios in the main text; appendix wording now states the allocation without editorial precedence commentary.

### TRAIN — main-internal inconsistency
**Locations:** D.4; Section 5.4 trained retrievers versus Section 5.5 pretrained/lexical no-training statement
The frozen main paper gives incompatible retriever-training descriptions. Appendix reports concrete retrieval/evaluation settings without inventing task-split training.
**Needed:** Confirm actual fitting scope and authorize resolution of the main-text inconsistency.

## Retained qualifications

- **Backbone ceiling (G.4):** The appendix confirms the endpoint ordering and 99.64% ratio, consistent with rounded main values. These endpoints alone do not establish an irreducible capacity ceiling.

- **F1 and fixed-budget outputs (E.1 / H.5 / H.6):** Selected-set F1 differs from F1@k; top-k can pad or truncate the selected set. These explanations prevent misreading simplified main wording.

- **Token scope and uncertainty (E.1 / G.2 / G.3):** Recorded token counts are not complete cost accounts, single-run results are distinct from three-run component means, and model adjudication is not human-validated accuracy.

## Per-subsection evidence and actions

### A.1 Initialization and Online Routing
Source: `sections/appendix/procedure_routing.tex`
Main anchors: [{"file": "sections/method.tex", "lines": "16", "evidence": "The initial cold-start predicates \\(p_{si}\\) are generated from the skill key \\(K_{s}\\).", "excerpt_line": 16}, {"file": "sections/problem_definition.tex", "lines": "8", "evidence": "we only evaluate the predicates from skills in the top k based on retrieval score", "excerpt_line": 8}, {"file": "sections/experiments.tex", "lines": "47", "evidence": "The skill routing baselines are conditioned on a pool of retrieved 50 skills", "excerpt_line": 47}, {"file": "sections/experiments.tex", "lines": "47", "evidence": "we rank them by the sum of their binary label and the retrieval score", "excerpt_line": 47}]
Single predicate, public inputs, no evaluator gold labels, top-k-limited failure set, retrieval misses, and deterministic online commit ordering elaborate the main without conflict. Public name/description/body explain initialization inputs, while main K_s is not sufficiently defined to prove an inconsistency. Strict versus fixed-size ranking is essential; keep the lexicographic-versus-arithmetic qualification because unconditional agreement across all retrieval score scales is not established.

### A.2 Bounded Replay Construction
Source: `sections/appendix/procedure_replay.tex`
Main anchors: [{"file": "sections/method.tex", "lines": "28", "evidence": "\\mathcal{R}_s = \\{q_{rs}\\}\\cup\\{q_{is}\\}", "excerpt_line": 28}, {"file": "sections/method.tex", "lines": "44", "evidence": "across tasks where the skill is in the top \\(k\\)", "excerpt_line": 44}, {"file": "sections/method.tex", "lines": "56", "evidence": "\\arg\\min}_{m_p\\in M_p\\cup\\{p_f\\}} R_{\\mathrm{replay}}(m_p\\mid s_{fk})", "excerpt_line": 56}]
The bounded per-skill buckets, unbounded global lazy-materialization history, uniform-slot replacement (not reservoir sampling), deterministic order, duplicate handling, and prompt-example/scoring distinction are useful mechanics. Current-inclusive replay and its 2N+1 bound do not equal the main historical-only definition. The sentence asserting that main bounds refer only to retained history is an interpretation, not an established reconciliation. Preserve the truthful distinction pending main authorization; do not remove it as a code caveat.

### A.3 Candidate Admission and Minimum-Risk Selection
Source: `sections/appendix/procedure_mbr.tex`
Main anchors: [{"file": "sections/method.tex", "lines": "36", "evidence": "a max length \\(l\\)", "excerpt_line": 36}, {"file": "sections/method.tex", "lines": "56", "evidence": "\\arg\\min}_{m_p\\in M_p\\cup\\{p_f\\}} R_{\\mathrm{replay}}(m_p\\mid s_{fk})", "excerpt_line": 56}, {"file": "sections/method.tex", "lines": "28", "evidence": "\\mathcal{R}_s = \\{q_{rs}\\}\\cup\\{q_{is}\\}", "excerpt_line": 28}]
Candidate structural admission, separate unchanged candidate, binary mean-loss equation, and non-increasing average-risk argument agree with the main argmin. The qualifications that individual errors may trade off, ties need not improve, and no tie-break is prescribed accurately distinguish average-risk minimization from stronger per-example guarantees. Keep them: they are scientific, not saved-artifact caveats. Agreement of the loss formula does not settle the replay-set mismatch defined next door.

### A.4 Held-Out Gate and Partial Rollback
Source: `sections/appendix/procedure_validation.tex`
Main anchors: [{"file": "sections/method.tex", "lines": "80", "evidence": "R_v(m_p^*\\mid s_{fk})< R_v(p_{si}\\mid s_{fk})", "excerpt_line": 80}, {"file": "sections/related_works.tex", "lines": "8", "evidence": "Selected candidate is discarded by the held-out validation gate if its validation error is higher or equal to the initial predicate", "excerpt_line": 8}]
Strict cold-start comparison and rejection of ties agree with the main equation and method caption. Mean Boolean correctness equals 1 minus error. Per-skill rollback to iteration-start state, unsupported-skill rejection, non-monotonicity relative to the previous retained state, test exclusion, and pre-/post-rollback score distinctions are scientifically useful clarifications, not artifact-quality disclaimers. Main introduction/related-work prose uses looser higher-error phrasing, but the explicit main gate equation resolves ties strictly; do not weaken the appendix rule.

### A.5 Optimization Procedure
Source: `sections/appendix/procedure_algorithm.tex`
Main anchors: [{"file": "sections/method.tex", "lines": "56", "evidence": "\\arg\\min}_{m_p\\in M_p\\cup\\{p_f\\}} R_{\\mathrm{replay}}(m_p\\mid s_{fk})", "excerpt_line": 56}, {"file": "sections/method.tex", "lines": "80", "evidence": "R_v(m_p^*\\mid s_{fk})< R_v(p_{si}\\mid s_{fk})", "excerpt_line": 80}, {"file": "sections/related_works.tex", "lines": "8", "evidence": "Selected candidate is discarded by the held-out validation gate if its validation error is higher or equal to the initial predicate", "excerpt_line": 8}]
Optimization order, fixed corpus/partitions, task-level provisional commits, iteration-end gate and partial rollback are useful procedural details. The linked section is an appendix subsection, not the main text; delete only that erroneous adjective. Current-inclusive replay inherits the unresolved main-equation mismatch.

**Change:** Correct a cross-reference that identifies an appendix subsection as the main formulation.

Before:
```tex
The update loop below follows the main minimum-average-risk formulation in Section~\ref{app:procedure-mbr}.
```
After:
```tex
The update loop below expands the main minimum-average-risk formulation, with candidate selection detailed in Appendix~\ref{app:procedure-mbr}.
```

### B.1 Initial Predicate Generation
Source: `sections/appendix/prompts_initialization.tex`
Main anchors: [{"file": "sections/method.tex", "lines": "16", "evidence": "The initial cold-start predicates \\(p_{si}\\) are generated from the skill key \\(K_{s}\\).", "excerpt_line": 16}, {"file": "sections/method.tex", "lines": "36", "evidence": "a max length \\(l\\)", "excerpt_line": 36}, {"file": "figs/mbr_replay_test_ndcg@1_std/description.text", "lines": "1", "evidence": "across three runs starting from the same initial predicates at iteration 0", "excerpt_line": 1}]
Single-user-message structure, JSON encoding, public inputs, strict one-string schema and length limit add reproducible detail. The editorial statement about preserving prompt wording can be removed without changing the template. The exact template remains untouched, and no assertion of identical initialization across runs should be imported from the blocked figure caption.

**Change:** Remove manuscript-production narration; preserve exact prompt and schema.

Before:
```tex
We preserve the prompt wording below, with paragraph wrapping for readability. 
```
After:
```tex
[removed]
```

### B.2 Replacement Proposals
Source: `sections/appendix/prompts_proposal.tex`
Main anchors: [{"file": "sections/method.tex", "lines": "36", "evidence": "a max length \\(l\\)", "excerpt_line": 36}, {"file": "sections/method.tex", "lines": "56", "evidence": "\\arg\\min}_{m_p\\in M_p\\cup\\{p_f\\}} R_{\\mathrm{replay}}(m_p\\mid s_{fk})", "excerpt_line": 56}, {"file": "sections/method.tex", "lines": "28", "evidence": "\\mathcal{R}_s = \\{q_{rs}\\}\\cup\\{q_{is}\\}", "excerpt_line": 28}]
Fields distinguish current relevance labels from prior predicate activations, immutable initial predicate from supplied current predicate, exact candidate schema, and trusted retry correction. Prompt instructions to correct the current case/preserve prior correct behavior are generation objectives, not extra hard eligibility constraints in the main average-risk argmin. Keep this distinction and every literal prompt/retry string; do not rewrite the prompt to imply the weaker selection guarantee.

### B.3 Boolean Predicate Evaluation
Source: `sections/appendix/prompts_evaluator.tex`
Main anchors: [{"file": "sections/method.tex", "lines": "16", "evidence": "The initial cold-start predicates \\(p_{si}\\) are generated from the skill key \\(K_{s}\\).", "excerpt_line": 16}, {"file": "sections/limitations.tex", "lines": "8", "evidence": "we keep the predicate checker's instructions fixed", "excerpt_line": 8}, {"file": "sections/method.tex", "lines": "56", "evidence": "\\arg\\min}_{m_p\\in M_p\\cup\\{p_f\\}} R_{\\mathrm{replay}}(m_p\\mid s_{fk})", "excerpt_line": 56}]
Exact task/predicate pair, single-Boolean schema, no gold relevance input and same evaluator for routing/replay explain the main predicate checker. The prompt asks for predicate truth independently of desirability, while the router uses that truth for selection; these are distinct stages, not a contradiction. Preserve every prompt token and output example.

### B.4 A Complete Replay Decision
Source: `sections/appendix/prompts_trace.tex`
Main anchors: [{"file": "sections/method.tex", "lines": "56", "evidence": "\\arg\\min}_{m_p\\in M_p\\cup\\{p_f\\}} R_{\\mathrm{replay}}(m_p\\mid s_{fk})", "excerpt_line": 56}, {"file": "sections/method.tex", "lines": "80", "evidence": "R_v(m_p^*\\mid s_{fk})< R_v(p_{si}\\mid s_{fk})", "excerpt_line": 80}, {"file": "sections/related_works.tex", "lines": "8", "evidence": "Selected candidate is discarded by the held-out validation gate if its validation error is higher or equal to the initial predicate", "excerpt_line": 8}]
Useful complete repair example: Candidate 2 has least risk but leaves positive errors, then passes a separate iteration-end gate against cold-start. The current question, predicates, candidates, labels, table values and validation counts must remain unchanged. No provenance-quality caveat should be deleted here: exact-versus-condensed text and pre-repair-versus-cold-start labels protect interpretation.

### C.1 Task Filtering and Split Construction
Source: `sections/appendix/data_splits.tex`
Main anchors: [{"file": "sections/experiments.tex", "lines": "12", "evidence": "We split each dataset into train, validation, and test splits with ratios of 70\\%, 15\\%, 15\\%, respectively.", "excerpt_line": 12}, {"file": "tables/skill_routing_performance_average/table.tex", "lines": "4", "evidence": "Average uses each retriever's task-weighted scores over 748 tasks.", "excerpt_line": 4}]
Filtering whole tasks, iterative low-frequency removal, constrained allocation, split seed, exact table, and shared skill vocabulary are useful scientific/reproducibility detail. The table total agrees with the main routing-table caption (748 evaluation tasks), but global-versus-per-dataset allocation is a real unresolved textual mismatch; do not force the exact table to match a simplified main description.

**Change:** Replace editorial precedence commentary with the actual allocation limitation; preserve counts and global-split definition.

Before:
```tex
The constraints can shift an individual dataset away from the global proportions, particularly when many skills have few examples; the exact counts therefore take precedence over an assumed per-dataset ratio.
```
After:
```tex
The coverage constraints can shift individual datasets away from the target proportions, particularly when many skills have few examples.
```

### C.2 Required-Skill Labels and Task Types
Source: `sections/appendix/data_labels.tex`
Main anchors: [{"file": "sections/experiments.tex", "lines": "12", "evidence": "Each instance is paired with annotated gold skill(s) and evaluated against a shared external skill corpus", "excerpt_line": 12}, {"file": "sections/experiments.tex", "lines": "20", "evidence": "Averages are measured across task instances.", "excerpt_line": 20}]
Useful elaboration: preserves whole multi-skill label sets; distinguishes annotation occurrences from unique skills and task counts; specifies precision/recall/F1 targets. Unannotated downstream usefulness is a necessary scientific distinction, not disposable artifact-quality language. No conflict with the main annotation-based evaluation description; no values changed.

### C.3 Shared Skill Corpus and Data Access
Source: `sections/appendix/data_corpus.tex`
Main anchors: [{"file": "sections/introduction.tex", "lines": "29", "evidence": "sharing a 26k skill corpus", "excerpt_line": 29}, {"file": "sections/experiments.tex", "lines": "12", "evidence": "Each instance is paired with annotated gold skill(s) and evaluated against a shared external skill corpus", "excerpt_line": 12}, {"file": "sections/ethics_statement.tex", "lines": "3", "evidence": "Reuse should respect dataset, skill, and model licenses", "excerpt_line": 3}]
Useful elaboration: exact 26,262 corpus entries distinguishes 636 original gold identifiers, 25,626 distractors, and 306 retained gold skills. The main rounded 26k statement is compatible. Access/package metadata and preservation of task-to-skill mappings support reproducibility, not caveats about saved result quality. Retain package MIT wording together with the component-license qualifications in data_scope; do not infer a uniformly MIT corpus.

### C.4 Dataset Coverage and Reuse
Source: `sections/appendix/data_scope.tex`
Main anchors: [{"file": "sections/ethics_statement.tex", "lines": "3", "evidence": "Bounded replay and held-out validation assess routing behavior rather than factual correctness, fairness, or safety.", "excerpt_line": 3}, {"file": "sections/ethics_statement.tex", "lines": "3", "evidence": "Reuse should respect dataset, skill, and model licenses", "excerpt_line": 3}, {"file": "sections/experiments.tex", "lines": "12", "evidence": "Each instance is paired with annotated gold skill(s) and evaluated against a shared external skill corpus", "excerpt_line": 12}]
Language limits, component-specific licenses, identifying-information risks, and untrusted executable content usefully elaborate the main ethics statement. Keep these factual scope/safety boundaries. The credential-file archive sentence is unrelated packaging/provenance commentary and can be deleted without weakening dataset privacy review. Rename the heading to make its dataset focus explicit.

**Change:** Use a scientific coverage heading rather than an artifact-audit heading.

Before:
```tex
\subsection{Artifact Coverage and Reuse}
```
After:
```tex
\subsection{Dataset Coverage and Reuse}
```

**Change:** Remove software-packaging aside while retaining privacy, license and safety scope.

Before:
```tex
Credential-file exclusion from a software archive is distinct from reviewing and de-identifying task content or model traces. 
```
After:
```tex
[removed]
```

### D.1 Shared Configuration
Source: `sections/appendix/implementation_settings.tex`
Main anchors: ["Experiments: Implementation Details (SkillSight, Qwen3.5-4B, 50 candidates, downstream k=5, temperatures, 10 iterations)", "Method: bounded replay N, generated candidates M_p, predicate limit l"]
RETAIN: shared settings, embedded table, unchanged-predicate option, character rather than token limit, current-inclusive replay bound, and distinct retrieval/downstream budgets are useful methodology. Preserve every setting and numeric value. Single-predicate validation specialization is explained by the referenced appendix; do not substitute a different objective.

### D.2 Requests, Caching, and Reproducibility
Source: `sections/appendix/implementation_runtime.tex`
Main anchors: ["Experiments: Implementation Details (proposal temperature 1; evaluation temperature 0)", "Method: sequential recursive updates; Limitations: computational cost"]
EDIT: remove only the legacy-field/request-wrapper implementation-history sentence. KEEP request schema, effective temperatures, model-specific reasoning parameters, timeouts, retry exhaustion, overflow behavior, concurrency without task-order changes, cache semantics, and initial-library/prompt binding: these describe reproducibility-relevant behavior, not artifact-quality assurances.

**Change:** Remove legacy-code commentary; effective temperature already stated.

Before:
```tex
 In the active proposal branch, the request wrapper sets temperature one explicitly; a legacy proposal-temperature configuration field does not override this branch.
```
After:
```tex
[removed]
```

### D.3 Controlled Method Variants
Source: `sections/appendix/implementation_variants.tex`
Main anchors: ["Ablations: Impact of MBR based on Replay and Held-out Validation Gate", "Ablations: Performance and Token Usage Tradeoff", "Method: bounded replay and held-out gate"]
RETAIN: capacity and candidate-budget settings; no-gate rollback semantics; no-MBR still uses historical context; replay-F1 zero-denominator convention and distinction from Boolean error; single-predicate validation equivalence. These prevent the ablations being misread as removing all history or changing the default loss.

### D.4 Retrieval and Evaluation Software
Source: `sections/appendix/implementation_software.tex`
Main anchors: ["Experiments: Baselines and Implementation Details", "Experiments: Evaluation Metrics and Benchmarks and Skill Corpus"]
EDIT: neutralize three repository-local "in-tree" qualifiers. KEEP tokenizer, model, scoring, rank-score exposure, reranker input truncation, precision, task-specific evaluation rules/tolerances, resource limits, ToolQA demonstrations, and split solver details. These are useful operational methodology, not removable provenance. All three paragraphs explicitly covered: Retrieval and reranking; Task evaluation; Examples and split construction.

**Change:** Remove repository-relative provenance adjective.

Before:
```tex
The in-tree SRA BM25 implementation
```
After:
```tex
The SRA BM25 implementation
```

**Change:** State evaluation protocol positively; subsequent exact rules preserve the scientific distinction.

Before:
```tex
We use the in-tree SRA task evaluators rather than a single exact-match rule for every benchmark.
```
After:
```tex
We use benchmark-specific SRA task evaluators.
```

**Change:** Remove repository-relative provenance adjective; retain demonstrations and citation.

Before:
```tex
ToolQA's in-tree ReAct prompt
```
After:
```tex
ToolQA's ReAct prompt
```

### E.1 Ranking and Selection Metrics
Source: `sections/appendix/routing_metrics.tex`
Main anchors: ["Experiments: Evaluation Metrics (per-task averages)", "Experiments: Baselines/Implementation Details (strict versus top-k routing)", "Main table tab:skill_routing_performance_average (task-weighted 748-task scores; equal retriever means)", "Main ablation figure fig:mbr_replay_test_ndcg@1_std (three-run variation)"]
RETAIN: nDCG/recall/F1 definitions, ranked-versus-selected distinction, task weighting, and retriever averaging. Statistical reporting is required-useful uncertainty, not process narration: single evaluations, non-seed repetitions, common replay seed, population SD rather than SE/CI, absent run-to-run estimates and absent significance tests must remain. Do not rewrite set-level F1 as fixed-cutoff F1 merely because the main overview uses F1@k.

### E.2 Results by Benchmark and Retriever
Source: `sections/appendix/routing_results.tex`
Main anchors: ["Results: Skill Routing Performance (TheoremQA and MedCalc-Bench exceptions)", "Main table tab:skill_routing_performance_average"]
RETAIN: benchmark/retriever decomposition, exact illustrative endpoints, TheoremQA SkillRouter advantage and Vector MedCalc-Bench boundary. These qualify the aggregate claim and should not be removed as negative results. All three included routing tables explicitly covered.

### F.1 Coverage and Retention
Source: `sections/appendix/retention_definition.tex`
Main anchors: ["Experiments: Evaluation Metrics (Ret@k)", "Results: Required Skill Retention", "Main figure fig:average_recall_degradation (retention mean across retrievers)"]
RETAIN: ratio of task-mean recalls, then equal averaging of three retriever-specific ratios. Each method has its own Recall@50 denominator, including SkillDAG expanded ranking. Preserve the distinction from averaging task-level ratios and from end-to-end recall. These are essential estimand/candidate-pool qualifications that make the compressed main wording interpretable.

### F.2 Results Across Routing Budgets
Source: `sections/appendix/retention_results.tex`
Main anchors: ["Results: Required Skill Retention", "Abstract/Introduction: RouterBSI 90.5% retention", "Main figure fig:average_recall_degradation"]
RETAIN: RouterBSI 90.5%/94.6% and SkillRouter 83.9%/87.9% comparisons, SkillDAG coverage-versus-ordering boundary, and fixed-ranking-prefix interpretation. The statement that updater reruns are not required explains what varying k measures and is useful methodology, not removable process history.

### G.1 Replay and Held-Out Gate
Source: `sections/appendix/ablation_components.tex`
Main anchors: ["sections/ablations.tex: Impact of MBR based on Replay and Held-out Validation Gate", "sections/method.tex: Held-Out Validation and Recursive Improvement", "figs/mbr_replay_test_ndcg@1_std/description.text"]
Covered configuration definition, endpoint table/caption, initialization/trajectory paragraph, gate rule, and admission-count paragraph. Endpoint means support main ordering and gains. Preserve task-weighted test means, three-run population SD, selected-set F1 versus ranking metrics, strict improvement over initialization, rollback on ties/absent support, and possible worsening relative to previous policy. The admission counts sum to 12,390; these are decisions rather than distinct skills. No scientific qualification is merely artifact clutter.

### G.2 Token Accounting and Replay Capacity
Source: `sections/appendix/ablation_cost_capacity.tex`
Main anchors: ["sections/ablations.tex: Performance and Token Usage Tradeoff of MBR Replay and Held-out Gate", "figs/performance_token_usage/table.tex", "sections/method.tex: MBR Update Selection with Bounded Replay"]
Covered accounting paragraph, single-run component table/caption, replay-capacity paragraph, and sensitivity table/caption. Main cost figure is a single-run comparison, not the three-run component means. Keep known-token scope, unavailable-usage counts, retry/cache treatment, phase definitions, and per-class capacity interpretation. Preserve all initialization wording unchanged. Sensitivity is metric-dependent and does not conflict with the main method.

**Change:** Use experimental terminology instead of saved-snapshot terminology.

Before:
```tex
Quality is measured on the final-test snapshot over 748 tasks.
```
After:
```tex
Quality is measured on the final policy over 748 test tasks.
```

### G.3 Candidate-Pool Size and Token Usage
Source: `sections/appendix/ablation_candidate_pool.tex`
Main anchors: ["sections/experiments.tex: Implementation Details.", "sections/ablations.tex: Performance and Token Usage Tradeoff of MBR Replay and Held-out Gate", "figs/performance_token_usage_by_topk/description.text"]
Covered candidate-versus-selected-budget definition, task-instance aggregation, all three measured endpoints, and token-accounting/comparison scope. K=10/25/50 is a sensitivity study around the default top-50 pool, not a contradiction. Keep known tokens versus full/per-query costs and the absence of a controlled budget-matched comparison. Do not alter initialization claims.

**Change:** Use experimental terminology instead of saved-snapshot terminology.

Before:
```tex
quality is measured on the final-test snapshot over 748 tasks
```
After:
```tex
quality is measured on the final policy over 748 test tasks
```

### G.4 Backbone Comparison
Source: `sections/appendix/ablation_backbones.tex`
Main anchors: ["sections/ablations.tex: Skill Routing Performance across LLM Backbones", "figs/routing_performance_across_llms_init/description.text"]
Covered full paragraph, all initial/final/reference rows, caption, and within-stage ranking marks. Main and appendix agree on all displayed nDCG@1 endpoints, improvement of every backbone, and nonmonotonic final performance. The appendix 99.64% and main 99.6% have compatible display precision; do not recompute from rounded endpoint cells. Keep single-run/748-task/ten-iteration scope.

### H.1 Predicate-Evaluator Validation
Source: `sections/appendix/evaluator_validation.tex`
Main anchors: ["Limitations: fixed predicate-checker instructions and checking errors", "Experiments: Evaluation Metrics; Method: predicate-based skill routing"]
EDIT: delete only the checksum/journal/request-payload verification sentence. This active subsection is H.1, not D.5. KEEP the named adjudicator, observed saved Boolean/non-blinding, predicate-satisfaction rather than relevance target, unique-review versus occurrence weighting, class imbalance, provisional-reference recall, always-False comparison, stratified second-pass design, previous-sample exclusion, blinded assessment, ambiguous/likely-incorrect outcomes, AI-not-human status, lack of True checks, and nonrepresentative-sample limits. These qualifications are necessary to prevent 97.10% agreement being presented as human accuracy.

**Change:** Remove artifact-integrity assurance from scientific results; preserve sampling, weighting, blinding and agreement scope.

Before:
```tex
 Source checksums, journal-record hashes, request payloads, and occurrence-weighted counts were verified before tabulation.
```
After:
```tex
[removed]
```

### H.2 False Positives and False Negatives
Source: `sections/appendix/error_counts.tex`
Main anchors: ["sections/problem_definition.tex: missing required or selected irrelevant skills", "sections/results.tex: MedCalc-Bench and TheoremQA exceptions", "sections/limitations.tex: annotation and checker limitations"]
Covered both set definitions, full confusion-count table/caption, error-direction paragraph, retrospective attribution definitions, and complete attribution table/caption. Explicit nonstandard FP/FN definitions are essential because numeric column labels use the authors' convention; do not silently standardize them. Preserve candidate rejection versus retrieval miss, pooled observations versus distinct tasks, and retrospective interpretation versus checker-generated explanation. Error shares reproduce 62.24% and 79.81%; attribution counts sum to 331. No change needed.

### H.3 Why RouterBSI Trails SkillRouter on Two Datasets
Source: `sections/appendix/error_routing_gap.tex`
Main anchors: ["sections/results.tex: Skill Routing Performance, 5.01%/6.10% deficits", "sections/limitations.tex: annotation quality and checker interpretation", "sections/ablations.tex: observed late-iteration plateau"]
Covered introduction, matched-ranking table/caption, Required-skill nonactivation, Predicate design versus checker judgments and attribution table, examples, and Implications for refinement. The diagnostic matches the main dataset exceptions and expands them without claiming downstream causality. Preserve task/retriever denominators, gross versus net loss, uncertainty in semantic assessments, and untested human-edit/training interventions. Late changes and restrictive-versus-checker distinctions are useful evidence, not artifact-quality caveats.

**Change:** Move task-provenance out of manuscript source; original remains in revision snapshot.

Before:
```tex
% Evidence: ../.wisc/verification/routerbsi-exception-investigation/
% analysis.json, independent_verification.json, theoremqa/summary.json,
% medcalc/summary.json, and trajectory_spotcheck.json.

```
After:
```tex
[removed]
```

**Change:** Remove archive/process qualifier; preserve noncausal status.

Before:
```tex
These are retrospective archived-run diagnostics, not new intervention results.
```
After:
```tex
These are retrospective diagnostics, not intervention results.
```

**Change:** Replace snapshot terminology with the measured policy state.

Before:
```tex
Accepted-policy test snapshots show mixed late progress:
```
After:
```tex
Test results for the retained policies show mixed late progress:
```

### H.4 Representative Predicate Decisions
Source: `sections/appendix/error_examples.tex`
Main anchors: ["sections/results.tex: MedCalc-Bench and TheoremQA exceptions", "sections/limitations.tex: incorrect predicate interpretation"]
Covered Representative Predicate Decisions and all four paragraphs: nonrequired business skill accepted for Newton-Raphson, required de Broglie skill rejected, restrictive P/E predicate, and calcium-correction judgment. Preserve quoted predicates, saved Boolean observations, nonstandard labels explained in preceding subsection, and explicit excerpt qualification. These are useful distinct scientific examples, not documentation of code-artifact quality. No changes proposed.

### H.5 Routing Errors Within Downstream Disagreements
Source: `sections/appendix/error_downstream.tex`
Main anchors: ["sections/results.tex: Downstream Performance", "sections/experiments.tex: Baselines and Implementation Details."]
Covered cohort definition, every conditional-table row and caption, extra-selection-share paragraph, and required-skill-coverage/comparator paragraph. It distinguishes actual supplied top-five skills from predicate decisions and routing correctness from downstream success. Keep noncausal interpretation, one-gold/five-supplied context, and conditioned/pooled denominators. Conditional shares reproduce 94.68% and 93.75%.

**Change:** Remove irrelevant archive qualifier while retaining denominators and interpretation.

Before:
```tex
These archived extra-selection shares
```
After:
```tex
These extra-selection shares
```

### H.6 Complete Downstream Results
Source: `sections/appendix/error_downstream_results.tex`
Main anchors: ["sections/results.tex: Downstream Performance", "sections/experiments.tex: Evaluation Metrics. and Baselines", "figs/downstream_average/description.text"]
Covered subsection prose, strict/top-five/direct/oracle definitions, mean-versus-benchmark distinction, and both table inputs. Definitions agree with main; two tables follow, so singular introduction is stale.

**Change:** Two included tables follow; correct the stale singular reference.

Before:
```tex
The following table reports downstream task-success rates by benchmark and retriever,
```
After:
```tex
The following tables report downstream task-success rates by benchmark and retriever,
```
