"""Exact-approved-edit verification and isolated build; no manuscript edits."""
from pathlib import Path
import datetime
import difflib
import hashlib
import json
import re
import shutil
import subprocess

R = Path(__file__).resolve().parent
ROOT = R.parents[2]
BEFORE = json.loads((R / 'before.json').read_text())
EDITS = json.loads((R / 'edits_approved.json').read_text())
FILES = sorted({e['file'] for e in EDITS})
assert len(EDITS) == 18 and len(FILES) == 13
assert all(Path(f).parent == Path('sections/appendix') for f in FILES)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def digest(value):
    return sha(json.dumps(value, ensure_ascii=False).encode())

def extracts(text):
    return {
        'numeric_tokens': re.findall(r'\d+(?:[.,]\d+)*', text),
        'display_math': re.findall(r'\\\[.*?\\\]|\$\$.*?\$\$|\\begin\{(?:equation\*?|align\*?|gather\*?|multline\*?|displaymath)\}.*?\\end\{(?:equation\*?|align\*?|gather\*?|multline\*?|displaymath)\}', text, re.S),
        'tabular_blocks': re.findall(r'\\begin\{tabular\*?\}.*?\\end\{tabular\*?\}', text, re.S),
        'prompt_groups': re.findall(r'\\begingroup.*?\\endgroup', text, re.S),
        'citations': re.findall(r'\\cite\w*\*?(?:\[[^\]]*\])*\{[^}]*\}', text),
        'labels': re.findall(r'\\label\{[^}]*\}', text),
    }

def verify():
    changed = []
    evidence = {}
    diff = []
    invariants = {}
    for f, oldhash in BEFORE.items():
        current = (ROOT / f).read_bytes()
        snapshot = R / 'before' / f
        if not snapshot.exists():
            assert f not in FILES and not (f.startswith('sections/appendix/') and f.endswith('.tex')), f'Required snapshot missing: {f}'
            assert sha(current) == oldhash, f'Protected file drift: {f}'
            continue
        original = snapshot.read_bytes()
        assert sha(original) == oldhash, f'Snapshot drift: {f}'
        if sha(current) != oldhash:
            changed.append(f)
        if f not in FILES:
            assert current == original, f'Protected file drift: {f}'
        else:
            expected = original.decode()
            applied = []
            for index, e in enumerate(EDITS, 1):
                if e['file'] != f:
                    continue
                assert expected.count(e['old']) == 1, (f, index, 'old not unique')
                expected = expected.replace(e['old'], e['new'], 1)
                assert e['old'] not in current.decode(), (f, index, 'old remains')
                assert not e['new'] or e['new'] in current.decode(), (f, index, 'new missing')
                applied.append(index)
            assert current == expected.encode(), f'Unapproved edit or concurrent drift: {f}'
            evidence[f] = {'before_sha256': oldhash, 'after_sha256': sha(current), 'edit_ids': applied, 'exact_expected_bytes': True}
            diff.extend(difflib.unified_diff(original.decode().splitlines(True), current.decode().splitlines(True), fromfile='before/' + f, tofile='after/' + f))
        if f.startswith('sections/appendix/') and f.endswith('.tex'):
            oldparts, newparts = extracts(original.decode()), extracts(current.decode())
            invariants[f] = {}
            for kind in oldparts:
                assert oldparts[kind] == newparts[kind], (f, kind, 'invariant failed')
                invariants[f][kind] = {'unchanged': True, 'count': len(oldparts[kind]), 'before_sha256': digest(oldparts[kind]), 'after_sha256': digest(newparts[kind])}
    assert sorted(changed) == FILES, ('Wrong changed-file list', changed)
    (R / 'appendix_task.diff').write_text(''.join(diff))
    main = {f: {'before_sha256': h, 'after_sha256': sha((ROOT / f).read_bytes()), 'unchanged': True} for f, h in BEFORE.items() if f == 'main.tex' or (f.startswith('sections/') and not f.startswith('sections/appendix/') and f.endswith('.tex'))}
    protected = {f: {'before_sha256': h, 'after_sha256': sha((ROOT / f).read_bytes())} for f, h in BEFORE.items() if f not in FILES}
    return {'exact_replacements': True, 'replacement_count': len(EDITS), 'changed_file_count': len(FILES), 'files': evidence, 'all_new_strings_present_or_exact_deletions_verified': True, 'invariants': invariants, 'protected_files': protected, 'protected_file_count': len(protected), 'main_source_hashes': main, 'original_main_pdf_unchanged': sha((ROOT / 'main.pdf').read_bytes()) == BEFORE['main.pdf'], 'disputed_ablation_components_unchanged': sha((ROOT / 'sections/appendix/ablation_components.tex').read_bytes()) == BEFORE['sections/appendix/ablation_components.tex'], 'diff_path': str(R / 'appendix_task.diff'), 'diff_sha256': sha((R / 'appendix_task.diff').read_bytes())}

report = {'root': str(ROOT), 'revision_root': str(R), 'approved_edits_sha256': sha((R / 'edits_approved.json').read_bytes()), 'edits': [dict(e, edit_id=i) for i, e in enumerate(EDITS, 1)], 'pre_edit_snapshot_check': {'all_initial_protected_files_matched': True, 'initial_protected_count': len(BEFORE), 'all_13_targets_checked_against_before_json_before_patch': True, 'concurrent_drift_observed': False}, 'verification': verify(), 'parent_verify_alignment_invoked': False}
(R / 'implementation_source_checks.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'source_checks': 'PASS', 'edits': len(EDITS), 'files': len(FILES), 'protected_count': len(BEFORE)}, indent=2), flush=True)

source = R / 'build_before'
build = R / 'build_after'
assert source.is_dir()
assert not build.exists(), 'Refuse to overwrite existing isolated build'
excluded = sorted(p.name for p in source.iterdir() if p.is_file() and p.name.startswith('main.') and p.name != 'main.tex')
def ignore(path, names):
    return excluded if Path(path) == source else []
shutil.copytree(source, build, ignore=ignore)
copy_checks = []
for p in source.rglob('*'):
    if p.is_file() and not (p.parent == source and p.name in excluded):
        rel = p.relative_to(source)
        assert p.read_bytes() == (build / rel).read_bytes(), f'Copy mismatch {rel}'
        copy_checks.append(str(rel))
for f in FILES:
    shutil.copy2(ROOT / f, build / f)
    assert (build / f).read_bytes() == (ROOT / f).read_bytes()
assert not (build / 'main.pdf').exists()
report['isolation'] = {'source': str(source), 'destination': str(build), 'excluded_root_outputs': excluded, 'copied_file_count_verified': len(copy_checks), 'replaced_appendix_files': FILES, 'stale_main_pdf_absent_before_build': True}
report['commands'] = []
for target in ['build', 'check']:
    log = R / ('implementation_make_' + target + '.log')
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with log.open('w') as out:
        result = subprocess.run(['make', target], cwd=build, stdout=out, stderr=subprocess.STDOUT)
    report['commands'].append({'command': ['make', target], 'cwd': str(build), 'exit_code': result.returncode, 'log': str(log), 'started_utc': start, 'log_sha256': sha(log.read_bytes())})
    print(json.dumps(report['commands'][-1]), flush=True)
report['verification'] = verify()
assert report['approved_edits_sha256'] == sha((R / 'edits_approved.json').read_bytes()), 'Approval changed while building'
for f in FILES:
    assert (build / f).read_bytes() == (ROOT / f).read_bytes()
pdf = build / 'main.pdf'
report['pdf'] = {'path': str(pdf), 'exists': pdf.exists()}
if pdf.exists():
    report['pdf'].update({'sha256': sha(pdf.read_bytes()), 'size_bytes': pdf.stat().st_size})
    result = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True)
    (R / 'implementation_pdfinfo.log').write_text(result.stdout + result.stderr)
    report['pdf']['pdfinfo_exit_code'] = result.returncode
    report['pdf']['pdfinfo_log'] = str(R / 'implementation_pdfinfo.log')
    match = re.search(r'^Pages:\s+(\d+)', result.stdout, re.M)
    if match:
        report['pdf']['pages'] = int(match.group(1))
log = build / 'main.log'
report['final_latex_diagnostics'] = [line for line in log.read_text(errors='replace').splitlines() if any(x in line for x in ['Overfull', 'Missing character', 'undefined', 'LaTeX Error', 'Warning'])] if log.exists() else ['No main.log']
report['status'] = 'PASS' if pdf.exists() and all(c['exit_code'] == 0 for c in report['commands']) else 'BUILD_OR_CHECK_FAILED'
report['scope_caveat'] = 'Implementation and isolated build only; disputed initialization claim preserved; parent full alignment audit not invoked.'
(R / 'implementation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'status': report['status'], 'pdf': report['pdf'], 'evidence': str(R / 'implementation.json'), 'diagnostics': report['final_latex_diagnostics']}, indent=2), flush=True)
