#!/usr/bin/env python3
"""Check standalone TeX dependencies, including the disabled appendix."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
references = []
tex_files = sorted(ROOT.glob('*.tex')) + sorted((ROOT / 'sections').rglob('*.tex'))
tex_files += sorted(ROOT.glob('figs/*/*.tex')) + sorted(ROOT.glob('tables/*/*.tex'))
pattern = re.compile(r'\\(input|include|includegraphics|bibliography)(?:\[[^\]]*\])?\{([^}]+)\}')
for source in tex_files:
    # Include commented references too: the optional appendix must be portable.
    for kind, name in pattern.findall(source.read_text()):
        if '#' in name:  # macro parameter, not a concrete file
            continue
        names = name.split(',') if kind == 'bibliography' else [name]
        for item in names:
            target = ROOT / item
            extensions = ['.pdf', '.png', '.jpg'] if kind == 'includegraphics' else ['.bib' if kind == 'bibliography' else '.tex']
            candidates = [target] if target.suffix else [target.with_suffix(e) for e in extensions]
            found = next((p for p in candidates if p.is_file()), None)
            if found is None or not found.resolve().is_relative_to(ROOT):
                errors.append(f'{source.relative_to(ROOT)}: missing or external {name}')
            else:
                references.append(str(found.relative_to(ROOT)))
for p in ROOT.rglob('*'):
    if any(part in {'.git', '.temp', '.wisc'} for part in p.relative_to(ROOT).parts):
        continue
    if p.is_symlink():
        errors.append(f'Symlink is not allowed: {p.relative_to(ROOT)}')
    # Provenance sidecars may name external experiment sources; they are not
    # manuscript compilation dependencies. Check machine paths in TeX only.
    if p.suffix == '.tex' and p.is_file():
        text = p.read_text()
        if '/workspace/' in text or '/root/' in text:
            errors.append(f'Machine-specific path: {p.relative_to(ROOT)}')
for p in ['acl.sty', 'acl_natbib.bst', 'references.bib']:
    if not (ROOT / p).is_file():
        errors.append(f'Missing local style/bibliography: {p}')
log = ROOT / 'main.log'
if log.exists():
    for line in log.read_text(errors='replace').splitlines():
        if any(s in line for s in ['Overfull', 'Missing character', 'undefined', 'LaTeX Error']):
            errors.append(line)
print(json.dumps({'tex_files': len(tex_files), 'resolved_references': len(references), 'errors': errors}, indent=2))
sys.exit(bool(errors))
