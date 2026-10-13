# Independent narrative and self-containment review

**Internal scores (1–5, not official ARR): contribution 3; presentation 3; overall 3 (borderline).**

The contribution is clear: editable applicability predicates refine language-agent skill routing through empirical replay selection and a cold-start validation gate, without weight updates. The current replay, ranking, global-split/adaptation, and frozen-baseline corrections materially improve the paper. The strongest remaining confirmed overclaim is the asserted model-capability ceiling. The historical initialization question below is **conditional and excluded as a confirmed defect from the scores**.

## Strengths

- Main §§3–4 define a concrete NLP-agent problem and explicit empirical Boolean-risk objective, including the unchanged predicate. No invented Bayesian derivation or forced rename is needed.
- All three introduction contributions have delivery sections and conclusion revisits: predicate representation, update procedure, and measured routing/retention/ablation results.
- §5.1 now correctly explains global allocation, represented-skill generalization, update eligibility, and cold-start retention for skills never retrieved during training. Exact counts can remain in C.1.
- Main §§5.4–5.5 now clearly state frozen retrieval and released SkillRouter without task-split fine-tuning; normalized scores and selected-first ties agree with A.1.
- Main results acknowledge both benchmark reversals and SkillDAG’s higher downstream mean. H.1/H.3 carefully distinguish model adjudication from human ground truth and retrospective diagnosis from intervention evidence.

## Six priority items

Five are confirmed manuscript reporting/claim issues; one is a conditional historical-binding question. IDs use the **supplied final REVIEW_JSON issue list**, not the differently numbered older review embedded inside it.

### ISSUE-009 — MAJOR: Three single-run backbone comparisons do not establish a predicate-capability ceiling.

**Anchor:** §7.3 Skill Routing Performance across LLM Backbones, PDF p.7; `source/sections/ablations.tex:24`.

> They also suggest that predicates reach a plateau that cannot be overcomed with more capable LLMs, where it's difficult for the predicate to be narrow enough to be false for irrelevant tasks but broad enough to be true for all relevant tasks

**Assessment:** Section 7.3 reports final nDCG@1 of 0.742, 0.802 and 0.745 and then says more capable LLMs cannot overcome a plateau. Appendix G.4 identifies one run per backbone; nonmonotonic endpoints and within-run diminishing returns are not evidence of an irreducible representational ceiling. The strong impossibility claim overstates an otherwise useful empirical result; this is a scientific interpretation problem, not a policy gate.

**Minimal action:** Delete the final plateau/expressivity sentence. Preserve the endpoint comparison and add, at most, a single-run caveat. Replace significantly improve with improve the reported scores unless a significance analysis supports it. No new backbone sweep is necessary for the narrower claim.

**Acceptance:** No claim of an unovercomable model-capability ceiling remains.; Reported endpoints remain unchanged.; The comparison is identified as three single-run settings and does not imply tested statistical significance.

### ISSUE-005 — CONDITIONAL — not a confirmed design flaw: The common-initialization premise behind the strong component-attribution wording still requires historical binding, not inference from current file paths.

**Anchor:** §G.1 Replay and Held-Out Gate, PDF p.20; `source/sections/appendix/ablation_components.tex:25`.

> All four configurations start from the same initial predicates at iteration 0, as in Figure~\ref{fig:mbr_replay_test_ndcg@1_std}.

**Assessment:** The present manuscript still claims common initial predicates and says in contribution 3 that ablations establish the contributions of replay and validation. The supplied prior review reported differing predicate maps in manifest-linked repetitions, but explicitly left their binding to the plotted historical runs unconfirmed. This narrative review has not independently certified that binding. Different initial scores alone do not prove different predicate libraries. The appropriate action is a scoped evidence request before treating the attribution as controlled or declaring it invalid.

**Minimal action:** Obtain an immutable run-to-initial-predicate map for the plotted repetitions. If common initialization is verified, close the question without rewriting the design. If the earlier audit maps to these exact runs, qualify the design and the words establish the contributions in the introduction and corresponding conclusion/caption text. Do not import obsolete artifact prose or mandate reruns before binding is settled.

**Acceptance:** Every plotted arm/repetition maps to an immutable initial-predicate payload or hash.; Common-initialization claims agree with the bound run evidence.; Attribution wording is narrowed only if the confirmed design requires it; all observed values are preserved.

### ISSUE-007 — MAJOR: Primary comparative gains remain single-evaluation point estimates, with the repetition and inferential limits disclosed only in the appendix.

**Anchor:** §6.1 Skill Routing Performance, PDF p.6; `source/sections/results.tex:9`.

> SkillRouter is the strongest routing baseline, yet RouterBSI the nDCG@1 and nDCG@10 is 10.9\% and 8.4\% higher on average.

**Assessment:** The main paper presents headline superiority and cross-retriever averages without naming their single-evaluation status. Appendix E.1 explicitly says these are distinct retrieval conditions rather than repeated seeds, provides no run-to-run uncertainty for them, and reports no significance tests. Component-run dispersion is not uncertainty for the main baseline comparison. This limits how confidently a reviewer can generalize the reported superiority. It does not invalidate the displayed descriptive means or create an official minimum-seed requirement.

**Minimal action:** Promote a concise single-evaluation/no-significance scope sentence beside Table 1 and the primary-results interpretation. If exact matched task predictions are available, estimate paired task-sampling intervals with retriever observations for the same task clustered together and dataset stratification, explicitly conditional on the evaluated checkpoints. If unavailable, keep results descriptive and remove significance language; do not fabricate intervals or automatically launch training repeats.

**Acceptance:** Main readers can distinguish cross-retriever averaging from repeated training trials.; Any interval names its pairing unit, aggregation and checkpoint conditioning.; Claims remain descriptive if inferential evidence is unavailable.

### ISSUE-008 — MINOR: The main token-cost comparison omits the single-run and known-recorded-usage qualifications already supplied in the appendix.

**Anchor:** §7.2 Performance and Token Usage Tradeoff, PDF p.7; `source/sections/ablations.tex:20`.

> while MBR alone reduces token usage by 10.8\% at the cost of a 7.7\% relative decrease in nDCG@1 compared with using both.

**Assessment:** Figure 6 is juxtaposed with the three-run component comparison but uses the first run of each configuration. Appendix G.2 excludes attempts with unavailable usage from known totals and states run-local phase coverage; these are not complete economic costs. A short local qualifier is enough to prevent main-only readers from confusing populations or complete versus recorded costs; this is not a demand for another experiment.

**Minimal action:** Prefix the main comparison and Figure 6 caption with single-run known-recorded-token scope, point to G.2, and label the axis Known recorded tokens (millions). Keep percentages unchanged absent a separate arithmetic finding. State omitted unavailable usage; do not assert historical shared-initialization costs from unbound artifacts.

**Acceptance:** Main text/caption identify one run per configuration.; Known recorded usage is not labeled complete cost accounting.; The distinction from Figure 5 three-run means is explicit.

### ISSUE-011 — MINOR: The main metric names obscure selected-set F1 and the method-specific ratio-of-means retention used for headline comparisons.

**Anchor:** §5.2 Evaluation Metrics, PDF p.5; `source/sections/experiments.tex:20`.

> We additionally report F1@\(k\) to compare filtering capabilities. We also report retention as Ret@\(k\) to compare the percentage of required skills retained in top k from the retrieved skills.

**Assessment:** Appendix E.1 defines the ablation F1 on the predicate-selected set, not the first k entries of a possibly padded ranked list. Appendix F.1 defines Ret@k as a ratio of task-mean recalls, normalized by each method/retriever own Recall@50, then averaged across retrievers; SkillDAG uses its expanded pool. These distinctions are needed to interpret the main claims but can be promoted in two short sentences rather than all appendix equations.

**Minimal action:** Use selected-set F1 rather than F1@k for the predicate ablation metric. Define retention in main as the ratio of task-mean Recall@k to that method/retriever task-mean Recall@50, followed by equal averaging across retrievers; mention SkillDAG expanded coverage. Optionally unify Hit@1/nDCG@1 terminology without changing values.

**Acceptance:** Selected-set F1 is not described as a ranked-cutoff metric.; Retention states ratio of means and method-specific denominator.; No implication that normalized retention is unconditional gold-skill recall is introduced.

### ISSUE-002 — MINOR: After the replay correction, the remaining main-method gap is a compact operational description of gate timing, rollback state and absent validation support.

**Anchor:** §4.3 Held-Out Validation and Recursive Improvement, PDF p.4; `source/sections/method.tex:89`.

> End the iteration by updating the next predicate \(p_{sk}^{\mathrm{(i+1)}}\) of the skill \(s\) if the selected candidate update \(\partial\)passed the held-out validation gate. Repeat this self-improvement loop until i iterations.

**Assessment:** The current main correctly includes the current failed task, de-duplicates the replay set, and gives the 2N+1 bound. It also correctly compares validation error with the initial predicate and rejects ties. Appendix A.4 clarifies that all local training-task repairs are provisional until the full pass ends, and rejection or absent support restores the iteration-start predicate. The main otherwise state is not explicitly named as iteration-start, and the mean validation error is undefined for empty support without the appendix convention. This is now a minor self-containment clarification, not the old major replay-membership contradiction or evidence of a wrong historical implementation.

**Minimal action:** Replace the last method sentence with a compact statement: after each full training pass, gate each changed skill against its cold-start predicate; reject ties or absent support and restore the iteration-start predicate. If space permits, note that bounded replay refers to per-skill scoring buckets, while global seen-task history remains unbounded; do not characterize the existing replay definition as wrong.

**Acceptance:** The main explicitly names full-pass gate timing, iteration-start rollback and no-support behavior.; The already-correct current-inclusive replay set and initial-predicate comparator remain intact.; No global fixed-memory guarantee is added.

## Related work and novelty

JTPRO and SkillRouter are already cited; neither should be reported missing. The saved primary JTPRO PDF (pp.1–4) supports the stated connection to joint textual editing, minibatch evaluation, and validation selection. A candidate-context pool is not the same object as per-skill replay-task buckets. The SkillRouter abstract establishes a body-aware retrieve-and-rerank pipeline, not the historical configuration of these experiments; a full-pipeline parameter total does not contradict naming the reranker component size.

The defensible novelty is the **specific predicate representation and update/admission combination**, not reflective optimization or validation selection in general. No mandatory new optimizer baseline or missing-citation finding is established by this bounded review. No broad literature-completeness claim is made.

Sources already available and inspected: [JTPRO](https://aclanthology.org/2026.findings-acl.2017), [SkillRouter](https://arxiv.org/abs/2603.22455). Saved evidence paths are in the JSON.

## Main/appendix boundary

The thesis and principal results stand alone. Brief main-text additions would make gate execution, selected-set F1/retention, single-evaluation scope, and known-token accounting interpretable without the appendix. Defining the no-MBR arm as first valid current-task proposal while retaining historical proposal context would also sharpen §7.1.

Exact prompts, retries/caching, split counts, full per-retriever tables, trajectories, additional sensitivities, and the carefully qualified evaluator/error diagnoses can stay supplementary. Do not demand wholesale appendix promotion or infer a policy violation from these small omissions.

## Prior-review reconciliation

| Prior ID | Current disposition |
|---|---|
| ISSUE-001 | **resolved_stays_resolved** — The prior final review resolved stale PDF wording. Current PDF/source both say non-increasing empirical error and limit regressions; no stale source/PDF complaint revived. |
| ISSUE-002 | **mostly_resolved_narrowed_minor** — Current task inclusion, deduplication and 2N+1 bound are fixed in main. Only gate timing/rollback/no-support self-containment retained. |
| ISSUE-003 | **resolved** — Main now explicitly normalizes retrieval scores to [0,1] and favors selected skills on ties; A.1 states equivalent selected-first ordering. No arbitrary-raw-sum contradiction remains. |
| ISSUE-004 | **resolved** — Main now states global target proportions, varying dataset proportions, shared represented skills, update eligibility and cold-start retention for never-retrieved skills. Exact per-dataset counts may remain in C.1. |
| ISSUE-005 | **conditional_evidence_request** — Same-initial-predicates claim persists, but historical binding of earlier inspected files is unconfirmed. Not a newly proven flaw. |
| ISSUE-006 | **training_status_resolved_model_roles_deferred** — Frozen retrievers and released non-fine-tuned SkillRouter are explicit in main and D.4. Main still lists five models while backbone results show three; roles of Llama-3.3-70B-Instruct and GPT-5.4 remain an author question, not inferred missing experiments. |
| ISSUE-007 | **retained_with_descriptive_fallback** — E.1 honestly discloses single evaluations but primary-comparison uncertainty remains absent. Narrow claims and promote scope if matched predictions are unavailable. |
| ISSUE-008 | **retained_minor** — Single-run known-token scope remains appendix-only; no unbound historical cost asymmetry asserted. |
| ISSUE-009 | **retained_major** — Unovercomable backbone/predicate ceiling sentence still present verbatim. |
| ISSUE-010 | **optional_not_retained_as_important_finding** — Dependency suggestion remains tentative; unequal budgets are already stated in main. A local budget reminder is optional, not a mandatory causal experiment. |
| ISSUE-011 | **retained_minor** — F1@k and retention-definition alignment still needed; no numerical invalidity inferred. |
| ISSUE-012 | **minor_editorial_not_in_six_priority_findings** — Duplicate RouterBSI naming, malformed captions and grammar persist. They affect presentation but are not major scientific flaws. |
| ISSUE-013 | **deferred_visual_audit** — No fresh rendered-figure inspection in this scoped narrative review; no inherited font or color finding asserted. |

Optional editorial refinements are not additional major findings: replace speculative extra-training remedies with a pointer to existing H.3 diagnosis; place the already-disclosed unequal downstream budgets beside the dependency hypothesis; copyedit duplicate naming and captions. No new human-edit or dependency experiment is required for the current tentative suggestions.

## Score justification and limits

- **Contribution 3:** identifiable and useful language-agent routing combination, with six task settings; novelty remains primarily the specific representation/update design.
- **Presentation 3:** recoverable thesis and substantial corrections, but remaining main/appendix qualifications, an unsupported ceiling, and copyediting defects prevent a strong score.
- **Overall 3:** borderline from the manuscript evidence and calibrated claims. The conditional historical-initialization question is not counted as a proved design defect or extra score penalty.

Frozen current main and supporting appendix were reviewed against current PDF text. Exact quotes and line anchors were checked; snapshot hashes match. This was not a full artifact investigation, fresh arithmetic audit, rendered-figure inspection, or venue-policy certification. Stage/upload permissions remain unknown. No manuscript changes, experiments, builds, commits, or uploads were made. Outputs: `narrative.json` and `narrative.md` only.
