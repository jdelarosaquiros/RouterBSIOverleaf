# Fresh ACL/ARR critique — RouterBSI

**Internal overall: 3/5 — borderline, up from 2/5.** Internal editorial recommendation: borderline reject. These are not official ARR ratings or a prediction of acceptance.

The revised paper merits an internal overall score of 3/5 (borderline), up from 2/5. Replay membership, normalized ranking, global skill-balanced splits and frozen-retriever status are now explicit. The remaining material concerns are incomplete non-parametric baseline protocol reporting, comparison-level uncertainty and an unsupported backbone-ceiling inference. This is a manuscript assessment, not an official ARR rating or certification of historical experimental provenance.

| Dimension | Score / 5 |
|---|---:|
| Soundness | 3 |
| Presentation | 3 |
| Contribution | 3 |
| Overall | 3 |
| Confidence | 4 |

**Active findings: 8: 3 major, 5 minor, 0 confirmed blockers.**

## What improved

- Current-inclusive replay, deduplication, and the scoring bound are explicit.
- Normalized retrieval scores and selected-first tie handling are consistent.
- Global split targets, per-skill coverage, and the adaptation rationale are explicit.
- Retrievers and SkillRouter are explicitly frozen on the task-training split.
- The concurrent Table 1 caption now makes averaging and benchmark exceptions clearer.

These corrections are credited, not re-reported as unresolved contradictions. The remaining baseline issue concerns Skill-Pro/SkillDAG configuration, not whether SkillRouter was fine-tuned.

## Remaining major concerns

### ISSUE-006 — The paper does not specify the Skill-Pro and SkillDAG adaptation configurations sufficiently to reproduce or interpret the optimizer comparison.

**Location:** Section 5.4 Baselines, p. 5; `sections/experiments.tex:39`.

> SkillRouter likewise uses its released reranker checkpoint without fine-tuning on our task-training split.

1. Section 5 describes the frozen retrievers/SkillRouter and RouterBSI ten-iteration optimization clearly.
2. The same section names Skill-Pro and SkillDAG as non-parametric optimization baselines, but their adaptation settings, feedback use and checkpoint selection are not specified in the current source. Appendix D.4 details retrieval and task evaluation rather than those baseline protocols.
3. Baseline citations do not uniquely specify the adaptations to the shared skill pool and current split. This is a material reproducibility and interpretation gap, not proof of unfair implementation.

**Action:** Add a compact appendix baseline-protocol table reporting the actual Skill-Pro and SkillDAG feedback/objective, mutable state, training/validation data use, optimization budget or stopping rule, checkpoint choice, backbone and deliberate upstream deviations. Mark non-applicable fields explicitly for fixed graph construction or methods not trained in this study. Frame frozen SkillRouter as an off-the-shelf comparator, as the paper already does, and restrict superiority claims to the tested configurations. A new fine-tuned SkillRouter run is not required to fix this reporting issue.

### ISSUE-007 — The main comparative advantage is supported by point estimates without paired uncertainty for the reported method comparisons.

**Location:** 6 Results, p. 6; `sections/results.tex:9`.

> SkillRouter is the strongest routing baseline, yet RouterBSI the nDCG@1 and nDCG@10 is 10.9\% and 8.4\% higher on average.

1. Observed: Table 1 and Figure 4 report main competitor means; Appendix E.1 explicitly states one evaluation per method–retriever setting and no significance tests.
2. Internal scientific standard: task-matched comparisons should distinguish the observed effect from sampling and optimization variability; three retrieval conditions are not independent seed repetitions.
3. Counterevidence: the appendix transparently discloses the limitation, and Table 1 aggregates reproduce; the issue is inferential strength, not proven arithmetic error.
4. Consequence: the small downstream margins and per-dataset reversals have unknown comparative precision; the separate three-run component ablation does not quantify those gaps.

**Action:** Where saved task-level outcomes exist, compute paired task-bootstrap intervals for RouterBSI minus SkillRouter routing and downstream metrics, preserving retriever pairing and dataset weights. Report that these intervals condition on the observed fitted policies. State single-run scope in main text. If predictions are unavailable, keep comparisons explicitly descriptive; do not fabricate intervals or require arbitrary additional seeds.

### ISSUE-009 — Three backbone endpoints do not establish an irreducible predicate-capacity ceiling.

**Location:** 7 Ablations, p. 7; `sections/ablations.tex:24`.

> They also suggest that predicates reach a plateau that cannot be overcomed with more capable LLMs, where it's difficult for the predicate to be narrow enough to be false for irrelevant tasks but broad enough to be true for all relevant tasks

1. Observed: Figure 7 reports final nDCG@1 of 0.742, 0.802 and 0.745; the middle backbone has the strongest endpoint.
2. Internal scientific standard: a finite, single-run cross-model comparison cannot establish that greater capability cannot overcome a plateau or identify predicate expressivity as its cause.
3. Counterevidence: Section 7.3 correctly acknowledges nonmonotonic endpoints, and the 99.6% endpoint ratio is a valid descriptive comparison.
4. Consequence: the final mechanistic/scaling inference exceeds what those measurements distinguish from optimization, evaluator, task and model-family effects.

**Action:** Replace only the unsupported ceiling sentence with a measured-scope statement; retain the actual endpoints. No new experiment is required if the claim is narrowed.

## Minor concerns

| ID | Concern | Location |
|---|---|---|
| ISSUE-008 | The main cost trade-off omits the single-run and recorded-token scope that is supplied in Appendix G.2. | 7 Ablations, p. 7 |
| ISSUE-010 | The dependency explanation is not isolated from differing skill budgets and baseline mechanisms. | 6 Results, p. 6 |
| ISSUE-011 | The main metric shorthand does not distinguish selected-set F1 from ranked-cutoff metrics, and the retention aggregation is defined only in the appendix. | 5 Experiments, p. 5 |
| ISSUE-012 | Persistent grammatical and notation defects reduce clarity of the core method and figure captions. | 4 Method, p. 4 |
| ISSUE-013 | Figure 4 has an ungrammatical headline caption and unnecessarily small labels for a full-width chart. | 6.3 Downstream Performance, p. 7 |

Exact quotes, executable fixes, counterevidence where applicable, and acceptance criteria are in `REVIEW_JSON.json`.

## Strengths and contribution

- Explicit, editable routing criteria with a coherent risk-minimization and validation procedure (§4).
- Coverage across six task collections, three retrievers, strong frozen SkillRouter comparison, and separate routing/downstream measurements (§5–7).
- Table 1 aggregates reproduce from saved per-dataset means; RouterBSI leads the reported overall routing metrics while dataset reversals and SkillDAG downstream advantage are acknowledged.
- Appendix documents exact splits, prompts, settings, gate behavior and evaluator limitations, including class-imbalance and non-human-adjudication caveats.
- Recent corrections resolve the principal manuscript-internal setup inconsistencies.

## Self-containment and evidence scope

The core algorithm and setup are now understandable from the main paper. Add compact main-text statistical-scope, cost-scope and metric-definition statements rather than moving the whole appendix. Frozen off-the-shelf baselines are legitimate; the review does not require fine-tuning SkillRouter. No human study is required to establish that predicate text is inspectable. Faithful execution is a separate property, and the main Limitations already acknowledges checker error.

The historical initialization-binding question remains open. Figure 5 and Appendix G.1 agree textually; this review does not count an unverified historical binding allegation as a demonstrated manuscript contradiction. This is not a finding that the archived initialization issue has been settled.

## Submission and formatting checks

- **31 total pages; main content extends through page 8**, including Figures 5–7. This fits the assumed long-paper review budget. Actual venue/cycle/stage remain unconfirmed.
- A4, two-column prose, ACL review mode, page/line numbering and embedded fonts checked. All eight figures inspected; no new clipping or overlap in the revised Table 1 caption.
- Limitations and ethics precede references; appendix follows references in the same PDF.
- Current ARR instructions permit an acknowledgment containing only generative-AI disclosure. Actual AI-use scope and submission-checklist entries require author confirmation.
- Official style-file byte provenance, supplementary anonymity and submission-portal logistics remain unverified. These unknowns are not asserted policy violations.

## Suggested priority

1. Recover and document actual Skill-Pro/SkillDAG settings; do not invent defaults.
2. State single-run scope in main results. Use saved paired predictions for uncertainty if available; otherwise keep descriptive claims and acknowledge the limitation.
3. Replace the intrinsic-ceiling inference with the observed non-monotonic backbone result.
4. Apply approved minor metric/caption/copyediting changes and recheck the eight-page content budget.

Most prose corrections are small; baseline-record recovery and saved-output uncertainty analysis have unknown effort. No new model experiment is prescribed unconditionally. There is no verified deadline from which to infer whether a later cycle is necessary.

## Version and verification

- Reviewed current PDF SHA-256: `657b0b21b328fdf897d790d36506f640fc6a8c9cf263fd982456196a08ab4ae8`.
- Earlier snapshot retained under `source/`; current reviewed snapshot under `current_snapshot/`.
- A concurrent Table 1 caption/PDF update was detected and reconciled. It did not change results or the assessment.
- Review-authored manuscript edits: none. Training/evaluation runs: none. Saved Table 1 data were reaggregated, not rerun.
- Independent audits: `science.json`, `presentation.json`, `narrative.json`; final judgment is the reconciled parent review.
- Supporting checks: `verification.json`, `numeric_spotchecks.json`, `concurrent_changes.json`, `policy/`.
