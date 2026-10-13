# WISC report: baseline settings and backbone claim

## Purpose and scope
Document the author-confirmed Skill-Pro condition-only implementation and SkillDAG default-settings/top-k behavior in Appendix D.4. Research the Skill-Pro paper for terminology. Propose—but do not apply—a narrower backbone conclusion. No other manuscript edits or experiments authorized.

## SELECT
Read live main.tex, README, Makefile, experiments, ablations, appendix implementation and backbone files. No applicable CLAUDE.md or .wisc/rules found. The working tree contains unrelated pending changes; preserve them.

## ISOLATE
Research scout identified Skill-Pro §3.2 pp. 3–4: activation condition is distinct from execution procedure and termination condition. Parent independently fetched the primary paper and checked the definition. Claim scout inspected the backbone observations and scope. Research evidence: skillpro-research.md and skillpro-definition-pages.txt.

## WRITE
Plan: ../../plans/baseline-settings-20261013.md. Exact insertion: addition.tex. Unapplied alternatives: ceiling-proposals.md. Before-state: before.json and implementation_software.before.tex.

## Implementation
Only authorized source target: sections/appendix/implementation_software.tex. Two paragraphs explain frozen skills/condition generation and default SkillDAG with graph expansion, depth/retrieval ranking, top-k truncation, downstream k=10. Existing citation keys reused. No caveat/provenance prose in additions.

## Validation
PASS: make build and make check exited 0; check resolved 115 references with no errors. Parent verify.py passed: exact insertion, only appendix source and generated main.pdf changed among 282 protected files; main first eight pages text identical; PDF remains 31 pages; citation keys resolved; no fatal/undefined log lines. Pages 19–20 visually inspected with no clipping/overlap or broken transitions. Evidence: build.log, check.log, verification.json, page-19.png, page-20.png, task-only.diff. Preliminary verification ran before implementation completed; a later PDF check required geometric removal of ACL line-number gutters. Both corrected checks pass.

## COMPRESS
TaskMaster unavailable; Hermes todo tracks completion. No commit: preserve unrelated pending changes. Main §7.3 rewrite remains pending user approval, not a blocked implementation task.

## Final status
Complete: baseline additions applied and verified, source-informed claim alternatives supplied for approval. No numerical results changed. No experiment reruns or commits. Only future action: apply the preferred §7.3 alternative if approved.
