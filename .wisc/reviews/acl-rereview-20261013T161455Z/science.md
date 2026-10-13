# RouterBSI: independent scientific rereview

**Paper-only verdict: borderline; overall 3/5, soundness 3/5, contribution 3/5.** These are internal integer scales, not official ARR scores. No confirmed fundamental validity blocker was found. The artifact-binding question is separate and does not affect these scores.

**Target:** `/workspace/storage/healthcare_workspace/project_skill_selection/RouterBSIPaper/.wisc/reviews/acl-rereview-20261013T161455Z/source/main.pdf` (31 pages); SHA-256 `ddd4e45dcc8920cde89966c50e5a12598d73eee2dda1701b67f783057aeb1e63`. Anchors below use 1-based source lines relative to the review directory and PDF page numbers.

## Credit for the current revisions

- **Current-task replay inclusion is repaired in the main method.** source/sections/method.tex:24–29, PDF p.4: the scoring set includes the current task, is deduplicated by task identifier, and is bounded by 2N+1.
- **Constrained global splits and the represented-skill adaptation scope are now clear.** source/sections/experiments.tex:12, PDF pp.4–5; appendix/data_splits.tex:3–7, p.16. The split is globally targeted rather than independently 70/15/15 within each dataset. Shared skill vocabulary is deliberate, not train/test task overlap.
- **Frozen retrievers and released SkillRouter are explicitly disclosed.** source/sections/experiments.tex:39,47, PDF p.5. No task-split fine-tuning is assumed or alleged.
- **Binary-label plus normalized-score ranking is coherent.** source/sections/experiments.tex:47, PDF p.5; appendix/procedure_routing.tex:18, p.11. Scores lie in [0,1] and ties favor selected skills, matching the lexicographic description.
- **Shared initialization is treated as textually consistent.** Figure 5 caption, appendix/ablation_components.tex:25, and appendix/ablation_cost_capacity.tex:2 agree. Slightly varying reported initial evaluations do not prove different predicate text. No historical saved-library mismatch is asserted.
- **Gate, checker, downstream, and cost qualifications are substantially improved in the appendix.** A.3–A.4 distinguish replay risk from per-example preservation and cold-start from previous-predicate comparisons; E.1 discloses single-run limits; H.1 distinguishes agreement from accuracy; H.3/H.5 avoid untested causal explanations; G.2–G.3 qualify token-accounting scope.

## Prioritized issues

### SCI-001 — MAJOR: Headline comparisons lack uncertainty over tasks and optimization runs

**Anchor:** `source/sections/appendix/routing_metrics.tex:25`, PDF p. 19, Appendix E.1 Statistical reporting.

> The main routing, recall/retention, and downstream comparisons use one evaluation per method--retriever setting, rather than an average over repeated runs.

**Finding.** Single-run headline estimates cannot establish the robustness of rankings or small downstream differences, and the uncertainty limitation is not visible beside the main results.

1. Appendix E.1 explicitly states that routing, retention, downstream, cost, capacity, pool-size, and backbone comparisons are single-run; cross-retriever averaging is not replication.
2. Initialization and proposals are stochastic, while the ablation repetitions share one replay-replacement seed and do not measure replay-seed sensitivity.
3. The main Table 1 and Figure 4 give point estimates without paired task-level intervals. This matters particularly for the downstream 0.611 versus 0.602 comparison and claims about near-equal backbone endpoints.
4. This is an evidence-strength limitation, not evidence that reported gains are false, that a significance test is universally mandatory, or that the existing three-run ablation is invalid.

**Counterevidence / scope limits:**
- The paper now discloses these limitations accurately in E.1, including the distinction between standard deviations, confidence intervals, and independent seeds.
- Figure 5 and Tables 10–11 provide three-run component-ablation means and dispersion; complete trajectories use a fixed iteration-10 endpoint rather than the best test checkpoint.
- Routing gains are often substantial and appear across several retrievers and datasets, so uncertainty does not erase all empirical support.

**Additional exact anchors:**
- `source/sections/appendix/routing_metrics.tex:25`, PDF p. 20: “These deviations describe dispersion among run-level scores, not standard errors or confidence intervals, and the repetitions are not distinct-seed trials.”
- `source/sections/appendix/downstream_mean_table.tex:15`, PDF p. 30: “$\mathrm{RouterBSI}_{\mathrm{top}5}$ & \underline{0.606} & 0.599 & 0.627 & \underline{0.611} \\”

**Fix:** Move a compact single-run/repeated-run disclosure into Section 5 and the Table 1/Figure 4 captions. If saved per-task outputs are available, report paired task-level confidence intervals for the principal differences, preserving repeated observations of the same task across retrievers and the stated dataset weighting; explain that these intervals condition on the fitted policies. For robustness over training, add independently seeded end-to-end repeats for RouterBSI and the strongest comparable optimizer when feasible, distinguishing initialization, proposal, and replay randomness. If no new evidence is available, retain descriptive point-estimate language and explicitly leave run-to-run robustness unresolved.

**Acceptance:**
- Main text identifies which comparisons use one run and which use three.
- Any task-level interval describes its resampling unit and does not count three retrievers as three independent task samples.
- Any seed-robustness claim has independently seeded results; otherwise the unresolved limitation is explicit.

**Inputs needed:** Saved paired per-task outputs for intervals; new independent repeats only if a run-robustness claim is retained.

### SCI-002 — MAJOR: Baseline adaptation and resource matching are not sufficiently documented to isolate method advantage

**Anchor:** `source/sections/experiments.tex:39`, PDF p. 5, Section 5.4 Baselines.

> SkillRouter likewise uses its released reranker checkpoint without fine-tuning on our task-training split.

**Finding.** The comparison establishes observed performance against the chosen deployed baselines, but does not isolate the benefit of the proposed optimizer from task-specific supervision, adaptation budget, and incompletely specified non-parametric baseline training.

1. The current main text clearly and correctly says the retrievers and SkillRouter are frozen on this task split, whereas RouterBSI adapts for ten iterations using task labels and validation admission.
2. Frozen off-the-shelf baselines are legitimate practical references, but their scores alone do not establish superiority over a comparably adapted routing system.
3. SkillDAG and Skill-Pro are named as optimization baselines, yet the supplied main text and appendix do not specify their complete adaptation objective/feedback, training passes, stopping or checkpoint selection, and optimization cost. The detailed software subsection covers retrieval/reranking and evaluators, not this missing optimizer protocol.
4. This missing information limits reproducibility and attribution of the claimed advantage over alternative non-parametric optimizers; it does not demonstrate that those implementations were unfair.

**Counterevidence / scope limits:**
- The frozen-checkpoint status is now explicit: there is no remaining ambiguity about whether SkillRouter or retrievers were fine-tuned.
- The main text reports a shared top-50 pool, the SkillDAG expansion exception and its ranking rule; Appendix H.3 verifies identical ordered top-50 candidates for the matched two-dataset SkillRouter analysis.
- RouterBSI initialization/final comparisons and the component ablation already provide useful within-method controls.
- A same-data neural fine-tuning experiment is not mandatory if the claim is limited to black-box adaptation versus the reported deployed configurations.

**Additional exact anchors:**
- `source/sections/experiments.tex:47`, PDF p. 6: “RouterBSI is optimized for 10 iterations.”
- `source/sections/appendix/implementation_software.tex:6`, PDF p. 19: “SkillRouter uses the released 0.6B reranker~\citep{zheng2026skillrouter}.”
- `source/sections/results.tex:9`, PDF p. 6: “Compared to the other non-parametric optimization baselines, RouterBSI has a mean 29.2\% and 26.7\% nDCG@10 score over SkillDAG and Skill-Pro, respectively.”

**Fix:** Add a baseline protocol table covering each method’s checkpoint/backbone, permitted training/validation labels, mutable state, feedback/objective, iterations or stopping rule, checkpoint choice, candidate and supplied-skill budgets, and optimization/inference cost. Describe the Skill-Pro and SkillDAG adaptations sufficiently to rerun them, including intentional deviations from their original settings. Explicitly frame frozen SkillRouter as an off-the-shelf reference. To claim optimizer superiority rather than a deployment comparison, add a comparably supervised, budget-reported optimizer control, or narrow the claim to the measured configurations; do not imply fine-tuning occurred.

**Acceptance:**
- Skill-Pro and SkillDAG adaptation settings are specified rather than inferred from citations.
- The training-signal and resource differences are stated next to the comparison.
- Broad claims of optimization superiority are supported by an appropriate control or narrowed to the tested configurations.

**Inputs needed:** Actual baseline training configurations and cost records; a new matched-adaptation control only for a stronger attribution claim.

### SCI-003 — MAJOR: Predicate-fidelity evidence is load-bearing but remains appendix-only and model-adjudicated

**Anchor:** `source/sections/introduction.tex:42`, PDF p. 2, Introduction contribution 1.

> making routing criteria interpretable and directly editable without updating the underlying language model.

**Finding.** The main paper presents predicates as interpretable routing criteria without exposing the appendix’s substantial predicate-positive disagreement, which limits how faithfully predicate text explains the actual selector.

1. Appendix H.1 reports 97.10% pooled agreement, but only 59.93% agreement for saved True decisions and 53.71% positive recall relative to a provisional model adjudicator; an always-False predictor would obtain 96.47% pooled agreement.
2. The initial adjudicator saw the saved labels. The additional blinded AI review is small, is not human validation, and contains no approved True cases in its correct stratum.
3. These results do not establish human-ground-truth checker accuracy. They do show that positive-case semantic fidelity is uncertain and that an inspectable predicate is not automatically a faithful explanation of an executed decision.
4. This materially qualifies the interpretable-routing contribution and the attribution of failures to predicate scope versus checker behavior. The main limitations acknowledge checker errors generally but omit the quantitative diagnostic and its implications.

**Counterevidence / scope limits:**
- H.1 now carefully separates model agreement from accuracy, reports class imbalance, and explicitly states the lack of human validation; it does not misuse the pooled figure as validated accuracy.
- H.3–H.4 provide concrete checker-error versus restrictive-predicate examples and appropriately mark retrospective attributions as fallible.
- The routing metrics against released required-skill annotations remain valid measurements of output behavior; disagreement with an adjudicator does not invalidate them.
- Explicit natural-language predicates remain inspectable and editable even when execution is imperfect.

**Additional exact anchors:**
- `source/sections/appendix/evaluator_validation.tex:9`, PDF p. 24: “agreement is 35,606/36,217 for saved False decisions (98.31\%) but 709/1,183 for saved True decisions (59.93\%).”
- `source/sections/appendix/evaluator_validation.tex:11`, PDF p. 24: “These judgments are AI-assisted qualitative checks, not human validation.”

**Fix:** Promote a short diagnostic paragraph into the main results or discussion, with the pooled and saved-True agreement rates, the always-False comparison, and the model-adjudicated/non-human qualification. Distinguish textual inspectability from faithful execution and keep semantic failure attributions provisional. If reliable predicate execution or human interpretability is a central positive claim, conduct an independently blinded human assessment stratified over saved True/False and adjudicator agree/disagree cases, or narrow that claim without adding a study.

**Acceptance:**
- Main paper contains the positive-class caveat and labels all rates as model-adjudicated agreement, not ground-truth accuracy.
- Interpretability wording distinguishes editable text from faithful checker execution.
- No failure-cause or accuracy claim relies solely on the non-blinded adjudicator as ground truth.

**Suggested text:** Predicates are directly inspectable and editable, but their execution is not guaranteed to follow their apparent semantics. In one final-run diagnostic, model-adjudicated agreement was 97.10% overall but 59.93% for saved True decisions; an always-False predictor would reach 96.47% overall. These are model-agreement rates, not human-validated accuracy.

### SCI-004 — MINOR: Main gate narrative needs the already-documented limits of its regression control

**Anchor:** `source/sections/introduction.tex:25`, PDF p. 2, Section 1.

> independently checked for generalization.

**Finding.** The main narrative can be read as stronger regression protection than the empirical cold-start-relative gate provides; the explicit limits and observed accepted regressions appear only in the appendix.

1. The main equation correctly compares a changed predicate with its fixed initialization, not the previously accepted predicate.
2. Appendix G.1 reports 262 accepted decisions that score below the previous predicate, despite improving on initialization. Appendix A.4 explicitly explains this behavior.
3. The same validation set repeatedly selects retained updates across ten passes; it is held out from proposal examples but participates in adaptive model selection and is not a fresh independent generalization test each pass.
4. The replay inequality is local to the current retained scoring set and permits trading individual errors. These facts do not contradict the algorithm, but should constrain the main narrative about retaining prior corrections and unseen-task regressions.

**Counterevidence / scope limits:**
- Section 4.3 already gives the correct strict cold-start comparison; no proposed issue claims that its equations promise previous-iteration monotonicity.
- Appendices A.3–A.4 and G.1 candidly document replay tradeoffs, partial rollback, missing validation support, and nonmonotonicity.
- The untouched test evaluation and component ablation provide empirical evidence that the gate improves aggregate final performance; there is no evidence here of test leakage.
- Repeated validation use is a normal model-selection practice, not itself an invalid protocol.

**Additional exact anchors:**
- `source/sections/appendix/procedure_validation.tex:19`, PDF p. 12: “Comparing to $p_{si}$ does not ensure monotonic validation performance relative to $p_s^{(i)}$.”
- `source/sections/appendix/ablation_components.tex:31`, PDF p. 21: “Of the retained decisions, 262 score below the previous predicate while still improving over initialization.”

**Fix:** Add two sentences to Section 4.3 explaining that the gate uses a repeatedly consulted validation set and compares to initialization, so it neither guarantees improvement over the previous accepted predicate nor unseen-task monotonicity. Summarize the 262 accepted prior-predicate regressions in the ablation discussion with their 2,299 retained-decision denominator. Keep unseen-task benefits empirical. No new experiment is required for this scoped correction.

**Acceptance:**
- Main text states the cold-start-relative, nonmonotonic scope explicitly.
- Any accepted-regression count is labeled a skill–iteration count rather than distinct skills.
- Validation is described as an adaptation gate and test as final generalization evidence, not interchangeable independent checks.

**Suggested text:** The gate compares each changed predicate with its cold-start baseline, not with the previous accepted predicate, and therefore need not make validation performance monotonic across iterations. The validation set is repeatedly used for update admission; generalization is assessed separately on the untouched test tasks.

### SCI-005 — MINOR: Downstream average hides the default-retriever reversal and cannot isolate dependency benefits

**Anchor:** `source/sections/results.tex:19`, PDF p. 6, Section 6.3.

> This finding suggests expanding selected skills to include dependent skills could improve downstream performance even if the dependent skills are not required.

**Finding.** Downstream evidence supports a modest cross-retriever mean improvement, not a consistent improvement at the default retriever or a tested mechanism for SkillDAG’s advantage.

1. Table 21 gives RouterBSI top-five 0.611 versus SkillRouter 0.602 in the cross-retriever mean, but under default SkillSight gives 0.627 versus SkillRouter 0.638 and the retriever alone 0.628.
2. SkillDAG’s 0.631 mean is measured with ten supplied skills while RouterBSI top-five uses five; the paper discloses this budget difference.
3. Different supplied budgets and skill composition prevent attributing SkillDAG’s advantage specifically to dependent skills. The oracle is an annotated-required-set reference, not an upper bound on useful context.
4. Because the claim is already hedged and routing is the main contribution, this is a scope/interpretation issue rather than a fundamental validity failure.

**Counterevidence / scope limits:**
- Section 6.3 correctly describes a mean, acknowledges SkillDAG as the stronger downstream baseline, and uses hypothetical language for dependency expansion.
- The complete appendix discloses all per-retriever and per-dataset outcomes rather than concealing reversals.
- H.5 explicitly states that non-gold supplied context does not by itself establish causation and that missing required skills cannot explain every failure.
- Section 5.5 already explains why SkillDAG uses ten skills; the remaining issue is causal comparability, not an undisclosed budget.

**Additional exact anchors:**
- `source/sections/appendix/downstream_mean_table.tex:11`, PDF p. 30: “SkillRouter & 0.578 & 0.590 & \underline{0.638} & 0.602 \\”
- `source/sections/experiments.tex:47`, PDF p. 6: “In downstream tasks, we use k = 5 skills for SkillRouter and $\mathrm{RouterBSI}_{\mathrm{top}k}$, and we set k = 10 for SkillDAG because k = 5 would match the retriever's performance.”

**Fix:** Add the default-SkillSight reversal to Section 6.3 and describe dependency expansion as an untested explanation confounded by the ten-versus-five skill budget. Call the oracle a gold-skill reference, not a ceiling. To make a mechanism claim, compare methods at matched skill/token budgets and intervene on dependent versus other added context; otherwise the textual scope correction suffices.

**Acceptance:**
- Section 6.3 reports 0.627 versus 0.638 under default SkillSight alongside the aggregate mean.
- The dependency interpretation explicitly notes the unequal supplied-skill budgets and remains a hypothesis.
- No generic downstream-superiority or oracle-upper-bound claim is introduced.

**Suggested text:** The downstream gain is not uniform across retrievers: with default SkillSight, RouterBSI top-five obtains 0.627 success versus 0.638 for SkillRouter and 0.628 for the retriever alone. SkillDAG supplies ten skills rather than five, so its stronger mean motivates, but does not establish, a benefit from dependency expansion.

### SCI-006 — MINOR: Three backbone endpoints do not establish a model-insensitive predicate ceiling

**Anchor:** `source/sections/ablations.tex:24`, PDF p. 7, Section 7.3.

> They also suggest that predicates reach a plateau that cannot be overcomed with more capable LLMs, where it's difficult for the predicate to be narrow enough to be false for irrelevant tasks but broad enough to be true for all relevant tasks

**Finding.** The claimed ceiling and narrow-versus-broad predicate explanation exceed what three single-run model endpoints establish.

1. Figure 7 compares one initial and one final endpoint for each of three backbones, not a controlled scaling curve or a test of an inherent representation limit.
2. The middle-sized model is the best final performer; the small model nearly matches the largest only in one ranking metric. This establishes nonmonotonic observed endpoints, not that more capable models cannot improve.
3. Checker errors, proposal quality, optimization budget, and predicate length can all affect these outcomes, so the hypothesized breadth tradeoff is not identified by this comparison.
4. A local plateau over iterations also does not establish a universal ceiling across model capabilities.

**Counterevidence / scope limits:**
- The paper accurately reports all three values, openly states the nonmonotonic ordering, and frames the last sentence with “suggest.”
- All three backbones improve over initialization; this legitimate empirical result survives removing the ceiling interpretation.
- Table 14 gives F1 and nDCG@10 as well as nDCG@1, preventing the near-equality claim from standing as the entire backbone analysis.

**Additional exact anchors:**
- `source/sections/appendix/ablation_backbones.tex:1`, PDF p. 22: “\subsection{Backbone Comparison}”

**Fix:** Replace the ceiling sentence with a direct observation about nonmonotonic final nDCG@1 across these three runs and mark the breadth tradeoff as an untested hypothesis if retained. Remove “significantly” unless used explicitly in a non-statistical sense or backed by an uncertainty analysis. No new experiment is needed to preserve the supported backbone result.

**Acceptance:**
- No sentence states or implies that more capable models cannot surpass the observed endpoints.
- The result is scoped to the three measured backbones and one run per configuration.
- Any explanation involving predicate breadth is labeled untested rather than established.

**Suggested text:** Final nDCG@1 is nonmonotonic across these three backbones: Qwen3.8 27B performs best, while Qwen3.5 4B and GPT-OSS 120B have similar endpoints in these single runs. This comparison does not establish a model-independent ceiling or identify its cause.

## Score rationale

- **Soundness 3/5:** The current method is coherent and the paper provides broad routing evidence, a three-run component ablation, exact split counts, and honest diagnostics. The repaired replay and split descriptions remove prior ambiguities. Main comparisons remain single-run, baseline adaptation/resource matching is insufficiently specified, and the predicate-fidelity diagnostic limits semantic interpretations. No fundamental invalidity is established from this snapshot.
- **Contribution 3/5:** Editable natural-language applicability predicates with bounded per-skill replay and a held-out admission gate are a useful, substantive language-agent routing contribution, supported across six datasets and multiple retrievers/backbones. The selection rule is empirical risk minimization over generated candidates and the paper itself identifies closely related candidate/validation optimization in JTPRO. Present evidence supports a useful integration more clearly than a decisively new optimization principle or robust downstream improvement over strong adapted alternatives.
- **Overall 3/5:** Borderline on paper-only scientific quality: the current revisions deserve credit and the empirical result is plausible, but uncertainty, reproducible baseline adaptation, and main-text qualification of central claims keep it below a clearly competitive score of 4. Most interpretation defects can be corrected using evidence already in the appendix; stronger comparative claims require additional evidence.
- **Presentation 3/5:** Main structure and central equations are understandable, and the appendix is unusually explicit about limitations. Important uncertainty and positive-class fidelity results remain appendix-only, while some main interpretations exceed the evidence. This score is not a visual-layout or policy audit.
- **Confidence 4/5:** Read the supplied extracted PDF across all scientific sections and the source/appendix at the cited anchors. Conclusions are grounded in the current snapshot; no implementation, raw prediction, external citation, or artifact-binding re-audit was performed.

## Scope and completion

- Read the current extracted PDF and source/appendix. All six issues have checked verbatim source anchors, PDF pages, counterevidence, executable fixes, and acceptance criteria.
- Rechecked all 169 files in the supplied snapshot manifest: no mismatches or missing files. This checks review-target stability, not historical artifact provenance.
- No manuscript changes, experiment execution, new policy research, raw-artifact re-audit, or external citation verification. Submission stage and edit/upload permissions remain unknown.
- This is a fresh assessment, not an invented numerical change from a prior review. Most wording/self-containment corrections can use existing appendix evidence; stronger robustness or causal claims need additional evidence.
- Created only `science.json` and `science.md` for this review.
