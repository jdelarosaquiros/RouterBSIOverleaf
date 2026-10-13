# Task: Responsible NLP checklist evidence and appendix coverage

## What
Answer all 13 questions in the author-supplied A/B/C checklist using RouterBSI code and the live RouterBSIPaper. Add missing supported reproducibility/artifact details to the appendix without changing main-paper prose, figures, data or experiments.

## Source contract
- Questions: `/workspace/storage/.hermes/webui/attachments/5ad86524c0e7/pasted-text-2026-10-13_08-27-27-302.md`.
- Code: sibling `RouterBSI`, not an assumed alias of BayesGSI. Current launch defaults are not evidence of historical run settings.
- Existing appendix: sections A--H; many answers already covered. Author revised main text/ethics/acknowledgment since previous tasks: preserve current bytes.
- Official ARR guidance fetched to `.temp/responsible_nlp_audit/official_guidance.txt`. Its numbering differs from attachment; retain attachment IDs A1,B,B1--B6,C,C1--C4 in answer document.
- Independent audits in `.temp/responsible_nlp_audit/{artifacts,compute,statistics}_audit.md` (pending when plan initiated).

## Files to change
- Existing appendix data and implementation containers: add separate naturally titled subsections only where supported facts are missing.
- Existing relevant appendix prose: targeted clarifications if necessary, no rewrite of tables/results.
- `references.bib`: only necessary missing primary dependency citations, if verified.
- `.temp/acl_requirements/responsible_nlp_checklist_answers.md`: complete answer + elaboration for every supplied item, with final compiled section references.
- `.temp/responsible_nlp_audit/`: source evidence, exact change scope and verification report.

## Decisions
- Existing Ethical Considerations suffices for A1; do not restore author-removed environmental-cost/AI-assistance passages.
- Do not claim licensing clearance, anonymization, offensive-content audits, human validation, historical GPU hardware/hours, search exhaustiveness, or release commitments without evidence.
- Answer compound questions conservatively. Missing recorded all-experiment compute means C1 cannot be fully Yes even if token totals/model sizes are present.
- Release-specific N/A requires an actual release decision; uncertainty is not N/A. Describe open author decisions separately.
- Preserve inherited nonstandard error-label terminology and unrelated current edits.
- No experiment reruns, no secret exposure, no external publication, no commit.
- WISC TaskMaster tools are unavailable: use Hermes todo; implementation child receives exact bounded edits after evidence reconciliation.

## Approved implementation batch 1: statistical reporting
Only append the following paragraph to `sections/appendix/routing_metrics.tex`; preserve existing bytes and all other sources. The independent statistical audit confirms the selected input maps and three-run component provenance. This centralizes the disclosure without duplicating result tables or modifying captions.

```tex
\paragraph{Statistical reporting.}
The main routing, recall/retention, and downstream comparisons use one evaluation per method--retriever setting, rather than an average over repeated runs. Their cross-retriever means average three distinct retrieval conditions, not random-seed repetitions. The token, replay-capacity, candidate-pool, and backbone analyses likewise use one run per configuration. We do not estimate run-to-run uncertainty for these single-run comparisons. The component ablation in Appendix~\ref{app:ablations} instead reports means and population standard deviations over three runs, all with replay-replacement seed 20260324. These deviations describe dispersion among run-level scores, not standard errors or confidence intervals, and the repetitions are not distinct-seed trials. We do not report statistical-significance tests.
```

## Approved implementation batch 2: bounded factual additions
- Exact approved new source text is in `.temp/responsible_nlp_audit/planned_additions.json`, keyed by manuscript-relative filename. Create the two specified `.tex` files without rewriting the existing appendix.
- Append `\\input{sections/appendix/data_scope}` to `sections/appendix/data.tex` and `\\input{sections/appendix/implementation_software}` to `sections/appendix/implementation.tex` (single backslash in actual TeX).
- Append the payload's `bibliography_entry` to `references.bib` if absent. Qwen3 Embedding title and ordered authors were verified against primary arXiv metadata; the historical Vector source hash matches its selected run's sealed source record.
- Preserve all main sections, method formulas, figures, captions, existing tables and statistics. No code or experiment changes.
- Answers: Yes A1/B/B1/B5/B6/C/C2/C3/C4 after additions; No B2/B3/B4/C1 on the available evidence. B2--B4 applicability depends on author-confirmed release scope, so these are conservative proposed answers, not invented N/A determinations.
- Keep unresolved rights, release safeguards, all-study compute, unknown historical hyperparameter-selection provenance, and current-code versus paper MBR admission discrepancy in the separate answer document. Do not silently change the authored method.

## Citation completion
Added original BM25 and ReAct references to the new software subsection, verified with Crossref and primary arXiv metadata; existing references are preserved.

## Validation
- Verify 13 unique supplied IDs, each with answer, elaboration, evidence/section references.
- Independently recompute existing dataset eligibility/counts; compare new claims to exact code or recorded configuration.
- Snapshot/hash protected sources before edits; diff only allowlisted appendix sources and necessary bibliography additions.
- `make rebuild`, `make check`, final log scan, `git -c safe.directory=<paper> diff --check`.
- Read final `.aux` section mapping; normalize PDF text to check additions; render/inspect modified appendix pages and their transitions.
- Mark missing author-only facts explicitly; do not imply checklist or publication clearance from a successful build.
