"""Render final current-version review; paper and results are read-only."""
from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parent
load=lambda n:json.loads((R/n).read_text())
J=load('REVIEW_JSON.json');F=load('REVISION_REPORT.json');V=load('verification.json');D=load('concurrent_changes.json')
C=J['severity_counts'];quote=lambda s:'\n'.join('> '+l for l in s.splitlines())
def location(x):
 a=x['location'];return f"Current PDF p. {a['page']}, {a['section']}"+(f"; `{a['tex_file']}` lines {a['line_range']}" if a['tex_file'] else '')
version=f'''## Version and authorization boundary

This review began with the 29-page PDF `{D['initial_pdf_sha256']}`. During review, the paper changed outside this review-only action set: {len(D['changed_preexisting_files'])} existing files changed and two appendix source files were added. No actor is inferred and no changes were reverted. The final critique was reconciled against the **30-page PDF `{D['current_pdf_sha256']}`**, preserved in `current_snapshot/main.pdf`. Main content still ends on page 8.

**ISSUE-001 was resolved by that concurrent revision**, not by this review: non-increasing replay wording, the narrowed objective and Figure 2 tie rejection are now in the PDF. New software/evaluator/statistical/data-reuse paragraphs are credited; ISSUE-006 is narrowed and downgraded, and ISSUE-007 acknowledges the new uncertainty disclosure. Stable issue IDs are retained, so the active list begins at ISSUE-002.

This work created only review artifacts and a WISC plan. **No manuscript edits, compilation, new model runs, commits or uploads were performed by this review.** Current primary issue anchors were rechecked literally against the new PDF and source. Auxiliary appendix page references inherited from the initial scouts refer to the preserved initial snapshot; section/table identifiers remain stable. The final review’s primary location fields and figure page numbers refer to the new PDF.
'''
text=f'''# RouterBSI — ACL-style critique

**Internal verdict: substantial revision, overall 2/5.** This is an internal rubric, not an official ARR score or acceptance prediction.

**{len(J['issues'])} active anchored findings: {C['major']} major, {C['minor']} minor; no confirmed mandatory-policy blocker.** One additional finding was resolved during concurrent revision. Every active issue has a proposal in [PROPOSALS.md](PROPOSALS.md).

{J['headline_verdict']}

{version}
## Scorecard

| Dimension | Internal score | Justification |
|---|---:|---|
'''
for k in ['soundness','presentation','contribution','overall','confidence']:
 s=J['internal_scores'][k];text+=f"| {k.title()} | {s['score']}/5 | {s['justification']} |\n"
text+='\n## Supported strengths\n\n'+'\n'.join('- '+s for s in J['review_form']['strengths'])+'\n'
text+='''
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
'''
for x in J['issues']:
 text+=f"\n### {x['id']} — {x['severity'].upper()}: {x['problem']}\n\n**Location:** {location(x)}. **Class:** `{x['proposal_class']}`.\n\n{quote(x['readable_anchor'])}\n\n"
 text+='\n'.join('- '+s for s in x['reasoning_chain'])+'\n\n**Proposed route:** '+x['fix']['instruction']+'\n'
text+='\n## All-figure audit\n\n| Figure | Current page | Finding / proposal |\n|---|---:|---|\n'
for f in J['figure_diagnostics']:text+=f"| {f['figure_id']} | {f['page']} | {f['recommendation']} |\n"
text+='''
Figure 1 need not become a mandatory method teaser. Small labels and Figure 8 shade-only identification are optional design improvements, not invented official font-size violations. Preserve measured data; Figure 5 bands are population SD, not confidence intervals. All eight graphical assets were reviewed, and their unchanged files were checked while current page locations were remapped.

## Prior criticisms not repeated

- The old 94.68%/93.75% interpretation is not a current main-text defect; the appendix now includes a substantive matched-loss diagnosis.
- Replay-average and initial-predicate-gate equations are already correct. No new theorem, posterior derivation or blanket guarantee disclaimer is requested.
- JTPRO and SkillRouter are already cited. No mandatory GEPA/JTPRO run or human-edit study is established here.
- Dependency expansion is already hypothetical, with budgets disclosed in setup. A local budget caveat is optional.
- The strongest new ablation concern is based on fresh predicate-map checks, not recycled obsolete prose or metric differences alone.

## Decisions needed

'''
text+='\n'.join('- '+s for s in J['open_questions_for_human_author'])+'\n'
text+='\n**Artifacts:** [Proposed solutions](PROPOSALS.md), [review JSON](REVIEW_JSON.json), [proposal-only revision report](REVISION_REPORT.json), [verification](verification.json), [concurrent-change record](concurrent_changes.json), [WISC report](WISC_REPORT.md).\n'
(R/'REVIEW.md').write_text(text)
S='/workspace/storage/.hermes/skills/research/grounded-citations/scripts/sources.py'
subprocess.run(['python',S,'--ledger',str(R/'policy/ledger.json'),'render','--replace-in',str(R/'REVIEW.md')],check=True,capture_output=True,text=True)
pro='''# RouterBSI — proposed solutions for approval

**No proposal has been applied.** This `fix_acl_critic` stage consumed the current `REVIEW_JSON.json` and produced a solution and acceptance criteria for each active issue. No new experimental results were generated. The revision JSON marks every manuscript action `not_executed` and leaves all post-edit text null.

## Recommended decision batches

| Batch | Issues | Scope |
|---|---|---|
| A — supported manuscript corrections | 002, 003, 004, 008, 009, 011, 012 | Main/appendix alignment, concise accounting/metric explanations, deletion of the unsupported ceiling, targeted copyediting. Confirm intended implementation; no benchmark rerun inherently needed. |
| B — evidence-dependent choices | 005, 006, 007 | Confirm historical initialization binding; finish model-role alignment; decide whether saved predictions support paired uncertainty. Never invent settings or intervals. |
| C — optional refinements | 010, 013 | Local downstream-budget caveat; selected figure legibility/accessibility improvements. |
| Resolved outside this review | 001 | No additional synchronization fix requested for the corrected PDF passages. |

No deadline or measured ETA is available. Approving wording does not implicitly approve experiments, rebuilds or uploads.

'''+version+'\n## Issue-by-issue proposals\n'
for x,p in zip(J['issues'],F['proposals']):
 pro+=f"\n### {x['id']} — {x['problem']}\n\n**Location:** {location(x)}\n\n**Severity / type:** {x['severity']}; {x['proposal_class']}. **Estimated scope:** {x['fix']['estimated_effort']} (not a time estimate).\n\n**Current PDF anchor:**\n\n{quote(x['readable_anchor'])}\n"
 if x['source_anchor']:pro+=f"\n**Exact current TeX anchor:**\n\n```tex\n{x['source_anchor']}\n```\n"
 else:pro+='\n**Editable source:** confirm the diagram source mapping before applying any optional redesign.\n'
 pro+='\n**Proposed replacement/action — not applied:**\n\n'+quote(p['proposed_text_or_action'])+'\n\n**Execution details:** '+x['fix']['instruction']+'\n'
 pro+='\n**Required inputs:** '+('; '.join(x['fix']['required_inputs']) or 'Author approval; no new measurements required for this wording route.')+'\n'
 if x['depends_on']:pro+='\n**Dependencies:** '+', '.join(x['depends_on'])+'.\n'
 pro+='\n**Acceptance after authorized implementation:**\n\n'+'\n'.join('- [ ] '+a for a in x['fix']['acceptance_criteria'])+'\n'
 if x['id']=='ISSUE-005':pro+='\n**Evidence route:** all first runs share initialization. Both Enabled runs 2/3 differ from that library on 26,262/26,261 predicates. The other nine arm/repeat files reuse it. Verify historical binding using `parent_initial_policy_verification.json`. Preserve results as descriptive if matched reruns are not approved; do not silently label unmatched means as paired.\n'
 if x['id']=='ISSUE-007':pro+='\n**No-new-run fallback:** preserve the new statistical disclosure; retain explicitly descriptive point estimates; remove unsupported significance language. Missing paired precision remains a limitation, not a fabricated interval or a reason to silently start inference.\n'
pro+='\n## Optional studies — unrun and unapproved\n'
for e in J['optional_new_experiments']:
 pro+=f"\n### {e['id']} — {e['name']}\n\n- **Purpose:** {e['motivation']}\n- **Design:** {e['design']}\n- **Hypothetical support criterion:** {e['expected_outcome']}\n- **If negative:** {e['risk_if_negative']}\n- **Compute, deadline feasibility and stage permission:** unknown.\n"
pro+='''
## Targeted upgrade passes

- **Figures:** all eight audited; per-figure specifications and conditional caption drafts are in `REVISION_REPORT.json`. No figures were regenerated. Approved caption updates should use `description.text` and synchronize embedded captions. Preserve RouterBSI variant subscripts and verified numeric series.
- **Writing:** short replacements/deletions, not broad stylistic rewriting. Abstract counted as 200 words under the reported convention. Preserve limitations and uncertainty; editorial length/font targets are not official rules.
- **Narrative:** retain the editable-predicate NLP contribution, three delivered themes and distinction between routing results and downstream outcomes. No invented theorem or stronger novelty claim.

## Verification and approval boundary

All current primary PDF/source anchors, 12 proposal mappings, dependencies and eight-figure coverage passed checks. Current paper bytes were stable after the updated snapshot; earlier concurrent changes are explicitly recorded. This review itself made no paper edits. Source/PDF compilation is not claimed. Manuscript acceptance criteria are intentionally unchecked because proposals are not implemented fixes.

To authorize later work, name individual IDs or batches—for example, “Apply Batch A; inspect Batch B evidence without running models; leave optional figures unchanged.” Recheck the current source/PDF version before any implementation. No commit or upload is implied.
'''
(R/'PROPOSALS.md').write_text(pro)
wisc=f'''# WISC execution report

## Task
Critique the RouterBSI paper using `acl_critic` and propose `fix_acl_critic` solutions without modifying the manuscript pending author review.

## SELECT
Actual root: `{J['provenance']['paper_root']}`. Loaded both full skill contracts, WISC, local ACL/appendix guides and agent context. Venue/cycle/stage unknown. Captured the original snapshot and later captured/reconciled a concurrently updated 30-page PDF.

## ISOLATE
Three independent scouts covered science/provenance, presentation/compliance, and narrative/self-containment. Parent rechecked reported arithmetic, every initial policy in the 12-run ablation manifest, updated PDF anchors and concurrent source additions.

## WRITE
Plan: `../../plans/acl-critic-proposals-20261013T133137Z.md`.
Deliverables: `REVIEW.md`, `REVIEW_JSON.json`, `PROPOSALS.md`, `REVISION_REPORT.json`, `verification.json`, `concurrent_changes.json`.

## Implementation / verification
- Review-authored manuscript edits/builds/new model runs/commits/uploads: **0**.
- Current PDF: **30 pages**, main content ends on **8**, SHA-256 `{D['current_pdf_sha256']}`.
- **{V['issues_checked']}** literal current PDF issue anchors; **{V['source_anchors_checked']}** current source anchors; **{V['proposal_count']}** mapped proposals; **{V['figure_count']}** figures.
- Strict JSON contracts and dependency coverage passed.
- **{V['current_snapshot_protected_count']}** current protected files remained unchanged after the reconciled snapshot.
- Earlier **{len(D['changed_preexisting_files'])}** preexisting files changed and **2** sources were added outside this review-only action set. Do not claim the manuscript stayed unchanged for the whole session. No changes were reverted and no actor inferred.

## COMPRESS / handoff
No commit: proposal-only scope. TaskMaster unavailable; Hermes todo used. Implementation is intentionally not authorized. The reports preserve stable IDs, conditional inputs, exact anchors and acceptance criteria for later approval.

## Standalone executive summary
The requested critique and proposed solutions are complete. There are **{len(J['issues'])} active findings ({C['major']} major, {C['minor']} minor)** and one resolved finding from concurrent revision. The strongest concern is heterogeneous initialization in a three-run ablation described as common-initialization. Other major concerns are operational replay/ranking and split inconsistencies, absent paired uncertainty, and a backbone-capacity overclaim. Headline aggregate arithmetic reproduces, and new software/evaluator/statistical/data-reuse documentation is credited. All eight figures were audited. No paper edits were made by this review; concurrent paper changes were detected and reconciled transparently. Next step: the author approves/rejects proposal IDs and supplies the specified evidence. New experiments and uploads remain unapproved.
'''
(R/'WISC_REPORT.md').write_text(wisc)
print(json.dumps({'files':['REVIEW.md','PROPOSALS.md','WISC_REPORT.md'],'active_issues':len(J['issues']),'severity_counts':C,'status':V['status']},indent=2))
