#!/usr/bin/env python3
"""Explicit editorial projection of figs/tables; never a source certification.

Run plan, review its complete change ledger, then apply and verify. Raw generators
and their validation tests are deliberately untouched. See README_publishing_cleanup.md.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys

EXTENSIONS = {".json", ".text", ".tex", ".md", ".txt"}
PARENT_PREVIEW_REFRESH = {
    "tables/retrieval_and_reranking_performance/preview.pdf",
    "tables/retrieval_and_reranking_performance/preview.png",
}
FLAGS = re.compile(r"reportab|analysis[-_ ]only|non[-_ ]?canonical|diagnostic[-_ ]only|publication[- ](?:valid|eligib)|provisional|unresolved[- ]provenance", re.I)
REASON = "SRA_GATEDROUTER_ALLOW_SOURCE_DRIFT=1 and final audit disabled; development run is nonreportable; runtime_judgment_lookup_cache enabled, so repeated judgments may skip exact request reconstruction"
DELETE_KEYS = {"reportable", "source_reportability", "analysis_only", "diagnostic_only", "nonreportable_reason"}
# Exact reviewed phrases, not a blanket sentence/line scrubber. Unknown flags fail.
REPLACEMENTS = [
    ("Analysis-only (non-reportable or unknown source provenance). ", ""),
    ("Source status: completed_noncanonical; reportable=false; analysis-only. Not a controlled shared-candidate comparison.", "Not a controlled shared-candidate comparison."),
    ("Source status: completed_noncanonical; reportable=false; analysis-only.\n", ""),
    ("Nonreportable reason: " + REASON + "\n", ""),
    ("Nonreportable reason(s): " + REASON + "\n", ""),
    ("Source reportability: diagnostic_only=true; reportable=false; completed_noncanonical.\n", ""),
    ("Source reportability: non-reportable\n", ""),
    ("Source reportability: unknown\n", ""),
    ("Analysis-only: source provenance does not certify publication validity.\n", ""),
    ("Analysis-only, non-reportable: this rendering does not establish publication eligibility.\n", ""),
    ("Completion/reportability: refreshed runs are in_progress, passed=false, reportable=false; derived values are analysis-only and non-reportable.", "Refreshed runs are in_progress."),
    ("The alternate run completion status is completed_noncanonical and reportable=false.\n", ""),
    (", which is completed\\_noncanonical (reportable=false); these results are analysis-only.", "."),
    (", which is completed_noncanonical (reportable=false); these results are analysis-only.", "."),
    ("Analysis-only/non-reportable: mixed run families and unresolved publication validity.", "Mixed run families."),
    ("Analysis-only/non-reportable: mixed run families, incomplete Only Gate and unresolved publication validity.", "Mixed run families; Only Gate is incomplete."),
    ("Analysis-only/non-reportable; sources and run families differ.", "Sources and run families differ."),
    ("Analysis-only; conditions mix refreshed and historical runs.", "Conditions mix refreshed and historical runs."),
    ("Analysis-only; conditions mix run sources.", "Conditions mix run sources."),
    ("Analysis-only; run provenance differs.", "Run sources differ."),
    (" Analysis-only: source run provenance remains unresolved; publication validity is not certified.", ""),
    (" Analysis-only: the source table carries unresolved run provenance, and publication validity is not certified.", ""),
    (" Analysis-only: source runs are non-reportable.", ""),
    ("No uncertainty estimates supplied; analysis-only and run reportability unresolved.", "No uncertainty estimates supplied."),
    ("No uncertainty estimates supplied; analysis-only. Fixed Vector RouterBSI source is completed_noncanonical, reportable=false; other run reportability unresolved.", "No uncertainty estimates supplied."),
    ("Analysis-only; source reportability unknown. No run-level re-audit or inference performed.", "No run-level re-audit or inference performed."),
    ("The paper provenance records the refreshed source hash. Its unresolved-provenance warning is carried forward, not resolved by count consistency or a newer CSV.", "The paper provenance records the refreshed source hash."),
    ("Inherited paper-table provenance (not a new certification):", "Inherited paper-table provenance:"),
    ("Scope: manuscript integration; no publication-eligibility promotion or sibling changes.", "Scope: manuscript integration; no sibling changes."),
    ("Analysis-only known token totals", "Known token totals"),
    ("; Source Reportable=False", ""),
    ("Analysis-only. ", ""),
    ("Red method labels mark provisional rows. Method-to-run correspondence remains unresolved, so this table is diagnostic rather than publication-validated.", "Red method labels identify Vector-source rows."),
    ("CSV methods do not match input_runs.json; provenance is unresolved.", "CSV methods do not match input_runs.json."),
    ("CSV methods do not match input\\_runs.json; provenance is unresolved.", "CSV methods do not match input\\_runs.json."),
    ("Existing selection/provenance records remain immutable evidence. This manifest supersedes their PDF/PNG hashes and rendering settings only; it does not promote reportability.", "This manifest records the PDF/PNG hashes and rendering settings."),
    ("Analysis-only; fixed Vector RouterBSI run is completed_noncanonical with reportable=false; other run reportability unresolved; no inference or new evaluation.", "No inference or new evaluation."),
    ("Analysis-only; inherited unresolved run provenance; no inference or new evaluation.", "No inference or new evaluation."),
]
DELETE_VALUES = {
    ("status", "completed_noncanonical"), ("status", "non-reportable"),
    ("use", "analysis-only; publication validity not established"),
    ("caveat", "Analysis-only; source provenance unresolved."),
    ("caveat", "Inherited unresolved run provenance; not a publication-validity certification."),
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    """All fig/table files (including previews/code) are bound against drift."""
    result = {}
    for directory in ("figs", "tables"):
        base = root / directory
        if not base.is_dir() or base.is_symlink():
            raise ValueError(f"Missing or symlinked scope root: {base}")
        for path in sorted(base.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Symlink in artifact scope: {path}")
            if path.is_file():
                result[str(path.relative_to(root))] = digest(path.read_bytes())
    return result


def protected_csvs(root):
    """Read only: all paper CSVs and sibling BayesGSI/tables source CSVs."""
    files = list(root.rglob("*.csv"))
    source = root.parent / "BayesGSI" / "tables"
    if source.is_dir():
        files += list(source.rglob("*.csv"))
    return {str(p.resolve()): digest(p.read_bytes()) for p in sorted(files)
            if not p.is_relative_to(root / ".wisc")}


def text_projection(text):
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text


def pointer(parent, key):
    return parent + "/" + str(key).replace("~", "~0").replace("/", "~1")


def project_json(value, changes, path=""):
    if isinstance(value, dict):
        output = {}
        for key, child in value.items():
            loc = pointer(path, key)
            remove = key in DELETE_KEYS or (isinstance(child, str) and (key, child) in DELETE_VALUES)
            if remove:
                if isinstance(child, (dict, list)) or type(child) in (int, float):
                    raise ValueError(f"Refusing to remove structured/numeric data at {loc}")
                changes.append({"operation": "remove_json", "path": loc, "before": child})
            else:
                output[key] = project_json(child, changes, loc)
        return output
    if isinstance(value, list):
        return [project_json(child, changes, pointer(path, i)) for i, child in enumerate(value)]
    if isinstance(value, str):
        new = text_projection(value)
        if new != value:
            changes.append({"operation": "replace_json_text", "path": path, "before": value, "after": new})
        return new
    return value


def numeric_leaves(value, path=""):
    out = {}
    if isinstance(value, dict):
        for key, child in value.items():
            out.update(numeric_leaves(child, pointer(path, key)))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            out.update(numeric_leaves(child, pointer(path, i)))
    elif type(value) in (int, float):
        out[path] = (type(value).__name__, value)
    return out


def validate_projection(name, before, after):
    flag = FLAGS.search(after)
    if flag:
        raise ValueError(f"Unreviewed presentation flag in {name}: {flag.group()}")
    if Counter(re.findall(r"\b[0-9a-f]{64}\b", before)) != Counter(re.findall(r"\b[0-9a-f]{64}\b", after)):
        raise ValueError(f"Hash identity changed: {name}")
    if name.endswith(".json"):
        if numeric_leaves(json.loads(before)) != numeric_leaves(json.loads(after)):
            raise ValueError(f"JSON numeric drift: {name}")
    else:
        # The only removed numeric-bearing prose is the exact audit setting =1,
        # not a result/row/count/axis token. Its full original is in the ledger.
        numeric = lambda s: re.findall(r"\d+(?:\.\d+)?", s.replace(REASON, ""))
        if numeric(before) != numeric(after):
            raise ValueError(f"Text numeric drift: {name}")
        if name.endswith(".tex"):
            tables = lambda s: re.findall(r"\\begin\{tabular\}.*?\\end\{tabular\}", s, re.S)
            if tables(before) != tables(after):
                raise ValueError(f"Table-body drift: {name}")


def transform(name, data):
    before = data.decode("utf-8")
    changes = []
    if name.endswith(".json"):
        original = json.loads(before)
        projected = project_json(original, changes)
        after = (json.dumps(projected, indent=2, ensure_ascii=False) + "\n") if changes else before
    else:
        pieces = []
        for number, line in enumerate(before.splitlines(keepends=True), 1):
            new = text_projection(line)
            pieces.append(new)
            if new != line:
                changes.append({"operation": "replace_text", "line": number, "before": line, "after": new})
        after = "".join(pieces)
    validate_projection(name, before, after)
    return after.encode("utf-8"), changes


def make_plan(root, backup):
    baseline = inventory(root)
    changes = []
    count = 0
    for name, sha in baseline.items():
        if Path(name).suffix not in EXTENSIONS:
            continue
        count += 1
        data = (root / name).read_bytes()
        if digest(data) != sha:
            raise ValueError(f"Concurrent drift before planning: {name}")
        output, edits = transform(name, data)
        if edits:
            changes.append({"file": name, "before_sha256": sha, "after_sha256": digest(output),
                            "backup": str(backup / "publishing-cleanup" / sha / name), "changes": edits,
                            "after_text": output.decode("utf-8")})
    if inventory(root) != baseline:
        raise ValueError("Concurrent artifact drift while planning")
    return {"schema": 1, "root": str(root), "script_sha256": digest(Path(__file__).read_bytes()),
            "presentation_files_scanned": count, "baseline_artifact_hashes": baseline,
            "protected_csv_hashes": protected_csvs(root), "files": changes,
            "interpretation": "Editorial projection only; raw sources and validation guards are unchanged. Existing embedded source/snapshot hashes remain historical bindings; this ledger binds current presentation bytes."}


def verify(root, plan, require_after=True, allow_preview_refresh=False):
    expected = dict(plan["baseline_artifact_hashes"])
    for entry in plan["files"]:
        if require_after:
            expected[entry["file"]] = entry["after_sha256"]
    actual = inventory(root)
    exceptions = PARENT_PREVIEW_REFRESH if allow_preview_refresh else set()
    delta = sorted(k for k in set(actual) | set(expected)
                   if actual.get(k) != expected.get(k) and k not in exceptions)
    if set(actual) != set(expected) or delta:
        raise ValueError(f"Artifact drift: {delta}")
    if protected_csvs(root) != plan["protected_csv_hashes"]:
        raise ValueError("Protected CSV drift")
    if require_after:
        for entry in plan["files"]:
            archived = Path(entry["backup"]).read_bytes()
            if digest(archived) != entry["before_sha256"]:
                raise ValueError(f"Archive drift: {entry['file']}")
            output, edits = transform(entry["file"], archived)
            if digest(output) != entry["after_sha256"] or edits != entry["changes"]:
                raise ValueError(f"Ledger replay mismatch: {entry['file']}")
        for name in actual:
            if Path(name).suffix in EXTENSIONS:
                data = (root / name).read_bytes()
                output, edits = transform(name, data)
                if edits or output != data:
                    raise ValueError(f"Not idempotent: {name}")
    operations = Counter(c["operation"] for f in plan["files"] for c in f["changes"])
    return {"presentation_files_scanned": plan["presentation_files_scanned"],
            "changed_files": len(plan["files"]), "change_counts": dict(operations),
            "artifact_files_bound": len(actual), "protected_csv_files": len(plan["protected_csv_hashes"]),
            "remaining_flags": 0 if require_after else None,
            "numeric_invariance": True, "source_hash_invariance": True, "csv_invariance": True,
            "preview_and_other_artifact_invariance_except_declared": True,
            "intentional_mutable_preview_exceptions": sorted(exceptions),
            "preview_refresh_observed": {k: {"before": expected[k], "after": actual[k]}
                                         for k in sorted(exceptions & set(actual))
                                         if actual[k] != expected[k]},
            "idempotent": require_after}


def apply_plan(root, plan):
    # All guards and backups complete before the first presentation write.
    expected_after = dict(plan["baseline_artifact_hashes"])
    expected_after.update({f["file"]: f["after_sha256"] for f in plan["files"]})
    if inventory(root) == expected_after:
        return verify(root, plan)
    verify(root, plan, require_after=False)
    for entry in plan["files"]:
        name = entry["file"]
        if Path(name).parts[0] not in ("figs", "tables") or ".." in Path(name).parts or Path(name).suffix not in EXTENSIONS:
            raise ValueError(f"Out-of-scope write: {name}")
        data = (root / name).read_bytes()
        if digest(data) != entry["before_sha256"]:
            raise ValueError(f"Drift before archival: {name}")
        output, edits = transform(name, data)
        if digest(output) != entry["after_sha256"] or output.decode() != entry["after_text"] or edits != entry["changes"]:
            raise ValueError(f"Plan/policy drift: {name}")
        archive = Path(entry["backup"])
        archive.parent.mkdir(parents=True, exist_ok=True)
        if archive.exists():
            if archive.read_bytes() != data:
                raise ValueError(f"Refusing to overwrite archive: {archive}")
        else:
            with archive.open("xb") as handle:
                handle.write(data)
    verify(root, plan, require_after=False)
    for entry in plan["files"]:
        target = root / entry["file"]
        if digest(target.read_bytes()) != entry["before_sha256"]:
            raise ValueError(f"Drift immediately before write: {target}")
        target.write_text(entry["after_text"], encoding="utf-8")
    return verify(root, plan)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("plan", "apply", "verify"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--record", type=Path, required=True, help="Immutable detailed plan/change ledger JSON")
    parser.add_argument("--backup", type=Path, required=True, help="Existing revision backup directory")
    parser.add_argument("--allow-preview-refresh", action="store_true",
                        help="Verify only: permit the parent's retrieval/reranking PDF+PNG refresh")
    args = parser.parse_args()
    if args.allow_preview_refresh and args.mode != "verify":
        raise ValueError("Preview exceptions are allowed only in verification, never writes")
    root, backup, record = args.root.resolve(), args.backup.resolve(), args.record.resolve()
    revisions = root / ".wisc" / "revisions"
    if not backup.is_dir() or not backup.is_relative_to(revisions) or not record.is_relative_to(revisions):
        raise ValueError("Use an existing revision backup and a revision-local ledger")
    if args.mode == "plan":
        plan = make_plan(root, backup)
        record.parent.mkdir(parents=True, exist_ok=True)
        with record.open("x", encoding="utf-8") as handle:
            json.dump(plan, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        result = verify(root, plan, require_after=False)
    else:
        plan = json.loads(record.read_text())
        if plan["root"] != str(root) or plan["script_sha256"] != digest(Path(__file__).read_bytes()):
            raise ValueError("Root or cleanup-script drift; create a new reviewed plan")
        for entry in plan["files"]:
            if Path(entry["backup"]) != backup / "publishing-cleanup" / entry["before_sha256"] / entry["file"]:
                raise ValueError("Archive path drift")
        result = apply_plan(root, plan) if args.mode == "apply" else verify(
            root, plan, allow_preview_refresh=args.allow_preview_refresh)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError) as exc:
        print(f"Publishing cleanup refused: {exc}", file=sys.stderr)
        sys.exit(1)
