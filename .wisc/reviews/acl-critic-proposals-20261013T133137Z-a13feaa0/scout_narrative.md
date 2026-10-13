# RouterBSI narrative, novelty and self-containment scout

**Outcome:** The language-agent applicability-predicate thesis is recoverable, and all three contribution themes are delivered and revisited. Six retained findings: four major scientific-description/claim issues and two minor alignment issues. Four additional refinements are optional. No missing baseline is established as mandatory.

**Scope:** Proposal-only review of `reviewed_main.pdf` (29 pages) and frozen `source/`; current manuscript read before prior review. No paper edits, builds, experiments, commits or uploads. Exact venue/cycle/stage and active page budget remain unknown. This scout supplies evidence to the parent review; it does not assign overall ARR scores.

## Do not reapply stale changes

- **Risk/gate equations are correct as written:** §4.2 explicitly averages replay error; §4.3 explicitly compares against the INITIAL predicate and rejects ties. No blanket mathematical caveat or comparator rewrite is requested.
- **Two PDF-only defects are already corrected in source.** Parent should group them into source/PDF synchronization, not redundant source edits.
- **Prior error-percentage issue is resolved.** The incorrect 94.68%/93.75% interpretation is gone from main; new H.3 includes a substantive matched-loss diagnosis.
- **Old ablation and token-init rationales are stale.** Current G.1/G.2 now say common initial predicates. Differing initial metrics remain an experimental reconciliation question, not proof that obsolete prose still describes the runs.
- JTPRO and SkillRouter are already cited. No human-edit study is required to support the narrow claim that text predicates are editable.

## PDF/source synchronization handoff

### VERSION-N1: The reviewed PDF still prints the wrong error direction, but the frozen source already fixes it.
- PDF p.2; `source/sections/related_works.tex:14`.
> RouterBSI ensures non-decreasing em- pirical error on the retained set while bounding re- play evaluation costs.
- Counterevidence: Source already says “RouterBSI ensures non-increasing empirical error on the retained set while bounding replay evaluation costs.”
- Proposal: Include in the parent source/PDF synchronization issue. After explicit build permission, rebuild from the approved current source and verify the PDF says non-increasing. Do not reapply a source edit or add equation caveats.
- Acceptance: Approved regenerated PDF matches the corrected non-increasing source wording.; No changes to the correct empirical-average risk equation.

### VERSION-N2: The reviewed PDF still states a stronger no-degradation objective, while the source has already narrowed it.
- PDF p.3; `source/sections/problem_definition.tex:8`.
> to correct the observed error without degrading previously learned or unseen routing decisions.
- Counterevidence: Source already says “to reduce average replay error while using held-out validation to limit regressions..”
- Proposal: Group with source/PDF synchronization; use the corrected source on an author-approved future build. The duplicate terminal full stop is optional copyediting. Do not revive blanket demands to restate replay-average or initial-predicate-gate caveats.
- Acceptance: Approved regenerated PDF contains the narrowed average-error/limit-regressions objective.; The cold-start comparator and risk equations remain unchanged.

## Retained findings

### NAR-001 — MAJOR: Core operational details in Appendix A change the replay set, rank ordering, and update timing stated or left ambiguous in the main paper.
**Anchor:** §4.2 MBR Update Selection with Bounded Replay, PDF p.4; `source/sections/method.tex:24–40`.
> For each skill, the replay set contains previously seen relevant and irrelevant tasks:

**Counterevidence considered:** §4.2 explicitly defines average Boolean replay error, includes the current predicate in the argmin, and states the correct local non-increase inequality. No rewrite of those equations is requested. §4.3 explicitly compares against the INITIAL predicate and rejects validation ties. The comparator is already correct; do not replace it with a previous-policy comparator or append blanket guarantee caveats. §5.5 already gives the 50-candidate pool and five-skill downstream budget; Appendix D.1 makes their distinction explicit. The issue is not that these values are absent everywhere.

**Evidence/reason:** Appendix A.2 p.11 (procedure_replay.tex:3,7–13) scores deduplicated H+ union H- union {q}, permitting 2N+1 tasks, and retains an unbounded global seen-task history. A.1 p.11 (procedure_routing.tex:18) explicitly rejects the main unnormalized score-sum wording for arbitrary retrieval scores. A.4 p.12 (procedure_validation.tex:3,12–21) gates after a full training pass and restores iteration-start predicates. These details affect the actual scientific algorithm, not merely implementation convenience.

**Minimal proposal:** Replace the main replay-set construction with the current-inclusive set and distinguish history capacity from total replay size. Replace the §5.4/5.5 arithmetic-sum wording with predicate-label-first lexicographic ranking. Add one sentence to §4.3 that gating occurs after a full training pass and restores the iteration-start predicate on rejection or absent support. Add one compact statement that the bounded objects are per-skill replay buckets/evaluations, not the global task history. Preserve the already-correct average-risk and initial-predicate gate equations.

**Acceptance:**
- Main replay set contains the current task once, historical class capacities are N, and the maximum scored size is 2N+1.
- Ranked versus strict output is defined consistently with A.1; no arbitrary unnormalized score sum is claimed across all retrievers.
- Main text specifies iteration-end gating and iteration-start rollback, without changing the cold-start comparator.
- No claim implies all stored history has fixed memory size.

**Prior review:** Prior ISSUE-003 survives in operational scope only; exclude the redundant guarantee expansion tied to prior ISSUE-002.

### NAR-002 — MAJOR: The main per-dataset split statement does not match the global constrained split reported in Appendix C.
**Anchor:** §5.1 Benchmarks and Skill Corpus, PDF p.4; `source/sections/experiments.tex:12–12`.
> We split each dataset into train, validation, and test splits

**Counterevidence considered:** The next main-text sentence already discloses filtering/balancing for shared required skills. Therefore the represented-skill evaluation is not wholly hidden, and deliberate skill overlap is not evidence of task leakage. Appendix C.1 p.16 explicitly states disjoint task identifiers and held-out tasks involving represented skills.

**Evidence/reason:** Appendix C.1 pp.16–17 (data_splits.tex:3–7,18–25) reports 4,987 retained tasks, global 3,491/748/748 partitions, and TheoremQA 259/106/105. It says individual dataset proportions differ. A reader relying on §5.1 would otherwise use the wrong protocol.

**Minimal proposal:** Replace the two split sentences, rather than add another paragraph: say that filtering retains 4,987 tasks; a constrained global 70/15/15 target yields 3,491/748/748 task-disjoint partitions; all 306 evaluated gold skills occur in each partition, with dataset-level proportions varying. Point to Table 3 for exact counts.

**Acceptance:**
- No sentence asserts exact 70/15/15 splits for each benchmark.
- The main text reports global counts and held-out-task/represented-skill scope.
- No unsupported leakage or unseen-skill-generalization accusation is introduced.

**Prior review:** Prior ISSUE-007 retained, narrowed to the actual contradiction and compact scope disclosure.

### NAR-003 — MAJOR: The strongest named comparator has no usable baseline specification, and the main setup contradicts itself on whether retrievers are trained.
**Anchor:** §5.4 Baselines, PDF p.5; `source/sections/experiments.tex:39–47`.
> They are trained on training split and frozen on validation and test splits.

**Counterevidence considered:** SkillRouter is already cited in §2.2 and appears in Table 1; it is not a missing citation or an omitted comparison. §5.5 does give candidate-pool and downstream-budget information; Appendix D provides extensive RouterBSI details, but not a corresponding SkillRouter training/checkpoint/input-field protocol. External SkillRouter record verifies that the original system is a body-aware retrieve-and-rerank pipeline; this does not establish which checkpoint or adaptation this draft actually used.

**Evidence/reason:** §5.4 says the retrievers are trained, whereas §5.5 (experiments.tex:47) says pretrained/lexical retrievers do not require training. SkillRouter is called the strongest routing baseline in §6.1 (results.tex:9), but §5.4 never describes it by name. Without identifying its adaptation, training status and inputs, the main comparative claim is not independently interpretable.

**Minimal proposal:** Ask the authors for the actual SkillRouter checkpoint/version, input fields, training/adaptation split and candidate policy. Add one concise sentence defining this comparator and correct the antecedent of the train/freeze statement to the components actually optimized. Add extended baseline configuration in the appendix only where needed. Do not infer these settings from the upstream paper.

**Acceptance:**
- SkillRouter has an explicit method description and reference in the baseline section.
- Trained, pretrained and frozen components are distinguished without contradiction.
- Claimed comparator settings are backed by the actual run configuration, not copied unverified from the upstream paper.

**Prior review:** Prior ISSUE-008 retained for narrative/protocol specification; model-role and run-provenance questions should merge with the experimental scout rather than create duplicate issues.

### NAR-004 — MAJOR: Three non-monotonic backbone endpoints do not establish a ceiling that more capable LLMs cannot overcome.
**Anchor:** §7.3 Skill Routing Performance across LLM Backbones, PDF p.7; `source/sections/ablations.tex:24–24`.
> They also suggest that predicates reach a plateau that cannot be overcomed with more capable LLMs

**Counterevidence considered:** The preceding sentences correctly report non-monotonic final scores and explicitly identify Qwen3.8-27B as strongest. §7.1 supplies evidence for diminishing returns across iterations in one optimization setting; that is not evidence for a universal cross-model ceiling. The word suggest weakens the sentence, but cannot overcome still asserts a strong impossibility; no such cause or limit is tested.

**Evidence/reason:** Figure 7 p.8 and Appendix G.4/Table 14 p.25 report final nDCG@1 0.742/0.802/0.745, one run per backbone. The 27B endpoint itself exceeds the 4B endpoint. The main claim conflates observed endpoints, convergence over iterations, and predicate expressivity.

**Minimal proposal:** Delete the final plateau/expressivity sentence in §7.3, retaining the already-correct descriptive comparison immediately before it. Replace significantly improve with improve the reported routing scores unless an actual significance analysis is supplied. No replacement experiment or additional boilerplate is necessary.

**Acceptance:**
- No universal model-capacity ceiling is inferred from these endpoints.
- The existing non-monotonic endpoint summary remains.
- Statistical significance is not implied without its analysis.

**Prior review:** Prior ISSUE-010 still present verbatim; minimal deletion avoids a redundant second descriptive paragraph.

### NAR-005 — MINOR: The main metric names and headline retention omit distinctions defined only in the appendix.
**Anchor:** §5.2 Evaluation Metrics, PDF p.5; `source/sections/experiments.tex:20–20`.
> We additionally report F1@\(k\) to compare filtering capabilities.

**Counterevidence considered:** §5.2 already distinguishes routing from downstream success, and §6.2 explicitly discusses SkillDAG’s higher coverage; retention is not misrepresented as unconditional recall everywhere. Appendix E.1 defines selected-set F1 and nDCG@1 clearly; Appendix F.1 defines the ratio-of-means normalization. Thus definitions exist and need only concise main-text alignment. Hit@1 in the third contribution equals nDCG@1 under binary nonempty relevance, as Table 10 already notes; this is not an unsupported additional result.

**Evidence/reason:** §5.2 announces F1@k while E.1 p.18 uses F1 of the predicate-selected set, not necessarily the first k ranked skills. F.1 pp.18–19 (retention_definition.tex) normalizes each method by its own task-mean Recall@50, including SkillDAG’s expanded pool; the distinction matters to Figure 3’s comparison.

**Minimal proposal:** Change F1@k to selected-set F1 where describing the ablation metric; define Ret@k in one sentence as each method/retriever’s ratio of task-mean Recall@k to Recall@50 followed by equal averaging across retrievers. Replace contribution-list Hit@1 with nDCG@1 or state equivalence once. Do not duplicate all metric equations.

**Acceptance:**
- Selected-set F1 is not labelled a ranked-cutoff metric.
- Main retention definition names method-specific coverage and ratio of task means.
- Hit@1/nDCG@1 naming is consistent or explicitly equated.

**Prior review:** Subset of prior ISSUE-011 retained and downgraded; explicit nonstandard appendix FP/FN mapping is not by itself a validity failure.

### NAR-006 — MINOR: The main token comparison lacks the single-run and recorded-known-usage scope that makes the appendix accounting interpretable.
**Anchor:** §7.2 Performance and Token Usage Tradeoff, PDF p.7; `source/sections/ablations.tex:20–20`.
> while MBR alone reduces token usage by 10.8\% at the cost of a 7.7\% relative decrease in nDCG@1 compared with using both.

**Counterevidence considered:** Appendix G.2 pp.20–21 now says all configurations use the same initial predicates and explicitly defines recorded totals and excluded unknown usage; do NOT repeat the prior review’s assertion that current prose reports asymmetric initialization. Table 12 p.24 supplies total and iteration-only tokens and counts unknown-usage attempts. §7.2 reports an observed comparison, not an explicit serving-cost claim or a theorem about efficiency; this warrants a compact qualifier rather than a major new experiment demand.

**Evidence/reason:** G.2 distinguishes Figure 6’s first run per configuration from Figure 5’s three-run mean and excludes unavailable usage. That information changes interpretation of the main percentage and is not signposted in §7.2.

**Minimal proposal:** Prefix the existing §7.2 comparison with: “For the first run of each configuration, Figure 6 compares recorded known token usage (excluding attempts with unavailable usage).” Add the same scope to the caption or point to Table 12. Leave all numbers unchanged unless the experimental audit identifies a separate error.

**Acceptance:**
- Main cost text identifies single-run rather than three-run aggregation.
- Tokens are labelled recorded known usage, not full cost accounting.
- No stale initialization-asymmetry assertion is added without current artifact evidence.

**Prior review:** Prior ISSUE-005 narrowed; old asymmetry rationale is no longer supported by current manuscript wording.

## Contribution ladder

| Contribution | Delivery and evidence | Judgment |
|---|---|---|
| We propose RouterBSI, a non-parametric skill-routing framework that evaluates explicit applicability predicates over retrieved candidates, making routing criteria interpretable and directly editable without updating the underlying language model. | §4.1; Appendix A.1/B; Figure 1 — Explicit natural-language predicate interface and concrete examples. | Inspectability/editability is a representation property; no human-edit benefit was measured, and no such experiment is required for this modest claim. All revisited in conclusion. |
| We develop a recursive self-improvement procedure that refines predicates from routing failures, selects updates through minimum Bayes risk over a bounded replay of relevant and irrelevant tasks, and rejects updates with higher held-out validation error than the cold-start predicate. | §4.2–4.3; Appendix A; §7.1 — Minimum-average-risk equation, initial-predicate gate and four component configurations. | The core equations are clear; operational main/appendix mismatches are NAR-001. Timing is iteration-end, not necessarily immediately after each local repair. All revisited in conclusion. |
| We evaluate RouterBSI on six SRA-Bench datasets with a shared 26K-skill corpus, achieving the highest aggregate nDCG@10 and Hit@1 among evaluated methods while ablations establish the contributions of replay and validation. | §§5–7; Appendices E–G — Table 1 aggregate nDCG@1/nDCG@10; Figures 3,5–7 and detailed tables. | Observed routing leadership is delivered and benchmark exceptions acknowledged. Hit@1 naming should align with nDCG@1. Downstream leadership is not claimed as this contribution and belongs to SkillDAG in the displayed means. All revisited in conclusion. |

**Front-page narrative:** Title and abstract identify feedback refinement, replay and gating; Figure 1 illustrates applicability versus topical similarity with single-day versus date-range coffee-price queries. It does not show optimization, but Figure 2 does. A mandatory Figure-1 redesign is not justified by narrative self-containment.

## Main-to-appendix dependency map

There are no active main-text Appendix/app: cross-references in the frozen section sources. These are implicit dependencies, not invented explicit delegations. The central idea and primary results stand alone; exact method execution and split protocol do not.

| Appendix content | Main dependency | Decision |
|---|---|---|
| Replay-set membership, capacity scope, selected-first ranking and iteration-end rollback (A.1–A.5, pp.11–12; procedure_routing.tex:18; procedure_replay.tex:3–13; procedure_validation.tex:3–21) | §4.2–4.3 p.4 and §5.4–5.5 p.5; Main-text-only implementation would differ. | summarize_in_main_text |
| Exact prompts and worked repair (B.1–B.4, pp.12–16; prompts_initialization.tex, prompts_proposal.tex, prompts_evaluator.tex, prompts_trace.tex) | §4.1–4.2 pp.3–4; Exact prompt replication needs appendix, but the essential natural-language interface and update objective are in main. | acceptable_as_is |
| Constrained global split, exact task counts, rare-skill filtering and represented-skill scope (C.1–C.3, pp.16–17; data_splits.tex:3–7,18–25) | §5.1 pp.4–5; Protocol and external-validity scope are not stated accurately in main. | summarize_in_main_text |
| Default parameter values, schema/retry/cache/runtime configuration (D.1–D.2, pp.17–18; implementation_settings.tex:11–23) | §4.2 p.4 and §5.5 p.5; Most are replication detail. A compact N=5, Mp=3, l=400-character default sentence would make the bounded-cost design concrete. | acceptable_as_is |
| Definition of the MBR-disabled control: first valid proposal, history still supplied (D.3 p.18 and G.1 pp.19–20; implementation_variants.tex:5; ablation_components.tex:2) | §7.1 p.7; ablations.tex:16; Ablation removes replay-based selection, not all historical feedback; readers may otherwise overattribute gains to memory presence. | summarize_in_main_text |
| Extended benchmark/retriever tables and metric definitions (E.1–E.2 pp.18–21; routing_metrics.tex; routing_results.tex) | Table 1 p.5 and §6.1 pp.5–6; Detailed rows can stay supplementary because main reports aggregate and benchmark-level nDCG and names exceptions. Selected-set F1 naming requires alignment. | acceptable_as_is |
| Retention denominator and ratio-of-task-means aggregation (F.1–F.2 pp.18–22; retention_definition.tex; Tables 8–9) | §5.2 p.5 and §6.2/Figure 3 p.6; Method-specific expanded coverage affects comparisons. | summarize_in_main_text |
| Component trajectory tables, repeated-run statistics, gate-decision counts (G.1 pp.19–24; Tables 10–11; ablation_components.tex:25–31) | §7.1/Figure 5 p.7; Main already contains the central component evidence. Experimental scout must resolve current initial-score differences against same-predicate assertions; do not import old unpaired-design prose. | acceptable_as_is |
| Recorded token scope and first-run aggregation; replay capacity and candidate-pool sensitivity (G.2–G.3 pp.20–25; ablation_cost_capacity.tex; Table 12) | §7.2/Figure 6 p.7; Main cost text can look like the neighboring three-run comparison or complete cost accounting. | summarize_in_main_text |
| Backbone one-run scope and additional F1/nDCG@10 (G.4 p.22 and Table 14 p.25) | §7.3 p.7/Figure 7 p.8; Main endpoint results are present, but broader ceiling interpretation is unsupported. | acceptable_as_is |
| Model-adjudicated evaluator diagnostic and full semantic error accounting (H.1–H.5 pp.22–28; evaluator_validation.tex; error_routing_gap.tex) | §6.1 p.6 and Limitations p.8; These are not load-bearing validation claims in the current main text. A concise new H.3 diagnosis can improve discussion, but no mandatory promotion of all diagnostic caveats is warranted. | acceptable_as_is |
| Per-retriever and per-benchmark downstream outcomes (H.6 pp.28–29; Tables 21–22) | §6.3/Figure 4 p.6; Main aggregate outcome is present and SkillDAG advantage acknowledged. Budget caveat near comparison is optional; full rows may stay in appendix. | acceptable_as_is |

## Optional refinements — not additional major defects

### NAR-E01: Optional: the novelty contrast would be more precise if it named reflective prompt optimization and distinguished the optimized object, not merely bounded experience.
Anchor: PDF p.2, `source/sections/related_works.tex:14`.
> Similar to our approach, JTPRO evaluates candidates on sampled training minibatches and held-out validation but does not provide bounded experience management for online adaptation

**Counterevidence:** JTPRO is already cited and the minibatch/validation comparison is accurate; do not accuse the draft of omitting it. The current paper does not claim that it invented all reflective updates or all validation gates. GEPA is absent from references.bib, but a citation does not automatically make its full implementation a mandatory baseline.

**Proposal:** Optionally add a short GEPA citation beside JTPRO and replace generic novelty language with the precise objects: per-skill applicability predicates, per-label replay histories, empirical Boolean-loss candidate selection, and strict admission against cold-start validation. Describe bounded replay evaluation, not globally bounded memory. No extra citation cluster or mandatory GEPA/JTPRO experiment is justified by this audit.

**Acceptance:** JTPRO remains credited for reflective updates and train/validation candidate evaluation.; Any GEPA citation uses the verified arXiv record.; Bounded candidate-context pools are not confused with bounded replay-task buckets.; Any new optimizer baseline is explicitly conditional on a stronger algorithmic-superiority claim and separate authorization.

### NAR-E02: Optional: clarify the empirical sense of the title-level MBR label without recasting the method as posterior inference.
Anchor: PDF p.4, `source/sections/method.tex:44`.
> Our risk function is the average skill selection error on replayed tasks.

**Counterevidence:** The risk, average, supervision, candidate set and inequality are already explicitly defined. A missing mathematical definition is not established. The paper makes no posterior-inference theorem claim. A forced rename or invented Bayesian derivation would overcorrect.

**Proposal:** If the authors retain the MBR label, optionally add “Here, minimum risk refers to mean empirical Boolean error on the replay tasks.” Do not add an invented posterior or change the selection equation. Otherwise leave the already-clear equation alone.

**Acceptance:** Any clarification preserves the existing risk equation and candidate inclusion.; No claim of Bayesian posterior inference is added.; No external MBR-decoding citation is treated as mandatory without an actual decoding connection.

### NAR-E03: Optional: the main exception paragraph speculates about remedies while omitting the newly added, more informative diagnosis in Appendix H.3.
Anchor: PDF p.6, `source/sections/results.tex:11`.
> RouterBSI could further improve its performance on these cases with more training iterations or relying on a human to directly edit the predicates.

**Counterevidence:** Could is already hypothetical, not a claim that either intervention was tested. Current H.3 pp.25–26 contains matched ranking-loss analysis and qualified semantic attribution; a critique that the paper lacks investigation of these exceptions is stale. Neither the broad nonactivation explanation nor the narrower semantic category should be promoted as experimentally established causation.

**Proposal:** Optionally replace the remedy sentence with: “Matched ranking-loss cases mainly involve retrieved required skills whose predicates remain false; retrospective inspection points to restrictive predicates in TheoremQA and likely checker errors in MedCalc-Bench (Appendix H.3). These diagnoses do not establish that additional training will close the gaps.”

**Acceptance:** Any promoted diagnosis is restricted to the matched ranking-loss subset and labelled retrospective.; No unrun human-edit or extra-iteration result is asserted.; Do not recreate the deleted 94.68%/93.75% misinterpretation or demand another duplicate diagnostic.

### NAR-E04: Optional: place the already-disclosed unequal skill budgets beside the dependency hypothesis.
Anchor: PDF p.6, `source/sections/results.tex:19`.
> This finding suggests expanding selected skills to include dependent skills could improve downstream performance even if the dependent skills are not required.

**Counterevidence:** Suggests and could already mark the interpretation as a hypothesis; the sentence does not explicitly establish causation. §5.5 already says SkillDAG receives ten skills versus RouterBSI top-five, and §6.3 explicitly acknowledges SkillDAG’s stronger downstream result. The conclusion states dependency work as future work, not a completed contribution.

**Proposal:** Optionally add “with SkillDAG using ten supplied skills versus five for RouterBSI, this comparison does not isolate a dependency effect” immediately before the hypothesis, or include the budgets in Figure 4’s caption. Only propose budget-matched interventions if the author chooses a stronger causal claim.

**Acceptance:** Budget difference is visible at the point of interpretation.; Dependency benefit remains a hypothesis, not a measured mechanism.; No new experiment is imposed merely to support the existing future-work suggestion.

## Verified related-work boundary

JTPRO is already credited. Its verified record describes jointly optimizing global instructions and per-tool schema/argument descriptions from trace-driven reflection.[1] Its method uses minibatch improvement, a validation-best context, and a bounded candidate-context pool; those are not a bounded per-skill replay-task history.[4]
GEPA is a real, absent conceptual neighbor: its abstract describes trajectory reflection, proposal testing and combining lessons from the Pareto frontier.[2] Adding one citation is optional positioning; running GEPA/JTPRO is not made mandatory by this audit.
SkillRouter’s verified upstream record describes a body-aware retrieve-and-rerank system.[3] That verifies its identity, not this draft’s actual checkpoint, adaptation or training settings.
No additional MBR-decoding citation or invented Bayesian derivation is proposed. The explicitly defined empirical selection rule is understandable; naming clarification remains optional.

## Prior-review reconciliation

| Prior issue | Current disposition | Reason |
|---|---|---|
| ISSUE-001 | resolved | Incorrect 94.68%/93.75% interpretation has been removed from current main; H.3 now adds matched ranking-loss diagnosis. Do not resurrect missing-error-analysis claims. |
| ISSUE-002 | source_resolved_pdf_sync_needed | The wrong error direction and stronger objective persist in PDF but are corrected in frozen source. Core average-risk and initial-predicate equations are already correct. |
| ISSUE-003 | partially_retained_narrowed | Operational replay/ranking/timing discrepancies remain; blanket risk/gate caveats are redundant. |
| ISSUE-004 | old_rationale_stale_current_question_deferred | Current G.1 now says common initial predicates. Table 10 initial metrics still vary; this is a fresh reconciliation question for experiment/provenance scout, not proof the old unpaired-initialization design still applies. |
| ISSUE-005 | partially_retained_downgraded | Current G.2 no longer says only one configuration includes local initialization. Keep single-run known-usage scope; verify artifacts before asserting asymmetry. |
| ISSUE-006 | outside_scope_defer_independent_recheck | No audit verdict is copied from old manifests. Current artifact reportability and source binding belong to experimental/provenance scout. |
| ISSUE-007 | retained_narrowed | Per-dataset ratio contradicts current constrained-global counts; shared-skill balancing is partly stated already. |
| ISSUE-008 | retained_in_scope | Strongest comparator lacks main baseline specification and retriever train/freeze wording conflicts. Five-model role issue is separately deferred. |
| ISSUE-009 | downgraded_optional | Main already uses suggests/could and states budgets in setup; qualify locally rather than assert current text claims a causal proof. |
| ISSUE-010 | retained_minimal_delete | Universal backbone ceiling sentence remains; remove it rather than append a duplicate endpoint paragraph. |
| ISSUE-011 | partially_retained_downgraded | Retain selected-set F1/retention/Hit@1 alignment. Appendix openly defines unusual FP/FN labels and neutral descriptions; do not treat labels alone as invalid numbers. |
| ISSUE-012 | major_rejected_optional_positioning | Explicit average loss already defines the selection objective. No forced Bayesian posterior derivation, renaming, or MBR-decoding citation. JTPRO is already cited; GEPA is an optional verified conceptual addition. |
| ISSUE-013 | outside_scope_defer | No invented paired uncertainty or new statistical results. Parent experimental scout should distinguish point estimates from inferential claims. |
| ISSUE-014 | outside_scope_except_teaser | Figure 1 is a valid task-applicability example; requiring it to carry the full update algorithm is optional editorial redesign. Full rendering audit belongs to layout scout. |
| ISSUE-015 | retained_minor_editorial | Repeated RouterBSI introduction and visible grammatical errors remain. Keep copyediting separate from major scientific issues. |

## Handoffs / remaining inputs

- **Version sync:** Group VERSION-N1/N2 with parent PDF/source discrepancy issue. Source already corrected; proposed action is later authorized rebuild, not source re-edit.
- **Experiments:** Current G.1 common-initial-predicate statement versus differing initial metrics needs fresh reconciliation. Do not copy obsolete unpaired-library explanation.
- **Experiments:** §5.3 lists five models; §7.3/Table 14 provide three backbones. Ask for model-to-experiment roles; do not invent missing results.
- **Experiments:** Current token scope still needs main qualification, but old asymmetric-initialization wording is absent. Independently inspect manifests before a stronger charge.
- **Method/ablations:** Define MBR-disabled selection in one main sentence: first valid current-task proposal, with historical proposal context retained. Do not characterize as memory-free.

## Verification and tool limits

All ten retained/optional source anchors were checked against the specified source line ranges; PDF-only synchronization quotes were checked verbatim against pages.json. All 15 prior issue IDs are accounted for. No models or experiments were run. The JSON includes explicit counterevidence, minimal proposals and checkable acceptance criteria.
Web extraction and browser startup failed; direct official-source HTTP fetches succeeded. Saved source evidence and citation ledger are under `external_narrative_sources/`. Full source/PDF sync, experimental provenance and venue compliance remain parent/human responsibilities.
## Sources

[1] https://aclanthology.org/2026.findings-acl.2017
[2] https://arxiv.org/abs/2507.19457
[3] https://arxiv.org/abs/2603.22455
[4] https://aclanthology.org/2026.findings-acl.2017.pdf
