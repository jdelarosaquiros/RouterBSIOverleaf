# RouterBSI — independent presentation, figure and compliance audit

**Review target:** `source/main.pdf`, SHA-256 `ddd4e45dcc8920cde89966c50e5a12598d73eee2dda1701b67f783057aeb1e63`.

**Outcome:** 31 total pages, **8 content-bearing pages**, all **8 figures** and all **31 pages** checked. Main prose concludes on p7, but Figures 5–7 continue on p8 before Limitations. No manuscript edits or experiments. Source snapshot hashes verified unchanged.

## Internal scores (1–5, not official ARR ratings)

| Dimension | Score | Rationale |
|---|---:|---|
| Presentation | 3 | Clean layout and recoverable method, offset by ambiguous main captions, small downstream chart labels and grammar defects. |
| Figure Quality | 3 | All eight figures render and carry interpretable evidence; statistics, normalization and cost scopes need main-caption clarification. |
| Narrative | 3 | Predicate→replay→gate thesis is recoverable and Figure 2 conveys it; Figure 1 is motivation only, and Section 7.3 overstates its three-backbone comparison. |
| Confidence | 4 | All 31 pages rendered/text-checked; all eight figures inspected at detail scale; source anchors/hash manifest verified. No fresh experiments, style-file provenance comparison, portal or venue/cycle validation. |

Scientific soundness/contribution and an acceptance recommendation are outside this focused audit. Official ARR scales remain unverified.

## Physical facts versus venue obligations

- **Physical facts:** every page is A4 (595.276 × 841.890 pt); two-column prose, ACL review class/options, page numbers and prose review rulers are present. All font records are embedded according to `pdffonts`, including Type 3. Searchable text is present on every page; no text span lies outside its page box. Rendered pages show no gross overlap or clipping.
- **Page boundary:** conclusion p7; body Figures 5–7 p8; Limitations starts p8 left column at y≈687 pt and continues into the right column; ethics and AI-only acknowledgment follow; References pp8–11; appendices A–H pp11–31. Wide tables on float-only pp29–31 are not single-column appendix prose.
- **Conditional page assessment:** fits the assumed long-review 8-page limit, with zero whole pages spare. Actual venue, cycle, stage, paper type and PDF-upload permission are unknown; no unconditional submission-compliance claim.
- **Anonymity/disclosure:** anonymous byline/metadata, no obvious PDF identity leak. Fresh `policy/3.txt` explicitly permits AI-only acknowledgments. The existing p8 disclosure is therefore **not** an anonymity violation. Current CFP asks for scope in the Responsible NLP Checklist and details in acknowledgments; actual use and form completeness remain human checks.
- **Limitations/ethics:** both occur before references; no new results or figures appear inside Limitations. Ethics discusses medical non-validity, untrusted execution, licenses and sensitive external-service data. This does not establish actual license/privacy compliance.
- **Unverified:** official style-file provenance, submission-form/checklist fields, supplements, author approval/profiles, reviewer obligations, eligibility, overlap/prior submission and preprint status. Do not infer these from the PDF.
- **Abstract:** 200 whitespace-delimited words in source; no abstract-length finding. PDF title metadata omits “Replay” from the printed title, a minor metadata synchronization note, not an anonymity issue.

## Prioritized findings

### PRES-001 — MAJOR: The headline retention figure does not define its ratio-of-mean-recalls denominator or disclose that SkillDAG uses its own expanded pool in the main caption.
**Anchor:** PDF p6, 6.2 Required Skill Retention; `source/figs/average_retention_degradation/table.tex:4–4`.
> Retention of required skills averaged across retrievers: BM25, Vector, and SkillSight.

1. Figure 3 plots all methods at 100% for k=50; the caption describes retention but provides no formula.
2. Appendix F.1, p20, defines a ratio of task-averaged recalls and method-specific Recall@50; this is not mean per-task retention or a shared-pool controlled comparison.
3. Because the abstract headline is 90.5% retention, the exact quantity is load-bearing main-paper information rather than merely replication detail.

**Fix, only in a permitted revision window:** Add Ret_{m,r}@k = 100 * mean-task Recall_{m,r}@k / mean-task Recall_{m,r}@50 to the main metric definition or Figure 3 caption; state that the three ratios are averaged equally and SkillDAG normalizes by its expanded pool. Preserve the current numerical results.
**Acceptance:** Main paper defines ratio of mean recalls, not mean task-level ratios.; Caption or adjacent main prose explicitly states per-method denominator and SkillDAG expanded pool.; Retention is not described as absolute recall or candidate-matched superiority.

### PRES-002 — MAJOR: The adjacent ablation figures leave the main reader unable to distinguish three-run mean/population-SD evidence from one-run final quality and incomplete known-token totals.
**Anchor:** PDF p8, 7.1; `source/figs/mbr_replay_test_ndcg@1_std/description.text:1–1`.
> The lines and areas represent the standard mean and variation, respectively across three runs starting from the same initial predicates at iteration 0.

1. Figure 5 says “standard mean and variation,” which does not define its shaded bands; Figure 6 says “token usage” without identifying one run or missing usage.
2. Appendix G.1/Table 10 defines three-run means and population SD, whereas G.2/Table 12 uses the first run with unavailable usage excluded and counted separately.
3. Figures 5 and 6 appear together on p8 with different final values (both enabled 0.724 mean versus 0.742 single run). Their interpretation requires a compact main-paper clarification.

**Fix, only in a permitted revision window:** Rewrite Figure 5 caption to state task-weighted test nDCG@1 over 748 tasks, three runs, mean ± one population standard deviation (not CI). Rewrite Figure 6 caption/axis as first-run final-test nDCG@1 versus known recorded input+output tokens across run-local phases; explicitly exclude unavailable usage and cite Table 12. Identify initialization/final policies consistently without altering values.
**Acceptance:** Figure 5 bands and split are named exactly.; Figure 6 says single run and known recorded tokens, not complete cost or per-query serving cost.; Main captions explain why Figure 5 and Figure 6 endpoints differ.

### PRES-003 — MAJOR: The Figure 7 interpretation turns a three-backbone non-monotonic comparison into an unsupported capability-independent predicate ceiling.
**Anchor:** PDF p7, 7.3 Skill Routing Performance across LLM Backbones; `source/sections/ablations.tex:24–24`.
> They also suggest that predicates reach a plateau that cannot be overcomed with more capable LLMs, where it's difficult for the predicate to be narrow enough to be false for irrelevant tasks but broad enough to be true for all relevant tasks

1. Figure 7 shows final nDCG@1 values 0.742, 0.802, and 0.745, with the middle-sized model best.
2. This supports improvement over each initialization and non-monotonic final performance by model size, not an intrinsic ceiling that more capable models cannot overcome.
3. Appendix Table 14 reports one run per backbone, so “significantly” should not imply an unreported significance test.

**Fix, only in a permitted revision window:** Replace the last two sentences of Section 7.3 with a bounded interpretation: all tested backbones improve; final quality is not monotonic in parameter count; Qwen3.5-4B approaches GPT-OSS-120B while Qwen3.8-27B is strongest. Describe the predicate expressivity explanation as an untested hypothesis or remove it. Name the one-run scope in Figure 7 caption.
**Acceptance:** No claim of a capability-independent ceiling remains.; No statistical-significance wording without a reported test.; Figure 7 caption identifies initial versus ten-iteration final policies and one run per model.

### PRES-004 — MINOR: Figure 4 has an ungrammatical headline caption and unnecessarily small labels for a full-width chart.
**Anchor:** PDF p7, 6.3 Downstream Performance; `source/figs/downstream_average/description.text:1–1`.
> outperforms strict selection and most other approaches oracle performance.

1. The actual caption ends “most other approaches oracle performance,” obscuring the intended comparison.
2. PDF text spans measure method names/value labels at about 6.44 pt and strict/top-5 subscripts at 4.51 pt despite full-width placement.
3. The chart correctly shows SkillDAG (0.631) above RouterBSI top-5 (0.611); the caption should preserve that exception. Bars start at 0.4, visually magnifying absolute gaps.

**Fix, only in a permitted revision window:** Rewrite the caption to say RouterBSI top-5 exceeds strict selection and most evaluated alternatives, remains below SkillDAG, and approaches oracle success. Re-render with larger labels; use a zero-based bar axis or a dot plot for the zoomed scale. Keep all reported values unchanged.
**Acceptance:** Caption is grammatical and preserves SkillDAG exception.; Labels are clearly legible on A4 at normal viewing/printing size; review enlarged labels against current 6.44-pt baseline.; Zoomed scale is explicit or bars begin at zero.

### PRES-005 — MINOR: Repeated copy-editing defects weaken an otherwise recoverable method narrative.
**Anchor:** PDF p4, 4.2 MBR Update Selection with Bounded Replay; `source/sections/method.tex:24–24`.
> Compare difference between \(P_{q}\)with \(G_{q}\) and identify the any of the following failures:

1. The method opens with a malformed imperative and contains “must not exceeds”; Figure 2 says “drive revisions selected which are selected”; the conclusion has “optmization.”
2. These are observed textual defects, not evidence that the revised replay or ranking definitions are wrong.
3. Editing the grammar and using consistent predicate-versus-risk notation would make the contribution easier to audit without changing the algorithm.

**Fix, only in a permitted revision window:** Copy-edit the anchored sentences: compare predicted and gold skill sets; constrain each candidate to maximum length; remove duplicated “selected” in Figure 2 caption; correct optmization. In Figure 2 label numerical examples R_replay(p_f)=0.50 and R_v(p_si)=0.60 rather than equating predicates with numbers. Preserve the cold-start validation comparator and strict inequality.
**Acceptance:** Anchored grammatical errors are removed without changing replay set, split, ranking normalization, tie rules or retriever training description.; Figure 2 numerical labels explicitly denote risks.; Figure 2 still compares candidate validation error with cold-start p_si, not previous accepted predicate.

## Every figure: visual inventory

| Figure / PDF page | Source anchor | What is actually shown / assessment | Internal score |
|---|---|---|---:|
| Figure 1 / p1 | `source/sections/introduction.tex:15` | Single-day versus multi-year coffee-price tasks routed through one predicate. The 218.25 by 59.18 point raster diagram is high-resolution but its text is small at one-column print size. It motivates applicability versus similarity; it does not show the replay/gate innovation. This is an editorial opportunity, not a mandatory teaser requirement. | 3 |
| Figure 2 / p3 | `source/sections/related_works.tex:8` | Three-stage route → failure-driven proposals → bounded-replay selection and held-out gate, with an iteration loop. The diagram correctly uses cold-start p_si and candidate validation error 0.45 < 0.60. It writes predicates equal to numeric risks and has a duplicated phrase in its caption; color is reinforced by text labels. | 4 |
| Figure 3 / p6 | `source/figs/average_retention_degradation/table.tex:4` | Six-series retention curve at categorical cutoffs 50,25,10,5,1, all normalized to 100 at 50. Distinct markers and line styles supplement colors. Descending equally spaced categorical cutoffs are readable; the ratio and method-specific denominator are not defined in the main caption. | 3 |
| Figure 4 / p7 | `source/figs/downstream_average/description.text:1` | Seven bars and direct/oracle horizontal reference lines; SkillDAG is highest at 0.631, RouterBSI top-5 0.611, strict 0.596. Numerical labels and reference lines make the rank ordering honest. Small 6.44-pt names/values and 4.51-pt subscripts, truncated bar baseline, and malformed caption reduce polish. No uncertainty is displayed; no significance can be inferred. | 3 |
| Figure 5 / p8 | `source/figs/mbr_replay_test_ndcg@1_std/description.text:1` | Four nDCG@1 trajectories over iterations 0–10 with shaded variability bands; both enabled has best final three-run mean. Shapes/linestyles provide non-color encoding; curves are compact but legible. “Standard mean and variation” fails to define bands; test split and population-SD meaning live in the appendix. Starting from the same predicate text need not force numerically identical measured initialization; appendix values differ slightly and are not evidence of a plotted contradiction. | 3 |
| Figure 6 / p8 | `source/figs/performance_token_usage/table.tex:4` | Four shape-coded nDCG@1 versus token-use points; both enabled has strongest quality and highest observed tokens. Shape-coded configuration legend is accessible. It reports first-run outcomes, unlike neighboring Figure 5. “Total Token Usage” hides incomplete known-token scope. | 3 |
| Figure 7 / p8 | `source/figs/routing_performance_across_llms_init/description.text:1` | SkillSight reference plus hatched initialization/solid optimized pairs for three backbones, with numerical labels. Hatching makes initial/final distinction readable without color; caption correctly notes smaller-versus-largest proximity. One-run scope is only in Table 14. The plotted non-monotonic final ordering does not support a universal capability ceiling. | 4 |
| Figure 8 / p23 | `source/figs/performance_token_usage_by_topk/description.text:1` | Three measured nDCG@10/token points for candidate pools 10,25,50, rendered at full width. Readable axes and sparse composition; three blue shades are the sole category cue. Caption explicitly distinguishes candidate pool from selected budget. Adjacent Appendix G.3 states single-run, incomplete known-token and non-causal/budget-unmatched interpretation. Axis still says total tokens although accompanying prose correctly qualifies recorded known usage. | 4 |

Detailed figure crops: `renders/figure-01.png` through `figure-08.png`; complete method/downstream crops are `figure-02-complete.png`, `figure-04-complete.png`, with full p8 figure stack in `figures-05-07-complete.png`. Page renders preserve full captions when an individual detail crop ends mid-caption.

## Cold-start and validation semantics

Figure 2 is **correct about the comparator**: candidate validation risk 0.45 passes cold-start risk 0.60. The main method (source `sections/method.tex:69–85`, PDF p4) explicitly rejects higher-or-equal cold-start-relative error and otherwise retains the previous predicate. This is not a monotonic guarantee against the previous accepted predicate. Appendix G.1 (`sections/appendix/ablation_components.tex:29–31`, PDF p21) states that distinction and reports 262 retained decisions worse than the previous predicate. A compact main caveat would improve interpretation without alleging a diagram inconsistency.

Figure 5 shows test trajectories, not validation curves; Figure 7 shows initialization versus optimized policies, not zero-shot generalization to unseen skills. The current main split description explicitly identifies held-out tasks with retained gold skills represented during training. The corrected replay definition/current-task inclusion, normalized ranking/tie handling, global split wording and fixed retriever setup are not treated as unresolved historical issues.

## All-page coverage

All pages were rendered at 108 dpi and inspected in eight contact sheets; all figure-bearing pages additionally received high-resolution detail inspection. Text extraction and page-boundary checks cover every page. This is presentation coverage, not a claim of independently reproducing every table or checking every citation.

| Page | Content / inspection result |
|---:|---|
| 1 | Title, abstract, Figure 1 and introduction. No gross clipping/overlap observed; searchable text present. |
| 2 | Contributions and related work. No gross clipping/overlap observed; searchable text present. |
| 3 | Figure 2, related work, problem definition and method. No gross clipping/overlap observed; searchable text present. |
| 4 | Method equations and experimental setup. No gross clipping/overlap observed; searchable text present. |
| 5 | Table 1 and experimental settings. No gross clipping/overlap observed; searchable text present. |
| 6 | Figure 3, results and ablation opening. No gross clipping/overlap observed; searchable text present. |
| 7 | Figure 4, ablations and conclusion. No gross clipping/overlap observed; searchable text present. |
| 8 | Figures 5–7; Limitations, Ethical Considerations, AI-only Acknowledgment; References start. No gross clipping/overlap observed; searchable text present. |
| 9 | References. No gross clipping/overlap observed; searchable text present. |
| 10 | References. No gross clipping/overlap observed; searchable text present. |
| 11 | References end and Appendix A start. No gross clipping/overlap observed; searchable text present. |
| 12 | Appendix A replay, validation and optimization procedure. No gross clipping/overlap observed; searchable text present. |
| 13 | Appendix A procedure and Appendix B initialization prompt. Dense but structurally clean two-column monospaced prompts; principal prompt text about 8.97 pt. No clipping observed. |
| 14 | Appendix B initialization and replacement prompts. Dense but structurally clean two-column monospaced prompts; principal prompt text about 8.97 pt. No clipping observed. |
| 15 | Appendix B replacement/evaluation prompts and worked trace. Dense but structurally clean two-column monospaced prompts; principal prompt text about 8.97 pt. No clipping observed. |
| 16 | Table 2 trace; Appendix C splits/labels. No gross clipping/overlap observed; searchable text present. |
| 17 | Table 3 split counts; data/corpus scope and Appendix D settings. No gross clipping/overlap observed; searchable text present. |
| 18 | Table 4 settings; requests/caching and variants. No gross clipping/overlap observed; searchable text present. |
| 19 | Implementation continuation and Appendix E metrics. No gross clipping/overlap observed; searchable text present. |
| 20 | Retention definition/results and Appendix G ablations. No gross clipping/overlap observed; searchable text present. |
| 21 | Table 5; gate caveats and token accounting. Dense, readable full-width result table with about 8.97-pt principal entries. Figure 8 also checked individually on p23. |
| 22 | Table 6; candidate pools/backbones and Appendix H evaluator. Dense, readable full-width result table with about 8.97-pt principal entries. Figure 8 also checked individually on p23. |
| 23 | Table 7; Figure 8 and evaluator continuation. Dense, readable full-width result table with about 8.97-pt principal entries. Figure 8 also checked individually on p23. |
| 24 | Table 8; evaluator and error definitions. No gross clipping/overlap observed; searchable text present. |
| 25 | Table 9; routing losses against SkillRouter. No gross clipping/overlap observed; searchable text present. |
| 26 | Table 10; representative error cases. No gross clipping/overlap observed; searchable text present. |
| 27 | Tables 11–12; downstream disagreement diagnosis. No gross clipping/overlap observed; searchable text present. |
| 28 | Tables 13–14; downstream outcomes. No gross clipping/overlap observed; searchable text present. |
| 29 | Tables 15–18 float-only appendix page. Sparse float-only page with full-width tables; not evidence of noncompliant one-column appendix prose. No clipping observed. |
| 30 | Tables 19–21 float-only appendix page. Sparse float-only page with full-width tables; not evidence of noncompliant one-column appendix prose. No clipping observed. |
| 31 | Table 22 float-only appendix page. Sparse float-only page with full-width tables; not evidence of noncompliant one-column appendix prose. No clipping observed. |

## Verification and remaining inputs

- Parsed figures from PDF captions: [1, 2, 3, 4, 5, 6, 7, 8]; matches the eight-figure visual inventory.
- Checked 169 immutable snapshot entries against `snapshot.json`: no mismatches.
- `pdffonts`: 28 font records, all embedded; 5 Type 3 records. Existing font-extraction warnings are not font-embedding findings.
- All issue quotations are programmatically found in the cited source, with computed 1-based line anchors. Fixes are recommendations only; stage/permission remains unknown.
- Required human inputs: target/stage, actual AI use/checklist, submission logistics and supplements. No experiment or manuscript edit was needed for this audit.

**Files:** `presentation.json` (machine-readable source of truth), `presentation.md` (this report), `presentation_physical.json`, `pdffonts.txt`, page/text/figure renders and the two local audit/report scripts.
