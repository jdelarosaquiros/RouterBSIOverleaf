# Generate Word documents for the paper sections

From `RouterBSIPaper`:

```bash
uv run scripts/generate_sections_docs.py
```

The script resolves the paper directory relative to itself, so the same command
with an absolute script path also works from another directory. `uv` installs
pinned Pandoc (`pypandoc-binary==1.15`) and `python-docx==1.2.0` dependencies in an
isolated environment; no separate Pandoc install is required. Python 3.10+.

## Outputs

One `sections_docs/<source-stem>.docx` for every direct `sections/*.tex` file,
plus `sections_docs/manifest.json` containing source/dependency hashes, output
hashes, and heading/table/image/equation counts. Rerunning replaces matching
generated documents; it does not delete unrelated files or obsolete exports.
Check the manifest for the current output set. Do not hand-edit generated DOCX
files if you intend to regenerate them; save edited copies elsewhere.

- Prose, headings, lists, equations (Word OMML), and tables remain editable.
- Figures are embedded from PNG assets. PDF figure references use their sibling
  PNG previews, so these should be regenerated together when figures change.
- Tables with more than six columns use a landscape page and smaller table font.
- Citations are resolved from `references.bib` using Pandoc's default author-date
  style, not an exact reproduction of ACL's bibliography formatting. Each section
  includes its cited references; `citations.docx` collects citations from all
  exported section files.
- `appendix.docx` explicitly states that its current source has no section content
  (the source contains only comments). No appendix prose is invented.
- Cross-reference and figure/table caption numbers come from the existing `main.aux` snapshot. After editing
  manuscript structure, run `make rebuild` before exporting. The script never runs
  a LaTeX build or edits source files itself. Missing references fail the export.
- Layout is Word-friendly, not a pixel-identical copy of the two-column PDF.
- All conversions are staged and checked before publishing. A conversion warning,
  missing dependency, missing citation, or source mutation aborts generation.
  Publishing uses per-file atomic replacement, not a directory-wide transaction.

Optional paths:

```bash
uv run scripts/generate_sections_docs.py --paper-dir /path/to/RouterBSIPaper --output-dir /path/to/docs
```

## Tests

```bash
uv run --with pypandoc-binary==1.15 --with python-docx==1.2.0 \
  python -m unittest discover -s scripts -p 'test_generate_sections_docs.py' -v
```

Optional render check (requires LibreOffice Writer **and Math**):

```bash
libreoffice --headless --convert-to pdf --outdir /tmp/section-previews sections_docs/*.docx
```

LibreOffice without the Math component can silently omit equations in rendered
PDFs even when the DOCX contains valid editable Word math. This is not a reason to
replace editable equations with screenshots.
