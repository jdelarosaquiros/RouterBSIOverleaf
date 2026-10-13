"""Render the approved-scope review artifacts; no manuscript writes."""
from pathlib import Path
import json,subprocess,collections
R=Path(__file__).resolve().parent
J=json.loads((R/'REVIEW_JSON.json').read_text()); F=json.loads((R/'REVISION_REPORT.json').read_text())
V=json.loads((R/'verification.json').read_text()) if (R/'verification.json').exists() else None
counts=collections.Counter(x['severity'] for x in J['issues'])
q=lambda s:'\n'.join('> '+line for line in s.splitlines())
loc=lambda x:f"PDF p. {x['location']['page']}, {x['location']['section']}"+(f"; `{x['location']['tex_file']}` lines {x['location']['line_range']}" if x['location']['tex_file'] else '')
head=f"""# RouterBSI — ACL-style critique

**Scope:** critique of the supplied PDF and approval-only proposed revisions. **No manuscript changes, rebuilds, new benchmark runs, commits, or uploads.**

- Reviewed PDF: `main.pdf`, SHA-256 `{J['provenance']['pdf_sha256']}`.
- Input: {J['provenance']['pages']} total PDF pages; main content ends on page 8.
- Exact venue/cycle/stage: **unknown**. Long research paper is a working assumption; no deadline, extra page, or upload permission inferred.
- Review date: {J['review_date']}. Prior issues were reassessed against this snapshot, not copied as current facts.

## Internal verdict

**Substantial revision; overall 2/5 (internal rubric, not official ARR scoring).** {len(J['issues'])} anchored issues: **{counts['major']} major, {counts['minor']} minor, {counts['blocker']} blockers**. No confirmed mandatory-policy violation was established. Minor items include explicitly optional editorial suggestions; they are not required experiments or submission gates.

{J['headline_verdict']}

| Dimension | Internal score | Basis |
|---|---:|---|
"""
for k in ['soundness','presentation','contribution','overall','confidence']:
 s=J['internal_scores'][k];head+=f"| {k.title()} | {s['score']}/5 | {s['justification']} |\n"
head+='\n## What already holds up\n\n'+'\n'.join('- '+s for s in J['review_form']['strengths'])+'\n'
head+='''
## Highest-priority findings

1. **Ablation initialization (ISSUE-005; p.7/20/23):** the 12 manifest-linked initial-policy files contain three distinct predicate libraries. The first run is shared across all four arms, but Both Enabled runs 2/3 differ from every component-disabled repeat. Confirm historical run binding, then distinguish the shared-initialization first-run evidence from the heterogeneous three-run averages. This does not prove that component benefits disappear.
2. **Operational method (ISSUE-002/003; pp.4–5):** main replay omits the current failed task and its `2N+1` bound; arithmetic score addition differs from the appendix’s selected-first lexicographic ranking. Summarize the actual gate timing/rollback too. Preserve the already-correct average-risk and initial-baseline gate equations.
3. **Protocol and comparator reproduction (ISSUE-004/006; pp.4–5):** per-dataset 70/15/15 does not describe the actual constrained global split; SkillRouter’s run-specific setup and model-role assignments need a concise, artifact-backed account.
4. **Uncertainty (ISSUE-007; pp.5–6):** verified aggregate point estimates are not paired uncertainty estimates. Prefer analysis of saved predictions over new model calls; distinguish task-sampling from training-run uncertainty.
5. **Backbone inference (ISSUE-009; pp.7–8):** remove the universal plateau sentence. Keep the already-correct observed endpoint comparison; no extra sweep is needed if the claim is narrowed.

## Important version finding

The PDF and source are not synchronized. The PDF still prints **“non-decreasing” error**, the stronger **“without degrading … unseen routing decisions”** objective, and a Figure 2 caption omitting tie rejection. The captured TeX has already corrected these passages. ISSUE-001 proposes a later authorized rebuild—not repeating the source edits or changing the correct equations.

## Compliance, separated from quality

- The main text ends on page 8: consistent with the assumed long-paper review budget, not proof of an unknown target/stage’s active limit. The appendix begins after references in the same 29-page PDF.
- A4, two-column format, embedded fonts, review numbering and distinct Limitations before references were inspected. The supplied style matches its bundled official archive; the exact PDF-to-source build binding remains unresolved because of version drift.
- No obvious identity leak was found in visible author fields, PDF metadata or inspected links. This is not a complete anonymity audit of every external supplement or author relationship.
- Ethics and AI-assistance prose are present. Current ARR instructions require writing/coding use and scope in the Responsible NLP Checklist and direct details to Acknowledgements; generic ACLPUB review guidance says to omit the acknowledgment section. Do not treat a non-identifying AI disclosure as a confirmed violation based solely on its heading; verify the active form and specific policy.[1][3]
- Responsible NLP Checklist, actual assistance scope, licenses/consent, author approvals, profiles, service obligations, overlap/preprint declarations, eligibility and portal permissions require human verification. Unknown is neither compliant nor a confirmed violation.

## Self-containment

The thesis and primary results are visible in the main paper. The following compact details should move into, or be summarized accurately in, the main text: current-inclusive replay; bounded replay versus global history; lexicographic ranking; iteration-end gate/rollback; global split counts; no-MBR control semantics; retention normalization; and single-run known-token accounting. Full prompts, detailed tables and the existing error diagnostic can stay supplementary. Replace inaccurate prose rather than expanding beyond the page budget.

## Issue-by-issue critique
'''
for x in J['issues']:
 head+=f"\n### {x['id']} — {x['severity'].upper()}: {x['problem']}\n\n**Location:** {loc(x)}. **Class:** `{x['proposal_class']}`.\n\n{x['readable_anchor'] and q(x['readable_anchor'])}\n\n"
 head+='\n'.join('- '+s for s in x['reasoning_chain'])+'\n'
 head+='\n**Proposed route:** '+x['fix']['instruction']+'\n'
head+='\n## Figure coverage\n\n| Figure | Audit result / proposal | Issues |\n|---|---|---|\n'
for f in J['figure_diagnostics']:
 head+=f"| {f['figure_id']} (p. {f['page']}) | {f['recommendation']} | {', '.join(f['linked_issues'])} |\n"
head+='''
All eight figures were inspected. Figure 1 may remain an applicability example rather than a mandatory method teaser. Visual changes are optional where identified; numeric series and uncertainty must not be invented or replaced. Figure 5’s bands are population SD over recorded runs, not confidence intervals.

## Findings not repeated from the earlier review

- The deleted 94.68%/93.75% interpretation is not a current main-text defect; Appendix H.3 now supplies a matched-loss diagnosis.
- The replay-average inequality and initial-predicate gate are correctly specified. No invented global theorem or redundant blanket caveat is requested.
- JTPRO and SkillRouter are already cited. A forced Bayesian derivation, method rename, human-edit study, or mandatory GEPA/JTPRO run is not justified here.
- Dependency expansion is already presented as a hypothesis; a local budget caveat is optional, not evidence that the paper claims a causal proof.
- Old initialization/cost prose was not reused. The new initialization finding rests on fresh predicate-map comparisons.

## Author decisions needed

'''
head+='\n'.join('- '+s for s in J['open_questions_for_human_author'])+'\n'
head+='\n**Companion files:** [Proposals](PROPOSALS.md), [review JSON](REVIEW_JSON.json), [proposal-only revision report](REVISION_REPORT.json), [verification](verification.json), [WISC report](WISC_REPORT.md).\n'
(R/'REVIEW.md').write_text(head)
# Mechanically render policy source URLs from the established ledger.
S='/workspace/storage/.hermes/skills/research/grounded-citations/scripts/sources.py'
p=subprocess.run(['python',S,'--ledger',str(R/'policy/ledger.json'),'render','--replace-in',str(R/'REVIEW.md')],capture_output=True,text=True)
if p.returncode: raise RuntimeError(p.stdout+p.stderr)
pro='''# RouterBSI — proposed solutions for author approval

**Nothing below has been applied.** This is the `fix_acl_critic` proposal stage, consuming this review’s `REVIEW_JSON.json`. `EXPERIMENTAL_RESULTS=[]` means no newly generated results; existing manuscript and run artifacts were inspected read-only. The paired revision JSON marks every issue `not_executed`, with no post-edit text or claimed successful manuscript fix.

## Recommended approval batches

| Batch | Issue IDs | Action / evidence needed |
|---|---|---|
| A — supported corrections | 001, 002, 003, 004, 008, 009, 011, 012 | Author-approved PDF synchronization, main/appendix alignment, scoped cost/metric wording, removal of ceiling overclaim, targeted copyediting. Confirm intended implementation/source version; no new benchmark run is inherently needed. |
| B — evidence-backed decisions | 005, 006, 007 | Confirm historical initialization bindings; supply run-specific baseline/model roles; inspect saved paired predictions for uncertainty. Do not invent settings, paired seeds or intervals. |
| C — optional refinements | 010, 013 | Local downstream-budget qualification and figure legibility/accessibility changes. No automatic redesign or causal experiment. |

**Recommended order:** resolve ablation provenance and protocol inputs first; prepare supported textual changes; then update captions/figures consistently and rebuild only after approval. No active deadline or measured revision ETA is available, so no completion-before-deadline claim is made.

## Detailed proposals

Each entry gives the current PDF anchor, exact available TeX anchor, replacement/action, missing inputs and acceptance criteria. PDF/source differences are explicit. These are proposals, not an automatically applicable patch.
'''
for x,p in zip(J['issues'],F['proposals']):
 pro+=f"\n### {x['id']} — {x['problem']}\n\n**Location:** {loc(x)}\n\n**Priority / type:** {x['severity']}; {x['proposal_class']}. **Estimated scope:** {x['fix']['estimated_effort']} (not a measured time estimate).\n\n**Current PDF:**\n\n{q(x['readable_anchor'])}\n"
 if x['source_anchor']:
  pro+=f"\n**Captured source anchor** ({'already corrected relative to PDF' if x['id']=='ISSUE-001' else 'exact source text'}):\n\n```tex\n{x['source_anchor']}\n```\n"
 else:pro+='\n**Source mapping:** PDF figure anchor only; confirm the diagram’s editable source before changing it.\n'
 pro+='\n**Proposed replacement/action — not applied:**\n\n'+q(p['proposed_text_or_action'])+'\n'
 pro+='\n**Execution details:** '+x['fix']['instruction']+'\n'
 pro+='\n**Inputs / conditions:** '+('; '.join(x['fix']['required_inputs']) if x['fix']['required_inputs'] else 'Author approval; no new measurements needed for this wording route.')+'\n'
 if x['depends_on']:pro+='\n**Dependencies:** '+', '.join(x['depends_on'])+'.\n'
 pro+='\n**Acceptance after an authorized implementation:**\n\n'+'\n'.join('- [ ] '+c for c in x['fix']['acceptance_criteria'])+'\n'
 if x['id']=='ISSUE-005':
  pro+='''
**Existing evidence / minimal route:** all four first runs share one library. Both Enabled runs 2/3 differ in 26,262/26,261 predicates from that library, while the other nine arm/repeat files reuse it. See `parent_initial_policy_verification.json`. Keep observed values and disclose the actual repetition design. If the named files are not the historical inputs, supply the immutable alternatives before adopting the proposed wording. A matched-initialization study is an optional strengthening, not something performed or approved here.
'''
 if x['id']=='ISSUE-007':
  pro+='\n**Fallback if saved outputs are insufficient:** keep the reported means explicitly descriptive, remove unsupported significance language, and acknowledge absent paired uncertainty. Do not fabricate confidence intervals or silently launch reruns.\n'
pro+='\n## Optional new studies — not required for honest claim narrowing\n'
for e in J['optional_new_experiments']:
 pro+=f"\n### {e['id']} — {e['name']}\n\n- **When useful:** {e['motivation']}\n- **Design:** {e['design']}\n- **Support criterion:** {e['expected_outcome']}\n- **If negative:** {e['risk_if_negative']}\n- **Compute / deadline / permission:** unknown / unknown / unknown. **Status: unrun and unapproved.**\n"
pro+='''
## Figure, writing and narrative upgrade passes

- **Figures:** retain the actual data; define SD bands and accounting scopes correctly; enlarge small labels; provide a non-color identifier for Figure 8. All eight figure-specific specifications are in `REVISION_REPORT.json`. No figure code was executed or rewritten. Caption changes should use each figure’s `description.text` and synchronize the embedded caption after approval.
- **Writing:** make short replacements/deletions instead of broad rewriting. The abstract is 200 words under the reported counting convention. Keep uncertainty and limitations; do not turn editorial sentence-length or 7-pt targets into official policy.
- **Narrative:** preserve the concrete editable-predicate NLP contribution, three delivered contribution themes and the honest distinction between routing leadership and downstream outcomes. No forced novelty inflation or new theorem is proposed.

## What remains unchanged

The PDF, manuscript source, figure assets, results and prompts remain untouched. No compilation was attempted because it would update the paper artifact without approval. No actual manuscript acceptance criterion is marked fulfilled merely because a proposal was written. Submission eligibility, checklist and portal permissions are human-only unresolved checks.

## Approval interface

You can approve individual IDs or batches, for example: “Apply Batch A except ISSUE-003; investigate Batch B without running models; leave optional figures unchanged.” Any implementation must re-check current source/PDF versions first. Approval of prose does not implicitly approve new experiments or uploads.
'''
(R/'PROPOSALS.md').write_text(pro)
verification_text=(f"PASS: {V['protected_file_count']} protected files unchanged; {V['issues_checked']} PDF anchors, {V['source_anchors_checked']} source anchors, all {V['proposal_count']} proposals and {V['figure_count']} figures checked. PDF SHA-256 unchanged." if V and V['status']=='pass' else 'Pending final verification; see verification.json.')
wisc=f'''# WISC execution report — RouterBSI ACL critique and proposal-only fixes

## Task
Review `RouterBSIPaper/main.pdf` using `acl_critic`, then prepare `fix_acl_critic` solutions without changing the paper until author review.

## SELECT
- Actual paper root: `{J['provenance']['paper_root']}`.
- Loaded WISC and both full critic/fixer contracts; read local ACL/appendix guides and agent context.
- Captured an immutable 29-page PDF/source snapshot. Stage, venue/cycle and permissions remain unknown.

## ISOLATE
Three independent scouts examined science/provenance, presentation/compliance, and narrative/self-containment. Parent reconciled them, rechecked headline arithmetic and independently compared every manifest-linked initial policy. Stale prior findings were excluded.

## WRITE
- Plan: `../../plans/acl-critic-proposals-20261013T133137Z.md`.
- Critique: `REVIEW.md`, `REVIEW_JSON.json`.
- Solutions: `PROPOSALS.md`, `REVISION_REPORT.json`.
- Evidence: `parent_initial_policy_verification.json`, numeric checks, policy ledger and three scout reports.

## Implementation boundary
Only review artifacts and the WISC plan were created. Manuscript implementation is intentionally **not authorized**, so build/code-edit/commit tasks are inapplicable. Actual paper edits: 0. New benchmark runs: 0. Uploads: 0.

## Validation
{verification_text}

## COMPRESS
- Current state: critique and proposals ready for author review.
- Commit: not performed; out of scope.
- TaskMaster: unavailable; Hermes todo used instead.
- Handoff: these artifacts preserve source hash, issue IDs, dependencies, exact anchors, conditional inputs and approval boundary.

## Standalone executive summary
The requested two-stage review is complete in proposal-only mode. The current PDF contains a substantive editable-predicate skill-routing contribution and headline numeric improvements that reproduce from saved data. The review contains {len(J['issues'])} anchored issues ({counts['major']} major, {counts['minor']} minor, no blocker), with a solution and acceptance criteria for each. The most important new finding is that the recorded three-run ablation uses different initial libraries across configurations despite its common-initialization claim; historical binding still needs author confirmation. Main/appendix method and split inconsistencies, baseline reproduction, primary-comparison uncertainty and an unsupported backbone ceiling are the remaining major concerns. Several PDF statements are already corrected in the source and require only a future authorized synchronization, not repeated edits. All eight figures and submission-facing checks were audited, with policy uncertainties kept separate from scientific scores. The next action is for the author to approve/reject proposal IDs and supply specified evidence. No paper change or experiment has been executed.
'''
(R/'WISC_REPORT.md').write_text(wisc)
print(json.dumps({'markdown_files':['REVIEW.md','PROPOSALS.md','WISC_REPORT.md'],'issues':len(J['issues']),'verification_included':bool(V)},indent=2))
