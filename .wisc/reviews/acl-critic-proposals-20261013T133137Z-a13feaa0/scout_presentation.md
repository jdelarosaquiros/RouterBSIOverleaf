# RouterBSI — ACL compliance, figures and presentation scout

**Reviewed artifact:** `reviewed_main.pdf`, SHA-256 `a13feaa06ce9697e5d4d44119ea46f4403aff73a8743d3bb51bcc616dd3174e5`. **Scope:** read-only proposals; no manuscript/figure-asset changes or compilation. **Coverage:** all eight figures visually inspected. **Stage/venue/cycle:** unknown; long-paper review budget assumed, not confirmed.

## Outcome

No confirmed mandatory ACL/ARR violation established by this scout. Main content ends on page 8, within the assumed long-review budget; the 29-page total includes references and appendix. Submission readiness remains **unknown** because portal obligations and stage are not available. Presentation is **3/5 on an internal, non-ARR scale**. The two main scientific presentation concerns are incomplete token-accounting claims and the unsupported model-capacity plateau inference.

### Prioritized issues (proposals only)

| ID | Class / severity | Exact location | Proposed change |
|---|---|---|---|
| PRES-001 | optional editorial / minor | PDF p1; Figure 1 | Enlarge/shorten the small Figure 1 internal prose; inspect at actual A4 size. A teaser redesign is optional. |
| PRES-002 | scientific / minor | PDF p3; Figure 2 | Align Figure 2 rejection wording with strict gate admission; source already includes equality but reviewed PDF does not. Label illustrative risk values. |
| PRES-003 | scientific / minor | PDF p6; Figure 3 | Define Ret@k and per-method Recall@50 normalization in the main caption/text; distinguish normalized retention from absolute coverage. |
| PRES-004 | optional editorial / minor | PDF p6; Figure 4 | Increase 6.44 pt category labels / 4.51 pt subscripts; consider a dot plot; repair caption and preserve SkillDAG exception. |
| PRES-005 | scientific / minor | PDF p7; Figure 5 | Replace “standard mean and variation” with three-run mean ± one population SD, not a confidence interval, and specify task-weighted test context. |
| PRES-006 | scientific / major | PDF p7; Figure 6 | Label Figure 6/8 costs as known recorded run-local tokens; disclose incomplete accounting and exclusions. Distinguish Figure 6 single-run values from Figure 5 three-run means. |
| PRES-007 | scientific / major | PDF p7; Figure 7 | Remove “cannot be overcome” capacity-ceiling claim. State nonmonotonic observed endpoints, single-run evidence and historical-candidate confounding. |
| PRES-008 | optional editorial / minor | PDF p1; title metadata | Synchronize DocInfo title with visible title: metadata currently omits “Replay”. No identity leak is shown. |

Each JSON issue contains a verified verbatim PDF anchor, source path/line range, rationale, targeted proposed fix and acceptance criteria. All fix windows remain `unknown`; this audit does not authorize changes or uploads.

## Compliance findings

- **Size/layout:** all pages A4 (595.276 × 841.890 pt); two-column prose, with permitted full-width figures/tables. Figure pages visually checked; not an exhaustive all-page typography audit.
- **Style:** snapshot `acl.sty` is byte-identical to the bundled official ZIP (SHA-256 `19dfeddc2c0e448f3926a0bef048a9db3f3611b46265b760caabd7ada4f361de`). `main.tex` uses 11 pt article and ACL review mode. This establishes bundle equality, not the exact build dependencies of an older PDF.
- **Fonts/numbers:** `pdffonts` reports **all 28 resources embedded**, including Type 3 fonts. Page numbers 1–29 verified. Marginal line numbers present on prose pages 1–28; p29 is full-width tables/captions. Body ≈11 pt and captions ≈10 pt; small graph labels are assessed separately, not against an invented minimum.
- **Anonymity/links:** visible anonymous submission, anonymous DocInfo author, empty XMP, no attachments. Inventory: 317 link annotations / 46 unique external URIs; citations/model documentation, no obvious identifying author repository or tracked Drive/Dropbox URL. Links were inventoried, not resolved or matched to author identities. Separate supplementary archives are unknown.
- **Required sections:** Limitations and Ethical Considerations on p8 precede References. No new experiment/figure is placed in Limitations. Appendix starts on p11 after references in the same PDF; sections A–H, two-column prose.
- **AI acknowledgment:** **not a confirmed anonymity violation.** The current ARR CFP says writing/coding use and scope must be disclosed in the Responsible NLP Checklist and details should be in Acknowledgements. The anonymous p8 statement discloses writing/editing and code generation. Actual scope accuracy and form completion remain for authors. The older generic ACLPUB instruction omitting review acknowledgments should not override this specific current AI-disclosure instruction by itself.
- **Abstract:** 200 whitespace-delimited words, counting hyphenated words as one; at the ACLPUB guidance boundary under this count, not demonstrably overlength.
- **Unknown, not violations:** venue/track/cycle/stage/deadline; PDF-revision permissions; author approval/order; profiles; reciprocal-service duties/caps/exemptions; overlap/dual submission; prior ARR history; preprint declaration; portal metadata; checklist; actual license/consent/approval evidence. Do not import NAACL 2027 deadlines for an unidentified target.

## Every-figure visual audit

Captions below are reproduced from the reviewed PDF. Printed line-break hyphenation is retained; PDF text extraction flattens mathematical subscripts. Figures 1 and 2 are raster images, so exact internal font sizes cannot be inferred from the PDF text layer. The other sizes are measured in the **composed PDF**, not standalone figures.

### Figure 1 — PDF p1

**Render inspected:** `renders/page-1.png`.

**Exact printed-caption extraction:**
```text
Figure 1: Skill routing with a task applicability pred-
icate. The skill is appropriately selected for task q1
because the task asks about the price for a specific trad-
ing day. The skill is not accepted for task q2 because it
asks for the price between a range of years.
```

**Observed:** Column-width raster diagram: two coffee-price tasks flow through Coffee Price Data Single-Day Analysis and its predicate to green Selected/True and red Not Selected/False boxes. The single-day task asks whether May 19, 2021 was bullish or bearish; the multi-year task asks for the highest price between 2019 and 2021. Caption captures the single-day/range distinction. It illustrates applicability, not the proposed replay/gate update.

**Font/placement evidence:** {"exact_font_size": null, "reason": "Raster text, not PDF text spans", "placed_width_pt": 218.2541, "placed_height_pt": 59.178, "source_pixels": [3098, 840]}.

- Internal task/predicate prose is visibly much smaller than the adjacent 10 pt caption at column width; zoom makes it decipherable but does not establish print readability.
- Color is not the sole encoding: Selected/Not Selected and True/False are redundant labels.
- The contribution is not explained here; making Figure 1 a method teaser is optional editorial advice, not ACL policy.

**Proposed change:** Shorten task and predicate labels; allocate more vertical space or redraw as a vector while retaining the same semantics. Optionally add an explicit link to the replay/gate mechanism rather than replacing this explanatory example.
**Linked issues:** PRES-001.

### Figure 2 — PDF p3

**Render inspected:** `renders/page-3.png`.

**Exact printed-caption extraction:**
```text
Figure 2: RouterBSI’s bayes self-improvement algorithm of predicate psk for the skill sk in top k. Routing failures
drive revisions selected which are selected based on their bounded replay error using Minimum Bayes Risk (MBR).
Selected candidate is discarded by the held-out validation gate if its validation error is higher than the initial predicate
psi.
```

**Observed:** Full-width raster flowchart with Skill Routing, Update Proposal, and Update Selection. Markdown-table formatting falsely activates CSV Data Analysis; failure feedback generates three predicates. MBR box lists pf=0.50, m1=0.25, m2=0.00 selected, m3=0.25; gate displays psi=0.60 > m*=0.45 and Passed. Lower loop returns to predicate evaluation. Both Success and Failure paths are present.

**Font/placement evidence:** {"exact_font_size": null, "reason": "Raster text, no extractable font size", "placed_width_pt": 453.5463, "placed_height_pt": 257.0265, "source_pixels": [3568, 2022]}.

- The printed caption omits equality from gate rejection whereas PDF p4 states higher or equal and a strict less-than admission rule.
- Numbers are written as predicates equal to scores instead of explicitly named replay/validation risks, and not identified as illustrative.
- Routing success/failure edge conditions are not explicitly labeled; the shown True decision is not sufficient by itself to establish success.
- Diagram is legible at full width; no clipping observed. Red/green states have text labels.

**Proposed change:** Align the caption with strict admission; label score expressions R_replay and R_v and mark the example illustrative. Optionally label branches correct/incorrect relative to required-skill labels.
**Linked issues:** PRES-002.

### Figure 3 — PDF p6

**Render inspected:** `renders/page-6.png`.

**Exact printed-caption extraction:**
```text
Figure 3: Retention of required skills averaged across
retrievers: BM25, Vector, and SkillSight. The baseline
averages the base retrievers used to retrieve the initial
top 50 skill. RouterBSI preserves the most required
skills as the cutoff k decreases.
```

**Observed:** Six normalized retention curves at equally spaced categorical cutoffs 50,25,10,5,1. RouterBSI stays highest; different colors, markers and line patterns aid identification. Legend above the plotting area, no error bands. All curves begin at 100%.

**Font/placement evidence:** {"tick_and_legend": 8.01, "axis": 9.01}.

- Caption does not define Ret@k as a ratio of task-mean recalls normalized by each method/retriever own Recall@50; this definition is relegated to Appendix F.
- SkillDAG uses an expanded pool: normalized retention does not mean a controlled common-candidate comparison or absolute recovery of the full gold set.
- Legend/axes are readable at the reviewed render; no clipping observed.

**Proposed change:** Add the normalization and equal-across-retrievers aggregation in the caption or immediate main text; explicitly distinguish absolute recall and method-specific pool coverage. Keep categorical cutoffs labeled.
**Linked issues:** PRES-003.

### Figure 4 — PDF p6

**Render inspected:** `renders/page-6.png`.

**Exact printed-caption extraction:**
```text
Figure 4: Downstream success rates averaged equally across BM25, Vector, and SkillSight. Lines mark LLM Direct
and Oracle. RouterBSItop-5 outperforms strict selection and most other approaches oracle performance.
```

**Observed:** Full-width seven-bar downstream success plot with values 0.580,0.562,0.602,0.631,0.551,0.596,0.611. Dashed Direct=0.507 and dash-dot Oracle=0.638 lines; success-rate axis starts at 0.4. SkillDAG is the highest bar. All bars use the same blue; method identity uses text.

**Font/placement evidence:** {"category_and_value": 6.44, "category_subscript": 4.51, "tick_and_axis": 7.46, "reference_legend": 6.78}.

- Despite full width, rotated category labels and especially strict/top-5 subscripts are small relative to surrounding body/caption. No clipping seen.
- Truncated bar baseline visually amplifies differences; precise labels make the scale recoverable. A dot plot or zero-based bars would be clearer, but is an editorial recommendation, not a policy violation.
- Caption ends with the malformed phrase most other approaches oracle performance. It should explicitly preserve the SkillDAG exception and not suggest exceeding oracle.
- No uncertainty displayed; do not infer statistical significance from these bars.

**Proposed change:** Use a larger-font dot plot or larger-font zero-based bars, spell out strict/top-5 labels, and repair the caption with the displayed means and SkillDAG/oracle comparison.
**Linked issues:** PRES-004.

### Figure 5 — PDF p7

**Render inspected:** `renders/page-7.png`.

**Exact printed-caption extraction:**
```text
Figure 5: Ablation of MBR replay and held-out vali-
dation gate comparing routing performance. The lines
and areas represent the standard mean and variation,
respectively across three runs starting from the same
initial predicates at iteration 0. Combining replay and
gating yields the strongest final routing performance.
```

**Observed:** Four test nDCG@1 trajectories over iterations 0–10 with narrow shaded bands. Both Enabled finishes highest, Only MBR next, Only Gate next, Both Disabled lowest. Color, marker and line-style differences provide redundant distinctions. No clipping.

**Font/placement evidence:** {"tick_and_legend": 8.01, "axis": 9.01}.

- Caption calls lines/areas standard mean and variation, not an identifiable uncertainty statistic. Source provenance and Appendix Table 11 establish mean ± one population standard deviation across three runs (not a CI).
- Caption does not identify Qwen3.5 4B, SkillSight, test split or task weighting.
- Same initial predicates does not establish identical initial measured outcomes or independently seeded runs; appendix reports differing initial scores and one recorded seed. No unsupported accusation of unequal predicate initialization is made.

**Proposed change:** State test nDCG@1, backbone/retriever, 748-task within-run weighting, three-run mean and ±1 population SD using rounded source variance. Do not call bands confidence intervals or runs different seeds.
**Linked issues:** PRES-005.

### Figure 6 — PDF p7

**Render inspected:** `renders/page-7.png`.

**Exact printed-caption extraction:**
```text
Figure 6: Impact of MBR replay and held-out valida-
tion gate on routing performance (nDCG@1) and token
usage. Both enabled gives the strongest performance.
MBR alone uses fewer tokens at a performance cost.
```

**Observed:** Four-point performance/token scatter with distinct diamond, triangle, circle and square symbols. Both Enabled is top-right, Only MBR next in quality and cost; Both Disabled and Only Gate lower-left. No error bars; visibly legible 8/9 pt labels.

**Font/placement evidence:** {"tick_and_legend": 8.01, "axis": 9.01}.

- Horizontal axis says Total Token Usage although provenance explicitly records known-only incomplete run-local costs excluding external/shared initialization.
- Main caption does not explain this is a single-run comparison, unlike the three-run Figure 5; main text juxtaposes the two without the population distinction. Appendix Table 12 provides single-run status and unknown-attempt counts.
- No uncertainty or complete economic-cost claim is established.

**Proposed change:** Rename axis Known recorded tokens (millions), state phase scope/exclusions and unknown usage, and label single-run endpoint evidence in main caption or prose.
**Linked issues:** PRES-006.

### Figure 7 — PDF p8

**Render inspected:** `renders/page-8.png`.

**Exact printed-caption extraction:**
```text
Figure 7:
Initial and optimized routing perfor-
mance (nDCG@1) comparison between different LLM-
backbones using SkillSight as the retriever. Stronger
backbones improve initialization, while optimization
brings smaller model Qwen3.5 4B close to the opti-
mized performance of GPT-OSS 120B.
```

**Observed:** Grouped initial/optimized bars for Qwen3.5 4B (0.520/0.742), Qwen3.8 27B (0.635/0.802), GPT-OSS 120B (0.686/0.745), plus shared gray SkillSight reference 0.471. Initial bars hatched, final bars solid; zero-based axis; value labels readable. No error bars.

**Font/placement evidence:** {"tick_category_and_value": 8.01, "axis_and_legend": 9.01, "init_subscript": 6.31}.

- No uncertainty estimated; provenance says historical candidates are preserved, not a controlled common-candidate comparison.
- The surrounding claim of a plateau that cannot be overcome by more capable LLMs exceeds what three uncontrolled model endpoints establish. Nonmonotonic optimized scores alone do not prove an inherent capacity ceiling.
- Gray SkillSight reference visually resembles the generic solid optimized legend key; its separate x-axis label prevents a severe ambiguity but a baseline note would help.

**Proposed change:** Add single-run/existing-candidate qualification and reference-bar meaning. Replace the capacity-ceiling assertion with the observed nonmonotonicity and need for controlled comparison.
**Linked issues:** PRES-007.

### Figure 8 — PDF p23

**Render inspected:** `renders/page-23.png`.

**Exact printed-caption extraction:**
```text
Figure 8: Recorded tokens and routing performance at different candidate-pool sizes. Blue shades distinguish Top-K
settings, which specify how many retrieved candidates are evaluated rather than how many skills are ultimately
selected.
```

**Observed:** Full-width Appendix scatter: three candidate pool sizes (Top-K 10,25,50) shown by light-to-dark blue circles; larger pools have higher recorded tokens and final nDCG@10. Caption correctly distinguishes number of evaluated candidates from final selected skills. No clipping; comfortably larger labels than most main figures.

**Font/placement evidence:** {"tick_and_legend_title": 9.17, "axis": 10.09, "legend_entries": 8.26, "plot_title": 11.01}.

- Same-color-family circles rely on shade to map Top-K identity; direct labels or distinct shapes would strengthen accessibility.
- Axis Total Token Usage is stronger than caption Recorded tokens; provenance says incomplete known-only run-local totals excluding shared/external initialization.
- No uncertainty displayed; three observed pool sizes do not establish a general scaling law.

**Proposed change:** Use known-recorded-token wording consistently, state single-run scope if confirmed by the associated result table, and directly label the three points or use three marker shapes.
**Linked issues:** PRES-006.

## Writing and main-text self-containment

- Gate tie policy, retention denominator, uncertainty statistic and incomplete-cost scope should be understandable without reading the appendix. These are scientific reporting issues, not automatic desk-rejection findings.
- Figure 1 is an applicability example rather than a novelty teaser; changing it into a teaser is optional. Figure 2 already communicates the replay/gate mechanism.
- Visible grammar targets: p4 “Compare difference … identify the any”; “must not exceeds”; p6 “SkilDAG”; p7 “This suggest”, “overcomed”, and the missing final period. Repair prose without inventing new measurements.
- No assumption of additional content space: replace ambiguous wording and captions within the existing eight-page body.
- Important freshness limit: the snapshot Figure 2 source caption already says “higher or equal”, while the immutable PDF says “higher”. No compilation was run and no claim is made that a current source change is visible in the reviewed artifact.

## Verification / files

Created `scout_presentation.json` (source of truth) and `scout_presentation.md`. Added only the needed review renders `renders/page-3.png` and `renders/page-23.png`. All eight PDF figure IDs have visual diagnostics and exact caption blocks; all eight issue anchors were checked against PDF text (review line-number tokens removed only where needed). No manuscript or figure assets modified.

## Policy sources

Consulted the supplied `.temp/acl_requirements/` guides and the parent-fetched current official copies, recorded in `policy/ledger.json` (accessed 2026-10-13):
1. [ARR CFP](https://aclrollingreview.org/cfp) — AI disclosure, limitations and author/submission obligations (`policy/source-1.txt`).
2. [ARR author guidelines](https://aclrollingreview.org/authors) — workflow and revision/metadata distinction (`policy/source-2.txt`).
3. [ACLPUB formatting](https://acl-org.github.io/ACLPUB/formatting.html) — A4, embedding, two-column layout, figure legibility, captions and abstract guidance (`policy/source-3.txt`).

The `web_extract` backend was unavailable; the parent retrieved the official pages through requests. No policy was inferred from a failed fetch.
