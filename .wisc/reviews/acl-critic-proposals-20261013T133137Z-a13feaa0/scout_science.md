# Independent empirical/method scout — proposals only

The strongest new issue is verified heterogeneous initialization in the nominally common-initialization three-run ablation. Baseline reconstruction and headline uncertainty remain substantive reporting limitations. Many prior alleged omissions are already addressed in the appendix and must not be repeated.

**Findings:** 8 (3 major, 5 minor); no confirmed fundamental-validity blocker. Venue/stage unknown; long-paper assumption. Scientific judgments are not official ARR scores.

## Priority outcome
The common-initialization problem is verified from predicate payloads, not inferred from unequal initial means: Both Enabled runs 2/3 use different libraries while every disabled-component repeat shares run_1. Preserve the existing controlled run_1 descriptive evidence; do not discard the measured results.

## SCI-001 — MAJOR: The claimed common-initialization control fails across repeats

**Anchor:** PDF p20, review lines 1632–1635; `source/sections/appendix/ablation_components.tex:25`.
> All four configurations start from the same initial predicates at iteration 0

**Problem:** The common-initialization claim for the three-run component ablation conflicts with the initial libraries at the paths bound by its figure manifest.

**Evidence:**
- PDF p20 and Figure 5 p7 claim common initial predicates. Table 10 p23 has unequal initial means; that alone would not prove unequal predicate strings.
- Fresh read-only audit of all 12 manifest-named conditions_initial.json files: all nine component-disabled runs and Both Enabled/run_1 share predicate hash c4944010690969b90761102333978ac8dfbd14a649435f4b6710e656f4b90287. Both Enabled/run_2 differs on all 26,262 predicates (hash d3c9bc36c17e93d86a6867f38c961ffad8a40a2edb1277a75415a93cee1b89e5); run_3 differs on 26,261 (hash db60f926ebcddb2a053bab12bd482575aa88eccef068dee1ffbd28c404ab5277). Canonical hashing includes conditions.sra only, excluding metadata.
- The arms therefore do not vary the same factors across repeats, weakening controlled attribution and comparability of the reported SD.

**Counterevidence / limits:**
- Run_1 shares initialization across all four arms. Table 12 p24 reports the existing single-run nDCG@1 contrast 0.742 (Both Enabled) versus 0.684 (Only MBR). The qualitative component benefit is not disproved.
- The local run audit is external unpublished evidence, not content printed in the PDF; the runs might have changed since the PDF snapshot.

**Required proposal (not executed):** Reconcile all plotted runs with their initial-policy hashes. If these are the plotted runs, remove the all-repeats common-initialization claim, disclose the heterogeneous repeat design, and distinguish the already available shared-initialization run_1 descriptive comparison from the unmatched three-run means. Do not call the latter paired seeds.

**Required inputs:** Author confirmation that the manifest-named local runs are the plotted snapshot runs, or immutable historical initial-policy bindings if not.

**Acceptance criteria:**
- Map each of the 12 plotted runs to an initial-policy digest and evaluation protocol.
- Restrict common-initialization language to sets with equal predicate payloads.
- Figure 5, §7.1, Appendix G.1/Table 10 disclose matched versus unmatched repetitions; no score is changed to hide the difference.

**Optional only:**
- A future matched-initialization repeat study could restore stronger controlled attribution; not required for honest narrowing and not authorized here.

## SCI-002 — MAJOR: Baseline identities and adaptation/training protocols are under-specified

**Anchor:** PDF p5, review lines 315–350; `source/sections/experiments.tex:39`.
> They are trained on training split and frozen on validation and test splits.

**Problem:** The baseline section contradicts the training-free retriever description and does not establish how the strongest learned baseline or the adapted optimization baselines were instantiated.

**Evidence:**
- §5.4 p5 lines 315–325 says retrievers are trained; §5.5 lines 332–334 says pretrained/lexical retrievers require no training.
- SkillRouter is the strongest routing comparator, but the main setup and inspected appendices do not give its actual checkpoint, task-supervision/fitting protocol, validation selection or adaptation. The detailed RouterBSI prompts/settings do not substitute for baseline configurations.
- The current snapshot Table 1 provenance says archived candidate rankings are retained and the comparison is not a controlled shared-candidate comparison. Its selection.json binds the current final Vector run and explicitly overrides the stale input map; no obsolete nonreportable-run blocker is asserted.

**Counterevidence / limits:**
- The paper specifies default model, generally top-50 routing, SkillDAG expansion and downstream budgets. Appendix H.3 verifies identical SkillRouter/RouterBSI candidate lists for the two diagnosed datasets, but not for every comparator and dataset.

**Required proposal (not executed):** Add a compact baseline record naming each actual checkpoint/code revision, frozen versus trained components, supervision/splits, tuning/optimization budget, validation selection, and candidate/ranking deviations. Resolve the retriever training contradiction from actual configurations. Scope headline comparisons to the archived configurations unless matching is verified.

**Required inputs:** Actual configuration and training/selection records for SkillRouter, Skill-Pro, SkillDAG, LLM Select, Vector and SkillSight.

**Acceptance criteria:**
- Every Table 1 method has an unambiguous implementation identity and tuning/training protocol.
- No retriever is simultaneously called task-split-trained and training-free.
- Only verified comparisons are labeled shared-candidate; deviations are disclosed.

**Optional only:**
- A same-feedback, same-budget reflective predicate optimizer is a useful optional baseline, not an automatic mandatory experiment.

## SCI-003 — MAJOR: Comparison-level uncertainty is missing for headline advantages

**Anchor:** PDF p5, review lines 358–362; `source/sections/results.tex:9`.
> SkillRouter is the strongest routing baseline

**Problem:** The main inter-method routing and downstream advantages are point estimates without comparison-level uncertainty; component SD does not establish the reliability of these advantages.

**Evidence:**
- Table 1 p5 has point-estimate nDCG; Figure 4 p6 shows 0.611 RouterBSI_top5, 0.602 SkillRouter, and 0.596 strict. Appendix Table 21 p29 supplies the downstream retriever breakdown but no uncertainty.
- source/figs/downstream_average/provenance.text explicitly says no uncertainty estimates supplied. Three retrievers reuse the same 748 task IDs and are not independent task replicates.
- Three-run population SD exists in Table 10 for component ablations, not main competitor contrasts; SCI-001 further qualifies that design.

**Counterevidence / limits:**
- Task-weighted within-retriever and equal-weight across-retriever aggregation is already correctly defined in Table 1 and Appendix E.1. Descriptive ordering remains valid without statistical significance.

**Required proposal (not executed):** Minimally identify actual repeat counts and state that headline differences are descriptive without comparison-level confidence estimates. If inferential claims are desired, propose a paired analysis from saved task outputs, preserving each task across retrievers and separately acknowledging unmeasured training-run variability; do not run it under this task.

**Required inputs:** Actual repeat count and run-selection protocol for Table 1 and Figure 4.

**Acceptance criteria:**
- Main captions state run/task units and whether uncertainty is available.
- Retrievers are not treated as independent training repeats.
- Small downstream gaps and backbone proximity are not called statistically significant or equivalent without a suitable analysis.

**Optional only:**
- With separate authorization, stratified paired bootstrap over task IDs keeping all retriever outcomes together can estimate test-sample uncertainty conditional on trained policies; it cannot establish training-seed robustness.

## SCI-004 — MINOR: Main protocol obscures global allocation and represented-skill filtering

**Anchor:** PDF p4, review lines 283–292; `source/sections/experiments.tex:12`.
> We split each dataset into train, validation, and test splits with ratios

**Problem:** The main paper describes per-dataset 70/15/15 splits, whereas the appendix documents a constrained global allocation and a filtered shared-skill evaluation.

**Evidence:**
- Appendix C.1 p16/Table 3 p17 report 5,400 tasks reduced to 4,987, gold vocabulary reduced from 636 to 306, and a global 3,491/748/748 split. BigCodeBench is 813/123/123 and TheoremQA 259/106/105, not per-dataset 70/15/15.
- All retained gold skills occur in every split. This material scope is stated clearly only in Appendix C.1.

**Counterevidence / limits:**
- Appendix C.1 explicitly scopes generalization to new tasks involving represented skills; task IDs are disjoint. This is not evidence of leakage. Appendix C.2 already says annotations need not exhaust helpful skills.

**Required proposal (not executed):** Replace per-dataset ratio wording with the actual global constrained allocation; summarize filtering and all-306-skill overlap in §5.1. State that routing metrics measure recovery of released skill annotations on held-out tasks, not unseen-skill acquisition or exhaustive downstream necessity.

**Required inputs:** Existing manuscript evidence suffices.

**Acceptance criteria:**
- §5.1 agrees with Table 3 on global versus per-dataset allocation.
- The main paper communicates filtered represented-skill scope and released annotation targets.

**Optional only:**
- Unseen-skill/tail-skill or independently audited-label evaluations are optional extensions if broader claims are sought.

## SCI-005 — MINOR: Downstream dependency interpretation is confounded by budget

**Anchor:** PDF p6, review lines 394–412; `source/sections/results.tex:19`.
> This finding suggests expanding selected skills to include dependent skills could improve downstream performance even if the dependent skills are not required.

**Problem:** The dependency explanation is not isolated because SkillDAG receives a different number and pool of skills, and top-five versus strict is not purely an addition-only intervention.

**Evidence:**
- §5.5 p5 lines 352–355 gives SkillDAG ten skills versus five for fixed-budget RouterBSI/SkillRouter; Figure 4 p6 displays their observed means.
- Appendix E.1 and H.5 explain that top-five may pad or truncate the predicate-selected set.

**Counterevidence / limits:**
- The text calls the mechanism a suggestion and reports SkillDAG as best downstream. Appendix H.5 already rejects inferring causal harm merely from non-gold context.

**Required proposal (not executed):** Label §6.3/Figure 4 as an unequal-budget deployment comparison; annotate SkillDAG=10, fixed methods=5, strict=variable. Recast dependency expansion as an untested hypothesis, and describe top-five as padding or truncating strict selection.

**Required inputs:** Existing manuscript evidence suffices.

**Acceptance criteria:**
- The caption or adjacent text shows relevant budgets.
- The dependency mechanism is explicitly untested and top-five is not presented as addition-only.

**Optional only:**
- A future matched-skill-budget or matched-token-budget comparison could test the dependency mechanism; optional when the current claim is narrowed.

## SCI-006 — MINOR: Main ranking rule differs from implemented lexicographic ordering

**Anchor:** PDF p5, review lines 329–350; `source/sections/experiments.tex:47`.
> we rank them by the sum of their binary label and the retrieval score

**Problem:** The main rule is an arithmetic sum, while Appendix A.1 specifies selected-first lexicographic ordering and explicitly excludes a general unnormalized sum.

**Evidence:**
- PDF p5 lines 345–350 says sum; Appendix A.1 p11 lines 821–832 orders by label, retrieval score, then original order and explains sum equivalence only for SkillSight reciprocal-rank scores.

**Counterevidence / limits:**
- The operational rule is present in the appendix. This is not an absent-algorithm claim or proof of wrong code.

**Required proposal (not executed):** Use the existing Appendix A.1 lexicographic rule in §5.4–5.5. Keep score-sum equivalence only as a retriever-specific explanation.

**Required inputs:** Existing manuscript evidence suffices.

**Acceptance criteria:**
- Main definitions specify selected-first lexicographic ordering with retrieval tie breaking, with no universal unnormalized-sum claim.

## SCI-007 — MINOR: Backbone plateau claim is broader than three measured runs

**Anchor:** PDF p7, review lines 454–473; `source/sections/ablations.tex:24`.
> They also suggest that predicates reach a plateau that cannot be overcomed with more capable LLMs

**Problem:** Three heterogeneous single-run backbones do not establish that more capable models cannot improve the predicates.

**Evidence:**
- §7.3 p7 reports 0.742, 0.802, 0.745 final nDCG@1; Appendix Table 14 p25 states one run per backbone. The middle-sized model improves over both others.
- A ten-iteration optimization plateau is not a capability ceiling. Appendix H.3 p28 already reports mixed late changes and says more training is not an established remedy.

**Counterevidence / limits:**
- Nonmonotonic observed scores and smaller-model proximity are supported descriptive findings.

**Required proposal (not executed):** Retain the observed ranking and remove the impossibility/ceiling inference. State that these runs do not identify whether constraints come from representation, checking, proposal search or budget. Mark additional iterations/human editing in §6.1 as untested possible interventions, consistent with Appendix H.3.

**Required inputs:** Existing manuscript evidence suffices.

**Acceptance criteria:**
- No general inability of stronger models is inferred.
- Potential remedies for MedCalc/TheoremQA are labeled untested.

## SCI-008 — MINOR: PDF/source scientific wording is not fully bound

**Anchor:** PDF p2, review lines 147–150; Figure 2 p3; `source/sections/related_works.tex:8,14`.
> RouterBSI ensures non-decreasing em- 147 pirical error on the retained set

**Problem:** The primary PDF says non-decreasing error where supplied source says non-increasing; Figure 2 gate wording also differs.

**Evidence:**
- PDF p2 lines 147–148 says non-decreasing; source/sections/related_works.tex:14 says non-increasing. The correctly scoped average replay inequality itself is correct.
- PDF Figure 2 p3 says higher than the initial predicate; source related_works.tex:8 says higher or equal. PDF §4.3 p4 and Appendix A.4 already specify strict improvement.

**Counterevidence / limits:**
- Source already corrects these strings, but that does not mean the reviewed PDF contains the fixes. This is a binding/wording issue, not an error in the replay inequality or initial-predicate comparator.

**Required proposal (not executed):** For a future authorized build, use the already-correct source wording and bind the compiled PDF to exact source hashes. Verify both PDF strings; retain the correct scoped replay/gate definitions unchanged. No build or edit is authorized here.

**Required inputs:** Author-confirmed source/PDF build binding.

**Acceptance criteria:**
- The future reviewed PDF contains non-increasing error and a caption consistent with strict gate admission.
- The source binding and PDF hash are recorded without claiming this PDF already includes corrections.

## Initial-policy provenance audit
These are fresh local unpublished artifacts, not hashes printed in the PDF. Snapshot Figure 5 selection_manifest.json names these 12 runs. Full paths and hashes are in JSON; authors should confirm historical binding.

| Method | Run | Predicate payload hash | Changed predicates vs Both Enabled run_1 |
|---|---|---|---:|
| Both Enabled | run_1 | `c4944010690969b90761102333978ac8dfbd14a649435f4b6710e656f4b90287` | 0 |
| Both Enabled | run_2 | `d3c9bc36c17e93d86a6867f38c961ffad8a40a2edb1277a75415a93cee1b89e5` | 26262 |
| Both Enabled | run_3 | `db60f926ebcddb2a053bab12bd482575aa88eccef068dee1ffbd28c404ab5277` | 26261 |
| Both Disabled | run_1 | `c4944010690969b90761102333978ac8dfbd14a649435f4b6710e656f4b90287` | 0 |
| Both Disabled | run_2 | `c4944010690969b90761102333978ac8dfbd14a649435f4b6710e656f4b90287` | 0 |
| Both Disabled | run_3 | `c4944010690969b90761102333978ac8dfbd14a649435f4b6710e656f4b90287` | 0 |
| Only MBR | run_1 | `c4944010690969b90761102333978ac8dfbd14a649435f4b6710e656f4b90287` | 0 |
| Only MBR | run_2 | `c4944010690969b90761102333978ac8dfbd14a649435f4b6710e656f4b90287` | 0 |
| Only MBR | run_3 | `c4944010690969b90761102333978ac8dfbd14a649435f4b6710e656f4b90287` | 0 |
| Only Gate | run_1 | `c4944010690969b90761102333978ac8dfbd14a649435f4b6710e656f4b90287` | 0 |
| Only Gate | run_2 | `c4944010690969b90761102333978ac8dfbd14a649435f4b6710e656f4b90287` | 0 |
| Only Gate | run_3 | `c4944010690969b90761102333978ac8dfbd14a649435f4b6710e656f4b90287` | 0 |

## Do not reissue already resolved criticisms
- The average replay-risk inequality is correctly scoped; no per-example preservation guarantee is required or inferred.
- The gate explicitly compares with the initial predicate and the appendix warns it is not monotonic against the previous predicate. Do not reissue that as a missing caveat.
- Test-only evaluation/no test checkpoint selection is stated in Appendix A.4. Repeated use of validation is optimization, not demonstrated test leakage.
- Appendix C gives exact split/filtering counts, labels, skill corpus and license; the critique is main-text scope consistency, not total absence.
- Appendix A–D provide replay replacement rule, current-task inclusion, prompts, parameters, caching, retries and failure behavior; no generic missing-prompts critique.
- Appendix E/F define task weighting, nDCG/recall/F1, ratio-of-means retention and own-pool SkillDAG normalization. Aggregation is not mathematically erroneous.
- The evaluator diagnostic is explicitly model-adjudicated agreement, not human accuracy; it reports class imbalance, low positive agreement/recall, always-False reference, non-blinding and audit limitations. Do not claim these caveats are absent.
- Matched MedCalc/TheoremQA error analysis separates retrieval misses, predicate design, checker mistakes and annotation mismatch; reported causal interpretations are qualified.
- Current Table 1 selection.json binds a final Vector run and documents stale input-map override; no old analysis-only/nonreportable blocker is carried forward.

## Optional extensions, not required experiments
- Human validation of gold skill completeness and positive predicate decisions would strengthen external validity, but existing annotation and AI-audit limitations are already explicitly acknowledged.
- Unseen-skill or unfiltered-tail evaluation is useful only if broader generalization is claimed.
- The global seen-task history remains unbounded (Appendix A.2 p11); preserve the distinction between bounded per-skill replay evaluation and total storage. No blanket constant-memory claim is established here.
- Deployment latency/token cost, a same-budget reflective optimizer, and controlled dependency expansion are useful extensions, not mandatory reruns for the narrowed present claims.

## Inspection and scope
Exact inspected paths appear in `scout_science.json`. Inspected `reviewed_main.pdf` through `pages.json`/`paper.txt`, relevant source sections and appendix, figure/table selection/provenance, local ACL guides, and only the 12 external initial-policy files needed to verify the ablation claim. No manuscript or skill/memory files were changed; no experiments/reruns were launched.

- All scientific findings concern PDF text and actual source anchors; no independent visual/layout review was performed.
- Remaining section sources were searched for baseline/statistical details rather than all read verbatim; main PDF text and detailed relevant appendix files were inspected.
- No fresh literature or policy verification, code execution study, human annotation audit, or experimental rerun was performed.
- External policy files may not be immutable; hashes are reported for exact bytes/predicate payloads read during this scout.
