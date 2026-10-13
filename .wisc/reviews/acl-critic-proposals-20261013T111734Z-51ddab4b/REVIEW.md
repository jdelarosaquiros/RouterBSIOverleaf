# ACL/ARR critique — RouterBSI

**Internal assessment: substantial revision (2/5; not an official ARR score).**

Substantial revision is needed before treating this draft as submission-ready. The editable-predicate routing problem is relevant to language agents and the point estimates are promising. Several main-text interpretations contradict the more precise appendices, and the ablation/cost/provenance limits must be made visible. This is an internal editorial assessment of the frozen PDF, not an official ARR score or acceptance prediction.

## Scope and version
Reviewed all 28 pages of `reviewed_main.pdf`, SHA256 `51ddab4b827e211879ecf8c936083ea5fa2a03f6b34a32d230f98b90f5910d6b`. Main content ends on page 8. Exact venue/cycle/stage remain unknown; long-paper status is an explicit assumption. The live PDF changed externally during this review; see [VERSION_NOTE.md](VERSION_NOTE.md). No manuscript edits or runs were made by this workflow.

## Strengths
- Concrete language-agent problem: applicability of reusable natural-language skill instructions, not semantic similarity alone (§§1,3).
- Editable per-skill predicates, bounded local replay evaluation, strict cold-start gate and fixed model weights form an understandable operational method (§4/AppendixA).
- Six benchmark task types, three retrievers and an explicit initialization baseline; Table1 reports RouterBSI mean nDCG@1=0.687 and nDCG@10=0.728.
- Rich appendices include exact prompts, split counts, replay construction, per-retriever tables and unusually candid caveats about diagnostic provenance and judge imbalance.
- Limitations and ethics acknowledge annotation reliance, checker errors, untrusted code and lack of clinical validation.

## Prioritized issues

15 issues: 13 major, 2 minor, 0 confirmed blockers. Major means material scientific/editorial work, not an automatic desk-rejection rule.

### ISSUE-001 — MAJOR — The main text reverses the meaning of the conditional error percentages and overattributes failures to narrow predicates.

**Location:** p.6, 6.1 Skill Routing Performance.

> 94.68% of TheoremQA and 93.75% of MedCalc-Bench were cases where predicate failed to evaluate to true when the skill was required.

Appendix H.4/Table 18 pp.26–27 says 94.68%=89/(89+5) and 93.75%=90/(90+6) are extra-selection shares under nonstandard labels, not predicate-rejection rates. The required skill is supplied in 16/21 and 15/21 cases. H.2/H.3 distinguishes judgment error, scope mismatch and restrictive predicates.

**Proposed direction:** Replace the percentage attribution and its causal explanation with the supplied bounded interpretation. IMPORTANT: later PDF 0401ac8... and source results.tex already removed the two false sentences; do not reapply that deletion. An optional accurate summary still needs approval.

### ISSUE-002 — MAJOR — The guarantee has the wrong direction and omits its strictly local scope; the validation gate is not a no-regression guarantee relative to the previous policy.

**Location:** p.2, 2.1 Non-Parametric Routing Optimization.

> RouterBSI ensures non-decreasing empirical error on the retained set while bounding replay evaluation costs. A held-out gate additionally rejects updates that regress validation performance below the cold-start performance.

Section 4.2 proves only non-increase of mean replay loss on the same fixed replay set with the unchanged predicate as a candidate. Appendix A.4 says cold-start gating is not monotonic against the previous accepted predicate. G.1 p.20 reports 262 of 2,299 accepted skill–iteration updates score below the previous predicate.

**Proposed direction:** Replace non-decreasing error by a local non-increase statement, and synchronize abstract/introduction/Section 4/Figure 2. State the cold-start comparator and that previous-policy or test monotonicity is not guaranteed. Do not change the algorithm under a wording fix.

### ISSUE-003 — MAJOR — The main method does not describe the executed replay set, ranking, and iteration-end rollback accurately enough to reproduce it.

**Location:** p.4, 4.2–4.3 Method.

> For each skill, the replay set contains previously seen relevant and irrelevant tasks:

A.1 orders lexicographically by Boolean label, retrieval score, then original order, rather than an arbitrary unnormalized sum. A.2 uses current-inclusive H+ ∪ H− ∪ {q}, at most 2N+1 entries, and an unbounded global task history. A.4 gates after a full pass and restores iteration-start predicates. Section 4 omits these distinctions; Section 5.5 uses arithmetic-sum wording.

**Proposed direction:** Promote a compact operational definition to Section 4: distinguish K=50 candidates from k=5 output, current-inclusive replay, uniform slot replacement rather than reservoir sampling, global-history scope, iteration-end cold-start gate and rollback; replace score-sum prose with lexicographic ordering. Retain appendix details.

### ISSUE-004 — MAJOR — The ablation caption claims common initialization, but Appendix G.1 reports an unpaired initialization design.

**Location:** p.7, Figure 5 / 7.1.

> three runs starting from the same initial predicates at iteration 0.

G.1 p.20: both-enabled uses three separately generated libraries; other variants reuse the first both-enabled library; all runs record seed 20260324. Table 10 initial means and SDs differ. This confounds a paired component-effect interpretation; the existing data remain descriptive repeated-run evidence.

**Proposed direction:** Correct Figure 5 caption and Section 7.1 immediately. Either narrow causal language to observed configuration differences, or run a separately authorized paired ablation using shared immutable initial libraries and matched task order per replicate. Do not relabel repeated same-seed runs as independent seeds.

### ISSUE-005 — MAJOR — The main cost comparison omits asymmetric initialization and missing-usage accounting, presenting recorded totals as a controlled efficiency comparison.

**Location:** p.7, 7.2 Performance and Token Usage.

> MBR alone reduces token usage by 10.8% at the cost of a 7.7% relative decrease in nDCG@1 compared with using both.

G.2 pp.20–21 and Table 12 p.24: only both-enabled includes local initialization; the other variants reuse external initialization. Totals exclude unknown usage. 10.8% is reproducible from 1181.026M vs1324.251M recorded total tokens; iteration-only values1011.920M vs1073.904M give about5.8%, a different accounting scope. Figure6 uses first runs, not Figure5 three-run means.

**Proposed direction:** Label Figure6 and Section7.2 as single-run recorded known usage with asymmetric initialization; either present phase-matched existing iteration totals with their remaining caveats or perform complete common-initialization accounting. Do not imply end-to-end savings from an incomplete cost ledger.

### ISSUE-006 — MAJOR — Main-result manifests explicitly mark evidence nonreportable/analysis-only, so the provenance limitation is not confined to appendix diagnostics.

**Location:** p.5, Table 1 / Figures 3–7 / G.3 / H.1 provenance.

> Table 1: Skill routing performance using Qwen3.5 4B. Each router row is the equal-weight mean across BM25, Vector, and SkillSight. Columns report nDCG@1 (N@1) and nDCG@10 (N@10) for each benchmark; Average uses each retriever’s task-weighted scores over 748 tasks.

Parent independently checked seven paper-facing manifests, all unchanged from the baseline snapshot (parent_provenance_evidence.json). Table1 and Figure3 mark reportable=false/completed_noncanonical; all12 Figure5 component-run records are nonreportable; Figures6/7 are marked non-reportable; Figure4 includes a nonreportable Vector run. Recorded reasons include allowed source drift, disabled final audit and judgment cache bypass of exact request reconstruction. This establishes unresolved audit status, not fabrication, numerical falsity or proven test leakage.

**Proposed direction:** Create a read-only run-to-claim manifest identifying exact run IDs, source closure, prompt/caches, split and predicate hashes, retained-checkpoint state, reportability and token scope for every published result. Keep H.1/G.3 exploratory. Audit overlaps before promoting claims; rerun only affected missing canonical evidence after separate approval, never substitute a new run for historical provenance.

### ISSUE-007 — MAJOR — The main split description implies per-dataset70/15/15 allocation and generalization scope broader than the constrained shared-skill protocol.

**Location:** p.4, 5.1 Benchmarks and Skill Corpus.

> We split each dataset into train, validation, and test splits with ratios of 70%, 15%, 15%, respectively.

C.1/Table3: global3491/748/748 after filtering413 of5400 tasks; every partition covers the same306 gold skills from a26262-skill corpus. TheoremQA is259/106/105, not per-dataset70/15/15. Skill vocabulary overlap is deliberate and is not itself task leakage.

**Proposed direction:** Replace the split sentence with exact global counts, filtering and represented-skill scope; summarize exclusion bias in Limitations. Retain per-dataset counts in Table3. Only request unseen-skill/domain tests if authors want that broader claim.

### ISSUE-008 — MAJOR — Baseline/model roles are inconsistent or insufficiently specified, weakening reproducibility of the strongest comparison.

**Location:** p.5, 5.3–5.5 Experimental setup.

> They are trained on training split and frozen on validation and test splits.

Section5.4 says retrievers trained on the training split, while5.5 says pretrained/lexical retrievers require no training. SkillRouter is strongest in Table1 but is not adequately described in5.4. Section5.3 lists five evaluated models;7.3/Table14 report three routing backbones. Appendix D focuses on RouterBSI settings rather than a full baseline protocol. Baseline-stable routing and backbone manifests also explicitly preserve historical candidates, not a controlled common-candidate comparison; actual pool identity cannot be assumed.

**Proposed direction:** Add a compact protocol matrix for each retriever/router: upstream version, frozen/trained components, training labels/split, model role, candidate pool/order, optimization budget, output policy and deviations. Label the present comparisons historical/method-native, not shared-candidate-controlled; candidate-matched reruns are conditional on retaining isolated routing-effect claims. Resolve train/freeze wording from actual manifests. Correct five-model claim to evaluated roles; do not invent results for Llama/GPT-5.4.

### ISSUE-009 — MAJOR — The downstream advantage of graph expansion is confounded with a larger skill budget and cannot identify a dependency mechanism.

**Location:** p.7, 6.3 Downstream Performance.

> This finding suggests expanding selected skills to include dependent skills could improve downstream performance even if the dependent skills are not required.

Section5.5 uses10 skills for SkillDAG versus5 for RouterBSI_top5; Table19 gives0.631 versus0.611 average success. SkillSight-only RouterBSI_top5(0.627) also does not beat retriever-only(0.628) or SkillRouter(0.638). Existing evidence supports averages, not universal improvement or a causal dependency explanation.

**Proposed direction:** State the unequal budgets alongside Figure4 and narrow dependency claims to a hypothesis. Preserve per-retriever reversals. If claiming a dependency benefit, run a matched K=50 candidate and k∈{5,10} output-budget comparison with identical downstream model/context policy and appropriate controls, only after authorization.

### ISSUE-010 — MAJOR — The claimed plateau that stronger LLMs cannot overcome is not established by the three single-run backbone endpoints.

**Location:** p.7, 7.3 Skill Routing Performance across LLM Backbones.

> They also suggest that predicates reach a plateau that cannot be overcomed with more capable LLMs, where it’s difficult for the predicate to be narrow enough to be false for irrelevant tasks but broad enough to be true for all relevant tasks

Table14 final nDCG@1 is0.742,0.802,0.745; the27B endpoint exceeds the4B and120B endpoints. A non-monotonic three-model comparison does not identify a model-independent ceiling or predicate expressivity cause. No significance test is supplied for the word significantly.

**Proposed direction:** Replace the plateau interpretation and untested significance language with descriptive endpoint results. Keep a future-work hypothesis about checker/predicate capacity only if explicitly untested; no new runs are needed for this narrowing.

### ISSUE-011 — MAJOR — Reversed FP/FN terminology and the F1@k versus selected-set-F1 mismatch invite incorrect metric interpretation.

**Location:** p.24, H.2 False Positives and False Negatives.

> we use the authors’ nonstandard error labels: a false positive (FP) is a required skill whose evaluated predicate is false, and a false negative (FN) is a nonrequired skill whose evaluated predicate is true. Thus predicate FP counts |(Gq ∩Cq)\Pq| and predicate FN counts |Pq \ Gq|. We retain standard relevance-based TP as |Pq ∩Gq| and TN as |Cq \ (Pq ∪Gq)|; this hybrid naming is not a standard confusion-matrix convention.

H.2 explicitly calls required-but-rejected FP and nonrequired-but-accepted FN while retaining standard TP/TN. Section5.2 announces F1@k, but E.1/Table10 use selected-set F1; swapping FP/FN leaves symmetric F1 unchanged but reverses precision/recall/error diagnoses.

**Proposed direction:** For publication use standard positive=relevant/selected labels, or neutral Extra/Missing labels if archived naming must be preserved. Map all H tables/examples/captions consistently without changing counts. Define set-F1 versus ranked-cutoff F1 in5.2, and define retention as ratio of task-mean recalls normalized by each method’s own coverage.

### ISSUE-012 — MAJOR — The empirical selection rule is clear, but the title-level Bayesian framing and incremental distinction from reflective optimization need a precise justification.

**Location:** p.4, 4.2 Minimum-risk formulation / Related Work.

> Our risk function is the average skill selection error on replayed tasks.

Section4.2 averages supervised Boolean loss uniformly over replay tasks; no posterior distribution is specified. This can be described as an empirical risk estimate, not automatically a Bayesian inference contribution. Already-cited JTPRO also uses localized reflective edits, minibatch selection and validation-best context; its bounded candidate pool is distinct from a bounded experience buffer. Freitag et al.2022 defines MBR decoding using expected utility under a model distribution.

**Proposed direction:** State the empirical replay distribution explicitly or rename the selector empirical minimum-risk selection, and distinguish this supervised selection from posterior MBR decoding. In Related Work, contrast fixed per-skill task buffers and cold-start gating with JTPRO’s candidate/context optimization; do not claim all nonparametric competitors lack bounded state. A matched reflective-selector control is optional evidence if seeking a stronger mechanism-novelty claim.

### ISSUE-013 — MAJOR — Headline comparisons lack paired uncertainty, while the reported repeated-run variance covers a different ablation experiment.

**Location:** p.5, Table 1 / 6.1 / downstream results.

> RouterBSI improves routing performance of base retrievers by an average nDCG@1 and nDCG@10 across retrievers of 67.0% and 39.7%, respectively

Table1 and Tables19–20 provide point estimates across the same748 tasks and three retrievers; Table10 SDs cover only component ablations. Retrievers are not independent task samples. CHAMP test size is26 and benchmark reversals are visible in Table1. Point estimates can be reported honestly, but confidence in general superiority is not established.

**Proposed direction:** Report observed scores rather than statistical superiority; if making inferential claims, compute paired task-level bootstrap intervals from existing per-task outputs, preserving each task’s retriever results together and task-weighted aggregation. Distinguish task-sampling uncertainty from training-repeat variation; no rerun if preserved outputs suffice.

### ISSUE-014 — MINOR — Several figures need larger labels and self-contained captions; numerical plots must expose readable scales and their evidence scope.

**Location:** p.7, Figures 1–8.

> Figure 6: Impact of MBR replay and held-out validation gate on routing performance (nDCG@1) and token usage. Both enabled gives the strongest performance. MBR alone uses fewer tokens at a performance cost.

Frozen render: Figure1 is a218.25×59.18pt raster with dense tiny text; Figure4 method labels are about6.44pt and bars start at0.4. Figures3/5/6/7 have legible roughly8–9pt text, so they do not all need enlargement. Figure5 misstates initialization; Figures6/8 need known-usage/single-run or exploratory qualifiers. Figure2 omits rejection/rollback. Later Figure3 changed externally.

**Proposed direction:** Redraw only after approval, at ACL column/text width, with concise diagram boxes, non-color cues, distinguishable lines/markers and readable labels. Fix captions and evidence qualifiers before cosmetic work. Keep exact existing numbers; do not add fabricated error bars. Figure2 must show reject/rollback to iteration-start and strict cold-start threshold.

### ISSUE-015 — MINOR — Redundancy, grammar errors and inconsistent notation weaken an otherwise recoverable narrative.

**Location:** p.2, Introduction / method / captions.

> a black-box setting called RouterBSI.

Introduction repeats RouterBSI in the same sentence; Section4 has malformed operational prose; Figure2 says drive revisions selected which are selected; Figure4 ends approaches oracle performance; k denotes retrieval/output budgets. Abstract is201 whitespace tokens after PDF line-number removal, already below the internal250-word target.

**Proposed direction:** After technical fixes, edit only documented errors: remove repeated name, fix efficiencly/don’t directly minimizing/ssk/stray ∂, unify skill indices and K/k, and rewrite captions with description then supported takeaway. Compress generic opening prose to fund a compact main protocol summary; preserve Limitations/Ethics.

## Compliance and self-containment

The observed PDF fits the assumed 8-page long-paper limit, uses anonymous review presentation, and places Limitations/Ethics before References and the two-column appendix after them. All PDF fonts are embedded, and the official style files match the supplied template archive. The exact active stage budget, complete template compliance, supplementary anonymity, actual AI disclosure, checklist and portal logistics remain unverified. Essential method/split/ablation/cost caveats need compact main-text summaries, not more appendix-only detail.

## Decision before further work

Review [PROPOSALS.md](PROPOSALS.md). Existing evidence supports many direct corrections; conditional EXP-001–004 are not automatically required and have not run. No deadline is known, so no claim about finishing before a cycle or needing a later cycle is justified.
