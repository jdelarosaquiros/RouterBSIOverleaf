"""Render and verify the version-bound fresh ACL/ARR review (no paper edits)."""
from pathlib import Path
import hashlib
import json
import re
import fitz

R = Path(__file__).resolve().parent
root = R.parents[2]
r = json.loads((R / 'REVIEW_JSON.json').read_text())
source = R / r['reviewed_artifact']['source_snapshot']
manifest = json.loads((R / 'current_snapshot.json').read_text())
required = ['paper_id', 'venue_context', 'revision_mode', 'acl_arr_compliance',
            'review_form', 'internal_scores', 'issues', 'self_containment_audit',
            'figure_diagnostics', 'writing_diagnostics', 'narrative_diagnostics',
            'missing_citations', 'required_new_experiments', 'section_by_section_comments',
            'adversarial_pass_findings', 'author_response_prep',
            'open_questions_for_human_author', 'execution_order', 'pre_submission_action_plan']
assert all(k in r for k in required)
ids = {x['id'] for x in r['issues']}
assert len(ids) == len(r['issues'])
assert set(r['execution_order']) == ids
counts = {s: sum(x['severity'] == s for x in r['issues']) for s in ['blocker', 'major', 'minor']}
assert counts == r['severity_counts']
anchors = []
for x in r['issues']:
    assert x['fix_window'] == 'unknown'
    assert x['fix']['instruction'] and x['fix']['acceptance_criteria']
    assert set(x['depends_on']) <= ids
    anchors.extend([x['location']] + x.get('supporting_evidence', []) + x.get('additional_anchors', []))
for f in r['figure_diagnostics']:
    anchors.append(f['location'])
    assert set(f['linked_issues']) <= ids
assert len(r['figure_diagnostics']) == 8
for a in anchors:
    text = (source / a['tex_file']).read_text()
    assert a['quoted_text'] in text, a
    pos = text.index(a['quoted_text'])
    actual = [text[:pos].count('\n') + 1, text[:pos + len(a['quoted_text'])].count('\n') + 1]
    assert a['line_range'] == actual, (a, actual)
for c in r['narrative_diagnostics']['contribution_ladder']:
    assert c['claimed_contribution'] in (source / 'sections/introduction.tex').read_text()
for k in ['soundness', 'presentation', 'contribution', 'overall', 'confidence']:
    assert isinstance(r['internal_scores'][k]['score'], int)
    assert 1 <= r['internal_scores'][k]['score'] <= 5
    assert r['internal_scores'][k]['justification']
assert r['internal_scores']['rubric'] == 'internal_1_to_5_not_official_arr'
assert not r['internal_scores']['official_arr_scales_verified']
changed = [p for p, h in manifest.items() if not (root / p).is_file()
           or hashlib.sha256((root / p).read_bytes()).hexdigest() != h]
assert not changed, ('Concurrent changes since reconciliation', changed)
assert all(hashlib.sha256((source / p).read_bytes()).hexdigest() == h for p, h in manifest.items())
pdf = fitz.open(source / 'main.pdf')
assert len(pdf) == r['reviewed_artifact']['total_pages'] == 31
assert hashlib.sha256((source / 'main.pdf').read_bytes()).hexdigest() == r['reviewed_artifact']['sha256']

lines = [
    '# Fresh ACL/ARR critique — RouterBSI', '',
    '**Internal overall: 3/5 — borderline, up from 2/5.** Internal editorial recommendation: borderline reject. These are not official ARR ratings or a prediction of acceptance.', '',
    r['headline_verdict'], '',
    '| Dimension | Score / 5 |', '|---|---:|',
]
for k in ['soundness', 'presentation', 'contribution', 'overall', 'confidence']:
    lines.append(f"| {k.title()} | {r['internal_scores'][k]['score']} |")
lines += ['', f"**Active findings: {len(r['issues'])}: {counts['major']} major, {counts['minor']} minor, {counts['blocker']} confirmed blockers.**", '',
          '## What improved', '',
          '- Current-inclusive replay, deduplication, and the scoring bound are explicit.',
          '- Normalized retrieval scores and selected-first tie handling are consistent.',
          '- Global split targets, per-skill coverage, and the adaptation rationale are explicit.',
          '- Retrievers and SkillRouter are explicitly frozen on the task-training split.',
          '- The concurrent Table 1 caption now makes averaging and benchmark exceptions clearer.', '',
          'These corrections are credited, not re-reported as unresolved contradictions. The remaining baseline issue concerns Skill-Pro/SkillDAG configuration, not whether SkillRouter was fine-tuned.', '',
          '## Remaining major concerns', '']
for x in r['issues']:
    if x['severity'] != 'major':
        continue
    a = x['location']
    lines += [f"### {x['id']} — {x['problem']}", '',
              f"**Location:** {a['section']}, p. {a['page']}; `{a['tex_file']}:{a['line_range'][0]}`.", '',
              f"> {a['quoted_text']}", '',
              *x['reasoning_chain'], '',
              '**Action:** ' + x['fix']['instruction'], '']
lines += ['## Minor concerns', '', '| ID | Concern | Location |', '|---|---|---|']
for x in r['issues']:
    if x['severity'] == 'minor':
        lines.append(f"| {x['id']} | {x['problem']} | {x['location']['section']}, p. {x['location']['page']} |")
lines += ['', 'Exact quotes, executable fixes, counterevidence where applicable, and acceptance criteria are in `REVIEW_JSON.json`.', '',
          '## Strengths and contribution', '', *['- ' + s for s in r['review_form']['strengths']], '',
          '## Self-containment and evidence scope', '',
          'The core algorithm and setup are now understandable from the main paper. Add compact main-text statistical-scope, cost-scope and metric-definition statements rather than moving the whole appendix. Frozen off-the-shelf baselines are legitimate; the review does not require fine-tuning SkillRouter. No human study is required to establish that predicate text is inspectable. Faithful execution is a separate property, and the main Limitations already acknowledges checker error.', '',
          'The historical initialization-binding question remains open. Figure 5 and Appendix G.1 agree textually; this review does not count an unverified historical binding allegation as a demonstrated manuscript contradiction. This is not a finding that the archived initialization issue has been settled.', '',
          '## Submission and formatting checks', '',
          '- **31 total pages; main content extends through page 8**, including Figures 5–7. This fits the assumed long-paper review budget. Actual venue/cycle/stage remain unconfirmed.',
          '- A4, two-column prose, ACL review mode, page/line numbering and embedded fonts checked. All eight figures inspected; no new clipping or overlap in the revised Table 1 caption.',
          '- Limitations and ethics precede references; appendix follows references in the same PDF.',
          '- Current ARR instructions permit an acknowledgment containing only generative-AI disclosure. Actual AI-use scope and submission-checklist entries require author confirmation.',
          '- Official style-file byte provenance, supplementary anonymity and submission-portal logistics remain unverified. These unknowns are not asserted policy violations.', '',
          '## Suggested priority', '',
          '1. Recover and document actual Skill-Pro/SkillDAG settings; do not invent defaults.',
          '2. State single-run scope in main results. Use saved paired predictions for uncertainty if available; otherwise keep descriptive claims and acknowledge the limitation.',
          '3. Replace the intrinsic-ceiling inference with the observed non-monotonic backbone result.',
          '4. Apply approved minor metric/caption/copyediting changes and recheck the eight-page content budget.', '',
          'Most prose corrections are small; baseline-record recovery and saved-output uncertainty analysis have unknown effort. No new model experiment is prescribed unconditionally. There is no verified deadline from which to infer whether a later cycle is necessary.', '',
          '## Version and verification', '',
          f"- Reviewed current PDF SHA-256: `{r['reviewed_artifact']['sha256']}`.",
          '- Earlier snapshot retained under `source/`; current reviewed snapshot under `current_snapshot/`.',
          '- A concurrent Table 1 caption/PDF update was detected and reconciled. It did not change results or the assessment.',
          '- Review-authored manuscript edits: none. Training/evaluation runs: none. Saved Table 1 data were reaggregated, not rerun.',
          '- Independent audits: `science.json`, `presentation.json`, `narrative.json`; final judgment is the reconciled parent review.',
          '- Supporting checks: `verification.json`, `numeric_spotchecks.json`, `concurrent_changes.json`, `policy/`.', '']
(R / 'REVIEW.md').write_text('\n'.join(lines))
verification = {
    'status': 'pass_with_documented_concurrent_caption_update',
    'json_parse': True, 'issue_count': len(r['issues']), 'severity_counts': counts,
    'verified_source_anchors': len(anchors), 'contribution_quotes_verified': 3,
    'figures_reviewed': len(r['figure_diagnostics']), 'pdf_pages': len(pdf),
    'main_content_pages': 8, 'protected_files_after_reconciliation': len(manifest),
    'changed_after_reconciliation': changed, 'review_authored_manuscript_edits': False,
    'pdf_sha256': r['reviewed_artifact']['sha256'],
    'review_json_sha256': hashlib.sha256((R / 'REVIEW_JSON.json').read_bytes()).hexdigest(),
    'review_md_sha256': hashlib.sha256((R / 'REVIEW.md').read_bytes()).hexdigest(),
    'new_experiments': False,
}
(R / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
print(json.dumps(verification, indent=2))
