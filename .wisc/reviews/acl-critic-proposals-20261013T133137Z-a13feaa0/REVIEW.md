# RouterBSI — ACL-style critique

**Internal verdict: substantial revision, overall 2/5.** This is an internal rubric, not an official ARR score or acceptance prediction.

**12 active anchored findings: 6 major, 6 minor; no confirmed mandatory-policy blocker.** One additional finding was resolved during concurrent revision. Every active issue has a proposal in [PROPOSALS.md](PROPOSALS.md).

The paper has a concrete NLP-agent contribution and reproducible headline aggregate arithmetic. The strongest remaining concern is heterogeneous initialization in the nominally common-initialization three-run component study. Main/appendix method and split differences, paired uncertainty and an unsupported backbone ceiling also need attention. A concurrent revision resolved the stale-PDF issue and improved baseline/evaluator/statistical documentation; those improvements are credited rather than reported as absent. This is an internal review, not an official ARR score or acceptance prediction.

## Version and authorization boundary

This review began with the 29-page PDF `a13feaa06ce9697e5d4d44119ea46f4403aff73a8743d3bb51bcc616dd3174e5`. During review, the paper changed outside this review-only action set: 12 existing files changed and two appendix source files were added. No actor is inferred and no changes were reverted. The final critique was reconciled against the **30-page PDF `e68ac3a31d892feb1141089312c51d2a70929281cbfb57aa4cf5825088d91779`**, preserved in `current_snapshot/main.pdf`. Main content still ends on page 8.

**ISSUE-001 was resolved by that concurrent revision**, not by this review: non-increasing replay wording, the narrowed objective and Figure 2 tie rejection are now in the PDF. New software/evaluator/statistical/data-reuse paragraphs are credited; ISSUE-006 is narrowed and downgraded, and ISSUE-007 acknowledges the new uncertainty disclosure. Stable issue IDs are retained, so the active list begins at ISSUE-002.

This work created only review artifacts and a WISC plan. **No manuscript edits, compilation, new model runs, commits or uploads were performed by this review.** Current primary issue anchors were rechecked literally against the new PDF and source. Auxiliary appendix page references inherited from the initial scouts refer to the preserved initial snapshot; section/table identifiers remain stable. The final review’s primary location fields and figure page numbers refer to the new PDF.

## Scorecard

| Dimension | Internal score | Justification |
|---|---:|---|
| Soundness | 3/5 | The method is explicit and aggregate arithmetic checks out; unmatched initialization weakens ablation attribution and baseline uncertainty is absent. |
| Presentation | 3/5 | Thesis and results are recoverable and the new appendix improves documentation; method/split inconsistencies, captions and label sizes still need attention. |
| Contribution | 3/5 | An identifiable editable-predicate routing contribution with useful measurements; distinctiveness is primarily the specific representation/update combination rather than a new general risk principle. |
| Overall | 2/5 | Substantial revision is appropriate before relying on the controlled-ablation, replication and scaling interpretations. |
| Confidence | 4/5 | Full PDF/source, three independent audits, numeric checks, run-map verification and policy inspection; no live reproduction, historical-source binding or human/portal information. |

## Supported strengths

- Sections 3–4 provide a concrete language-agent routing problem and explicit natural-language predicates editable without changing model weights.
- The average replay-loss equation and strict validation comparison against the INITIAL predicate are already correct; Figure 2 makes the update mechanism tangible.
- Table 1 headline aggregate nDCG gains reproduce from saved data: 8.38% over SkillRouter, 29.25% over SkillDAG and 26.73% over Skill-Pro.
- The 75.5% top-five recall and 90.5% relative retention headlines reproduce; the paper acknowledges TheoremQA/MedCalc-Bench exceptions and SkillDAG’s stronger downstream mean.
- The appendix includes prompts, exact global split counts, gate/replay procedures, aggregate and per-dataset results, and a new matched-loss diagnostic. Limitations and ethics discussion are present.

## Priority findings and minimum solutions

| Priority | Finding | Minimum proposal |
|---|---|---|
| ISSUE-005 | Common-initialization description conflicts with the 12 manifest-linked predicate libraries. | Confirm historical binding; distinguish shared-initialization first runs from heterogeneous three-run averages. Preserve observed numbers. Matched reruns are optional and unapproved. |
| ISSUE-002/003 | Main replay and arithmetic ranking differ from the appendix’s current-inclusive replay and lexicographic ordering. | Replace the inaccurate main definitions; summarize gate timing/rollback. Preserve the correct loss inequality and cold-start gate comparator. |
| ISSUE-004 | Main per-dataset 70/15/15 statement differs from the constrained global split. | State 4,987 tasks and global 3,491/748/748 splits; keep represented-skill scope and full corpus distinct. Do not allege task leakage. |
| ISSUE-007 | Primary differences have no paired uncertainty estimate. | Prefer saved-output paired analysis. The new honest single-run disclosure is valuable, but not an interval estimate. If unavailable, keep claims descriptive; do not invent results or launch models. |
| ISSUE-009 | Three backbone endpoints do not establish an irreducible capacity ceiling. | Delete the final plateau/expressivity sentence and unsupported significance wording; keep the preceding descriptive result. |

## Compliance, separated from scientific judgment

- **Venue, cycle, stage, deadline and portal permissions remain unknown.** Long paper is an explicit assumption; 8 content pages fit that assumed review budget. No extra page is inferred.
- Current PDF: 30 pages, A4, two-column layout, all 28 font resources embedded. Review numbering, dedicated Limitations before references, ethics discussion and appendix placement were checked. Exact build closure and external-supplement anonymity remain unverified.
- Visible author fields and metadata are anonymous; no obvious identifying/tracking link was found. That is not a comprehensive audit of every external artifact or author relationship.
- Current ARR instructions require disclosure of writing/coding use and scope in the Responsible NLP Checklist and direct details to Acknowledgements; generic ACLPUB review guidance says to omit the acknowledgment section. Do not label a non-identifying AI-use disclosure a confirmed violation solely from its heading; verify the target’s specific policy and form.[1][3]
- New Appendix C.4 discusses language coverage, constituent licenses and privacy/safety risks. It does not certify license compliance, consent, de-identification or the portal checklist. Those and author/service/overlap/preprint obligations require human confirmation.

## Self-containment

The thesis and primary result displays are in the main paper. Summarize only load-bearing operational facts: current-inclusive replay and bounded-history scope; ranking; gate timing/rollback; actual global splits; no-MBR control semantics; retention normalization; and single-run known-token scope. Full prompts and extended tables can stay supplementary. Replace inaccurate prose instead of expanding the page budget or shrinking typography.

## Detailed current critique

### ISSUE-002 — MAJOR: The main replay definition omits the current failed task and does not distinguish bounded per-skill replay from the unbounded global history used by the implementation.

**Location:** Current PDF p. 4, 4.2 MBR Update Selection with Bounded Replay; `sections/method.tex` lines [24, 24]. **Class:** `necessary_correction`.

> the replay set contains previously seen relevant and irrelevant tasks:

- Step 1: Main p.4 defines a union of two buckets of at most N tasks each. Appendix A.2 (p.11) defines their union with the current task, de-duplicates IDs, permits 2N+1 tasks, and explicitly retains unbounded global seen-task history.
- Step 2: These details change the loss being minimized and the scope of the memory/efficiency claim; they are not merely optional implementation trivia.
- Step 3: A reader implementing the main definition can score a different candidate set and infer a stronger memory bound than the described system provides.

**Proposed route:** Replace the main replay-set definition with the current-inclusive definition already given in Appendix A.2. Define the historical bucket bounds separately. Add one sentence distinguishing bounded replay scoring from global history storage, plus default N=5, M_p=3 and l=400 characters from Appendix D.1. Keep bucket replacement mechanics in the appendix. Add one sentence from A.4 that validation gating occurs after a full training pass and rejection restores the iteration-start predicate; retain the already-correct initial-predicate comparator.

### ISSUE-003 — MAJOR: The main ranking rule describes arithmetic addition, while Appendix A.1 specifies selected-first lexicographic ordering.

**Location:** Current PDF p. 5, 5.4–5.5 Ranked routing; `sections/experiments.tex` lines [47, 47]. **Class:** `necessary_correction`.

> the sum of their binary label and the retrieval score

- Step 1: Main p.5 describes adding a Boolean label and retrieval score. Appendix A.1 (p.11) explicitly says the implementation orders by label, score and original order, and is not an unnormalized arithmetic sum for arbitrary scores.
- Step 2: The rules need not agree across sparse/dense score ranges; this directly determines nDCG, retention and which skills enter the downstream context.
- Step 3: The appendix supplies an operational definition, so the minimal fix is consistency, not an invented score-normalization scheme or a rerun.

**Proposed route:** Replace both sum descriptions in Sections 5.4 and 5.5 with the lexicographic rule from Appendix A.1. Distinguish retrieval pool K=50 from downstream budget k=5. Preserve original retrieval order for final ties and explicitly note that top-k may include predicate-negative skills.

### ISSUE-004 — MAJOR: The main per-dataset 70/15/15 statement contradicts the constrained global split in Appendix C.

**Location:** Current PDF p. 4, 5.1 Benchmarks and Skill Corpus; `sections/experiments.tex` lines [12, 12]. **Class:** `necessary_correction`.

> We split each dataset into train, validation, and test splits with ratios of 70%, 15%, 15%, respectively.

- Step 1: Appendix C.1 (p.16) documents 4,987 retained tasks, 306 gold skills, and 3,491/748/748 global splits. BigCodeBench is 813/123/123 and TheoremQA is 259/106/105, not per-dataset 70/15/15.
- Step 2: The data allocation and generalization population must be clear in the main paper. Shared skills are an intentional evaluation choice, not evidence of task leakage.
- Step 3: The next main sentence already discloses filtering and balancing for shared skills. Retain that counterevidence: the defect is the per-dataset allocation claim and missing exact counts, not demonstrated leakage or a wholly undisclosed shared-skill evaluation.

**Proposed route:** Replace the split sentences with the exact retained counts, global allocation and shared-skill scope. Cite Appendix C.1 for allocation constraints and per-dataset counts. Retain the distinction between the full 26,262-skill retrieval corpus and 306 evaluated gold skills.

### ISSUE-005 — MAJOR: The manifest-linked three-run ablation does not use common initial predicates across all configurations, contrary to the PDF and source claim.

**Location:** Current PDF p. 21, G.1 Replay and Held-Out Gate; Figure 5; `sections/appendix/ablation_components.tex` lines [25, 25]. **Class:** `necessary_correction_conditional_on_historical_binding`.

> All four configurations start from the same initial predicates at iteration 0, as in Figure 5.

- Step 1: Independently inspected all 12 manifest-named conditions_initial.json files. All four run_1 arms and all component-disabled repeats share one canonical predicate payload; Both Enabled/run_2 differs on 26,262 of 26,262 predicates and run_3 on 26,261.
- Step 2: The comparison mixes initialization variation in Both Enabled with fixed initial libraries in the other arms. Different initial metric values alone would not prove this; the predicate-map comparison does.
- Step 3: Run_1 is shared-initialization evidence and the qualitative benefit is not disproved. The three-run averages/SD cannot be described as a paired common-initialization component study. Local paths are mutable: authors must confirm their binding to the plotted historical snapshot.

**Proposed route:** First confirm that the manifest-linked files are the plotted historical runs, or supply immutable historical bindings. If confirmed, correct Figure 5 and G.1–G.3 to distinguish the shared-initialization first-run comparison from heterogeneous three-run averages; qualify component attribution and preserve observed scores. Define the MBR-disabled control as first valid current-task proposal, with historical examples still supplied. A matched-initialization repeat study is optional and requires separate approval.

### ISSUE-006 — MINOR: The main setup still contradicts itself on retriever training and leaves two listed models without a clear role, although the new appendix now specifies baseline and task-evaluation software.

**Location:** Current PDF p. 5, 5.3–5.5 Models and Baselines; `sections/experiments.tex` lines [39, 39]. **Class:** `remaining_alignment_after_concurrent_revision`.

> They are trained on training split and frozen on validation and test splits.

- Step 1: Main Section 5.4 says retrievers are trained, whereas 5.5 says pretrained/lexical retrievers need no training. Section 5.3 lists five models but the backbone comparison reports three.
- Step 2: The concurrent Appendix D.4 now specifies the released frozen 0.6B SkillRouter reranker, its input fields and limits, retrieval implementations and task evaluators. The earlier claim of wholly missing operational baseline/evaluator detail is no longer current.
- Step 3: Correct the conflicting main antecedent, point to D.4 and map the remaining models to verified experiment roles. This is a remaining reporting alignment issue, not proof of an invalid comparison.

**Proposed route:** Use Appendix D.4 to correct the main train/freeze statement and insert one concise SkillRouter description/cross-reference. Ask for the actual experiment roles of Llama-3.3-70B-Instruct and GPT-5.4; remove unused names from the evaluated-model statement if appropriate. Do not duplicate the newly added software/evaluator paragraphs.

### ISSUE-007 — MAJOR: The main superiority comparisons report point estimates without paired uncertainty; repeated-run dispersion is confined to a different ablation experiment.

**Location:** Current PDF p. 5, Table 1 / 6.1–6.3 Primary comparisons; `sections/results.tex` lines [9, 9]. **Class:** `necessary_correction`.

> SkillRouter is the strongest routing baseline,

- Step 1: Table 1 and Figure 4 report primary comparison point estimates. Newly added Appendix E.1 explicitly says these are single evaluations, not repeated seeds, and that statistical-significance tests are not reported; it correctly labels component bands as population SD.
- Step 2: Scientific comparison requires uncertainty appropriate to the paired task design and a clear distinction between task-sampling variation and training-run variation.
- Step 3: Honest disclosure now resolves the reporting ambiguity, but does not estimate paired precision for headline differences. Prefer a saved-prediction analysis; alternatively retain explicitly descriptive claims and remove unsupported significantly wording without fabricating intervals.

**Proposed route:** First reuse saved per-task predictions: report paired task-level differences with dataset-stratified, task-clustered bootstrap intervals for nDCG@10, Recall@5 and downstream success. Keep each task's retriever observations together. State whether estimates condition on one trained checkpoint. If repeats are unavailable, do not describe task-bootstrap intervals as training-seed uncertainty. Remove statistical-significance language without a supporting test. Preserve the newly added statistical-reporting paragraph. If the outputs are unavailable, the proposal-only fallback is to keep explicitly descriptive point estimates and remove unsupported significance language; no automatic rerun.

### ISSUE-008 — MINOR: The main efficiency comparison omits that Figure 6 uses one run per configuration and incomplete recorded token totals, rather than full matched costs.

**Location:** Current PDF p. 7, 7.2 Performance and Token Usage; Figure 6; `sections/ablations.tex` lines [20, 20]. **Class:** `necessary_correction`.

> MBR alone reduces token usage by 10.8%

- Step 1: Appendix G.2/Table 12 identifies the first run per configuration, unknown-usage attempts, cache accounting and phase boundaries. The figure manifest explicitly says known-only totals exclude external/shared initialization.
- Step 2: Observed known-token totals are reportable, but not equivalent to complete training cost or per-query serving efficiency. Figure 5 uses three-run means while Figure 6 uses single-run endpoints.
- Step 3: Readers cannot interpret the cost percentages correctly unless the accounting scope and different run aggregation are present beside the main cost claim.

**Proposed route:** Promote the existing accounting caveat into Section 7.2 and Figure 6, label the x-axis Known recorded tokens (millions), and state one run per configuration. Keep the recorded percentages if their arithmetic is verified; do not impute unavailable usage. Optionally add the already available iteration-only totals as a separate comparison.

### ISSUE-009 — MAJOR: Three backbone endpoints do not establish an irreducible predicate plateau or failure of more capable language models.

**Location:** Current PDF p. 7, 7.3 Skill Routing Performance across LLM Backbones; `sections/ablations.tex` lines [24, 24]. **Class:** `necessary_correction`.

> predicates reach a plateau that cannot be overcomed with more capable LLMs

- Step 1: The same paragraph reports optimized nDCG@1 of 0.742, 0.802 and 0.745; Appendix G.4/Table 14 reports one run per backbone. The 27B model improves on the 4B result.
- Step 2: A nonmonotonic cross-model pattern is not an asymptotic ceiling, and parameter count is not a controlled measure of capability.
- Step 3: The strong plateau sentence overstates otherwise useful empirical findings and can be fixed without new experiments by narrowing the interpretation.

**Proposed route:** Delete the final plateau/expressivity sentence in Section 7.3, retaining the already-correct preceding endpoint summary. Replace significantly improve with improve the reported routing scores unless a supporting statistical test is supplied. A short single-run caveat is sufficient; do not duplicate the endpoint paragraph or mandate further sweeps.

### ISSUE-010 — MINOR: The dependency interpretation is a plausible hypothesis, but the comparison also changes the downstream skill budget and does not isolate dependency utility.

**Location:** Current PDF p. 6, 6.3 Downstream Performance; `sections/results.tex` lines [19, 19]. **Class:** `optional_local_qualification`.

> This finding suggests expanding selected skills to include dependent skills could improve downstream performance even if the dependent skills are not required.

- Step 1: Section 5.5 assigns SkillDAG ten downstream skills and RouterBSI five; Figure 4 reports higher mean downstream success for SkillDAG. The paper already uses tentative could language.
- Step 2: Editorial/scientific qualification: an observational advantage under different budgets should not be presented as evidence isolating the dependency mechanism.
- Step 3: Because the current text already says suggests/could and the budgets are in Section 5.5, this is optional local qualification, not a claim that the paper currently proves a causal dependency effect.

**Proposed route:** Optional: Append a brief budget qualification to the dependency hypothesis and carry method budgets into Figure 4's caption. Preserve the fact that SkillDAG, not RouterBSI, has the highest measured downstream mean. Do not relabel the existing results as a matched-budget test.

### ISSUE-011 — MINOR: The main metric description conflates cutoff F1 with selected-set F1 and leaves the headline retention denominator unspecified.

**Location:** Current PDF p. 5, 5.2 Evaluation Metrics / Appendix E.1 and F.1; `sections/experiments.tex` lines [20, 20]. **Class:** `necessary_correction`.

> We additionally report F1@k to compare filtering capabilities.

- Step 1: Appendix E.1 explicitly says ablation F1 is computed on the predicate-selected set, not the first k ranked entries. Appendix F.1 defines retention as a ratio of task-mean recalls normalized by each method's own Recall@50.
- Step 2: The definitions needed to interpret headline results should appear in brief in the main metrics subsection.
- Step 3: The metrics are defined in the appendix, so this is a terminology/self-containment correction rather than evidence of a calculation error.

**Proposed route:** Replace F1@k with selected-set F1 where that is the measured quantity. Add the ratio-of-means retention definition and explain that SkillDAG's denominator uses its expanded pool. Preserve the task-weighted within-retriever and equal-weight across-retriever aggregation. Align contribution-list Hit@1 with nDCG@1 or state their equivalence once under binary nonempty relevance. Do not impose FP/FN renaming: the appendix already defines its convention.

### ISSUE-012 — MINOR: Redundant phrasing and grammatical errors make the exposition harder to follow, including malformed figure captions.

**Location:** Current PDF p. 2, Introduction; method prose; Figure captions; `sections/introduction.tex` lines [29, 29]. **Class:** `editorial_correction`.

> in a black-box setting called RouterBSI.

- Step 1: The introduction names RouterBSI twice in one sentence; p.4 contains "identify the any" and "must not exceeds"; Figure 4 ends "most other approaches oracle performance"; Figure 5 calls its bands "standard mean and variation".
- Step 2: These are editorial issues, not venue-policy violations. Fixing them should preserve scientific meaning and verified numerical values.
- Step 3: A small copyedit and precise captions would improve readability without a broad rewrite or another experiment.

**Proposed route:** Apply only a targeted copyedit after approval. Remove the duplicate RouterBSI phrase, fix subject/verb agreement and stray notation, and define Figure 5 lines as means and bands as population standard deviations over three runs. Describe Figure 4's aggregation and comparator budgets accurately. Use description.text as the caption source of truth and synchronize embedded captions after approval.

### ISSUE-013 — MINOR: Some figure labels are too small at their placed size, and Figure 8 distinguishes candidate-pool settings only by blue shade.

**Location:** Current PDF p. 1, Figures 1, 4 and 8. **Class:** `optional_editorial_redesign`.

> Figure 1: Skill routing with a task applicability predicate.

- Step 1: Figure 1 internal raster prose is visibly much smaller than its caption. Figure 4 category/value fonts are about 6.44 pt and variant subscripts about 4.51 pt; the same chart starts bars at 0.4. Figure 8 uses same-shaped blue circles.
- Step 2: These are figure-design recommendations, not proven official font-size violations. Existing Figure 1 selected/false labels already provide redundant encoding; not every chart is color-only.
- Step 3: Larger concise labels, direct point labels and either zero-based bars or a dot plot can improve readability without changing a data value or forcing Figure 1 to show the entire method.

**Proposed route:** After approval, shorten and enlarge Figure 1 labels or redraw as vector. Enlarge Figure 4 labels while preserving variant subscripts; use a dot plot or zero-based bars if acceptable. Add direct Top-K labels or distinct shapes in Figure 8. Preserve all measured data and do not invent uncertainty.

## All-figure audit

| Figure | Current page | Finding / proposal |
|---|---:|---|
| Figure 1 | 1 | Shorten task and predicate labels; allocate more vertical space or redraw as a vector while retaining the same semantics. Optionally add an explicit link to the replay/gate mechanism rather than replacing this explanatory example. |
| Figure 2 | 3 | Current caption now includes equality. Optional diagram precision: name replay/validation risk symbols and mark example numbers illustrative. No required gate correction remains. |
| Figure 3 | 6 | Add the normalization and equal-across-retrievers aggregation in the caption or immediate main text; explicitly distinguish absolute recall and method-specific pool coverage. Keep categorical cutoffs labeled. |
| Figure 4 | 6 | Use a larger-font dot plot or larger-font zero-based bars, spell out strict/top-5 labels, and repair the caption with the displayed means and SkillDAG/oracle comparison. |
| Figure 5 | 7 | State test nDCG@1, backbone/retriever, 748-task within-run weighting, three-run mean and ±1 population SD using rounded source variance. Do not call bands confidence intervals or runs different seeds. Disclose the verified initialization variation; the common-initialization claim applies to the first-run comparison, pending historical binding. |
| Figure 6 | 7 | Rename axis Known recorded tokens (millions), state phase scope/exclusions and unknown usage, and label single-run endpoint evidence in main caption or prose. |
| Figure 7 | 8 | Add single-run/existing-candidate qualification and reference-bar meaning. Replace the capacity-ceiling assertion with the observed nonmonotonicity and need for controlled comparison. |
| Figure 8 | 24 | Use known-recorded-token wording consistently, state single-run scope if confirmed by the associated result table, and directly label the three points or use three marker shapes. |

Figure 1 need not become a mandatory method teaser. Small labels and Figure 8 shade-only identification are optional design improvements, not invented official font-size violations. Preserve measured data; Figure 5 bands are population SD, not confidence intervals. All eight graphical assets were reviewed, and their unchanged files were checked while current page locations were remapped.

## Prior criticisms not repeated

- The old 94.68%/93.75% interpretation is not a current main-text defect; the appendix now includes a substantive matched-loss diagnosis.
- Replay-average and initial-predicate-gate equations are already correct. No new theorem, posterior derivation or blanket guarantee disclaimer is requested.
- JTPRO and SkillRouter are already cited. No mandatory GEPA/JTPRO run or human-edit study is established here.
- Dependency expansion is already hypothetical, with budgets disclosed in setup. A local budget caveat is optional.
- The strongest new ablation concern is based on fresh predicate-map checks, not recycled obsolete prose or metric differences alone.

## Decisions needed

- Do the 12 manifest-linked initialization files represent the plotted historical runs? If not, supply immutable bindings; if yes, approve correction of the common-initialization claim.
- Do the frozen retrieval and released SkillRouter descriptions in new Appendix D.4 apply to every reported run, and what are the two remaining main-listed model roles?
- What roles did Llama-3.3-70B-Instruct and GPT-5.4 serve in the reported experiments, and where are their bound configurations?
- Are saved matched per-task predictions available for uncertainty analysis without new model calls?
- What are the intended venue, cycle, submission stage, paper type, deadline and local-PDF/upload permissions?
- Which proposed corrections/redesigns should be applied? Manuscript changes, builds and new experiments remain unapproved.

**Artifacts:** [Proposed solutions](PROPOSALS.md), [review JSON](REVIEW_JSON.json), [proposal-only revision report](REVISION_REPORT.json), [verification](verification.json), [concurrent-change record](concurrent_changes.json), [WISC report](WISC_REPORT.md).

## Sources

[1] https://aclrollingreview.org/cfp
[3] https://acl-org.github.io/ACLPUB/formatting.html
