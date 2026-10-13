# RouterBSI Paper

Standalone, editable ACL manuscript. `main.tex` is at the repository root and builds to `main.pdf`. No sibling project, experiment repository, model service, Python environment, or original Word document is needed to compile it.

## Build

Install a complete TeX Live distribution (or equivalent), `latexmk`, and GNU Make. On Debian/Ubuntu, the relevant packages are:

```sh
sudo apt-get install make latexmk texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra
```

From this repository:

```sh
make             # build main.pdf
make rebuild     # force recompilation
make watch       # rebuild when source files change; Ctrl+C to stop
make check       # dependency/package checks; requires Python 3
make clean       # remove manuscript outputs, never figure/table assets
```

The Makefile prefers system TeX when `/usr/bin/latexmk` exists to avoid an incomplete competing installation. Else it uses TeX on PATH. Standard external TeX packages remain software prerequisites; they are not vendored.

### Overleaf

Upload the repository files (excluding `.git`), select `main.tex` as the main document, and use pdfLaTeX. All manuscript graphics and local style files are included. No shell escape or Python is required for the LaTeX build. Overleaf itself has not been tested.

## Layout

- `main.tex`: current manuscript entrypoint and ACL review settings.
- `sections/`: ten authoritative editable sections; `appendix.tex` and `citations.tex` contain only source-absence comments.
- `figs/`: refreshed data-backed result figures and the two hero images.
- `tables/`: three refreshed result tables with previews and provenance; only the skill-routing and downstream tables are active.
- `acl.sty`, `acl_natbib.bst`: unchanged supplied ACL style files.
- `references.bib`: existing empty bibliography placeholder; no bibliography is rendered.
- `snapshot-manifest.json`: historical packaging hashes, not a current manuscript-content manifest.
- `scripts/check_repository.py`: portable reference, asset and build-log checks.

## Authoritative source and section selection

The manuscript wording now comes from the exact supplied file `project_skill_selection/research-repo-template/paper/.wisc/temp/RouterBSI_Draft_Appendix.docx`, superseding the earlier V1 draft. This source is needed only for provenance, not compilation. Its 78 direct body paragraphs contain 73 nonempty paragraphs/headings, 60 Office Math expressions, and six hyperlinks. All 73 are mapped once to the editable sections using zero-based `% DOCX-P000-BEGIN/END` markers. Nine ordinary-text Unicode display equations and one inline update equation were mechanically converted to LaTeX, separately from the original 60 Office Math nodes. Original wording, literal author-year mentions, emphasis, mathematical notation, and hyperlink destinations are preserved; section/list formatting and bare figure/table references are mechanical integrations.

The source contains Abstract, Introduction, Related Works, Problem Definition, Method, Experiments, Results, Ablations, Limitations, and Conclusion. Despite its filename, it contains no appendix or citation-list section. Superseded appendix/citation prose was archived outside this compilation package and replaced with comment-only files; it is not recoverable by uncommenting an input here.

**Per the latest author instruction, Ablations is updated but disabled in `main.tex`.** Its four figure references and immutable snapshots remain in `sections/ablations.tex`; none are relocated into Results or rendered in the default PDF. The active manuscript therefore has nine source sections, the two early hero figures, and the two Results tables. Contribution bullets use compact local spacing.

Conversion evidence and the pre-edit dirty-tree backup are outside this standalone repository at `project_skill_selection/.wisc/artifacts/routerbsi-authoritative-docx/`: source hash and XML, raw Pandoc AST/LaTeX, per-paragraph raw conversions, source-to-section map, Unicode-equation/run map, reference integrations, and verification artifacts. These are audit material, not build dependencies.

## Scope and caveats

This is **self-contained for manuscript editing and PDF compilation**, not for rerunning experiments or regenerating the full result set. The `mbr_replay_test_f1` and `mbr_replay_test_ndcg` snapshots were refreshed from the split-labelled routing table; the other snapshots remain unchanged. External-data generators and experiment data are omitted. Each refreshed figure's `provenance.text` records its external CSV path and hash, test/accepted-row selection, source-run status, and analysis-only caveat. `snapshot-manifest.json` remains the historical packaging manifest and was intentionally not rewritten.

Scientific caveats remain intact: some result snapshots are analysis-only/non-reportable or have unresolved provenance, and token costs are incomplete. The authoritative prose contains literal author-year citations but supplies no bibliography; citation identity/support still needs author review. Source grammatical inconsistencies, the duplicated parametric-routing sentence, and potentially conflicting empirical claims are preserved rather than scientifically rewritten. The source's training description also says both that retrievers are trained and that they do not require training. Snapshot captions/caveats are preserved even when stronger claims appear in the source prose. This package does not certify submission readiness, citation accuracy, or page-limit compliance.

The local Git repository is initialized on `main`; no remote is configured and no commit or publication was made. `main.pdf` is generated and ignored by Git; figure/table PDFs and PNGs are intentionally not ignored. Before publishing, review the full manuscript and result provenance and choose an appropriate licensing policy.

## Third-party style

ACL style source: https://github.com/acl-org/acl-style-files/ . This is an independent third-party dependency link, not an external location for required first-party manuscript files. The supplied style files and their original notices are retained; no new license grant is asserted for the manuscript.
