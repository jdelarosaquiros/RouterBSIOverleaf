# RouterBSI revision proposals — author approval required

**PROPOSAL-ONLY. No manuscript revisions were executed.** All 15 issues remain unresolved pending author approval, evidence decisions, and a synchronized source/PDF target. The revision log records `not_executed` and null after-text; proposed prose appears only in the separate proposal payload. No builds, model/experiment runs, figure generation, uploads, or author responses were performed.

## Readiness and version boundary

**Not submission-ready on the present evidence.** The most consequential issue is confirmed nonreportable provenance of load-bearing main results, not merely possible overlap with appendix diagnostics. Seven baseline-hash-matched manifests support the finding: Table 1/Figure 3 are noncanonical/nonreportable; all twelve Figure 5 source runs are nonreportable; Figures 6/7 are nonreportable; Figure 4 includes a nonreportable Vector RouterBSI run. This is not proof of fabricated numbers, test leakage, or arithmetic error. Plot regeneration and wording edits cannot discharge the audit gate.

Primary source: frozen `reviewed_main.pdf`, SHA256 `51ddab4b827e211879ecf8c936083ea5fa2a03f6b34a32d230f98b90f5910d6b`. The later observed PDF SHA256 is `0401ac8acbac22ecefdd7b50d0582895aaa105ea094fa5e23cd42a569b0a27c7`. See `source_drift.json`, `live_pdf_text_diff.txt`, `VERSION_NOTE.md`, and `parent_provenance_evidence.json`.

**ISSUE-001 is historical:** the false percentage and narrow-predicate sentences were already removed externally from the current source/later PDF. Do not delete them again. Figure 3 and the conclusion also changed externally. Nothing here asserts that the entire paper worktree stayed unchanged.

Exact old text below is copied from the named frozen clean-page extract; raw review anchors remain verbatim in the JSON. Clean extracts normalize PDF layout and are not byte-for-byte TeX patches. Source/math mapping and a drift-aware merge are required after approval. Empty new text means a proposed deletion; the historical deletion is explicitly non-reapplicable.

## Compliance and scientific scope

- Venue/year/track/cycle/stage remain unknown; revision mode stays `unknown`, and PDF revision permission stays `not_allowed` for this task. Long paper is assumed, not confirmed.

- Existing main content ends on page 8 of the 28-page frozen PDF. This fits the assumed eight-content-page long-paper submission allowance; the active limit and remaining pages are unconfirmed. No ninth page is presumed. No revised PDF was built or counted.

- A4, two-column layout, embedded fonts, line/page numbers are verified in the parent audit. Official style files match the supplied ZIP, but overall template compliance remains `needs_human_check`. Full-width floats are not one-column-prose violations.

- Distinct Limitations and Ethics precede References; appendix A–H follows in the same PDF. Preserve honest caveats and clinical-safety limitations. No new evidence belongs in excluded sections merely to save space.

- The substantive language-agent contribution is explicit skill-applicability predicates with fixed model weights and feedback-based local selection. Neither inspectable text nor routing gains establish human-editing utility, uniform downstream gains, causal component effects, or a Bayesian inference contribution.

- Reproducibility is unresolved. Responsible NLP Checklist, actual AI-assistance disclosure policy/location, supplemental anonymity and author/portal logistics remain human checks; manuscript prose cannot complete those fields.

## Dependency order and decision gates

Critic execution order is preserved verbatim in the JSON. The proposal application order adds confirmed provenance and consistency dependencies:

ISSUE-002 → ISSUE-006 → ISSUE-001 → ISSUE-003 → ISSUE-004 → ISSUE-005 → ISSUE-007 → ISSUE-008 → ISSUE-009 → ISSUE-010 → ISSUE-011 → ISSUE-012 → ISSUE-013 → ISSUE-014 → ISSUE-015.

1. Approve scope and choose a synchronized source/PDF target. Independent sign correction can be planned immediately; audit ISSUE-006 before endorsing empirical interpretations.

2. Reuse verified records to establish run/claim bindings and method protocols. Preserve exploratory status where bindings remain unresolved; never toggle reportability by editorial fiat.

3. Choose narrow descriptive claims versus stronger claims. EXP-001–004 are conditional branches, not mandatory reruns. Existing outputs take priority, including uncertainty analysis without new model calls.

4. Apply technical/metric corrections before final captions, abstract, contributions and conclusion. ISSUE-004 and ISSUE-014 share one Figure 5 caption: apply it once.

5. Only after separate manuscript-edit authorization: map PDF-extracted anchors to the current source, apply approved changes, compile, inspect final-size figures and count content pages. Compress duplicated motivation rather than typography or load-bearing evidence.

No deadline is confirmed, so feasibility and whether a later eligible cycle is required remain unknown.

## Issue-by-issue exact proposals

### ISSUE-001 — MAJOR — The main text reverses the meaning of the conditional error percentages and overattributes failures to narrow predicates.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** ISSUE-006.

**Skeptical assessment:** Confirmed for frozen PDF only. Later PDF and current results.tex already omit the two incorrect sentences. The reviewer replacement is supported by H.4 but is downstream-disagreement evidence, not an explanation of the routing-score reversal in §6.1. Move any retained diagnosis to §6.3/H.4 and call it exploratory until provenance is bound. Do not reapply the external deletion.

**Review location:** 6.1 Skill Routing Performance; frozen page 6. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — historical_deletion_do_not_reapply — pages/page_06_clean.txt

**Old (exact clean-extract text):**

```text
From the samples where RouterBSItop5 failed and SkillRouter succeed, 94.68% of TheoremQA and 93.75% of MedCalc-Bench were cases where predicate failed to evaluate to true when the skill was required. The cause of these failures was likely overly narrow predicates leading to large percentages of predicates failing to correctly describe all applicable tasks.
```

**New (proposal only):**

```text

```

Already removed externally; this records the historical correction, not an instruction to delete current text.

#### Text proposal 2 — replace — pages/page_06_clean.txt

**Old (exact clean-extract text):**

```text
RouterBSI could further improve its performance on these cases with more training iterations or relying on a human to directly edit the predicates.
```

**New (proposal only):**

```text
Whether additional training or human predicate edits improve these cases remains untested.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 3 — proposed_main_text_summary_of_appendix — pages/page_27_clean.txt

**Old (exact clean-extract text):**

```text
Thus, missing required skills cannot explain all failures, and the presence of non-gold context alone does not demonstrate that it caused an incorrect answer.
```

**New (proposal only):**

```text
In the exploratory downstream-disagreement analysis, the required skill is present in the five supplied skills in 16 of 21 TheoremQA and 15 of 21 MedCalc-Bench task–retriever cases where RouterBSI_top5 fails and SkillRouter succeeds. Missing required skills do not explain all disagreements. Extra supplied skills may arise from top-five padding even when their predicates are false; these counts do not establish a dominant cause of failure.
```

Proposed new §6.3 paragraph summarizing this real H.4 anchor; leave the accurate appendix statement intact. Omit if space or unresolved provenance makes the diagnostic unnecessary.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

- Approve whether to retain a downstream diagnostic summary; identify provenance of H.4 if using it as evidence.

**Alternative / claim narrowing:** Keep the already-removed sentences absent and omit the optional diagnostic paragraph; retain only the untested-future-work wording.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] The 94.68%/93.75% figures are not described as predicate-rejection rates or task-level error rates.

- [ ] Any diagnosis distinguishes supplied top-five sets from predicate-selected sets and retrieval misses.

- [ ] Recheck current source/PDF before editing because the incorrect sentences were already removed externally.

**Consistency propagation:** §6.1, §6.3, H.2–H.4, Tables16–18.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-002 — MAJOR — The guarantee has the wrong direction and omits its strictly local scope; the validation gate is not a no-regression guarantee relative to the previous policy.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** none.

**Skeptical assessment:** Confirmed sign error; §4.3 already has the correct strict inequality, so do not claim the entire gate is absent. The unchanged candidate bounds only the evaluated mean loss on the same replay set under the same recorded judgments, not future re-evaluations.

**Review location:** 2.1 Non-Parametric Routing Optimization; frozen page 2. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_02_clean.txt

**Old (exact clean-extract text):**

```text
RouterBSI ensures non-decreasing empirical error on the retained set while bounding replay evaluation costs. A held-out gate additionally rejects updates that regress validation performance below the cold-start performance.
```

**New (proposal only):**

```text
Including the unchanged predicate ensures non-increasing mean empirical error on the current replay set under the evaluated Boolean judgments. This local comparison does not preserve every prior correct judgment or guarantee future-task improvement. At iteration end, a changed predicate is retained only if its validation error is strictly below its cold-start error; it may still regress relative to the previous accepted predicate.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

**Alternative / claim narrowing:** No new experiment is needed to correct the sign and scope; retain the existing algorithm and narrow its guarantee.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] No claim states non-decreasing error as a benefit.

- [ ] Replay guarantee names the fixed replay set and unchanged candidate.

- [ ] Strict cold-start comparison and possible previous-iteration regressions appear in the main method.

**Consistency propagation:** Abstract, §1 contribution2, §3 objective, §4.2–4.3, Figure2, Conclusion.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-003 — MAJOR — The main method does not describe the executed replay set, ranking, and iteration-end rollback accurately enough to reproduce it.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** ISSUE-002, ISSUE-006.

**Skeptical assessment:** Confirmed, but do not paste the review paragraph before the old replay equation and leave a contradiction. Replace the replay-definition block, ranking text and gate timing together. Tie-breaking is unspecified in A.3 and cannot be invented. Generalizing Appendix A ordering to every competitor is not justified.

**Review location:** 4.2–4.3 Method; frozen page 4. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_04_clean.txt

**Old (exact clean-extract text):**

```text
For each skill, the replay set contains previously seen relevant and irrelevant tasks: Rs = {qrs} ∪{qis}, |{qrs}| ≤N, |{qis}| ≤N
```

**New (proposal only):**

```text
For skill s, retain positive and negative histories H_s^+ and H_s^- with at most N tasks each. The effective replay set is R_s = H_s^+ ∪ H_s^- ∪ {q}, deduplicated by task identifier, so |R_s| ≤ 2N+1. A full bucket always inserts a new task by replacing a uniformly chosen slot; this is not reservoir sampling. Only these per-skill buckets are bounded; lazy materialization retains an unbounded global seen-task history.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 2 — replace — pages/page_05_clean.txt

**Old (exact clean-extract text):**

```text
RouterBSItopk are the top k skills using the sum of their predicate label and the retrieval score.
```

**New (proposal only):**

```text
RouterBSI_topk returns the first k candidates in a lexicographic ordering by predicate truth value, descending retrieval score, and original retrieval order, with predicate-positive skills first. We denote the retrieved candidate budget by K and the supplied-skill budget by k; the default values are K=50 and k=5.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 3 — replace — pages/page_05_clean.txt

**Old (exact clean-extract text):**

```text
The non-parametric baselines, including ours, do not output a continuous score like rerankers, so we rank them by the sum of their binary label and the retrieval score, where 1 is the label for selected skills and 0 otherwise.
```

**New (proposal only):**

```text
RouterBSI uses the lexicographic ordering defined above; an unnormalized arithmetic sum of the label and retrieval score is not its general ranking rule.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 4 — replace — pages/page_04_clean.txt

**Old (exact clean-extract text):**

```text
Evaluate the modified skill library Sm on a held-out validation set.
```

**New (proposal only):**

```text
Updates remain provisional during each training pass. At the end of the pass, evaluate the modified skill library on validation. For each changed skill, reject a tie with cold-start or a lack of validation retrieval support; restore the predicate saved at the start of this iteration when an update is rejected.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 5 — replace — pages/page_05_clean.txt

**Old (exact clean-extract text):**

```text
RouterBSI is optimized for 10 iterations.
```

**New (proposal only):**

```text
RouterBSI is optimized for 10 iterations with three proposed replacements per repair, a 400-character predicate limit, and history capacity N=5 per relevance class. The unchanged predicate is an additional selection option; the current-inclusive replay set contains at most 11 distinct tasks.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

- Run-bound implementation evidence for equal-risk tie-breaking and baseline-specific ranking rules.

- Confirm retained post-rollback checkpoint versus pre-rollback candidate state for reported results.

**Alternative / claim narrowing:** The empirical inequality does not require a particular tie-break; state that it is unspecified rather than fabricate one, but reproducibility remains unresolved.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] Main text distinguishes K from output k.

- [ ] Replay bound is 2N+1 including current task; bounded memory claims exclude global history.

- [ ] Main ranking and gate timing match Appendix A.

- [ ] Tie-break is documented from actual implementation, not invented.

**Consistency propagation:** §3 and §4 notation, Appendix A pseudocode, §5.4–5.5 baseline matrix, Figure2.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-004 — MAJOR — The ablation caption claims common initialization, but Appendix G.1 reports an unpaired initialization design.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** ISSUE-006.

**Skeptical assessment:** Confirmed confound; retain descriptive trajectories rather than discard useful evidence. All runs recording one replay seed is not independent-seed replication. The proposed phrase “Both components yield” would retain causality; use “both-enabled configuration has”. Bands derive from rounded variances, so do not imply raw replicate reanalysis.

**Review location:** Figure 5 / 7.1; frozen page 7. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_07_clean.txt

**Old (exact clean-extract text):**

```text
Figure 5: Ablation of MBR replay and held-out validation gate comparing routing performance. The lines and areas represent the standard mean and variation, respectively across three runs starting from the same initial predicates at iteration 0. Combining replay and gating yields the strongest final routing performance.
```

**New (proposal only):**

```text
Figure 5: Exploratory component trajectories with Qwen3.5-4B and SkillSight. Lines show mean task-weighted test nDCG@1 across three runs of 748 tasks each; bands show population SD reconstructed from rounded variances (Table 11), not confidence intervals. Both-enabled runs use separately generated initial libraries, whereas other configurations reuse the first both-enabled library; all record replay seed 20260324. The comparison is not initialization-paired, and all twelve source runs are nonreportable. Both enabled has the highest observed final mean.
```

Same Figure5 caption proposal as ISSUE-014; apply once, not twice.

#### Text proposal 2 — replace — pages/page_07_clean.txt

**Old (exact clean-extract text):**

```text
Figure 5 shows MBR with bounded replay alone achieved higher final performance on test dataset than the held-out validation gate alone: F1 increased from 0.495 to 0.594 and nDCG@1 from 0.644 to 0.691, relative improvements of 20.0% and 7.3%, respectively. Combining MBR with the held-out gate further improved final performance on unseen test tasks, increasing F1 by 3.28% and nDCG@1 by 4.71% to 0.724 compared with MBR alone. Relative to each configuration’s own initialization, disabling both only increases F1 and nDCG@1 by 21.0% and 6.8% which is much lower than the 100.9% and 38.8% increase when both are enabled. This supports empirical update selection without implying that unchecked updates invariably worsen performance. With both components enabled, diminishing returns appeared around iteration 5, by which point 96.5% of the final F1 gain and 93.0% of the final net nDCG@1 gain had accrued. Later iterations added only 0.011 F1 and 0.014 nDCG@1, indicating an approximate plateau. This suggest diminishing opportunities for useful predicate refinement on the plateau: early iterations correct broad, frequent routing errors, while later iterations encounter harder or less common cases.
```

**New (proposal only):**

```text
At iteration 10, the both-enabled configuration has the highest observed three-run mean F1 and nDCG@1 (Table 10). The replay-only configuration has higher observed final means than the gate-only configuration. Because initialization is not paired across configurations, these differences do not isolate causal component effects. Most of the observed mean improvement occurs before iteration 5, but the trajectories alone do not identify which error types are corrected early or late. The source records are nonreportable, so these observations remain exploratory pending provenance resolution.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

- EXP-001 only if authors retain causal component-effect claims; first search for already matched immutable initial libraries and compatible runs.

**Alternative / claim narrowing:** Use existing descriptive Figure5/Table10–11 results with full initialization caveat; no compulsory reruns.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] Caption discloses actual initialization sharing, repeat count, and population-SD definition.

- [ ] No independent-seed or paired-design claim without corresponding manifests.

- [ ] Causal attribution is narrowed or backed by matched-initialization runs.

**Consistency propagation:** §1 contribution3, §7.1, Figure5, Conclusion.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-005 — MAJOR — The main cost comparison omits asymmetric initialization and missing-usage accounting, presenting recorded totals as a controlled efficiency comparison.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** ISSUE-006.

**Skeptical assessment:** Confirmed accounting problem, not an arithmetic failure of the 10.8% rounded reduction. Switching to iteration-only totals does not make the runs fully controlled or recover unknown usage. Keep quality from the same first runs as the tokens.

**Review location:** 7.2 Performance and Token Usage; frozen page 7. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_07_clean.txt

**Old (exact clean-extract text):**

```text
Figure 6 demonstrates that combining replay and the gate provides the strongest final routing performance, while MBR alone reduces token usage by 10.8% at the cost of a 7.7% relative decrease in nDCG@1 compared with using both. Across configurations with and without the gate, replay improves final routing performance by 15.4% to 23.7% at the cost of a 40.6% to 52.9% increase in token usage.
```

**New (proposal only):**

```text
Figure 6 reports the first run of each configuration, not the three-run means in Figure 5. Replay-only records 1181.026 million known tokens and nDCG@1=0.684, compared with 1324.251 million and 0.742 for both components. Only the latter includes run-local initialization; both totals exclude attempts with unknown usage. These totals do not establish matched end-to-end savings. Recorded optimization iterations use 1011.920 versus 1073.904 million tokens, respectively, but remain a single-run, known-usage comparison. Table 12 reports the phase breakdown and unknown-usage attempt counts. The source records are nonreportable, so these observations remain exploratory pending provenance resolution.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

- Complete phase-level usage and initialization allocation only for an end-to-end cost claim; do not assign unavailable usage zero.

**Alternative / claim narrowing:** Keep recorded totals as a descriptive ledger or remove cost-saving percentages; serving-cost conclusions remain unsupported.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] Single-run versus three-run results are explicit.

- [ ] Known-only accounting, excluded external initialization and unknown attempts are disclosed next to the main cost claim.

- [ ] No complete-cost or serving-cost claim from these totals.

**Consistency propagation:** Figure6, Table12/G.2, Abstract/Conclusion if cost language added.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-006 — MAJOR — Main-result manifests explicitly mark evidence nonreportable/analysis-only, so the provenance limitation is not confined to appendix diagnostics.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** none.

**Skeptical assessment:** Confirmed beyond rounded-number overlap. Seven baseline-hash-matched paper-facing manifests identify Table1/Figure3 and all 12 Figure5 source runs as nonreportable; Figures6/7 are nonreportable and Figure4 includes a nonreportable Vector run. This is an unresolved execution/audit-validity gate, not proof of fabricated or numerically incorrect results. Wording or plot regeneration cannot make these results canonical.

**Review location:** Table 1 / Figures 3–7 / G.3 / H.1 provenance; frozen page 5. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_05_clean.txt

**Old (exact clean-extract text):**

```text
Skill routing performance using Qwen3.5 4B.
```

**New (proposal only):**

```text
Exploratory skill routing performance using Qwen3.5 4B. The source manifest marks this comparison noncanonical and nonreportable; numerical consistency does not establish publication validity.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 2 — replace — pages/page_05_clean.txt

**Old (exact clean-extract text):**

```text
Qwen3.5-4B is the default model used in our experiments.
```

**New (proposal only):**

```text
Qwen3.5-4B is the default model used in our experiments. The paper-facing manifests mark Table 1 and Figures 3, 5, 6, and 7 as nonreportable; Figure 4 includes a nonreportable Vector RouterBSI run. These comparisons are exploratory while their historical source, prompt, cache, split, initialization, and retained-checkpoint bindings remain unresolved. The same limitation applies to the candidate-pool and predicate-adjudication diagnostics in Appendices G.3 and H.1. Historical candidate rankings are not a controlled shared-candidate comparison.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

- Run-to-claim records for every numerical table/figure, including Tables1,5–20 and Figures3–8: run ID, code/source closure, effective model/prompt/checker/request cache bindings, split/order, initial and retained predicate hashes, rollback stage, reportability, token phases and unknown attempts.

- Reuse immutable verified artifacts; EXP-004 only after an exact unresolved claim-level gap is established and separately authorized.

**Alternative / claim narrowing:** Retain affected numerical comparisons only as explicitly exploratory, with captions, abstract, introduction and conclusion all qualified; alternatively remove affected empirical claims. Resolve each original audit requirement from existing records first. Only genuinely missing evidence may require separately authorized audited replacement runs, clearly identified as new evidence.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] Each confirmatory number maps to a verifiable run and source/prompt/cache/split binding.

- [ ] Exploratory/nonreportable diagnostics retain visible caveats wherever cited.

- [ ] The review does not infer all headline results invalid merely from matching rounded numbers.

- [ ] Do not relabel reportable=false records as canonical by editing metadata or prose.

- [ ] Table1/Figures3–7 and all dependent headline claims either have resolved audit bindings or conspicuous exploratory scope.

- [ ] Existing artifacts are inventoried before any conditional replacement run; fresh evidence is not described as historical validation.

**Consistency propagation:** §5 protocol, Tables13–15, Figures5–8, All main-text uses of G.3/H.1.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-007 — MAJOR — The main split description implies per-dataset70/15/15 allocation and generalization scope broader than the constrained shared-skill protocol.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** none.

**Skeptical assessment:** Confirmed; replace both split sentences, not just the first, to remove the vague balancing account. Iterative rare-skill filtering excludes entire tasks. Shared skill vocabulary is deliberate and is not by itself evidence of task leakage.

**Review location:** 5.1 Benchmarks and Skill Corpus; frozen page 4. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_04_clean.txt

**Old (exact clean-extract text):**

```text
We split each dataset into train, validation, and test splits with ratios of 70%, 15%, 15%, respectively. To evaluate the learning capabilities of baselines, we further filter and balance splits such that each split has at least one task that share the same required skill.
```

**New (proposal only):**

```text
Starting from 5,400 annotated instances, we iteratively remove whole tasks containing a skill with fewer than three remaining occurrences, excluding 413 tasks. The retained 4,987 tasks are allocated globally to 3,491/748/748 train/validation/test instances under a constrained 70%/15%/15% target; per-dataset proportions differ (Table 3). Task identifiers are disjoint, but every partition represents the same 306 gold skills. The retrieval corpus remains at 26,262 skills, so this evaluation concerns held-out tasks with represented skills, not unseen-skill generalization.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 2 — replace — pages/page_08_clean.txt

**Old (exact clean-extract text):**

```text
Limitations Our approach has three limitations.
```

**New (proposal only):**

```text
Limitations Our evaluation excludes tasks involving rare skills and requires every retained gold skill to appear in all partitions. It therefore does not establish performance on unseen skills or the excluded long-tail tasks. Our approach also has three limitations.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

**Alternative / claim narrowing:** Retain the represented-skill scope; request unseen-skill/domain experiments only for an explicit broader generalization claim.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] Main text uses exact global counts and makes the per-dataset exception explicit.

- [ ] Shared-skill scope and removed rare-skill tasks are disclosed.

- [ ] No claim of actual task leakage without evidence.

**Consistency propagation:** Abstract, §1 contribution3, §5.1/Table3, Limitations.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-008 — MAJOR — Baseline/model roles are inconsistent or insufficiently specified, weakening reproducibility of the strongest comparison.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** ISSUE-006, ISSUE-007.

**Skeptical assessment:** Confirmed ambiguity. Neither conflicting blanket statement establishes what was trained. A protocol matrix cannot be filled from memory or from the optional appendix outline. Historical candidate rankings are explicitly not matched; retain legitimate method-native settings but do not describe controlled routing isolation. The final review and baseline-stable manifests explicitly establish the historical/non-shared candidate caveat; this is no longer an inference from small coverage differences.

**Review location:** 5.3–5.5 Experimental setup; frozen page 5. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_05_clean.txt

**Old (exact clean-extract text):**

```text
They are trained on training split and frozen on validation and test splits.
```

**New (proposal only):**

```text

```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 2 — replace — pages/page_05_clean.txt

**Old (exact clean-extract text):**

```text
The retrievers use either pretrained embedding models and/or lexical matching, so they do not require training.
```

**New (proposal only):**

```text
The reported retrieval backends are BM25, Vector, and SkillSight. Their training and tuning roles must be distinguished from the feedback-driven router updates.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 3 — replace — pages/page_05_clean.txt

**Old (exact clean-extract text):**

```text
We evaluate five models spanning four open-weight checkpoints and one proprietary frontier model: Qwen3.5-4B (Qwen Team, 2026a), Qwen3.8-27B (Qwen Team, 2026b), Llama-3.3-70B-Instruct (Meta, 2024), gpt-oss-120b (OpenAI, 2025), and GPT-5.4 (OpenAI, 2026).
```

**New (proposal only):**

```text
The backbone comparison in Figure 7 and Table 14 reports Qwen3.5-4B, Qwen3.8-27B, and gpt-oss-120b. Qwen3.5-4B is the default routing and downstream model in the reported comparisons. These results do not establish evaluations of every model previously listed here.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 4 — replace — pages/page_05_clean.txt

**Old (exact clean-extract text):**

```text
The skill routing baselines are conditioned on the top 50 retrieved skills and use some optimization method to improve performance.
```

**New (proposal only):**

```text
The routing comparison retains archived method-specific candidate rankings rather than a controlled shared-candidate pool. RouterBSI evaluates K=50 candidates; SkillDAG instead starts from five retrieved skills and expands its graph. Method-native results do not by themselves isolate the routing algorithm from candidate-set differences.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

- Versioned settings for BM25, Vector, SkillSight, LLM Select, SkillRouter, SkillDAG, Skill-Pro, and RouterBSI; include Direct/Oracle downstream reference protocols.

- For each row: upstream version/checkpoint and citation, fitted versus frozen state, fitting labels/splits, retrieval representations/candidate IDs/order, output ranking and skill budget, model role, prompts/decoding, optimization/evaluation budget, context/token policy and deviations.

- Resolve actual Llama-3.3-70B-Instruct and GPT-5.4 roles before either removing or relabeling their citations; verify reported model IDs verbatim.

**Alternative / claim narrowing:** These exact deletions/replacements remove unsupported blanket claims but are not a reproducible final protocol. Do not submit until the matrix is populated from actual manifests or restrict comparisons to rows whose protocols can be documented.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] No conflicting trained/untrained description for the same component.

- [ ] Every compared router including SkillRouter has a reproducible protocol and citation.

- [ ] All listed evaluated models map to actual result artifacts or are removed/relabelled.

**Consistency propagation:** §5.3–5.5, Appendix D, Table1, Figures4/7.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-009 — MAJOR — The downstream advantage of graph expansion is confounded with a larger skill budget and cannot identify a dependency mechanism.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** ISSUE-006, ISSUE-008.

**Skeptical assessment:** Confirmed budget confounding. A method-native comparison is legitimate descriptive evidence but not dependency causality; the oracle is an annotated-context reference, not a proven upper bound. Preserve the SkillSight and Vector reversals rather than imply uniform gains.

**Review location:** 6.3 Downstream Performance; frozen page 7. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_07_clean.txt

**Old (exact clean-extract text):**

```text
This finding suggests expanding selected skills to include dependent skills could improve downstream performance even if the dependent skills are not required. Overall, results show that the higher RouterBSI retention of required skill in top 5 translates to a better average routing performance.
```

**New (proposal only):**

```text
SkillDAG has the highest observed mean downstream success among the compared routing methods (0.631), versus 0.611 for RouterBSI_top5, but supplies ten skills rather than five. This comparison does not isolate dependency expansion from the larger context budget. RouterBSI_top5 exceeds strict routing on average, but not for every retriever: under Vector the rates are 0.599 versus 0.610. Under SkillSight, RouterBSI_top5 (0.627) does not exceed retriever-only (0.628) or SkillRouter (0.638). These are exploratory point estimates because the aggregate includes a nonreportable Vector run. LLM Oracle supplies annotated required skills as a reference condition, not a guaranteed performance ceiling.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

- EXP-002 only for dependency attribution; first inventory reusable exact-request downstream outputs and budget-matched controls.

**Alternative / claim narrowing:** Report native-budget descriptive outcomes, explicitly exploratory until ISSUE-006 is resolved; leave dependency expansion as an untested future-work hypothesis.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] Unequal supplied-skill budgets are explicit in the main results/caption.

- [ ] Routing, downstream success and oracle-reference ratio are not conflated.

- [ ] Dependency benefit is hypothetical unless budget-matched evidence exists.

**Consistency propagation:** §6.3, Figure4, H.5/Tables19–20, Conclusion.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-010 — MAJOR — The claimed plateau that stronger LLMs cannot overcome is not established by the three single-run backbone endpoints.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** ISSUE-006, ISSUE-008.

**Skeptical assessment:** Confirmed overreach. Preserve model identifiers as reported rather than silently repair unfamiliar names. Different families and historical candidates prevent interpretation as an isolated parameter-count experiment; narrowing does not require new runs.

**Review location:** 7.3 Skill Routing Performance across LLM Backbones; frozen page 7. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_07_clean.txt

**Old (exact clean-extract text):**

```text
Overall, these results demonstrate that RouterBSI can significantly improve the routing performance of predicates across LLMs. They also suggest that predicates reach a plateau that cannot be overcomed with more capable LLMs, where it’s difficult for the predicate to be narrow enough to be false for irrelevant tasks but broad enough to be true for all relevant tasks
```

**New (proposal only):**

```text
In these three exploratory single-run comparisons, final nDCG@1 is 0.742 for Qwen3.5-4B, 0.802 for Qwen3.8-27B, and 0.745 for GPT-OSS-120B. Each endpoint exceeds its own initialization, but the final scores are not monotonic in parameter count. The records are nonreportable and retain historical candidates rather than a common candidate pool. They do not establish statistical significance, model equivalence, a model-independent ceiling, or a predicate-expressivity explanation.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

- Resolve model/checkpoint role and provenance under ISSUE-008/006; additional controlled repeats only if a capacity/ceiling hypothesis is retained.

**Alternative / claim narrowing:** Keep endpoint descriptions; remove “significantly”, “cannot be overcome”, and broad equivalence wording.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] No unsupported model-independent plateau or equivalence claim.

- [ ] Single-run endpoints and lack of inferential test are explicit.

- [ ] Speculative causes remain labelled hypotheses.

**Consistency propagation:** §5.3, §7.3, Figure7, Table14, Conclusion.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-011 — MAJOR — Reversed FP/FN terminology and the F1@k versus selected-set-F1 mismatch invite incorrect metric interpretation.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** ISSUE-001.

**Skeptical assessment:** The reviewer target conflates predicate-level missing skills with set-level misses: G\P includes retrieval misses, whereas predicate rejection is (G∩C)\P. Use separate definitions and neutral labels to avoid silently swapping archived counts. H.1 checker/adjudicator confusion matrices have a different target and must not be relabeled.

**Review location:** H.2 False Positives and False Negatives; frozen page 24. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_24_clean.txt

**Old (exact clean-extract text):**

```text
In this error analysis we use the authors’ nonstandard error labels: a false positive (FP) is a required skill whose evaluated predicate is false, and a false negative (FN) is a nonrequired skill whose evaluated predicate is true. Thus predicate FP counts |(Gq ∩Cq)\Pq| and predicate FN counts |Pq \ Gq|. We retain standard relevance-based TP as |Pq ∩Gq| and TN as |Cq \ (Pq ∪Gq)|; this hybrid naming is not a standard confusion-matrix convention. For set-level accounting over Cq ∪Gq, FP counts all missing required skills, |Gq \ Pq|, including retrieval misses |Gq \ Cq| listed separately below. A retrieval miss has no evaluated predicate and is not a predicate rejection. Unretrieved non-gold catalog skills do not inflate TN. For a supplied topfive set, the same set-level error labels describe missing required and extra nonrequired skills, not necessarily the underlying predicate decisions.
```

**New (proposal only):**

```text
For candidate set C_q, predicate-selected set P_q, and required set G_q, we use neutral error names. Extra = |P_q \ G_q| counts extra nonrequired selections; PredicateMissing = |(G_q ∩ C_q) \ P_q| counts required candidates rejected by their predicates; RetrievalMiss = |G_q \ C_q| counts required skills without evaluated predicates. SetMissing = |G_q \ P_q| includes both missing categories. Extra corresponds to the archived FN label, and SetMissing or PredicateMissing to the archived FP label at the stated level. TP and TN retain their relevance-based definitions. For a supplied top-five set, compute Extra and SetMissing on that supplied set, not on P_q. The predicate-adjudication confusion matrix in H.1 evaluates a different target and is unchanged.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 2 — replace — pages/page_05_clean.txt

**Old (exact clean-extract text):**

```text
We additionally report F1@k to compare filtering capabilities. We also report retention as Ret@k to compare the percentage of required skills retained in top k from the retrieved skills.
```

**New (proposal only):**

```text
We report selected-set F1 = 2|P_q ∩ G_q|/(|P_q|+|G_q|) separately from ranked Recall@k and nDCG@k; it is not F1 at a ranked cutoff unless P_q is explicitly that cutoff set. Ret@k is 100 times task-mean Recall@k divided by task-mean Recall@50 for the same method and retriever, then averaged equally across retrievers. Its denominator is method-specific, including SkillDAG’s expanded coverage, so retention is not unconditional recall.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

- Author approval of neutral Extra/Missing terminology; map Tables16–18 and H.2–H.4 examples by semantic category, preserving numeric cells and table sums.

- Confirm selected-set empty-denominator handling from actual metric implementation; do not invent a convention.

**Alternative / claim narrowing:** If archival FP/FN labels must remain, retain them only in an explicitly labeled archive mapping and use neutral names in publication prose.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] All counts preserved while labels/captions/examples use one documented mapping.

- [ ] No selected-set F1 is labelled F1@k without evaluating that cutoff.

- [ ] Main retention definition states ratio-of-means and method-specific denominator.

**Consistency propagation:** §5.2, H.2–H.4/Tables16–18, Figure3/F.1, Abstract retention wording.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-012 — MAJOR — The empirical selection rule is clear, but the title-level Bayesian framing and incremental distinction from reflective optimization need a precise justification.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** ISSUE-002, ISSUE-003.

**Skeptical assessment:** Empirical minimum-risk is the accurate default; uniformly sampling a supervised replay set alone does not supply a Bayesian posterior. The review contrast “rather than tool argument generation” understates JTPRO’s tool-selection role. Credit joint tool-selection and argument-instantiation optimization, and distinguish buffer types.

**Review location:** 4.2 Minimum-risk formulation / Related Work; frozen page 4. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_04_clean.txt

**Old (exact clean-extract text):**

```text
Our risk function is the average skill selection error on replayed tasks.
```

**New (proposal only):**

```text
Candidate selection minimizes empirical Boolean loss under the uniform distribution over the current replay set, using supervised required-skill labels. We call this empirical minimum-risk selection, not posterior Bayesian inference. The unchanged predicate is included in the candidate set.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 2 — replace — pages/page_02_clean.txt

**Old (exact clean-extract text):**

```text
Similar to our approach, JTPRO evaluates candidates on sampled training minibatches and held-out validation but does not provide bounded experience management for online adaptation (Ghoshal et al., 2026).
```

**New (proposal only):**

```text
JTPRO jointly refines global instructions and tool schemas for tool selection and argument instantiation, using reflective proposals, minibatch evaluation, and validation-based context selection (Ghoshal et al., 2026). RouterBSI instead edits one applicability predicate per reusable skill, evaluates proposals on class-bounded per-skill task histories, and gates iteration-end updates against cold-start validation. A bounded candidate pool is distinct from a bounded replay history; this distinction does not imply that all competing methods have unbounded state.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 3 — replace — pages/page_01_clean.txt

**Old (exact clean-extract text):**

```text
Recursive Self-Improvement of Predicates for Skill Routing via Minimum Bayes Risk Replay and Held-out Gates
```

**New (proposal only):**

```text
Improving Skill-Applicability Predicates with Bounded Empirical-Risk Replay and Cold-Start Validation Gates
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

- Author naming decision; if retaining MBR terminology, explicitly state its empirical decision-rule meaning and contrast it with model-distribution MBR decoding.

- Freitag et al. (2022), High Quality Rather than High Model Probability: Minimum Bayes Risk Decoding with Neural Metrics, is verified by local reference_MBR.txt pp811–825; bibliography key/insertion is still unexecuted.

- A matched reflective-selector control is optional only for a stronger mechanism comparison, not an automatic new baseline requirement.

**Alternative / claim narrowing:** Rename the selector and title without asserting a Bayesian contribution; preserve RouterBSI as the method identifier unless authors separately approve renaming.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] Risk distribution and supervised labels explicitly stated.

- [ ] Novelty claim identifies the actual combination and NLP/language-agent routing target.

- [ ] JTPRO is neither omitted nor misrepresented; tools and reusable skill documents remain distinct.

**Consistency propagation:** Title/PDF metadata, Abstract, §1 contribution2, §4.2 heading, Figures2/5/6 nomenclature, Appendix A, Conclusion.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-013 — MAJOR — Headline comparisons lack paired uncertainty, while the reported repeated-run variance covers a different ablation experiment.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** ISSUE-006, ISSUE-007, ISSUE-008.

**Skeptical assessment:** Observed point estimates can be stated without inference; paired intervals would improve certainty but cannot repair nonreportable provenance or historical candidate confounds. Do not count three retriever conditions per task as independent samples. The strongest aggregate claim should name the specific Table1 metrics.

**Review location:** Table 1 / 6.1 / downstream results; frozen page 5. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_05_clean.txt

**Old (exact clean-extract text):**

```text
RouterBSI improves routing performance of base retrievers by an average nDCG@1 and nDCG@10 across retrievers of 67.0% and 39.7%, respectively Table 1.
```

**New (proposal only):**

```text
In the exploratory Table 1 comparison, RouterBSI has the highest observed aggregate nDCG@1 (0.687) and nDCG@10 (0.728) among the listed router rows. Each score pools 748 tasks within a retriever and averages the three retrievers equally. These point estimates do not establish statistical superiority or controlled shared-candidate effects. The three-run dispersion in the component ablation is not an uncertainty estimate for this baseline comparison.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 2 — replace — pages/page_06_clean.txt

**Old (exact clean-extract text):**

```text
The exception is MedCalc-Bench and TheoremQA, where RouterBSI underperforms SkillRouter by a mean of 5.01% and 6.10% respectively.
```

**New (proposal only):**

```text
For nDCG@10, RouterBSI underperforms SkillRouter on MedCalc-Bench and TheoremQA by mean retriever-wise relative differences of 5.01% and 6.10%, respectively.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

- EXP-003 only for inference: exact saved per-task predictions/outcomes, joined IDs, metric definitions and provenance; keep all retriever outputs for a task together in resampling.

- Prespecify contrasts, confidence level, benchmark-stratified task resampling, task-weighted pooling, seed and precision target; report training-repeat variation separately.

**Alternative / claim narrowing:** Retain exploratory point estimates and documented reversals; do not invent intervals or rerun models if verified saved outputs suffice.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] Task-sampling and training-repeat uncertainty are not conflated.

- [ ] No retriever/task duplicates counted as independent observations.

- [ ] Claims either use descriptive language or cite paired intervals from actual outputs.

**Consistency propagation:** Table1 caption, §6.1, Figure4/§6.3, Abstract/Conclusion.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-014 — MINOR — Several figures need larger labels and self-contained captions; numerical plots must expose readable scales and their evidence scope.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** ISSUE-002, ISSUE-004, ISSUE-005, ISSUE-006, ISSUE-003, ISSUE-009, ISSUE-010, ISSUE-011, ISSUE-013.

**Skeptical assessment:** Accept caption/evidence corrections, but reject a blanket claim that all numerical labels are tiny: composed Figures3/5/6/7 are generally legible at8–9pt. Figure1 is physically tiny despite high resolution; Figure4 labels are around6.44pt and its bar baseline is truncated. Figure3 changed externally, so do not overwrite its newer asset.

**Review location:** Figures 1–8; frozen page 7. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_01_clean.txt

**Old (exact clean-extract text):**

```text
Figure 1: Skill routing with a task applicability predicate. The skill is appropriately selected for task q1 because the task asks about the price for a specific trading day. The skill is not accepted for task q2 because it asks for the price between a range of years.
```

**New (proposal only):**

```text
Figure 1: An applicability predicate distinguishes a single-trading-day price query (q1, accepted) from a date-range query (q2, rejected). This illustrative task setup separates applicability from topical similarity; the feedback-update procedure appears in Figure 2.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 2 — replace — pages/page_03_clean.txt

**Old (exact clean-extract text):**

```text
Figure 2: RouterBSI’s bayes self-improvement algorithm of predicate psk for the skill sk in top k. Routing failures drive revisions selected which are selected based on their bounded replay error using Minimum Bayes Risk (MBR). Selected candidate is discarded by the held-out validation gate if its validation error is higher than the initial predicate psi.
```

**New (proposal only):**

```text
Figure 2: RouterBSI routes retrieved candidates with skill-applicability predicates and proposes revisions after labeled routing failures. Candidate selection minimizes mean Boolean error on current-inclusive replay, including the unchanged predicate. Updates are provisional during a training pass. At iteration end, a changed predicate is retained only when its validation error is strictly below cold-start; ties or absent validation support restore its iteration-start value. This gate does not guarantee improvement over the previous accepted predicate.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 3 — replace — pages/page_06_clean.txt

**Old (exact clean-extract text):**

```text
Figure 3: Retention of required skills averaged across retrievers: BM25, Vector, and SkillSight. The baseline averages the base retrievers used to retrieve the initial top 50 skill. RouterBSI preserves the most required skills as the cutoff k decreases.
```

**New (proposal only):**

```text
Figure 3: Exploratory required-skill retention across ranked cutoffs. For each method and retriever, Ret@k is 100 times task-mean Recall@k divided by that method’s task-mean Recall@50; the three ratios are averaged equally over BM25, Vector, and SkillSight. Cutoffs are categorical, and 100% at k=50 is normalization, not complete gold-skill coverage. SkillDAG uses expanded coverage. The source manifest marks these records nonreportable. Values are point estimates, not confidence intervals.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 4 — replace — pages/page_06_clean.txt

**Old (exact clean-extract text):**

```text
Figure 4: Downstream success rates averaged equally across BM25, Vector, and SkillSight. Lines mark LLM Direct and Oracle. RouterBSItop-5 outperforms strict selection and most other approaches oracle performance.
```

**New (proposal only):**

```text
Figure 4: Exploratory downstream success rates. Each retriever score pools 748 test tasks; bars average BM25, Vector, and SkillSight equally. SkillDAG supplies ten skills, SkillRouter and RouterBSI_top5 five, and RouterBSI_strict a variable selected set. LLM Direct omits skills and LLM Oracle supplies annotated required skills as a reference, not an upper bound. The aggregate includes a nonreportable Vector RouterBSI run. RouterBSI_top5 exceeds strict routing on average, but not for every retriever; no paired uncertainty is shown.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 5 — replace — pages/page_07_clean.txt

**Old (exact clean-extract text):**

```text
Figure 5: Ablation of MBR replay and held-out validation gate comparing routing performance. The lines and areas represent the standard mean and variation, respectively across three runs starting from the same initial predicates at iteration 0. Combining replay and gating yields the strongest final routing performance.
```

**New (proposal only):**

```text
Figure 5: Exploratory component trajectories with Qwen3.5-4B and SkillSight. Lines show mean task-weighted test nDCG@1 across three runs of 748 tasks each; bands show population SD reconstructed from rounded variances (Table 11), not confidence intervals. Both-enabled runs use separately generated initial libraries, whereas other configurations reuse the first both-enabled library; all record replay seed 20260324. The comparison is not initialization-paired, and all twelve source runs are nonreportable. Both enabled has the highest observed final mean.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 6 — replace — pages/page_07_clean.txt

**Old (exact clean-extract text):**

```text
Figure 6: Impact of MBR replay and held-out validation gate on routing performance (nDCG@1) and token usage. Both enabled gives the strongest performance. MBR alone uses fewer tokens at a performance cost.
```

**New (proposal only):**

```text
Figure 6: Exploratory first-run nDCG@1 versus recorded known run-local tokens for the four component configurations (Table 12), distinct from Figure 5’s three-run means. Only both enabled includes local initialization; reused external initialization and attempts with unknown usage are excluded. Source records are nonreportable. These points do not establish complete end-to-end savings or per-query serving cost; no uncertainty is available for these first-run points.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 7 — replace — pages/page_08_clean.txt

**Old (exact clean-extract text):**

```text
Figure 7: Initial and optimized routing performance (nDCG@1) comparison between different LLMbackbones using SkillSight as the retriever. Stronger backbones improve initialization, while optimization brings smaller model Qwen3.5 4B close to the optimized performance of GPT-OSS 120B.
```

**New (proposal only):**

```text
Figure 7: Exploratory initial and final test nDCG@1 for three routing backbones using SkillSight, with the retriever-only score as a reference. Each model contributes one run over 748 tasks; hatching distinguishes initialization. Final values are 0.742, 0.802, and 0.745 for Qwen3.5-4B, Qwen3.8-27B, and GPT-OSS-120B, respectively. The source is nonreportable and historical candidate pools are not controlled. These endpoints do not establish statistical equivalence or a model-independent ceiling.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 8 — replace — pages/page_23_clean.txt

**Old (exact clean-extract text):**

```text
Figure 8: Recorded tokens and routing performance at different candidate-pool sizes. Blue shades distinguish Top-K settings, which specify how many retrieved candidates are evaluated rather than how many skills are ultimately selected.
```

**New (proposal only):**

```text
Figure 8: Analysis-only candidate-pool observations with Qwen3.5-4B and SkillSight after ten optimization iterations. K denotes retrieved candidates evaluated, not supplied skills. Each point is one nonreportable run evaluated on 748 test tasks; nDCG@10 is task-weighted. Tokens are recorded known run-local usage, excluding external/shared initialization and unavailable usage. The three settings are not a controlled budget-matched comparison and do not identify a generally optimal candidate count.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

- Approved synchronized figure assets/sidecars and selected-data manifests; provenance decisions must precede any stronger figure claims.

**Alternative / claim narrowing:** Keep readable assets; fix evidence qualifiers and only demonstrated accessibility/layout problems. Generation code is deliberately null because no asset generation is authorized.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] All8 figures are audited at final composed size; tiny essential labels are enlarged without altering template.

- [ ] Figure2 depicts rejection, iteration-end gate and correct comparator.

- [ ] Figures5–8 captions identify actual repeats, normalization and evidence scope.

- [ ] Caption sidecars and included assets remain synchronized; Figure3 is rechecked against newer live version.

**Consistency propagation:** All eight captions/sidecars, Figures_pass, Main text references.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

### ISSUE-015 — MINOR — Redundancy, grammar errors and inconsistent notation weaken an otherwise recoverable narrative.

**Status:** proposed, not applied; unresolved. **Window:** unknown. **Dependencies:** ISSUE-002, ISSUE-003, ISSUE-007, ISSUE-010, ISSUE-012, ISSUE-004, ISSUE-006, ISSUE-011, ISSUE-013, ISSUE-014.

**Skeptical assessment:** Confirmed concrete grammar defects; the reviewer’s proposed full sentence cannot replace only “a black-box setting called RouterBSI.” Expand to the complete duplicated sentence. The frozen conclusion already contains a downstream caveat; preserve it, noting that the later live conclusion changed externally. Abstract count is200 tokens in the clean extraction, versus201 in the critic: neither implies a venue violation.

**Review location:** Introduction / method / captions; frozen page 2. Raw anchor occurs once in `pages.json`.

#### Text proposal 1 — replace — pages/page_02_clean.txt

**Old (exact clean-extract text):**

```text
We introduce RouterBSI, a recursive selfimproving algorithm for skill routing in a black-box setting called RouterBSI.
```

**New (proposal only):**

```text
We introduce RouterBSI, a black-box algorithm that iteratively refines natural-language skill-applicability predicates without updating model weights.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 2 — replace — pages/page_02_clean.txt

**Old (exact clean-extract text):**

```text
efficiencly
```

**New (proposal only):**

```text
efficiently
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 3 — replace — pages/page_02_clean.txt

**Old (exact clean-extract text):**

```text
don’t directly minimizing
```

**New (proposal only):**

```text
do not directly minimize
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 4 — replace — pages/page_04_clean.txt

**Old (exact clean-extract text):**

```text
Compare difference between Pqwith Gq and identify the any of the following failures: required skill not selected, selected irrelevant skill.
```

**New (proposal only):**

```text
Compare the selected set P_q with the required set G_q to identify missing required candidates and extra selected skills; retrieval misses do not trigger predicate repair.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 5 — replace — pages/page_04_clean.txt

**Old (exact clean-extract text):**

```text
skill ssk
```

**New (proposal only):**

```text
skill s
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 6 — replace — pages/page_04_clean.txt

**Old (exact clean-extract text):**

```text
To reduce overly long and detailed predicates that may not generalize, we limit each proposed candidate mp ∈Mp must not exceeds a max length l.
```

**New (proposal only):**

```text
Each proposed candidate must contain at most l characters, including spaces and punctuation.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 7 — replace — pages/page_04_clean.txt

**Old (exact clean-extract text):**

```text
End the iteration by updating the next predicate p(i+1) sk of the skill s if the selected candidate update ∂passed the held-out validation gate. Repeat this self-improvement loop until i iterations.
```

**New (proposal only):**

```text
At iteration end, retain admitted predicates and restore rejected predicates to their iteration-start values. Repeat for the prespecified number of training iterations.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 8 — replace — pages/page_01_clean.txt

**Old (exact clean-extract text):**

```text
As agents are expected to solve broader and more complex tasks, they rely on external knowledge saved as skills to handle tasks beyond the LLM’s parametric capabilities. As the skill corpora grows into hundreds or thousands of skills, skill routing becomes a bottleneck, where the agent must efficiently retrieve and select the appropriate skills to complete a task. Recent skill routing approaches leverage task feedback to improve skill routing performance online. However, feedback-driven updates to routing criteria can regress performance, and accumulating task feedback at scale requires efficient experience management. We introduce a recursive self-improving algorithm for skill routing in a black-box setting called RouterBSI. It refines task applicability predicates using Minimum Bayes Risk (MBR) with bounded replay to minimize errors on seen tasks and a held-out validation gate to reduce regressions on unseen tasks. The router evaluates predicates for top-k retrieved skills then selects skills if the task satisfies their respective predicate. RouterBSI improves its cold-start top-5 recall of required skills by 24.9% across different retrievers on tasks from TheoremQA, LogicBench, ToolQA, MedCalc-Bench, CHAMP, and BigCodeBench sharing a 26k skill corpus. On average, it retains 90.5% of the required skills in top 5 from the top 50 skills retrieved.
```

**New (proposal only):**

```text
Skill routing must distinguish a reusable skill’s applicability from its topical similarity to a task. RouterBSI refines one natural-language applicability predicate per skill without updating language-model weights. It selects revisions by empirical Boolean loss on bounded, current-inclusive replay and applies an iteration-end validation gate against cold-start predicates. These checks do not guarantee monotonic improvement over previously accepted predicates or future tasks. We study six SRA-Bench collections using 748 held-out tasks involving skills represented in training, within a 26,262-skill retrieval corpus. In the current exploratory comparison, RouterBSI has the highest observed aggregate nDCG@1 and nDCG@10 among the reported router rows. Retention is normalized to each method’s own retrieval coverage, and improved routing does not establish uniform downstream gains. The paper-facing manifests mark load-bearing results nonreportable, so these observations require provenance resolution before they can support confirmatory claims.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 9 — replace — pages/page_08_clean.txt

**Old (exact clean-extract text):**

```text
We presented RouterBSI, a non-parametric framework that refines explicit skill applicability predicates from routing failures without updating model weights. It combines minimum Bayes risk selection over bounded replay with held-out validation. Experiments on six SRA-Bench datasets show that RouterBSI achieves the strongest average routing performance among evaluated methods and preserves more required skills as the selection budget decreases. Ablations support the complementary contributions of replay and validation and show improvements across model backbones. These findings demonstrate the value of editable predicates for feedback-driven skill routing, although stronger routing does not consistently yield the best downstream performance. Future work can incorporate skill dependencies to better connect skill selection with downstream task requirements.
```

**New (proposal only):**

```text
RouterBSI refines explicit skill-applicability predicates from labeled routing failures without updating model weights. Its empirical minimum-risk selector bounds per-update replay evaluation, not global task-history storage, and its iteration-end gate compares changed predicates with cold-start validation performance. The current six-benchmark results provide exploratory observations of routing gains; their nonreportable source status prevents confirmatory conclusions until execution and protocol bindings are resolved. Unpaired initialization limits component attribution, and routing gains do not consistently produce the best downstream success. Future work should test dependency expansion at matched skill budgets and assess checker and annotation errors without treating these hypotheses as established remedies.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 10 — replace — pages/page_02_clean.txt

**Old (exact clean-extract text):**

```text
We develop a recursive self-improvement procedure that refines predicates from routing failures, selects updates through minimum Bayes risk over a bounded replay of relevant and irrelevant tasks, and rejects updates with higher held-out validation error than the cold-start predicate.
```

**New (proposal only):**

```text
We develop a feedback-driven procedure that proposes predicate revisions from labeled routing errors, selects minimum empirical loss on bounded per-skill replay, and retains iteration-end changes only on strict validation improvement over cold-start. This does not guarantee monotonic validation performance over the previous predicate.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 11 — replace — pages/page_02_clean.txt

**Old (exact clean-extract text):**

```text
We evaluate RouterBSI on six SRA-Bench datasets with a shared 26K-skill corpus, achieving the highest aggregate nDCG@10 and Hit@1 among evaluated methods while ablations establish the contributions of replay and validation.
```

**New (proposal only):**

```text
We report exploratory routing and downstream comparisons on six SRA-Bench task collections with a shared 26,262-skill corpus. The archived point estimates favor RouterBSI on aggregate nDCG@1 and nDCG@10, but nonreportable provenance, historical candidate differences, and unpaired component initializations limit confirmatory and causal conclusions.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 12 — replace — pages/page_03_clean.txt

**Old (exact clean-extract text):**

```text
Given a failure in top k skills sk, the objective is to iteratively update the affected predicate psk(q) to correct the observed error without degrading previously learned or unseen routing decisions.
```

**New (proposal only):**

```text
Given a failed predicate among K retrieved candidates, the objective is to improve its applicability decisions using labeled routing feedback. The replay and validation checks constrain updates locally; they do not guarantee correction of the current failure or preservation of every prior or unseen decision.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 13 — replace — pages/page_02_clean.txt

**Old (exact clean-extract text):**

```text
It refines task applicability predicates using Minimum Bayes Risk (MBR) with bounded replay to minimize errors on seen tasks and a held-out validation gate to reduce regressions on unseen tasks.
```

**New (proposal only):**

```text
It refines applicability predicates by empirical minimum-risk selection on current-inclusive per-skill replay and applies an iteration-end gate against cold-start validation error. These local checks do not guarantee non-regression relative to the previous accepted predicate.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

#### Text proposal 14 — replace — pages/page_02_clean.txt

**Old (exact clean-extract text):**

```text
On average, it retains 90.5% of the required skills in top 5 from the top 50 skills retrieved.
```

**New (proposal only):**

```text
The exploratory mean Ret@5 is 90.5%: a ratio of task-mean Recall@5 to each method’s own task-mean Recall@50, averaged equally over three retrievers. This is not unconditional required-skill recall.
```

Author-approved prose proposal; PDF-to-TeX mapping must be confirmed before application.

**Required inputs / approvals:**

- Author approval of this exact proposal and a synchronized target source/PDF snapshot.

- Author approval of coordinated title/terminology, abstract and conclusion; source/TeX math mapping and rebase against externally changed conclusion.

**Alternative / claim narrowing:** Keep the already concise abstract if necessary, but add the provenance/represented-skill/retention scope and preserve downstream caveats. Do not enforce arbitrary sentence or paragraph quotas.

**Acceptance checks — all unverified for an unapplied revision:**

- [ ] Listed grammar/notation defects are removed and formulas/indices checked.

- [ ] Main-body promotions fit the assumed8-page submission budget without style changes.

- [ ] Required sections and honest caveats remain intact.

**Consistency propagation:** Title, Abstract, §1 contributions, §3–4 indices/K/k, Captions, Conclusion/Limitations/Ethics.

**Page impact:** unknown; replace superseded prose before adding summaries; no compilation or layout measurement authorized.

## Conditional evidence branches — none executed

### EXP-001 — Initialization-paired component ablation (conditional)

Needed only for a controlled component-effect claim beyond descriptive existing runs.

**Proposed design:** After source/provenance reconciliation, cross all four configurations with the same frozen initialization library within each independent replicate; fix split/candidate order, task order, model/checker/prompt settings and iteration endpoint. Prespecify replay/proposal randomness; report paired differences, task-weighted metrics and across-replicate uncertainty. Choose repeats from a justified budget/precision target, not an invented ACL minimum.

**If unsupported:** Keep descriptive results and remove causal-strength wording if effects are not stable.

**Status:** not executed; no authorization, new results, compute estimate, verified deadline or outcome prediction. Inventory saved artifacts first.

### EXP-002 — Matched downstream skill-budget comparison (conditional)

Needed only to attribute downstream improvement to dependency expansion.

**Proposed design:** Use identical downstream model, prompts, answer evaluation, query set and context truncation. Cross skill budget5 and10 for RouterBSI and SkillDAG, with retriever-only controls and explicit graph-expansion/candidate-pool differences. Cache valid prior outputs only where exact requests match; report paired outcomes and token context length.

**If unsupported:** Retain larger-budget graph result as contextual comparison, not dependency causality.

**Status:** not executed; no authorization, new results, compute estimate, verified deadline or outcome prediction. Inventory saved artifacts first.

### EXP-003 — Paired uncertainty from saved outputs

Quantify task-sampling uncertainty without rerunning models where outputs exist.

**Proposed design:** From exact saved predictions/outcomes, bootstrap task IDs with all retriever conditions for that task held together; stratify within benchmark and preserve task-weighted pooling. Prespecify comparisons and report confidence intervals plus effect sizes. Separate training-run variance. A resampling seed and precision target must be registered before reporting.

**If unsupported:** Use observed/descriptive superiority only when intervals do not establish a reliable difference.

**Status:** not executed; no authorization, new results, compute estimate, verified deadline or outcome prediction. Inventory saved artifacts first.

### EXP-004 — Canonical evidence recovery (only for proven gaps)

Bind confirmatory claims to exact artifacts without treating exploratory source drift as a canonical run.

**Proposed design:** First inventory per-result provenance, source/prompt/checkpoint/split/cache bindings and validation-rollback state. Reuse already verified artifacts. If missing, author decides whether to remove/narrow the claim or authorize a bounded fresh canonical run; label it new, not historical continuation.

**If unsupported:** Remove or retain as explicitly exploratory only any result whose required evidence cannot be reconstructed.

**Status:** not executed; no authorization, new results, compute estimate, verified deadline or outcome prediction. Inventory saved artifacts first.

## Pass A — all eight figures

The frozen contact sheet and composed-page scout were inspected. This is not a final-size check of redesigned assets. Figure 1 has tiny physical text despite high resolution; Figure 4 has roughly 6.44-point labels. Figures 3/5/6/7 are generally legible at approximately 8–9 points; do not redraw them simply on a blanket illegibility claim. Full caption old/new proposals appear under ISSUE-014.

### Figure 1

**Observed:** Column-width task/predicate illustration contrasting a single-date price query with a date-range query.

**Problems:** Tiny physical diagram despite high raster resolution; redraw only if approved. No low-DPI claim is established.

**Specification:** Vector task–predicate schematic at \columnwidth. Shorten the two query boxes without altering their meanings; use Accepted/Rejected labels and check/cross shapes as well as color. Aim for 8–9 pt labels at final size, with 7 pt only as an internal minimum guide. No quantitative axes or error bars apply. Keep Figure1 a setup example; do not imply an empirical human-interpretability result.

**Proposed caption:** Figure 1: An applicability predicate distinguishes a single-trading-day price query (q1, accepted) from a date-range query (q2, rejected). This illustrative task setup separates applicability from topical similarity; the feedback-update procedure appears in Figure 2.

**Generation code:** not produced; no asset generation authorized. Data must be bound to approved evidence before generation.

- [ ] Legible at final ACL column/text width; 7 pt is internal advice, not venue law — partial: Frozen rendering and scout_compliance.json inspected; specified revision not rendered or applied. Figure1/4 need attention; no final revised-size check exists.

- [ ] Information is not encoded by color alone — partial: Text/shape/marker encoding is specified; no revised figure has been generated or verified.

- [ ] Caption is self-contained and states only evidence-supported findings — fail: Exact caption rewrite is proposed only; original caption remains unchanged by this fixer.

- [N/A] Quantitative axes have labels and units — n/a: Schematic has no quantitative axes.

- [N/A] Measured uncertainty and sample/repeat counts stated where relevant — n/a: Illustrative schematic, no statistical estimate.

- [ ] No misleading axes, decorative distortions or cherry-picked ranges — partial: Retain full source series; Figure4 baseline correction specified; changes unexecuted.

- [ ] Figure1 conveys setup/contribution appropriately — partial: Setup-example role is deliberate; update mechanism reserved for Figure2; no compulsory teaser rule.

- [ ] Colors, fonts and markers consistent across figures — fail: Coordinated specifications only; no assets changed.

### Figure 2

**Observed:** Wide three-stage routing/proposal/replay-selection schematic with validation gate.

**Problems:** No explicit rejection/rollback path; caption conflates timing/comparator. Existing wide diagram is generally legible; avoid a blanket tiny-text claim.

**Specification:** Vector flow diagram at \textwidth. Separate inference routing from training repairs; mark K candidates versus k supplied skills. Draw an iteration-end gate diamond with retain and rollback branches, explicitly labeling the cold-start comparator and rollback destination. Show history caps N per class and current task q; distinguish unbounded global history. Blue/orange plus solid/dashed arrows and branch text; 8–9 pt labels. Schematic only: no axes/error bars.

**Proposed caption:** Figure 2: RouterBSI routes retrieved candidates with skill-applicability predicates and proposes revisions after labeled routing failures. Candidate selection minimizes mean Boolean error on current-inclusive replay, including the unchanged predicate. Updates are provisional during a training pass. At iteration end, a changed predicate is retained only when its validation error is strictly below cold-start; ties or absent validation support restore its iteration-start value. This gate does not guarantee improvement over the previous accepted predicate.

**Generation code:** not produced; no asset generation authorized. Data must be bound to approved evidence before generation.

- [ ] Legible at final ACL column/text width; 7 pt is internal advice, not venue law — partial: Frozen rendering and scout_compliance.json inspected; specified revision not rendered or applied. Figure1/4 need attention; no final revised-size check exists.

- [ ] Information is not encoded by color alone — partial: Text/shape/marker encoding is specified; no revised figure has been generated or verified.

- [ ] Caption is self-contained and states only evidence-supported findings — fail: Exact caption rewrite is proposed only; original caption remains unchanged by this fixer.

- [N/A] Quantitative axes have labels and units — n/a: Schematic has no quantitative axes.

- [N/A] Measured uncertainty and sample/repeat counts stated where relevant — n/a: Illustrative schematic, no statistical estimate.

- [ ] No misleading axes, decorative distortions or cherry-picked ranges — partial: Retain full source series; Figure4 baseline correction specified; changes unexecuted.

- [N/A] Figure1 conveys setup/contribution appropriately — n/a: Figure1-specific editorial criterion.

- [ ] Colors, fonts and markers consistent across figures — fail: Coordinated specifications only; no assets changed.

### Figure 3

**Observed:** Six-method required-skill retention curves over ranked cutoffs.

**Problems:** Normalization and provenance are missing from caption; dense legend is an editorial issue, not established illegibility. Existing non-color cues should be retained. Later Figure3 was changed externally.

**Specification:** Retain the six series from Table8 and verify against its bound selected-data file. Column-width line plot with categorical cutoffs 50,25,10,5,1; y=Ret@k (%), show 0–100 or clearly disclosed restricted limits. Distinct markers and dashes plus Okabe–Ito colors; simplify the legend without hiding baseline series. Do not fabricate uncertainty. Ordinary labels are already approximately8–9 pt; recheck the externally updated Figure3 before changing its asset.

**Proposed caption:** Figure 3: Exploratory required-skill retention across ranked cutoffs. For each method and retriever, Ret@k is 100 times task-mean Recall@k divided by that method’s task-mean Recall@50; the three ratios are averaged equally over BM25, Vector, and SkillSight. Cutoffs are categorical, and 100% at k=50 is normalization, not complete gold-skill coverage. SkillDAG uses expanded coverage. The source manifest marks these records nonreportable. Values are point estimates, not confidence intervals.

**Generation code:** not produced; no asset generation authorized. Data must be bound to approved evidence before generation.

- [ ] Legible at final ACL column/text width; 7 pt is internal advice, not venue law — partial: Frozen rendering and scout_compliance.json inspected; specified revision not rendered or applied. Figure1/4 need attention; no final revised-size check exists.

- [ ] Information is not encoded by color alone — partial: Text/shape/marker encoding is specified; no revised figure has been generated or verified.

- [ ] Caption is self-contained and states only evidence-supported findings — fail: Exact caption rewrite is proposed only; original caption remains unchanged by this fixer.

- [ ] Quantitative axes have labels and units — partial: Required units and scales are specified; no revised artifact exists.

- [ ] Measured uncertainty and sample/repeat counts stated where relevant — partial: No new intervals or repeat measurements available; caption explicitly limits inference and supplies known sample scope.

- [ ] No misleading axes, decorative distortions or cherry-picked ranges — partial: Retain full source series; Figure4 baseline correction specified; changes unexecuted.

- [N/A] Figure1 conveys setup/contribution appropriately — n/a: Figure1-specific editorial criterion.

- [ ] Colors, fonts and markers consistent across figures — fail: Coordinated specifications only; no assets changed.

### Figure 4

**Observed:** Downstream success bars with direct/oracle horizontal references.

**Problems:** Truncated bar axis starts at0.4; physically small method labels; malformed caption and missing native-budget/provenance scope.

**Specification:** Prefer horizontal dot plot at \textwidth with direct method labels; alternatively use bars starting at zero. y=method and x=success rate (0–1), retaining exact Table19 data and labeled Direct/Oracle reference lines. Label skill budgets alongside methods; distinguish references by dash patterns. Enlarge approximately6.44-pt method labels to8–9 pt. Add intervals only after approved paired analysis on verified outputs; no fabricated bars.

**Proposed caption:** Figure 4: Exploratory downstream success rates. Each retriever score pools 748 test tasks; bars average BM25, Vector, and SkillSight equally. SkillDAG supplies ten skills, SkillRouter and RouterBSI_top5 five, and RouterBSI_strict a variable selected set. LLM Direct omits skills and LLM Oracle supplies annotated required skills as a reference, not an upper bound. The aggregate includes a nonreportable Vector RouterBSI run. RouterBSI_top5 exceeds strict routing on average, but not for every retriever; no paired uncertainty is shown.

**Generation code:** not produced; no asset generation authorized. Data must be bound to approved evidence before generation.

- [ ] Legible at final ACL column/text width; 7 pt is internal advice, not venue law — partial: Frozen rendering and scout_compliance.json inspected; specified revision not rendered or applied. Figure1/4 need attention; no final revised-size check exists.

- [ ] Information is not encoded by color alone — partial: Text/shape/marker encoding is specified; no revised figure has been generated or verified.

- [ ] Caption is self-contained and states only evidence-supported findings — fail: Exact caption rewrite is proposed only; original caption remains unchanged by this fixer.

- [ ] Quantitative axes have labels and units — partial: Required units and scales are specified; no revised artifact exists.

- [ ] Measured uncertainty and sample/repeat counts stated where relevant — partial: No new intervals or repeat measurements available; caption explicitly limits inference and supplies known sample scope.

- [ ] No misleading axes, decorative distortions or cherry-picked ranges — partial: Retain full source series; Figure4 baseline correction specified; changes unexecuted.

- [N/A] Figure1 conveys setup/contribution appropriately — n/a: Figure1-specific editorial criterion.

- [ ] Colors, fonts and markers consistent across figures — fail: Coordinated specifications only; no assets changed.

### Figure 5

**Observed:** Four component configurations with trajectories and shaded across-run dispersion.

**Problems:** False common-initialization caption; undefined shaded quantity and nonreportability. Fonts generally readable, not a primary defect.

**Specification:** Keep four Table11 trajectories including iteration0 and all ten endpoints; x=iteration, y=nDCG@1 with a clearly labeled fixed scale. Column width, 8–9 pt labels already generally legible. Distinct markers/dashes and colorblind-safe colors; improve faint-band contrast but preserve population-SD meaning and rounded-variance caveat. Do not replace SD with CI or imply independent seeds.

**Proposed caption:** Figure 5: Exploratory component trajectories with Qwen3.5-4B and SkillSight. Lines show mean task-weighted test nDCG@1 across three runs of 748 tasks each; bands show population SD reconstructed from rounded variances (Table 11), not confidence intervals. Both-enabled runs use separately generated initial libraries, whereas other configurations reuse the first both-enabled library; all record replay seed 20260324. The comparison is not initialization-paired, and all twelve source runs are nonreportable. Both enabled has the highest observed final mean.

**Generation code:** not produced; no asset generation authorized. Data must be bound to approved evidence before generation.

- [ ] Legible at final ACL column/text width; 7 pt is internal advice, not venue law — partial: Frozen rendering and scout_compliance.json inspected; specified revision not rendered or applied. Figure1/4 need attention; no final revised-size check exists.

- [ ] Information is not encoded by color alone — partial: Text/shape/marker encoding is specified; no revised figure has been generated or verified.

- [ ] Caption is self-contained and states only evidence-supported findings — fail: Exact caption rewrite is proposed only; original caption remains unchanged by this fixer.

- [ ] Quantitative axes have labels and units — partial: Required units and scales are specified; no revised artifact exists.

- [ ] Measured uncertainty and sample/repeat counts stated where relevant — partial: Existing three-run population SD preserved, not an invented CI; revised caption unapplied.

- [ ] No misleading axes, decorative distortions or cherry-picked ranges — partial: Retain full source series; Figure4 baseline correction specified; changes unexecuted.

- [N/A] Figure1 conveys setup/contribution appropriately — n/a: Figure1-specific editorial criterion.

- [ ] Colors, fonts and markers consistent across figures — fail: Coordinated specifications only; no assets changed.

### Figure 6

**Observed:** Component-configuration quality versus token scatter plot.

**Problems:** Cost-axis completeness implication, unmatched phase accounting and missing single-run/provenance scope; not established unreadability.

**Specification:** Column-width scatter using the four first-run Table12 pairs; x=Recorded known run-local tokens (millions), y=test nDCG@1. Preserve all configurations; use distinct shapes, direct labels, Okabe–Ito colors and visible tick labels. Existing8–9 pt labels are generally legible. Optional separate panel uses iteration-only tokens with unchanged first-run quality; never mix total and iteration x-values without explicit labeling. No unmeasured error bars.

**Proposed caption:** Figure 6: Exploratory first-run nDCG@1 versus recorded known run-local tokens for the four component configurations (Table 12), distinct from Figure 5’s three-run means. Only both enabled includes local initialization; reused external initialization and attempts with unknown usage are excluded. Source records are nonreportable. These points do not establish complete end-to-end savings or per-query serving cost; no uncertainty is available for these first-run points.

**Generation code:** not produced; no asset generation authorized. Data must be bound to approved evidence before generation.

- [ ] Legible at final ACL column/text width; 7 pt is internal advice, not venue law — partial: Frozen rendering and scout_compliance.json inspected; specified revision not rendered or applied. Figure1/4 need attention; no final revised-size check exists.

- [ ] Information is not encoded by color alone — partial: Text/shape/marker encoding is specified; no revised figure has been generated or verified.

- [ ] Caption is self-contained and states only evidence-supported findings — fail: Exact caption rewrite is proposed only; original caption remains unchanged by this fixer.

- [ ] Quantitative axes have labels and units — partial: Required units and scales are specified; no revised artifact exists.

- [ ] Measured uncertainty and sample/repeat counts stated where relevant — partial: No new intervals or repeat measurements available; caption explicitly limits inference and supplies known sample scope.

- [ ] No misleading axes, decorative distortions or cherry-picked ranges — partial: Retain full source series; Figure4 baseline correction specified; changes unexecuted.

- [N/A] Figure1 conveys setup/contribution appropriately — n/a: Figure1-specific editorial criterion.

- [ ] Colors, fonts and markers consistent across figures — fail: Coordinated specifications only; no assets changed.

### Figure 7

**Observed:** Initial/final nDCG@1 bars for three backbones and SkillSight reference.

**Problems:** Caption overinterprets cross-model closeness; single-run, historical-candidate and nonreportable scope absent. Labels are generally legible.

**Specification:** Column-width paired bars with zero-based0–1 y-axis; x=reported backbone identifiers. Preserve Table14 initial/final values and independent SkillSight reference. Hatch initial bars and use outlined final bars plus consistent colors; readable8–9 pt labels. No invented uncertainty; compare within each reported run without presenting model size as the only controlled factor.

**Proposed caption:** Figure 7: Exploratory initial and final test nDCG@1 for three routing backbones using SkillSight, with the retriever-only score as a reference. Each model contributes one run over 748 tasks; hatching distinguishes initialization. Final values are 0.742, 0.802, and 0.745 for Qwen3.5-4B, Qwen3.8-27B, and GPT-OSS-120B, respectively. The source is nonreportable and historical candidate pools are not controlled. These endpoints do not establish statistical equivalence or a model-independent ceiling.

**Generation code:** not produced; no asset generation authorized. Data must be bound to approved evidence before generation.

- [ ] Legible at final ACL column/text width; 7 pt is internal advice, not venue law — partial: Frozen rendering and scout_compliance.json inspected; specified revision not rendered or applied. Figure1/4 need attention; no final revised-size check exists.

- [ ] Information is not encoded by color alone — partial: Text/shape/marker encoding is specified; no revised figure has been generated or verified.

- [ ] Caption is self-contained and states only evidence-supported findings — fail: Exact caption rewrite is proposed only; original caption remains unchanged by this fixer.

- [ ] Quantitative axes have labels and units — partial: Required units and scales are specified; no revised artifact exists.

- [ ] Measured uncertainty and sample/repeat counts stated where relevant — partial: No new intervals or repeat measurements available; caption explicitly limits inference and supplies known sample scope.

- [ ] No misleading axes, decorative distortions or cherry-picked ranges — partial: Retain full source series; Figure4 baseline correction specified; changes unexecuted.

- [N/A] Figure1 conveys setup/contribution appropriately — n/a: Figure1-specific editorial criterion.

- [ ] Colors, fonts and markers consistent across figures — fail: Coordinated specifications only; no assets changed.

### Figure 8

**Observed:** Appendix candidate-budget scatter plot of nDCG@10 versus recorded tokens.

**Problems:** Blue-shade-only identification and absent caption-level analysis-only/known-usage caveats.

**Specification:** Column-width scatter retaining G.3 coordinates for K=10,25,50. x=Recorded known run-local tokens (millions), y=test nDCG@10. Directly label each point with K and use circle/triangle/square, not three blue shades alone. Apply consistent8–9 pt fonts and visible ticks; remove redundant chart title if space needed. No fabricated error bars or fitted trend line.

**Proposed caption:** Figure 8: Analysis-only candidate-pool observations with Qwen3.5-4B and SkillSight after ten optimization iterations. K denotes retrieved candidates evaluated, not supplied skills. Each point is one nonreportable run evaluated on 748 test tasks; nDCG@10 is task-weighted. Tokens are recorded known run-local usage, excluding external/shared initialization and unavailable usage. The three settings are not a controlled budget-matched comparison and do not identify a generally optimal candidate count.

**Generation code:** not produced; no asset generation authorized. Data must be bound to approved evidence before generation.

- [ ] Legible at final ACL column/text width; 7 pt is internal advice, not venue law — partial: Frozen rendering and scout_compliance.json inspected; specified revision not rendered or applied. Figure1/4 need attention; no final revised-size check exists.

- [ ] Information is not encoded by color alone — partial: Text/shape/marker encoding is specified; no revised figure has been generated or verified.

- [ ] Caption is self-contained and states only evidence-supported findings — fail: Exact caption rewrite is proposed only; original caption remains unchanged by this fixer.

- [ ] Quantitative axes have labels and units — partial: Required units and scales are specified; no revised artifact exists.

- [ ] Measured uncertainty and sample/repeat counts stated where relevant — partial: No new intervals or repeat measurements available; caption explicitly limits inference and supplies known sample scope.

- [ ] No misleading axes, decorative distortions or cherry-picked ranges — partial: Retain full source series; Figure4 baseline correction specified; changes unexecuted.

- [N/A] Figure1 conveys setup/contribution appropriately — n/a: Figure1-specific editorial criterion.

- [ ] Colors, fonts and markers consistent across figures — fail: Coordinated specifications only; no assets changed.

## Pass B — writing

Frozen clean-extract abstract: **200 whitespace tokens** excluding headings; critic reported 201 with a different extraction boundary. Proposed abstract: **136 tokens**, not applied. The under-250 target is internal editorial guidance, not an established venue requirement. No words, overclaims or hedges were removed from the manuscript by this task; all actual change counts are zero. Longest paragraph length and revised layout remain unmeasured.

Concrete grammar, local guarantee, abstract, contribution and conclusion proposals are above. Do not rewrite uncertainty into confidence, turn “observed” into statistical significance, or present more iterations/manual edits as proven remedies. Preserve frozen conclusion’s downstream caveat when merging the externally changed live conclusion.

- [ ] Abstract states problem, contribution, method, supported result and implication; internal word target is not official policy — not verified for an unapplied revision.

- [ ] Introduction explains difficulty, distinction and evidence — not verified for an unapplied revision.

- [ ] Every abstract claim has body support and consistent scope — not verified for an unapplied revision.

- [ ] Novelty, significance and outperformance language is evidence-calibrated — not verified for an unapplied revision.

- [ ] Long paragraphs and sentence clarity reviewed without arbitrary quotas — not verified for an unapplied revision.

- [ ] Revised main content fits the active limit in a built PDF — not verified for an unapplied revision.

- [ ] Reproducibility details refer to actual artifacts/settings — not verified for an unapplied revision.

- [ ] Distinct Limitations remains before References without new results — not verified for an unapplied revision.

- [ ] Ethics/actual AI disclosure assessed separately from submission checklist completion — not verified for an unapplied revision.

## Pass C — narrative

Editable natural-language applicability predicates, empirical replay selection and cold-start validation provide an inspectable skill-routing procedure; current nonreportable comparisons support exploratory observations, not confirmed routing or downstream superiority.

- **Inspectable, editable per-skill applicability predicates with fixed model weights** — §4.1 and Appendix B. Evidence: Predicate interface and examples; no human editing/interpretability study claimed. Revisited in the frozen conclusion; proposed rewrite remains unapplied.

- **Current-inclusive class-bounded empirical replay and iteration-end cold-start gate** — §4.2–4.3 and Appendix A. Evidence: Algorithm and local inequality; Figure5/Tables10–11 are unpaired/nonreportable descriptive records, not confirmatory component isolation. Revisited in the frozen conclusion; proposed rewrite remains unapplied.

- **Exploratory routing, retention and downstream evaluation on represented-skill tasks** — §§5–7 and Appendices E–H. Evidence: Table1/Figures3–7 and Tables19–20; reportability/candidate/budget gates unresolved, downstream gains not uniform. Revisited in the frozen conclusion; proposed rewrite remains unapplied.

- [ ] Title accurately conveys contribution without unexplained Bayesian inference — unresolved for the proposed version.

- [ ] Abstract frames supported implications and provenance scope — unresolved for the proposed version.

- [ ] Opening material makes skill-applicability thesis recoverable — unresolved for the proposed version.

- [ ] Every contribution maps to delivery, evidence and conclusion with calibrated scope — unresolved for the proposed version.

- [ ] Related Work accurately distinguishes JTPRO and empirical risk from posterior MBR — unresolved for the proposed version.

- [ ] Conclusion states supported implications and genuinely untested next steps — unresolved for the proposed version.

- [ ] Main text contains all load-bearing method/protocol/evidence caveats within active budget — unresolved for the proposed version.

## Self-containment: left in place solely because this is proposal-only

- **Current-inclusive replay, global-history memory scope, gate timing/rollback and ranking semantics** (A.1–A.4 pp.11–12): `left_with_justification`. Proposal-only authorization: no main-text promotion or source edit has been executed. Proposed compact summaries are in the linked issue payload; existing appendix placement is not endorsed as adequate.

- **Filtering/exact counts and represented-skill rather than unseen-skill generalization** (C.1/Table3 pp.16–17): `left_with_justification`. Proposal-only authorization: no main-text promotion or source edit has been executed. Proposed compact summaries are in the linked issue payload; existing appendix placement is not endorsed as adequate.

- **Ablation initialization sharing and single-run known-only asymmetric cost accounting** (G.1–G.2/Tables10–12 pp.20–24): `left_with_justification`. Proposal-only authorization: no main-text promotion or source edit has been executed. Proposed compact summaries are in the linked issue payload; existing appendix placement is not endorsed as adequate.

- **Conditional error percentages do not measure predicate rejection** (H.4/Table18 pp.26–27): `left_with_justification`. Proposal-only authorization: no main-text promotion or source edit has been executed. Proposed compact summaries are in the linked issue payload; existing appendix placement is not endorsed as adequate.

- **Noncanonical exploratory provenance and class-imbalanced model adjudication** (G.3/H.1 pp.22–24): `left_with_justification`. Proposal-only authorization: no main-text promotion or source edit has been executed. Proposed compact summaries are in the linked issue payload; existing appendix placement is not endorsed as adequate.

## Human-only decisions and unperformed verification

- Select and freeze a synchronized source/PDF target; preserve externally completed ISSUE-001 deletion, revised Figure3, and later conclusion changes.

- Confirm venue/year/track/cycle/stage, long/short paper type, deadline and allowed revision window; assumed8-page long budget is not a confirmed active limit.

- Approve or reject each exact text/figure proposal before any application; choose empirical-risk naming and neutral Extra/Missing terminology.

- Inventory existing provenance and decide which nonreportable evidence can satisfy its original audit gates; otherwise narrow/remove claims or separately authorize bounded replacement work.

- Supply baseline/model/candidate configurations, tie-break implementation, and exact output/artifact bindings.

- Choose descriptive versus stronger causal/inferential claims. EXP-001–004 are conditional proposals, not work orders or completed evidence.

- After a separate edit authorization, map PDF anchors to current TeX, apply overlapping replacements once, synchronize sidecars/captions/metadata, and verify builds/layout without style compression.

- Confirm coauthor approval/order, metadata, profiles, review-service obligations/exemptions, quotas if applicable, cycle eligibility, originality/overlap/dual submission, prior ARR URL/materials and preprint status.

- Complete Responsible NLP Checklist with truthful evidence or N/A; verify actual AI-assistance disclosure policy/location, licenses/privacy obligations and supplement anonymity.

No REVISED_MANUSCRIPT, build, figure asset, experimental result, DOCX, author-response draft, or upload was produced. Approval of a proposal is not verification that its acceptance checks passed. The JSON preserves all 47 reviewer acceptance criteria, with none marked pass, all 15 issues unresolved, and separate figure/writing/narrative checks.

**Artifact validation only:** strict JSON serialization, 15 unique issue logs/proposals/unresolved entries, 8 figure entries, literal frozen review anchors, exact clean-extract old spans, shared-field equality, and dependency order were checked. These checks validate this proposal package, not the paper’s scientific claims or an unapplied manuscript revision.
