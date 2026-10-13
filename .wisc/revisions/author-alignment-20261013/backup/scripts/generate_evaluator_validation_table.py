#!/usr/bin/env python3
"""Render the diagnostic appendix table after offline source/journal verification.

No model calls, credentials, source writes, or paper builds. The historical
review module is hash-pinned and used only for its read-only validation methods.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import random
import sys

PAPER = Path(__file__).resolve().parents[1]
DATA = PAPER / "sections/appendix/evaluator_validation_data"
TABLE = PAPER / "sections/appendix/evaluator_validation_table.tex"
ALIASES = (
    ("theoremqa", "TheoremQA"),
    ("logicbench", "LogicBench"),
    ("toolqa", "ToolQA"),
    ("medcalcbench", "MedCalc-Bench"),
    ("champ", "CHAMP"),
    ("bigcodebench", "BigCodeBench"),
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_pins(workspace, provenance):
    for relative, expected in provenance["sha256"].items():
        require(sha256(workspace / relative) == expected,
                f"Source changed: {relative}; do not silently refresh the pins")


def verify_audit(workspace, provenance, results, cases):
    root = workspace / provenance["audit_directory"]
    summary = read_json(root / "summary.json")
    metadata = read_json(root / "metadata.json")
    sample = read_json(root / "sample.json")
    details = read_json(root / "audit_details.json")
    require(summary == provenance["audit_summary"], "Audit summary drift")
    require(summary["human_ground_truth"] is False, "Audit is not human ground truth")
    require(metadata["seed"] == summary["seed"] == 20261014, "Audit seed mismatch")
    excluded = set(metadata["excluded_review_ids"])
    previous = read_json(Path(metadata["excluded_source"]))
    require(excluded == {r["review"]["review_id"] for r in previous}, "Previous sample mismatch")
    require(len(excluded) == summary["excluded_previous_reviews"] == 20, "Exclusion count mismatch")
    rng = random.Random(metadata["seed"])
    selected = []
    for correct in (False, True):
        eligible = sorted(key for key, row in results.items()
                          if key not in excluded and row["verdict"]["is_correct"] is correct)
        selected.extend(rng.sample(eligible, 20))
    require(selected == [r["review"]["review_id"] for r in sample], "Audit sampling not reproduced")
    require(len(details) == len(sample) == len(set(selected)) == 40, "Audit cardinality mismatch")
    require(not excluded.intersection(selected), "Audit overlaps previous sample")
    require({r["review_id"] for r in details} == set(selected), "Audit detail membership mismatch")
    for row in sample:
        require(row["review"] == results[row["review"]["review_id"]], "Audit review differs from journal")
    for row in details:
        key = row["review_id"]
        require(row["saved_boolean"] is cases[key]["saved_boolean"], "Audit saved label mismatch")
        require(row["gpt_is_correct"] is results[key]["verdict"]["is_correct"], "Audit class mismatch")
        require(row["gpt_expected_boolean"] is results[key]["verdict"]["expected_boolean"], "Audit verdict mismatch")
    require(dict(Counter(r["audit_assessment"] for r in details)) == summary["overall"], "Audit tally mismatch")
    for name, expected in summary["by_stratum"].items():
        rows = [r for r in details if r["stratum"] == name]
        tally = Counter(r["audit_assessment"] for r in rows)
        require(len(rows) == expected["n"], "Audit stratum count mismatch")
        for category in ("supported", "likely_incorrect", "ambiguous"):
            require(tally[category] == expected[category], "Audit stratum tally mismatch")
        require(sum(r["saved_boolean"] for r in rows) == expected["saved_true"], "Audit Boolean tally mismatch")
    require(len(read_json(root / "blinded_assessments.json")) == 40, "Missing blinded second-pass cases")


def verify_sources(workspace, provenance, excerpt):
    verify_pins(workspace, provenance)
    root = workspace / provenance["source_review_directory"]
    manifest = read_json(root / "manifest.json")
    summary = read_json(root / "summary.json")
    require({k: summary[k] for k in provenance["summary_fields"]} == excerpt,
            "Sidecar differs from exact saved summary")
    for path, expected in manifest["evidence"]["file_sha256"].items():
        require(sha256(Path(path)) == expected, f"Consumed source changed: {path}")
    script = workspace / provenance["source_validation_script"]
    require(sha256(script) == manifest["script_sha256"], "Historical validator hash mismatch")
    # Importing does not run main(); disabling bytecode prevents source-tree writes.
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("_saved_predicate_review", script)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load the pinned historical validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cases, evidence, prompt = module.load_run(Path(manifest["evidence"]["run_dir"]))
    require(module.make_manifest(cases, cases, evidence, prompt) == manifest,
            "Reconstructed evidence/cohort/config differs from manifest")
    # Never enter the store context: __enter__ takes a writer lock and writes.
    store = module.ReviewStore(root, manifest, cases, prompt)
    for record in store.read_journal("successes.jsonl"):
        store.validate_success(record)
        store.results[record["review_id"]] = record
    for record in store.read_journal("errors.jsonl"):
        store.validate_error(record)
        store.errors.append(record)
    reconstructed = module.summarize(cases, cases, store.results, store.errors)
    require(all(summary[k] == value for k, value in reconstructed.items()),
            "Saved summary differs from occurrence-weighted journal reconstruction")
    require(summary["status"] == "complete" and summary["cohort"] == "full", "Incomplete cohort")
    require(summary["source_completion"]["status"] == "completed_noncanonical"
            and summary["source_completion"]["reportable"] is False, "Source caveat changed")
    verify_audit(workspace, provenance, store.results, store.cases)
    # Detect concurrent changes before emitting any output.
    verify_pins(workspace, provenance)
    for path, expected in evidence["file_sha256"].items():
        require(sha256(Path(path)) == expected, f"Source changed during verification: {path}")
    return {"unique_reviews": len(store.results), "error_attempts": len(store.errors),
            "consumed_source_hashes": len(evidence["file_sha256"]),
            "pinned_source_hashes": len(provenance["sha256"]), "audit_cases": 40}


def render(excerpt):
    require(set(excerpt["by_dataset"]) == {key for key, _ in ALIASES}, "Dataset coverage mismatch")
    rows = [(key, alias, excerpt["by_dataset"][key]["reviewed"],
             excerpt["by_dataset"][key]["correct"]) for key, alias in ALIASES]
    total = sum(row[2] for row in rows)
    agreements = sum(row[3] for row in rows)
    require(total == excerpt["reviewed_occurrences"] == 37400, "Pooled denominator mismatch")
    require(agreements == excerpt["correct"] == 36315, "Pooled agreement count mismatch")
    rows.append(("total", "Total", total, agreements))
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["dataset", "display_name", "reviewed", "agreements", "agreement_percent"])
    lines = ["% Generated by scripts/generate_evaluator_validation_table.py; do not hand-edit.",
             r"\begin{table*}[t]", r"\centering", r"\begin{minipage}{0.48\textwidth}", r"\centering", r"\small",
             r"\begin{tabular}{@{}lrrr@{}}", r"\toprule",
             r"Dataset & Reviewed & Agreements & Agree. (\%) \\", r"\midrule"]
    for key, alias, reviewed, correct in rows:
        rate = f"{100 * correct / reviewed:.2f}"
        writer.writerow([key, alias, reviewed, correct, rate])
        if key == "total":
            lines.append(r"\midrule")
        lines.append(f"{alias} & {reviewed:,} & {correct:,} & {rate}" + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}",
                  r"\caption{Agreement between saved predicate decisions and model adjudication. "
                  r"The pooled rate is 97.10\%; this noncanonical diagnostic is not human-validated accuracy.}",
                  r"\label{tab:app-evaluator-validation}", r"\end{minipage}", r"\end{table*}", ""])
    return "\n".join(lines), out.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, default=PAPER.parent.parent)
    parser.add_argument("--check", action="store_true", help="Verify generated bytes without writing")
    args = parser.parse_args()
    provenance = read_json(DATA / "provenance.json")
    excerpt = read_json(DATA / "summary_excerpt.json")
    checked = verify_sources(args.workspace_root.resolve(), provenance, excerpt)
    table, counts = render(excerpt)
    outputs = {TABLE: table, DATA / "counts.csv": counts}
    for path, text in outputs.items():
        if args.check:
            require(path.read_text(encoding="utf-8") == text, f"Stale generated output: {path}")
        else:
            path.write_text(text, encoding="utf-8")
    matrix = excerpt["confusion_matrix"]
    tp = matrix["saved_true_expected_true"]
    fn = matrix["saved_false_expected_true"]
    tn = matrix["saved_false_expected_false"]
    fp = matrix["saved_true_expected_false"]
    print(json.dumps({"status": "verified" if args.check else "generated", **checked,
                      "table_rows": 7, "reviewed_occurrences": excerpt["reviewed_occurrences"],
                      "agreements": excerpt["correct"], "disagreements": excerpt["incorrect"],
                      "agreement_percent": f"{100 * excerpt['correct'] / excerpt['reviewed_occurrences']:.2f}",
                      "reference_positive_recall_percent": f"{100 * tp / (tp + fn):.2f}",
                      "always_false_agreement_percent": f"{100 * (tn + fp) / (tn + fp + tp + fn):.2f}",
                      "model_calls": 0}, indent=2))


if __name__ == "__main__":
    main()
