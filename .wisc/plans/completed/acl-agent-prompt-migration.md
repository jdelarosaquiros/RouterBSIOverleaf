# Task: ACL/ARR agent prompt migration

## What
Update the two Markdown prompts in `.temp/agents/` from ICLR 2027 to ACL/ARR research-paper review and revision, grounded in the user-provided `.temp/acl_requirements/` sources. Do not edit manuscript, data, figures, results, or the requirement sources.

## Why
The critic and fixer currently encode ICLR-specific deadlines, page allowances, single-column typography, public-discussion assumptions, score scales, and JSON fields. Simple venue substitution would preserve incorrect policy.

## Sources and scope
- `.temp/acl_requirements/requirements_and_examples.md`: main requirements, template, page limits, submission-form duties, and dated NAACL 2027 schedule.
- `.temp/acl_requirements/appendix_requirements.md`: appendix placement, formatting, anonymity, self-containment, and Limitations.
- `.temp/acl_requirements/appendix_outline.md`: optional RouterBSI-specific evidence/reproducibility suggestions; not mandatory sections or evidence that an experiment ran.
- The folder is ACL/ARR guidance with **NAACL 2027** venue-specific context. Do not claim these are ACL 2027-specific deadlines or a verified official ARR scoring form.
- `.temp/` is git-ignored. The nested paper working tree contains unrelated edits; do not stage, change, or commit those. TaskMaster tools are unavailable; Hermes todo records workflow status.

## Files to change
- `.temp/agents/01-iclr2027_critics_agent 3.md`: critic role, venue context, compliance, review rubric, timing, JSON contract, and final checks.
- `.temp/agents/02-iclr2027_fix-critics_agent 3.md`: matching fixer contract, revision modes, compliance, typography, page budgeting, and final checks.
- Preserve existing filenames unless independent reference audit justifies renaming; prioritize not breaking callers. Filenames may be legacy labels, not policy.

## Key decisions
- ACL/ARR long paper is an explicit working default (8 content pages); support short papers (4). Final 9/5 allowance applies only after acceptance and confirmed venue instructions, never automatically during author response.
- Require official ACL review template: `\documentclass[11pt]{article}`, `\usepackage[review]{acl}`, A4, two columns, line/page numbers, embedded fonts; unchanged official style. Appendix after references in the same PDF, normally two-column, only documented math-heavy exception.
- Require distinct Limitations before references, with no new results hidden there. References, Limitations, and ethical-considerations exclusions follow supplied sources. Checklist is in submission form, not replaced by paper prose; AI assistance disclosure follows actual ACL/ARR policy, without inventing a universal standalone mandatory AI section.
- Explicitly verify venue/year/track/cycle/stage; preserve NAACL 2027 schedule only as dated reference if included. Never guess active deadlines, portal permissions, author quotas, or review duties.
- Do not infer revision/PDF-upload permission or public visibility from the presence of reviews. Separate pre-submission, author response, resubmission, and accepted camera-ready; no automatic page increase or evidence deferral.
- Preserve machine-parseable issue IDs, exact anchors, evidence-based fixes, dependency order, acceptance criteria, no fabricated results/citations, self-containment, figure/writing/narrative diagnostics, logs, optional DOCX, and pre-execution confirmation.
- Keep policy compliance separate from internal scientific scores and editorial preferences. Supplied sources do not establish an official ARR score scale: use an explicitly internal rubric or unknown/unverified official scales.
- Missing sections and portal obligations must be representable as compliance gaps or insertion fixes with a real adjacent anchor; no invented quote or silent omission.
- Keep illustrative JSON contract notation explicitly labeled; actual generated JSON must parse and contain concrete values, not alternatives/comments/placeholders.

## Validation
- Read both full originals before editing and save exact backups plus baseline hashes of protected manuscript/requirements files.
- Scan both updated contents for residual ICLR venue/policy, Sept/Nov deadlines, public-review permanency assumptions, 9/10-page review rules, tenth-page plans, old compliance/score keys, and inferred discussion modes.
- Verify both prompts agree on compliance field names, modes, fix-window vocabulary, and score semantics; preserve pipeline fields and no-fabrication guards.
- Verify all local source references exist and requirements coverage matches the local guides.
- Inspect actual before/after diff, including ignored files (ordinary git diff will omit them).
- Verify only the two prompt files plus scoped WISC records changed, using before/after hashes for protected files. Do not compile or edit the manuscript for this prompt-only task.
- Archive this spec under `.wisc/plans/completed/` after verified completion, with concise results/validation evidence. Because `.temp/` is ignored and the user requested prompt edits rather than repository tracking changes, leave prompts uncommitted rather than force-add private temporary files.

## Completion
Status: complete. Both existing prompt filenames are preserved; their contents now target ACL/ARR using the supplied sources. Manuscript and requirement sources were not edited.

- Full manual review of both revised prompts completed. Shared `venue_context` and `acl_arr_compliance` structures, revision modes, and fix-window values match exactly.
- Ad-hoc policy checks passed; no ICLR text remains in prompt bodies. An internal 1–5 rubric is explicitly not an official ARR scoring form.
- Baseline verification checked 784 scoped files: only the two prompts changed; 782 protected files remained byte-identical. Exact agents/requirements inventory contains the expected 12 files.
- An extra whole-tree inventory probe was discarded: unrelated `.temp/acl_compliance_audit/` files were outside the scoped baseline, not proof of new task edits. Those files were left untouched. Verification does not claim whole-tree exclusivity.
- Evidence: `.wisc/verification/acl-agent-prompt-migration/parent-independent-validation.json`, `reviewed-changes.diff`, `baseline-hashes.json`, and `originals/`.
- Verification is static prompt/policy/contract validation, not a live LLM review or manuscript compliance audit. No manuscript compilation was needed or performed by this task.
- Implementation was delegated; parent completed independent verification and final archival. No handoff remains. TaskMaster was unavailable; Hermes todo tracked completion.
- No commit: `.temp/` is ignored, and unrelated working-tree changes were not staged. The reusable venue-prompt migration checks were added to the `conference-submission-guidelines` skill.
