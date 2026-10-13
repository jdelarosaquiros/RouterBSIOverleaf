# Task: Baseline implementation clarification and backbone proposal

## What
Add author-confirmed Skill-Pro and SkillDAG implementation details only in Appendix D.4 (`sections/appendix/implementation_software.tex`). Research Skill-Pro's paper for condition terminology. Propose, but do not apply, a §7.3 ceiling-claim rewrite.

## Why
Document study-specific baseline adaptation and replace an unsupported universal ceiling inference with observations from the three tested backbones.

## Scope and decisions
- Preserve current dirty working files; baseline snapshot at `.wisc/revisions/baseline-settings-20261013/before.json`.
- Only manuscript source to change: `sections/appendix/implementation_software.tex`.
- Insert paragraphs after SkillRouter and before Task evaluation.
- Skill-Pro: frozen skills; generate only the respective applicability condition. Cite existing `pmlr-v306-mi26d`; terminology informed by primary paper, study adaptation supplied by author. Do not claim original Skill-Pro freezes skill content.
- SkillDAG: default settings; five retrieved seeds; graph-depth/retrieval-score ranking as main implementation; retain at most k after expansion even if candidate expansion exceeds k; downstream k=10 as main text states. Cite existing `bai2026skilldag`.
- No caveat/provenance prose in manuscript additions. No invented optimizer parameters, training budgets, or fine-tuning claims.
- Main source and all results remain unchanged. Ceiling alternatives saved separately in revision directory for approval.
- TaskMaster is unavailable; Hermes todo is the workflow tracker. No commits: unrelated pending edits are present.

## Validation
Run `make build` and `make check`. Verify only allowlisted source plus generated main.pdf changed among protected inputs. Check existing content retained, citations resolve, new prose appears in PDF; render and inspect changed appendix pages and transition. Preserve all main-page text and all numerical results.

## Execution
Research scout retrieves paper context; independent scout checks claim/placement. Implementer follows this exact scope after research. Parent independently validates resulting diff, log, hashes, and rendering. Save concise WISC report and verification JSON.
