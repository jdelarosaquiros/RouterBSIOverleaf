# RouterBSI Paper

Compilation-only source for the current ACL manuscript, including the appendix.
The main document is the root `main.tex`; the generated output is `main.pdf`.

## Overleaf

Pull the `main` branch from `jdelarosaquiros/RouterBSIOverleaf`, select the root
`main.tex` as the main document, and use pdfLaTeX. Recompile from scratch after
synchronizing a source update. No Python or shell escape is required.

## Local build

Install a complete TeX Live distribution (or equivalent), `latexmk`, and GNU Make.
The manuscript uses the ACL style and standard TeX packages, including `dsfont`.
On Debian/Ubuntu, install:

```sh
sudo apt-get install make latexmk texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra
```

```sh
make             # build main.pdf
make rebuild     # force recompilation
make watch       # rebuild as source files change; Ctrl+C to stop
make clean       # remove manuscript build outputs, not included graphics
```

The Makefile prefers `/usr/bin/latexmk` when available; otherwise it uses PATH.

## Included files

- `main.tex`: manuscript entrypoint and review-format configuration.
- `sections/`: active main-text and appendix sections, including appendix tables.
- `figs/`: only graphics, wrappers, and caption files loaded by the manuscript.
- `tables/`: the two table wrappers loaded from this directory; other active
  tables are directly defined under `sections/appendix/`.
- `references.bib`, `acl.sty`, `acl_natbib.bst`: bibliography and local ACL styles.
- `Makefile` and `.gitignore`: build commands and local-output exclusions.

Captions are edited in the active `.tex` wrapper, except where that wrapper
explicitly inputs a `description.text` file. Table 1's caption is in
`tables/skill_routing_performance_average/table.tex`.

This repository contains compilation inputs, not experiment or figure-regeneration
code. Unused figures/tables, duplicate preview images, analysis metadata, utility
scripts, generated Word exports, and scratch/review snapshots are excluded.
The existing manuscript text, numerical content, active captions, and required
artwork are unchanged by this packaging cleanup. Bibliography processing uses
BibTeX through `latexmk` or Overleaf.

## Third-party style

ACL style source: https://github.com/acl-org/acl-style-files/ . The supplied style
files and their original notices are retained. This repository does not assert a
new license grant for the manuscript or its third-party assets.
