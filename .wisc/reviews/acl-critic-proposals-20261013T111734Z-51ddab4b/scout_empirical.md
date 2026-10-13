# Read-only empirical audit — frozen PDF 51ddab4b

## Scope and boundary

- Reviewed all main results/ablations (pp. 5–8), Appendix E–H (pp. 18–28), and relevant C/D protocol details. **There is no Appendix I in this 28-page frozen PDF**; H.5 and Table 20 end p. 28.
- Frozen `reviewed_main.pdf` SHA-256 verified as `51ddab4b827e211879ecf8c936083ea5fa2a03f6b34a32d230f98b90f5910d6b`. All PDF anchors below refer to that frozen version, not live main.pdf.
- Live main.pdf had already changed to SHA-256 `0401ac8acbac22ecefdd7b50d0582895aaa105ea094fa5e23cd42a569b0a27c7`. Live `sections/results.tex` no longer contains the 94.68%/93.75% causal-error sentence that remains in the frozen PDF. Live figure previews/rendering script also have external changes. Parent should mark superseded issues after its separate comparison, not silently replace the reviewed evidence.
- Read current selected-data CSVs/manifests and source routing/recall CSVs to resolve numerical identities. Both source routing/recall CSV hashes match their paper selection manifests. Numerical matches to frozen PDF tables are noted below; this does not certify that every current source file was historically compiled into that PDF.
- No manuscript edits, builds, experiments, model calls, uploads, or figure generation performed. Only `scout_empirical.*` reports are written by this scout in the authorized review directory.

## Prioritized findings

### EMP-01 — MAJOR: load-bearing results have unresolved noncanonical provenance, not merely the explicitly qualified diagnostics

**PDF anchors:** p. 5, Table 1: “Skill routing performance using Qwen3.5 4B.”; p. 7 §7.1: “Combining MBR with the held-out gate further improved final performance”; p. 22 H.1: “The source is explicitly noncanonical and nonreportable”; p. 22 G.3: “We therefore treat this figure as analysis-only evidence.”

**Evidence:** Local paper-facing manifests for Table 1 and Figure 3 carry `reportable:false`, `status:completed_noncanonical`, and “analysis-only; publication validity not established.” The Figure 5 selection manifest marks all 12 component runs nonreportable. Its recorded reasons are source drift allowed, final audit disabled, and runtime judgment cache potentially bypassing exact request reconstruction. Figure 6 and Figure 7 selection manifests also mark nonreportable/analysis-only. Figure 4's selection metadata explicitly includes the nonreportable fixed Vector RouterBSI run. The PDF carefully qualifies Figure 8 and H.1 but presents the load-bearing main comparison/ablation/backbone results without the equivalent scope limitation.

**Paths:** `tables/skill_routing_performance_average/{selection.json,artifact-manifest.json}`; `figs/average_retention_degradation/selection.json`; `figs/mbr_replay_test_ndcg@1_std/selection_manifest.json`; `figs/performance_token_usage/selection_manifest.json`; `figs/routing_performance_across_llms_init/selection_manifest.json`; `figs/downstream_average/selection.json`.

**Interpretation:** The metadata is evidence of an unresolved audit/provenance gate, **not proof that the numbers are fabricated, test-contaminated, or numerically wrong**. Regenerating plots or changing wording cannot establish historical validity.

**Available fix:** Add accurate shared provenance qualification to every affected claim and identify exact source runs/artifacts. Trace each flagged run to frozen configuration, source, cache, candidate and prediction evidence, and determine which audit obligations can still be discharged retrospectively.

**Additional evidence:** If existing records cannot establish the execution/protocol binding, audited replacement runs would be required for confirmatory claims, or claims must remain explicitly exploratory. Do not prescribe rerunning everything before checking existing audit evidence. Acceptance: each headline result has an explicit run-to-table mapping and resolved audit status or a conspicuous analysis-only qualification; no relabeling `reportable` by editorial fiat.

### EMP-02 — MAJOR: main error attribution reverses what its percentages measure; existing Appendix H already supplies the correction

**PDF anchor:** p. 6 §6.1: “94.68% of TheoremQA and 93.75% of MedCalc-Bench were cases where predicate failed to evaluate to true when the skill was required.” Adjacent: “The cause of these failures was likely overly narrow predicates”.

**Exact contradiction:** H.4 pp. 26–27 / Table 18 gives 21 task–retriever downstream-disagreement cases per dataset. TheoremQA supplied top-five sets have 89 extra non-gold skill occurrences and 5 missing-required occurrences; MedCalc has 90 extras and 6 misses. The quoted percentages are **89/(89+5)=94.68085% and 90/(90+6)=93.75%**: shares of extra non-gold occurrences among occurrence errors, not fractions of tasks or rejected required predicates. Required skills are actually supplied in **16/21 and 15/21** cases, respectively. Thus only **23.81% and 28.57%** of these conditional cases omit the gold skill from top five. The predicate-selected sets separately have 24 extras/12 missing for TheoremQA and 0 extras/8 missing for MedCalc. Padding a five-skill list where only one gold skill exists guarantees at least four non-gold entries even for full coverage.

**Existing mechanism evidence:** Table 17 p. 27 classifies all 331 TheoremQA task–skill selection errors: 114 incorrect judgments (34.4%), 70 restrictive/misdirected predicates (21.1%), 78 annotation/scope mismatches (23.6%), 14 broad predicates (4.2%), 42 ambiguous (12.7%), 13 retrieval misses (3.9%). H.3 includes explicit evaluator mistakes even where predicates match the task. H.2 already warns that failure to activate alone is not evidence of narrowness.

**Available fix:** Replace the main causal paragraph with a short correct summary of H.4 and H.2/17: many downstream disagreements persist with the required skill supplied; errors have heterogeneous diagnosed sources. More iterations/manual edits are untested possibilities, not demonstrated remedies. No new experiment is needed to correct the misstatement.

**Acceptance:** Neither 94.68 nor 93.75 is called a required-skill rejection rate or a percentage of tasks. The supplied-set/predicate-set and task/occurrence denominators are explicit. Note: live source already removed the offending sentence; frozen PDF has not.

### EMP-03 — MAJOR: the component ablation is not a matched-initialization experiment as Figure 5 claims

**PDF anchor:** p. 7 Figure 5: “three runs starting from the same initial predicates at iteration 0.”

**Existing contradictory disclosure:** G.1 p. 20: “The both-enabled configuration uses three separately generated initial libraries; the other configurations reuse the first both-enabled library. All runs record seed 20260324.” Hence variation for Both Enabled mixes initialization and trajectory variation, unlike the comparator repetitions. Table 10 reports initial means nDCG@1 0.521 for Both Enabled versus 0.524 Only MBR, 0.523 Only Gate, 0.525 Both Disabled. These different scores alone would not prove different predicates; the explicit G.1 disclosure does.

**What is supported:** Three-run final means are 0.723708 / 0.691176 / 0.644385 / 0.560160. Both Enabled has the best observed endpoint. Source bands are ± one population SD, not confidence intervals; Table 10/11 specify this, but Figure 5 says merely “standard mean and variation.” All share one split/replay seed; these are three observed runs, not three independent split seeds.

**Available fix:** Correct the caption and describe this as an unmatched-initialization comparison; replace “standard mean and variation” with “mean ± one population standard deviation across three runs”; promote G.1's initialization caveat to the main ablation. Keep the positive observed ordering but do not claim the difference cleanly isolates the mechanisms.

**Additional evidence:** A paired common-initial-library ablation across multiple libraries and controlled candidates/evaluator settings is needed for stronger causal attribution. First check whether saved matched pairs already exist. Acceptance: caption matches G.1, uncertainty quantity and experimental unit are unambiguous, and paired/isolation claims are supported or removed.

### EMP-04 — MAJOR: efficiency percentages are arithmetically correct but use unequal/incomplete cost boundaries

**PDF anchors:** p. 7 §7.2: “MBR alone reduces token usage by 10.8% at the cost of a 7.7% relative decrease in nDCG@1”; Figure 6 axis “Total Token Usage (millions)”.

**Resolved numerical question:** This is **not an arithmetic contradiction with §7.1**. Figure 5/Table 10 are three-run means (Both 0.723708, MBR 0.691176: Both improves 4.70676%; dropping Both to MBR loses 4.49518%). Figure 6/Table 12 are first-run snapshots (Both 0.74197861, MBR 0.68449198: MBR loses 7.74775%). §7.1's MBR-versus-gate +7.3% is 7.26134% from 0.644385 to 0.691176. Main text fails to announce the switch to single-run evidence; the appendix does.

**Accounting problem already disclosed in G.2 pp. 20–21:** Only Both Enabled records local initialization; other runs reuse an external initialization whose generation cost is excluded. Known totals are Both 1324.250594M, MBR 1181.025935M, Gate 866.352051M, Neither 840.052489M. These yield 10.81553% MBR saving and 40.58954% / 52.85363% replay overhead. Iteration-only Both/MBR are 1073.903550M / 1011.919595M, yielding **5.77184%**, not 10.8%, MBR saving. Iteration-only replay overhead is 52.80930% without gate and 53.10133% with gate. Known totals exclude 16/20/13/12 attempts with unknown usage. Source records explicitly say `Complete=False`, `Known Only=True`, `Source Reportable=False`. Also G.1 says disabling the gate does not remove calculation of candidate-validation scores, so this is not a clean cost of removing validation computation.

**Available fix:** Label Figure 6 “known recorded run-local tokens,” explicitly state one run per condition and unequal initialization boundaries, and distinguish this from serving latency, complete total cost, or marginal component overhead. Use the already available iteration-only comparison if the claim is about iterative optimization costs, with its limitations. No invented missing token counts.

**Additional evidence:** Symmetric whole-run accounting and resolved missing usage are needed for a complete cost claim; uncertainty across matched runs would strengthen a claimed tradeoff. Acceptance: all comparisons state phase boundaries and run count, exclude unsupported causal cost language, and §7.1 vs §7.2 estimands are clearly separated.

### EMP-05 — MAJOR: baseline fairness/reproduction is under-specified; routing isolation and downstream skill budgets differ

**PDF anchors:** p. 5 §5.5: “The skill routing baselines are conditioned on the top 50 retrieved skills”; “we set k = 10 for SkillDAG because k = 5 would match the retriever’s performance.” §5.4: “They are trained on training split and frozen on validation and test splits.” §5.5: “they do not require training.”

**Evidence:** The two training statements conflict or have an unclear antecedent. SkillRouter appears in every comparison as the strongest baseline but §5.4 does not explain its checkpoint, training data, supervised/zero-shot use, candidate input and adaptation. The appendices give detailed RouterBSI prompts and knobs, not an equivalent per-baseline protocol and compute budget. Paper-facing routing manifest explicitly states: “Archived candidate rankings are retained; this is not a controlled shared-candidate comparison.” Figure 7's manifest similarly says historical candidates are preserved, not a common-candidate comparison. Small Recall@50 differences even among nominally same-retriever, non-expanding methods underscore why exact candidate identity must be disclosed (BM25 native 0.797282 vs RouterBSI 0.795945; SkillSight native 0.917714 vs Skill-Pro 0.919051). Do not infer the cause from scores alone.

**Downstream scope:** SkillDAG receives 10 skills while RouterBSI top5/SkillRouter receive 5; strict output is variable. This is disclosed and can be a valid method-native comparison, but not a matched context-budget mechanism ablation. The +4.41% recall comparison uses SkillDAG@10 vs RouterBSI@5 (ratio of aggregate recalls); it cannot establish that dependencies, rather than twice the skill budget, caused superior downstream performance.

**Available fix:** Add a method protocol matrix: exact checkpoint/version, input skills/text, training/validation labels, optimization passes, prompts/temperature, scoring/ranking, candidate identities, downstream skill/token/tool budget, and protocol deviations. Resolve retriever training wording. Label historical and native-budget comparisons explicitly. Replace dependency causality with an untested hypothesis.

**Additional evidence:** Common candidate pools for non-expanding routers and matched context-budget controls (e.g. top10 retrieval/RouterBSI alongside SkillDAG10) are required to isolate routing/dependency effects; inspect archives first. No need to strip legitimate SkillDAG capabilities from its native comparison. Acceptance: readers can distinguish native performance from controlled attribution, and reproduce each row's protocol.

### EMP-06 — MAJOR: backbone results do not establish a capability-independent plateau

**PDF anchor:** p. 7 §7.3: “predicates reach a plateau that cannot be overcomed with more capable LLMs”.

**Counterevidence:** Table 14/ Figure 7: Qwen4B 0.520053→0.741979, Qwen27B 0.635027→0.802139, GPT-OSS120B 0.685829→0.744652. All improve; Qwen27B is appreciably better than 4B in final nDCG@1 and all three reported final metrics. The final 4B/120B ratio is 99.64104%, but one close pair across different model families is not a universal capacity ceiling. Table 14 has one run per backbone; Figure 7 source explicitly has no uncertainty and is not a controlled common-candidate comparison. The model set in §5.3 lists five models, but main/appendix result tables here contain three routing backbones and Qwen4B downstream results; map the uses of Llama70B/GPT5.4 or narrow that statement.

**Available fix:** Keep the measured gain and non-monotonic ordering. Replace ceiling claim with “The final scores are not monotonic in parameter count in these runs.” State single-run and candidate caveats and map each listed model to its experiment.

**Additional evidence:** Matched candidates and prompts, repeated runs and training trajectories of stronger models would be needed for a saturation explanation. No new evidence needed to narrow the claim. Acceptance: no universal ceiling or statistical-significance implication from three endpoints.

### EMP-07 — MAJOR/MINOR depending on intended claim: strongest and downstream differences lack paired uncertainty beyond the component ablation

**PDF anchors:** p. 7 §7.3: “significantly improve the routing performance”; p. 6 §6.3: “2.5% higher”; p. 5 Table 1 caption: “equal-weight mean across BM25, Vector, and SkillSight.”

**Existing uncertainty:** Do not claim the whole paper lacks repeats: G.1/Table 10/11 provide three-run population SDs for the component ablation. However, Table 1, Figure 4, and backbone/capacity comparisons do not supply corresponding repeated-run/paired uncertainty. Retrievers evaluate the same 748 tasks and are not three independent samples of tasks. SkillRouter versus RouterBSI top5 average downstream improvement is only **0.89127 percentage points**, i.e. **1.48148% relative**; counts across the three evaluations are 1350 versus 1370 successes out of 2244 task–retriever observations (not 2244 independent tasks). Under SkillSight alone RouterBSI top5 is 469/748 versus SkillRouter 477/748 and native retriever 470/748. Mean improvement is not per-retriever dominance. CHAMP has only 26 test tasks.

**Available fix:** Use “observed” rather than “significantly” absent a significance analysis; expose per-retriever reversals (Table 19 already has them). Add paired uncertainty from existing saved per-task outputs using task-clustered/resampling analysis appropriate to shared tasks; do not treat retriever means as independent replicates. Report run variability separately from test-sampling uncertainty. This is offline analysis, not necessarily new experiment runs.

**Additional evidence:** New repeated training/evaluation runs only if needed to estimate model/run variability and archives lack them. Acceptance: effect sizes and uncertainty units are declared; a confidence/significance claim is tied to an actual appropriate analysis or removed.

### EMP-08 — MINOR but important: hybrid reversed FN/FP notation encourages the main-text error and should be standardized

**PDF anchor:** p. 24 H.2: “a false positive (FP) is a required skill whose evaluated predicate is false”; next: “a false negative (FN) is a nonrequired skill whose evaluated predicate is true.”

**Evidence:** TP/TN retain standard relevance-positive meanings while FP/FN are swapped. H.2 admits the hybrid naming is nonstandard. Table 16 totals themselves reconcile correctly when evaluated over C∪G: each row total equals 50×tasks + retrieval misses; TP + missing-required equals task count for these single-gold datasets. The issue is notation, not faulty counts. H.1 provisional adjudicator confusion matrix uses expected predicate satisfaction, a different target, and must remain distinct from gold-skill selection.

**Available fix:** Swap FN/FP labels consistently in H.2–H.4/Tables 16–18/examples, or replace them by unambiguous “missing required” / “extra non-gold” labels throughout. Preserve numeric cells in their semantic categories; do not blindly move numbers or merge retrieval misses with evaluated rejection counts. Acceptance: all equations, columns, headings and prose use one positive-class convention and identify retrieval misses separately.

### EMP-09 — MINOR/self-containment: evaluator audit is useful but validates neither required labels nor human correctness

**PDF anchors:** p. 23 H.1: “97.10% model-adjudicated agreement, not accuracy against human ground truth”; p. 24: “All sampled correct-stratum decisions were originally False”.

**Verified audit arithmetic:** provisional TP=709, FP=474, FN=611, TN=35606; agreement 36315/37400=97.09893%; always-False 36080/37400=96.47059%; positive precision 709/1183=59.93238%, positive recall 709/1320=53.71212%, positive F1=0.56652. Gain over always-False agreement is only 0.62834 percentage points. This class-imbalance caveat **already exists** and should be credited. 37,350 unique reviews represent 37,400 occurrences, also explicitly disclosed. The additional 40-review audit is AI-only and stratified, not prevalence-representative; all 20 agreement-stratum decisions are False. It cannot quantify reliability of adjudicator-approved True decisions. H.1 explicitly omits gold skill labels and skill bodies, so it is not an annotation audit. Table 17's 78 plausible annotation/scope mismatches concern a selected TheoremQA error cohort, not an overall gold-label error rate.

**Available fix:** Promote a short version of the positive-class limitation near main error interpretation; preserve “model agreement” wording and separate evaluator consistency from label validity. No issue should demand the already-existing agreement audit as missing.

**Additional evidence only for stronger validity claims:** blinded human/domain adjudication covering positive, negative and ambiguous strata, with sampling weights and inter-annotator information; independent review of required-skill annotations if asserting completeness or downstream necessity. Acceptance: no use of pooled agreement as proof of robust applicability recognition or gold-label correctness.

## Numerical checks that passed / should not be raised as arithmetic errors

Calculations use exact/six-decimal source operands, not rounded display cells. `%` is relative unless stated.

| Frozen claim | Recomputed | Interpretation |
|---|---:|---|
| Abstract/init top5 gain 24.9% | 24.902428% | Mean of retriever-wise relative gains; ratio of means would be 24.720529%. |
| Mean top5 recall 75.5% | 75.498367% | Task-average recall within retriever, equal mean across retrievers. |
| Retention 90.5% | 90.468694% | Mean of own-R@50-normalized ratios, not pooled skill-occurrence retention. |
| Baseline top5 recall improvements 7.9–33.6% | 7.867378–33.640209% | Mean retriever-wise relative gains vs SkillRouter and SkillDAG/native retrieval. |
| Base nDCG@1 / @10 gains 67.0 / 39.7% | 66.988145 / 39.718146% | Mean retriever-wise relative gains. |
| SkillRouter nDCG@1 / @10 gains 10.9 / 8.4% | 10.932766 / 8.379891% | Same aggregation. |
| SkillDAG / Skill-Pro nDCG@10 gains 29.2 / 26.7% | 29.248647 / 26.727340% | Same aggregation. |
| MedCalc / Theorem underperformance 5.01 / 6.10% | 5.014653 / 6.099438% | Correct for **nDCG@10**, which the exception sentence should name; not nDCG@1. |
| SkillDAG R@50 96.86 vs 83.45% | 96.864233 vs 83.446233% | Correct. 16.079815% gain is ratio of means; mean of relative gains is 16.574530%. Declare aggregation switch, not an arithmetic error. |
| top5 downstream vs strict +2.5% | +2.468212% | 0.610516934 vs 0.595811052. |
| top5 fraction of oracle 95.7% | 95.737247% | Oracle 477/748. Oracle is an annotated-context reference, not a proven upper bound (some native method outcomes exceed it). |
| top5 downstream advantage range 1.5–20.5% | 1.481481–20.492524% | Upper end uses LLM Direct, not only skill-routing bars; label this comparator. |
| DAG vs top5 recall difference 4.41% | 4.409190% | Ratio of aggregate DAG@10 to RouterBSI@5 recalls, not common-budget recall. |
| MBR vs gate +7.3% (Fig5) | 7.261342% | Three-run nDCG@1 means. |
| Both vs MBR +4.71% (Fig5) | 4.706761% | Three-run nDCG@1 means. |
| MBR loss from Both 7.7% (Fig6) | 7.747748% | First-run snapshots, a different estimand. |
| Both total-token saving using MBR 10.8% | 10.815525% | Unequal/incomplete accounting boundaries. |
| Replay quality gain 15.4–23.7% | 15.384615–23.671498% | Correct single-run comparisons. |
| Replay total-token overhead 40.6–52.9% | 40.589541–52.853634% | Correct as recorded, not causal marginal overhead. |
| Both nDCG gain 38.8%; Neither 6.8% | 38.803583%; 6.796820% | Correct own-initialization changes. |
| nDCG gain accrued by iteration5 93.0% | 92.951196% | Correct; endpoint still fluctuates. |

Headline aggregation formulas vary between mean of relative gains and relative gain of means. Most are correct under their actual source definition, but a short global convention plus explicit exceptions would prevent apparent contradictions with rounded Table 1.

## Figures' empirical/visual diagnostics (frozen rendered pages inspected)

- **Figure 3, p. 6:** Values agree with Table 8 and own-method denominator definition in F.1. Main caption should explicitly say own Recall@50; SkillDAG's denominator is expanded coverage, not the same initial pool. X cutoffs 50,25,10,5,1 are equally spaced categorical points, not a linear numeric axis. Lines/markers provide non-color cues; tightly packed top legend and small panel make close top1 differences hard to distinguish. No numerical-coordinate error established.
- **Figure 4, p. 6:** Bars agree with Table 19. Bar y-axis starts at 0.4, visually exaggerating small differences; use a zero-based bar chart or a point plot with a clearly labeled restricted range. No uncertainty is shown. Caption ends with the broken phrase “most other approaches oracle performance.” Oracle line is a reference, not an upper bound. Distinct skill budgets should be in caption/key.
- **Figure 5, p. 7:** Main error is the false common-initialization caption. “standard mean and variation” should be mean ± one population SD. Means/bands agree with Table 11 and selected CSV; population SD derives from variances rounded to six decimals, so a displayed zero SD need not mean determinism. Light small bands are difficult to read at column size; use explicit SD wording rather than allowing CI interpretation.
- **Figure 6, p. 7:** Correct first-run coordinates, but caption omits one-run status, nonreportability, unequal initialization and incomplete costs. Axis “Total Token Usage” overstates completeness. It should not be read as the same mean endpoints as Figure 5 or serving cost.
- **Figure 7, p. 8:** Bars numerically match Table 14. No uncertainty, one run/backbone, historical candidates not held common. Source does not establish a plateau or model-capacity ordering. Colored backbone groups plus hatching distinguish initial/final; at actual width labels are small but readable. No numerical plotting error established.
- **Figure 8, p. 23:** Coordinates agree with G.3 (K10: 692.788M/0.702; K25: 1013.401M/0.742; K50: 1324.251M/0.800). G.3 already discloses nonreportable, incomplete, known-only and non-budget-matched evidence. Caption/axis should carry “known recorded” and single-run status, not imply full totals. Three blue shades alone are the identity cue; directly label points K=10/25/50 for grayscale/accessibility. Title is redundant but not a scientific error.

## Evidence already present — do not request again as wholly missing

- Exact split/filter counts, shared-skill vocabulary and generalization-to-seen-skills limitation: C.1/C.2 Tables 3, pp.16–17. This is not a new-skill generalization benchmark. Source tasks removed: 413/5400; retained gold vocabulary 306/636. Test examples are task-ID disjoint, but near-duplicate/template independence is not established by that alone.
- Per-benchmark/retriever routing and complete coverage metrics: Tables 5–7.
- Retention formula and denominator scope: F.1, Tables 8–9.
- Three-run means and population SDs/full trajectories: G.1, Tables 10–11.
- First-run cost boundaries and unknown attempts: G.2, Table 12; replay-capacity sensitivity Table 13.
- Three-backbone expanded metrics: Table 14.
- Evaluator agreement, class-imbalance caveat and second blinded AI pass: H.1 / Table 15.
- Full semantic TheoremQA error categorization and examples, conditional supplied-vs-predicate-set accounting: H.2–H.4, Tables 16–18.
- Complete per-retriever and per-benchmark downstream counts/rates: H.5, Tables 19–20.

## Bottom line

Most headline percentage arithmetic checks out once the actual estimands are separated. Highest-priority problems are empirical provenance, the frozen main-text inversion of conditional error shares, falsely claimed matched initializations, incomparable cost boundaries, and causal claims beyond the native/historical comparison design. Several strong corrections can be made by promoting existing appendix evidence; canonical validity, matched-protocol attribution and stronger uncertainty require additional audit evidence or controlled experiments only if the author wants to retain those stronger claims.
