# Task: Modular RouterBSI appendix

## What
Write sections/appendix/appendix.tex and separately editable subsection files following the saved NAACL appendix outline, grounded in the live manuscript, BayesGSI code, stored runs and displayed result sources. Integrate after References and compile the full ACL review manuscript.

## Why
The existing requested entrypoint is a comment-only placeholder. The appendix must supply replication detail, prompts, dataset statistics, extended quantitative results, retention, ablations and error/downstream analyses without repeating the main narrative or introducing unsupported measurements.

## Files to change
- sections/appendix/appendix.tex: appendix switch and section/subsection includes.
- sections/appendix/*.tex: individually editable procedure, prompts/trace, data, implementation, routing, retention, ablation and error/downstream subsections and supporting tables.
- main.tex: include the requested appendix after citations; preserve all main-text wording.
- scripts/check_repository.py: recognize nested section dependencies.
- .temp/appendix_work/: research notes, extracted data, baseline hashes and validation results, not paper prose.

## Decisions
- Match concise technical first-person prose and notation, not inherited grammatical errors.
- Render in the same two-column ACL review PDF, lettered sections after References; keep Limitations where it is.
- Current manuscript and current figure selections outrank stale README/snapshot tables for scope. Trace numeric values to current source tables and compute summaries in code.
- Shared missing configuration fields may be filled from richer matching artifacts as the user authorizes. Distinct observed configurations and metrics remain distinct; never infer new measurements or replicate counts.
- No provenance/non-reportability disclaimers, internal paths or draft TODOs in appendix prose. Maintain any evidence qualifications/assumptions only in technical notes; preserve original sidecars unmodified.
- Use exact prompts and genuine examples, identifying excerpts if shortened. Do not invent a complete end-to-end trace where the saved evidence contains only a subset.
- Essential unresolved methodological choices will go into a DOCX only if source/code/artifact inspection cannot resolve them. Contradictions can be described accurately in appendix and reported separately without changing main prose.
- Preserve existing deletion of sections/appendix.tex and all unrelated author edits. No experiment reruns, credentials, API calls, publication or commits.
- TaskMaster unavailable; Hermes todo tracks execution.

## Validation
- Snapshot current manuscript hashes and clean baseline build.
- Generate quantitative appendix tables from structured CSV/JSON with numerical checks and row counts.
- Validate include/citation/label closure and absence of internal provenance language or placeholders.
- make rebuild; inspect final log for undefined references/citations, overfull boxes and errors.
- make check with nested-source coverage.
- Render and inspect every appendix page and boundary; check labels, tables/prompts, clipping and two-column layout.
- Verify untouched main sections and source artifacts retain baseline hashes; save concise verification report.
