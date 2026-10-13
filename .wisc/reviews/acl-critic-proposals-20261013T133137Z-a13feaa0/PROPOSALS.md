# RouterBSI — proposed solutions for approval

**No proposal has been applied.** This `fix_acl_critic` stage consumed the current `REVIEW_JSON.json` and produced a solution and acceptance criteria for each active issue. No new experimental results were generated. The revision JSON marks every manuscript action `not_executed` and leaves all post-edit text null.

## Recommended decision batches

| Batch | Issues | Scope |
|---|---|---|
| A — supported manuscript corrections | 002, 003, 004, 008, 009, 011, 012 | Main/appendix alignment, concise accounting/metric explanations, deletion of the unsupported ceiling, targeted copyediting. Confirm intended implementation; no benchmark rerun inherently needed. |
| B — evidence-dependent choices | 005, 006, 007 | Confirm historical initialization binding; finish model-role alignment; decide whether saved predictions support paired uncertainty. Never invent settings or intervals. |
| C — optional refinements | 010, 013 | Local downstream-budget caveat; selected figure legibility/accessibility improvements. |
| Resolved outside this review | 001 | No additional synchronization fix requested for the corrected PDF passages. |

No deadline or measured ETA is available. Approving wording does not implicitly approve experiments, rebuilds or uploads.

## Version and authorization boundary

This review began with the 29-page PDF `a13feaa06ce9697e5d4d44119ea46f4403aff73a8743d3bb51bcc616dd3174e5`. During review, the paper changed outside this review-only action set: 12 existing files changed and two appendix source files were added. No actor is inferred and no changes were reverted. The final critique was reconciled against the **30-page PDF `e68ac3a31d892feb1141089312c51d2a70929281cbfb57aa4cf5825088d91779`**, preserved in `current_snapshot/main.pdf`. Main content still ends on page 8.

**ISSUE-001 was resolved by that concurrent revision**, not by this review: non-increasing replay wording, the narrowed objective and Figure 2 tie rejection are now in the PDF. New software/evaluator/statistical/data-reuse paragraphs are credited; ISSUE-006 is narrowed and downgraded, and ISSUE-007 acknowledges the new uncertainty disclosure. Stable issue IDs are retained, so the active list begins at ISSUE-002.

This work created only review artifacts and a WISC plan. **No manuscript edits, compilation, new model runs, commits or uploads were performed by this review.** Current primary issue anchors were rechecked literally against the new PDF and source. Auxiliary appendix page references inherited from the initial scouts refer to the preserved initial snapshot; section/table identifiers remain stable. The final review’s primary location fields and figure page numbers refer to the new PDF.

## Issue-by-issue proposals

### ISSUE-002 — The main replay definition omits the current failed task and does not distinguish bounded per-skill replay from the unbounded global history used by the implementation.

**Location:** Current PDF p. 4, 4.2 MBR Update Selection with Bounded Replay; `sections/method.tex` lines [24, 24]

**Severity / type:** major; necessary_correction. **Estimated scope:** small (not a time estimate).

**Current PDF anchor:**

> the replay set contains previously seen relevant and irrelevant tasks:

**Exact current TeX anchor:**

```tex
For each skill, the replay set contains previously seen relevant and irrelevant tasks:
```

**Proposed replacement/action — not applied:**

> For each skill s, retain at most N relevant and N irrelevant historical tasks. Score candidates on the union of these buckets and the current failed task, de-duplicated by task identifier; this set contains at most 2N+1 tasks. The per-skill replay sets are bounded, but the global seen-task history used for lazy bucket materialization is not. Our default uses N=5, three generated replacements, and a 400-character predicate limit. After each full training pass, validation admission is checked against the initial predicate; rejection or absent validation support restores the iteration-start predicate.

**Execution details:** Replace the main replay-set definition with the current-inclusive definition already given in Appendix A.2. Define the historical bucket bounds separately. Add one sentence distinguishing bounded replay scoring from global history storage, plus default N=5, M_p=3 and l=400 characters from Appendix D.1. Keep bucket replacement mechanics in the appendix. Add one sentence from A.4 that validation gating occurs after a full training pass and rejection restores the iteration-start predicate; retain the already-correct initial-predicate comparator.

**Required inputs:** Author approval; confirmation that Appendix A.2/D.1 describes the evaluated runs

**Acceptance after authorized implementation:**

- [ ] Main and appendix define the same current-inclusive replay set and 2N+1 bound.
- [ ] No passage implies bounded total history storage.
- [ ] The main method states default replay capacity, proposal count and character limit.
- [ ] Gate timing and rollback state agree with A.4; no previous-policy comparator is substituted for the initial-predicate comparator.

### ISSUE-003 — The main ranking rule describes arithmetic addition, while Appendix A.1 specifies selected-first lexicographic ordering.

**Location:** Current PDF p. 5, 5.4–5.5 Ranked routing; `sections/experiments.tex` lines [47, 47]

**Severity / type:** major; necessary_correction. **Estimated scope:** small (not a time estimate).

**Current PDF anchor:**

> the sum of their binary label and the retrieval score

**Exact current TeX anchor:**

```tex
we rank them by the sum of their binary label and the retrieval score
```

**Proposed replacement/action — not applied:**

> For ranked output, we order candidates first by the binary selection label (selected first), then by descending retrieval score, and finally by original retrieval order. The top-k variant returns the first k skills in this ordering and can include predicate-negative candidates; strict routing returns only selected skills.

**Execution details:** Replace both sum descriptions in Sections 5.4 and 5.5 with the lexicographic rule from Appendix A.1. Distinguish retrieval pool K=50 from downstream budget k=5. Preserve original retrieval order for final ties and explicitly note that top-k may include predicate-negative skills.

**Required inputs:** Author confirmation that the documented lexicographic adapter applies to each reported baseline/retriever, not just RouterBSI

**Acceptance after authorized implementation:**

- [ ] No main-text description implies arbitrary raw-score addition.
- [ ] The exact tie-break and strict versus fixed-size outputs agree with Appendix A.1.
- [ ] A per-baseline adapter mapping is documented, or unresolved exceptions are named.

### ISSUE-004 — The main per-dataset 70/15/15 statement contradicts the constrained global split in Appendix C.

**Location:** Current PDF p. 4, 5.1 Benchmarks and Skill Corpus; `sections/experiments.tex` lines [12, 12]

**Severity / type:** major; necessary_correction. **Estimated scope:** small (not a time estimate).

**Current PDF anchor:**

> We split each dataset into train, validation, and test splits with ratios of 70%, 15%, 15%, respectively.

**Exact current TeX anchor:**

```tex
We split each dataset into train, validation, and test splits with ratios of 70\%, 15\%, 15\%, respectively.
```

**Proposed replacement/action — not applied:**

> After skill-frequency filtering, we retain 4,987 tasks covering 306 annotated gold skills. A constrained global 70%/15%/15% allocation yields 3,491 training, 748 validation, and 748 test tasks; per-dataset proportions may differ. Task identifiers are disjoint, while every retained gold skill occurs in all three partitions. We therefore evaluate held-out tasks involving represented skills, not entirely unseen skills (Appendix C.1).

**Execution details:** Replace the split sentences with the exact retained counts, global allocation and shared-skill scope. Cite Appendix C.1 for allocation constraints and per-dataset counts. Retain the distinction between the full 26,262-skill retrieval corpus and 306 evaluated gold skills.

**Required inputs:** Author approval; no new measurements required for this wording route.

**Acceptance after authorized implementation:**

- [ ] Main split counts match Appendix C.1.
- [ ] The per-dataset 70/15/15 claim is removed.
- [ ] The main paper distinguishes held-out tasks, shared gold skills, and the full retrieval corpus.

### ISSUE-005 — The manifest-linked three-run ablation does not use common initial predicates across all configurations, contrary to the PDF and source claim.

**Location:** Current PDF p. 21, G.1 Replay and Held-Out Gate; Figure 5; `sections/appendix/ablation_components.tex` lines [25, 25]

**Severity / type:** major; necessary_correction_conditional_on_historical_binding. **Estimated scope:** medium (not a time estimate).

**Current PDF anchor:**

> All four configurations start from the same initial predicates at iteration 0, as in Figure 5.

**Exact current TeX anchor:**

```tex
All four configurations start from the same initial predicates at iteration 0, as in Figure~\ref{fig:mbr_replay_test_ndcg@1_std}.
```

**Proposed replacement/action — not applied:**

> The first run of each configuration shares an initial predicate library. In the recorded repeats, Both Enabled uses distinct initial libraries for runs 2 and 3, whereas the other configurations reuse the first library. The three-run means therefore summarize heterogeneous repetitions rather than a paired common-initialization comparison. Disabling MBR removes replay-based proposal selection; historical examples remain available to the proposer.

**Execution details:** First confirm that the manifest-linked files are the plotted historical runs, or supply immutable historical bindings. If confirmed, correct Figure 5 and G.1–G.3 to distinguish the shared-initialization first-run comparison from heterogeneous three-run averages; qualify component attribution and preserve observed scores. Define the MBR-disabled control as first valid current-task proposal, with historical examples still supplied. A matched-initialization repeat study is optional and requires separate approval.

**Required inputs:** Author confirmation that the 12 audited initial-policy files belong to the plotted snapshot, or immutable historical alternatives.

**Acceptance after authorized implementation:**

- [ ] Every initialization claim is supported by compared predicate-map hashes, not just matching seeds.
- [ ] Figure 5, G.1–G.3 and the captions consistently state the actual pairing design.
- [ ] Any causal component claim is limited to the verified design; existing unmatched runs are not described as paired.
- [ ] The no-MBR control is described as removing replay selection, not all memory or historical proposal context.

**Evidence route:** all first runs share initialization. Both Enabled runs 2/3 differ from that library on 26,262/26,261 predicates. The other nine arm/repeat files reuse it. Verify historical binding using `parent_initial_policy_verification.json`. Preserve results as descriptive if matched reruns are not approved; do not silently label unmatched means as paired.

### ISSUE-006 — The main setup still contradicts itself on retriever training and leaves two listed models without a clear role, although the new appendix now specifies baseline and task-evaluation software.

**Location:** Current PDF p. 5, 5.3–5.5 Models and Baselines; `sections/experiments.tex` lines [39, 39]

**Severity / type:** minor; remaining_alignment_after_concurrent_revision. **Estimated scope:** medium (not a time estimate).

**Current PDF anchor:**

> They are trained on training split and frozen on validation and test splits.

**Exact current TeX anchor:**

```tex
They are trained on training split and frozen on validation and test splits.
```

**Proposed replacement/action — not applied:**

> We use frozen BM25, vector and SkillSight retrieval implementations. SkillRouter reranks the retrieved candidates with its released 0.6B model in evaluation mode without gradients; Appendix D.4 specifies inputs and software. Model roles for the remaining listed models must be confirmed before adding definitive text.

**Execution details:** Use Appendix D.4 to correct the main train/freeze statement and insert one concise SkillRouter description/cross-reference. Ask for the actual experiment roles of Llama-3.3-70B-Instruct and GPT-5.4; remove unused names from the evaluated-model statement if appropriate. Do not duplicate the newly added software/evaluator paragraphs.

**Required inputs:** Author-confirmed roles for Llama-3.3-70B-Instruct and GPT-5.4; confirmation the described frozen components match reported runs.

**Acceptance after authorized implementation:**

- [ ] The main train/freeze statements agree with Appendix D.4.
- [ ] SkillRouter has a concise main description and appendix pointer.
- [ ] Every model listed in the main setup maps to a verified role or is removed as unused.

### ISSUE-007 — The main superiority comparisons report point estimates without paired uncertainty; repeated-run dispersion is confined to a different ablation experiment.

**Location:** Current PDF p. 5, Table 1 / 6.1–6.3 Primary comparisons; `sections/results.tex` lines [9, 9]

**Severity / type:** major; necessary_correction. **Estimated scope:** medium (not a time estimate).

**Current PDF anchor:**

> SkillRouter is the strongest routing baseline,

**Exact current TeX anchor:**

```tex
SkillRouter is the strongest routing baseline,
```

**Proposed replacement/action — not applied:**

> First reuse saved per-task predictions: report paired task-level differences with dataset-stratified, task-clustered bootstrap intervals for nDCG@10, Recall@5 and downstream success. Keep each task's retriever observations together. State whether estimates condition on one trained checkpoint. If repeats are unavailable, do not describe task-bootstrap intervals as training-seed uncertainty. Remove statistical-significance language without a supporting test. Preserve the newly added statistical-reporting paragraph. If the outputs are unavailable, the proposal-only fallback is to keep explicitly descriptive point estimates and remove unsupported significance language; no automatic rerun.

**Execution details:** First reuse saved per-task predictions: report paired task-level differences with dataset-stratified, task-clustered bootstrap intervals for nDCG@10, Recall@5 and downstream success. Keep each task's retriever observations together. State whether estimates condition on one trained checkpoint. If repeats are unavailable, do not describe task-bootstrap intervals as training-seed uncertainty. Remove statistical-significance language without a supporting test. Preserve the newly added statistical-reporting paragraph. If the outputs are unavailable, the proposal-only fallback is to keep explicitly descriptive point estimates and remove unsupported significance language; no automatic rerun.

**Required inputs:** Exact matched task-level predictions for compared methods/retrievers and run IDs; preregistered analysis choices before calculating intervals

**Dependencies:** ISSUE-006.

**Acceptance after authorized implementation:**

- [ ] Primary comparisons include absolute differences and declared confidence-interval methods/units.
- [ ] Repeated appearances of the same task across retrievers are not treated as independent tasks.
- [ ] Task-bootstrap uncertainty is distinguished from training-run variation.
- [ ] Any use of significant is either supported by a stated test or replaced with measured/descriptive language.

**No-new-run fallback:** preserve the new statistical disclosure; retain explicitly descriptive point estimates; remove unsupported significance language. Missing paired precision remains a limitation, not a fabricated interval or a reason to silently start inference.

### ISSUE-008 — The main efficiency comparison omits that Figure 6 uses one run per configuration and incomplete recorded token totals, rather than full matched costs.

**Location:** Current PDF p. 7, 7.2 Performance and Token Usage; Figure 6; `sections/ablations.tex` lines [20, 20]

**Severity / type:** minor; necessary_correction. **Estimated scope:** small (not a time estimate).

**Current PDF anchor:**

> MBR alone reduces token usage by 10.8%

**Exact current TeX anchor:**

```tex
MBR alone reduces token usage by 10.8\%
```

**Proposed replacement/action — not applied:**

> Figure 6 compares final-test quality with known recorded token use for one run per configuration, rather than the three-run means in Figure 5. MBR alone records 10.8% fewer tokens and 7.7% lower nDCG@1 than both components. Totals omit unavailable usage and external/shared initialization, so this is a descriptive run-local trade-off, not a complete or budget-matched efficiency estimate.

**Execution details:** Promote the existing accounting caveat into Section 7.2 and Figure 6, label the x-axis Known recorded tokens (millions), and state one run per configuration. Keep the recorded percentages if their arithmetic is verified; do not impute unavailable usage. Optionally add the already available iteration-only totals as a separate comparison.

**Required inputs:** Author approval; no new measurements required for this wording route.

**Dependencies:** ISSUE-005.

**Acceptance after authorized implementation:**

- [ ] The main text and caption state one run per configuration and known-only accounting.
- [ ] The x-axis does not imply full accounting.
- [ ] Unknown usage and shared initialization are not silently assigned zero cost.
- [ ] Figure 5 and Figure 6 aggregation differences are explicit.

### ISSUE-009 — Three backbone endpoints do not establish an irreducible predicate plateau or failure of more capable language models.

**Location:** Current PDF p. 7, 7.3 Skill Routing Performance across LLM Backbones; `sections/ablations.tex` lines [24, 24]

**Severity / type:** major; necessary_correction. **Estimated scope:** small (not a time estimate).

**Current PDF anchor:**

> predicates reach a plateau that cannot be overcomed with more capable LLMs

**Exact current TeX anchor:**

```tex
They also suggest that predicates reach a plateau that cannot be overcomed with more capable LLMs, where it's difficult for the predicate to be narrow enough to be false for irrelevant tasks but broad enough to be true for all relevant tasks
```

**Proposed replacement/action — not applied:**

> Delete the unsupported final plateau/expressivity sentence. Optional one-sentence qualification: These single-run comparisons do not establish a model-capability ceiling.

**Execution details:** Delete the final plateau/expressivity sentence in Section 7.3, retaining the already-correct preceding endpoint summary. Replace significantly improve with improve the reported routing scores unless a supporting statistical test is supplied. A short single-run caveat is sufficient; do not duplicate the endpoint paragraph or mandate further sweeps.

**Required inputs:** Author approval; no new measurements required for this wording route.

**Acceptance after authorized implementation:**

- [ ] No claim asserts that more capable models cannot overcome the plateau.
- [ ] The paragraph identifies the comparison as three evaluated backbones with one run each.
- [ ] The reported ranking and numerical results remain unchanged.

### ISSUE-010 — The dependency interpretation is a plausible hypothesis, but the comparison also changes the downstream skill budget and does not isolate dependency utility.

**Location:** Current PDF p. 6, 6.3 Downstream Performance; `sections/results.tex` lines [19, 19]

**Severity / type:** minor; optional_local_qualification. **Estimated scope:** small (not a time estimate).

**Current PDF anchor:**

> This finding suggests expanding selected skills to include dependent skills could improve downstream performance even if the dependent skills are not required.

**Exact current TeX anchor:**

```tex
This finding suggests expanding selected skills to include dependent skills could improve downstream performance even if the dependent skills are not required.
```

**Proposed replacement/action — not applied:**

> SkillDAG uses ten downstream skills, whereas RouterBSI_top5 uses five, so this comparison does not isolate the effect of dependency expansion from the larger context budget. Dependency-aware routing remains a hypothesis for a budget-matched follow-up.

**Execution details:** Optional: Append a brief budget qualification to the dependency hypothesis and carry method budgets into Figure 4's caption. Preserve the fact that SkillDAG, not RouterBSI, has the highest measured downstream mean. Do not relabel the existing results as a matched-budget test.

**Required inputs:** Author approval; no new measurements required for this wording route.

**Acceptance after authorized implementation:**

- [ ] The dependency discussion and Figure 4 identify the unequal skill budgets.
- [ ] No causal effect of dependency expansion is claimed without a matched intervention.
- [ ] SkillDAG's higher observed downstream mean remains explicit.

### ISSUE-011 — The main metric description conflates cutoff F1 with selected-set F1 and leaves the headline retention denominator unspecified.

**Location:** Current PDF p. 5, 5.2 Evaluation Metrics / Appendix E.1 and F.1; `sections/experiments.tex` lines [20, 20]

**Severity / type:** minor; necessary_correction. **Estimated scope:** small (not a time estimate).

**Current PDF anchor:**

> We additionally report F1@k to compare filtering capabilities.

**Exact current TeX anchor:**

```tex
We additionally report F1@\(k\) to compare filtering capabilities.
```

**Proposed replacement/action — not applied:**

> We report selected-set F1 for filtering. For each method and retriever, Ret@k is 100 times task-mean Recall@k divided by that method's task-mean Recall@50; the headline averages the three retriever-specific ratios. SkillDAG is normalized by its expanded candidate pool.

**Execution details:** Replace F1@k with selected-set F1 where that is the measured quantity. Add the ratio-of-means retention definition and explain that SkillDAG's denominator uses its expanded pool. Preserve the task-weighted within-retriever and equal-weight across-retriever aggregation. Align contribution-list Hit@1 with nDCG@1 or state their equivalence once under binary nonempty relevance. Do not impose FP/FN renaming: the appendix already defines its convention.

**Required inputs:** Author approval; no new measurements required for this wording route.

**Acceptance after authorized implementation:**

- [ ] Selected-set F1 is not mislabeled F1@k.
- [ ] Retention is explicitly a ratio of task means, not a mean of per-task retention ratios.
- [ ] The method-specific Recall@50 denominator and retriever averaging are stated.

### ISSUE-012 — Redundant phrasing and grammatical errors make the exposition harder to follow, including malformed figure captions.

**Location:** Current PDF p. 2, Introduction; method prose; Figure captions; `sections/introduction.tex` lines [29, 29]

**Severity / type:** minor; editorial_correction. **Estimated scope:** small (not a time estimate).

**Current PDF anchor:**

> in a black-box setting called RouterBSI.

**Exact current TeX anchor:**

```tex
We introduce RouterBSI, a recursive self-improving algorithm for skill routing in a black-box setting called RouterBSI.
```

**Proposed replacement/action — not applied:**

> We introduce RouterBSI, a non-parametric algorithm that refines skill-applicability predicates from routing failures while keeping the language model fixed.

**Execution details:** Apply only a targeted copyedit after approval. Remove the duplicate RouterBSI phrase, fix subject/verb agreement and stray notation, and define Figure 5 lines as means and bands as population standard deviations over three runs. Describe Figure 4's aggregation and comparator budgets accurately. Use description.text as the caption source of truth and synchronize embedded captions after approval.

**Required inputs:** Author approval; no new measurements required for this wording route.

**Dependencies:** ISSUE-005.

**Acceptance after authorized implementation:**

- [ ] The duplicate introductory phrase and identified grammatical errors are removed.
- [ ] Figure 5 names the actual band statistic and actual initialization design.
- [ ] Figure 4 has a grammatical caption that reports aggregation and budgets without claiming superiority to SkillDAG.
- [ ] Caption descriptions and embedded TeX captions match; no numerical results change.

### ISSUE-013 — Some figure labels are too small at their placed size, and Figure 8 distinguishes candidate-pool settings only by blue shade.

**Location:** Current PDF p. 1, Figures 1, 4 and 8

**Severity / type:** minor; optional_editorial_redesign. **Estimated scope:** medium (not a time estimate).

**Current PDF anchor:**

> Figure 1: Skill routing with a task applicability predicate.

**Editable source:** confirm the diagram source mapping before applying any optional redesign.

**Proposed replacement/action — not applied:**

> After approval, shorten and enlarge Figure 1 labels or redraw as vector. Enlarge Figure 4 labels while preserving variant subscripts; use a dot plot or zero-based bars if acceptable. Add direct Top-K labels or distinct shapes in Figure 8. Preserve all measured data and do not invent uncertainty.

**Execution details:** After approval, shorten and enlarge Figure 1 labels or redraw as vector. Enlarge Figure 4 labels while preserving variant subscripts; use a dot plot or zero-based bars if acceptable. Add direct Top-K labels or distinct shapes in Figure 8. Preserve all measured data and do not invent uncertainty.

**Required inputs:** Author approval; no new measurements required for this wording route.

**Acceptance after authorized implementation:**

- [ ] Figure 1 task/predicate labels are readable at its final ACL column width.
- [ ] Figure 4 labels/subscripts are readable at text width, and its axis design is explicit.
- [ ] Figure 8 Top-K settings can be identified without color or shade.
- [ ] All plotted data and measured uncertainty remain unchanged.

## Optional studies — unrun and unapproved

### EXP-001 — Matched-initialization component repetition

- **Purpose:** Strengthen causal component attribution beyond honest narrowing of ISSUE-005.
- **Design:** Freeze and hash one initial library per predeclared repetition and use it across all four arms. Match task order, candidate lists, prompts, evaluator, caches, iteration budget and validation gate baseline. Analyze paired per-task and per-repeat effects. Report complete measured usage and unknown fields; do not promise equal costs merely from equal iterations.
- **Hypothetical support criterion:** Hypothetical: component differences persist under matched initialization; no outcome is assumed.
- **If negative:** Report the negative result and narrow component-benefit claims.
- **Compute, deadline feasibility and stage permission:** unknown.

### EXP-002 — Budget-matched dependency intervention

- **Purpose:** Needed only for a stronger causal claim about dependency expansion, not for the current future-work hypothesis.
- **Design:** Compare dependency expansion on/off at the same supplied-skill budget, candidate evidence, agent model, task set and prompt/token constraints. Predeclare downstream paired differences and analyze actual context usage.
- **Hypothetical support criterion:** Hypothetical: dependency expansion improves success at fixed budget; no outcome assumed.
- **If negative:** Do not claim dependency expansion explains SkillDAG’s advantage.
- **Compute, deadline feasibility and stage permission:** unknown.

## Targeted upgrade passes

- **Figures:** all eight audited; per-figure specifications and conditional caption drafts are in `REVISION_REPORT.json`. No figures were regenerated. Approved caption updates should use `description.text` and synchronize embedded captions. Preserve RouterBSI variant subscripts and verified numeric series.
- **Writing:** short replacements/deletions, not broad stylistic rewriting. Abstract counted as 200 words under the reported convention. Preserve limitations and uncertainty; editorial length/font targets are not official rules.
- **Narrative:** retain the editable-predicate NLP contribution, three delivered themes and distinction between routing results and downstream outcomes. No invented theorem or stronger novelty claim.

## Verification and approval boundary

All current primary PDF/source anchors, 12 proposal mappings, dependencies and eight-figure coverage passed checks. Current paper bytes were stable after the updated snapshot; earlier concurrent changes are explicitly recorded. This review itself made no paper edits. Source/PDF compilation is not claimed. Manuscript acceptance criteria are intentionally unchecked because proposals are not implemented fixes.

To authorize later work, name individual IDs or batches—for example, “Apply Batch A; inspect Batch B evidence without running models; leave optional figures unchanged.” Recheck the current source/PDF version before any implementation. No commit or upload is implied.
