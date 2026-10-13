# Task: ACL critique and proposal-only revision package

## What
Review the current main.pdf using acl_critic; feed the grounded REVIEW_JSON to fix_acl_critic to propose—not execute—solutions. User explicitly prohibited manuscript modification pending review and confirmed the read-only scope at the skills' checkpoint.

## Inputs / selected context
- Paper root: /workspace/storage/healthcare_workspace/project_skill_selection/RouterBSIPaper
- Frozen PDF: .wisc/reviews/acl-critic-proposals-20261013T111734Z-51ddab4b/reviewed_main.pdf
- SHA256: 51ddab4b827e211879ecf8c936083ea5fa2a03f6b34a32d230f98b90f5910d6b
- PDF 28 pages, main content ends on page 8. Long-paper assumption only; venue year/track/cycle/stage unknown.
- Both complete skill reference prompts and local .temp/acl_requirements guides. ACL/ARR policy distinguished from NAACL 2027 dates; optional appendix outline not mandatory.
- Workspace AGENTS.md; no additional AGENTS.md/CLAUDE.md or scoped .wisc rules discovered in project/paper roots.

## Files to create
Only new artifacts under .wisc/reviews/acl-critic-proposals-20261013T111734Z-51ddab4b/ and this plan/archive. PAPER_SOURCE is PDF + extracted text; source tree may be inspected read-only for evidence. EXPERIMENTAL_RESULTS=[] (no new experiments authorized). Existing paper tables are evidence, not independently replicated results.
- REVIEW_JSON.json and REVIEW.md
- REVISION_REPORT.json and PROPOSALS.md
- Validation script/results and audit notes

## Isolation
Three independent read-only scouts examine method/guarantees; empirical/numerical consistency; ACL compliance/figures/narrative. Parent independently validates anchors and severity, assembles review contract. A separate fixer consumes final contract for proposals and reports all edits not_executed.

## Decisions
- No manuscript/source/figure/table/bibliography/style changes; no compilation or experiment execution; no uploads or commits (dirty worktree and approval gate).
- Unknown stage permits review/planning only. No deadline feasibility inferred. Internal scores not official ARR scores.
- Use literal PDF extraction quotes, with exact page anchors; null TeX location unless independently mapped. Keep evidence-based rationale concise.
- Propose exact old/new wording when existing evidence suffices; otherwise name required inputs and concrete analysis/experiment protocol, with safe claim-narrowing alternatives.
- Audit all 8 figures, including appendix Figure 8. Existing diagnostic/nonreportable evidence remains explicitly so labelled.
- Every issue has a solution proposal and measurable acceptance criteria; all manuscript-change criteria remain unresolved until authorized.

## Validation
Parse both JSON files; verify unique issue IDs, all exact page quote anchors, dependency DAG, execution ordering, issue-to-proposal one-to-one mapping and criterion coverage; check shared context/compliance equality and not_executed statuses. Recompute reported arithmetic using script. Compare all 351 protected baseline file hashes and PDF hash to originals; list exclusions/new artifacts without claiming whole-tree equivalence. No build claim.

## Completion
- Completed review/proposal package: REVIEW_JSON.json, REVIEW.md, REVISION_REPORT.json, PROPOSALS.md, README.md, VERSION_NOTE.md.
- Parent validation passed: 15 literal anchors, 15 proposal logs, 47 preserved acceptance criteria, 51 unique exact proposal spans, all 8 figures, strict JSON/shared context, dependency ordering and not_executed/null-after-text boundaries.
- Source manifests and selected CSV hashes independently checked; key arithmetic reproduced without model calls.
- Frozen PDF verified unchanged. All 351 protected baseline files were compared; external edits continued during finalization, so changed/unchanged counts and exact paths are timestamped in verification.json. No whole-worktree-unchanged assertion.
- No manuscript changes, build, experiments, uploads or commit performed by this workflow. Revisions remain approval-gated.
- PDF snapshot 856f39f7bf11594ee8689eff8a0b4bced019b8ce3cc59405693b259a356e4e6b observed at11:42:46 UTC was NOT substituted for the frozen review input; that observation retained all issue anchors except the already-removed ISSUE-001. Later live updates remain unreviewed.
- Temporary verifier is removed after final validation; verification.json and proposal_span_verification.json preserve outcomes.

## Tracking
TaskMaster unavailable; Hermes todo used. Plan archived after validated delivery; manuscript changes remain approval-gated, not unfinished review work.
