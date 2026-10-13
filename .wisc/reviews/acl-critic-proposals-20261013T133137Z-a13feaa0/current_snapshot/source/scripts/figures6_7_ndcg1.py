#!/usr/bin/env python3
"""Regenerate ONLY active Figures 6/7 from frozen CSV Hit@1 values.

Render branches copied from research-repo-template/paper/artifact_rendering.py
(lines 252-298, 337-340, 373-375, 443-453). No shared generator is invoked.
Run from any cwd: /usr/bin/python3 /path/to/RouterBSIPaper/scripts/figures6_7_ndcg1.py
Use a Python 3 environment with matplotlib; tests additionally use numpy and Pillow.
Verified environment: /usr/bin/python3, Matplotlib 3.8.4, NumPy 1.24.4, Pillow 10.2.0.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
TOKEN = "performance_token_usage"
LLMS = "routing_performance_across_llms_init"
SPECS = {
    TOKEN: ("routing_token_usage", "ba0fc6824888296f67d550a1a579254728eb13e1a3705203bfb448ad82f48e67", 4),
    LLMS: ("routing_performance_by_LLM", "8a2706128085096222ed3d7861a740f78c837406bc860fc16383ceefe7d81102", 63),
}
MODELS = ["Qwen3.5 4B", "Qwen3.8 27B", "GPT-OSS 120B"]
METHODS = ["RouterBSI_init", "RouterBSI"]
STYLES = {
    "Both Enabled": {"color": "#009E73", "marker": "D", "linestyle": "-."},
    "Both Disabled": {"color": "#7A7A7A", "marker": "^", "linestyle": ":"},
    "Only MBR": {"color": "#0072B2", "marker": "o", "linestyle": "-"},
    "Only Gate": {"color": "#D55E00", "marker": "s", "linestyle": "--"},
}
RCPARAMS = {"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"], "font.size": 10, "axes.labelsize": 11, "legend.fontsize": 9, "pdf.fonttype": 42, "ps.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": .22, "grid.linewidth": .5, "savefig.bbox": "tight"}
ALIAS = ("Source metric Hit@1 is displayed as nDCG@1 only for these binary-relevance tasks with nonempty gold. "
         "The source evaluator differs on empty gold: Hit@1=0, nDCG@1=1. The pinned complete benchmark "
         "annotation universe is checked to contain zero empty-gold tasks; its source loader also rejects "
         "empty annotations and unknown task IDs. This is not a universal alias or a graded-relevance claim.")
SELECTIONS = {
    TOKEN: "All four source rows in source order; Qwen3.5 4B / SkillSight, final test (748 tasks); exact Total Tokens / 1,000,000; no aggregation.",
    LLMS: "Dataset=Average, Retriever=SkillSight; shared Qwen3.5 4B SkillSight baseline, then RouterBSI_init immediately before RouterBSI for Qwen3.5 4B, Qwen3.8 27B, GPT-OSS 120B; stored task-weighted test summaries (748 tasks), no new aggregation.",
}
CAVEATS = {
    TOKEN: "Analysis-only known token totals. Source flags: Complete=False; Known Only=True; Source Reportable=False. Run-local costs exclude external/shared initialization; this is not full token accounting.",
    LLMS: "Historical candidates are preserved; this is not a controlled common-candidate comparison. No uncertainty is estimated.",
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative(path):
    return str(Path(path).resolve().relative_to(ROOT))


def record(path):
    return {"path": relative(path), "sha256": sha256(path)}


def finite_metric(row, field):
    try:
        value = float(row[field])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"missing/invalid {field}: {row.get('Method')}") from exc
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"out-of-range/nonfinite {field}: {value}")
    return value


def select_data(artifact, rows, metric="Hit@1"):
    """Strict selection; nDCG@10 allowed solely for the old-render control test."""
    if artifact not in SPECS or metric not in {"Hit@1", "nDCG@10"}:
        raise ValueError("unsupported artifact or metric")
    if len(rows) != SPECS[artifact][2]:
        raise ValueError("unexpected source row count")
    if artifact == TOKEN:
        expected = [(MODELS[0], "SkillSight", method) for method in STYLES]
        actual = [(r.get("Model"), r.get("Retriever"), r.get("Method")) for r in rows]
        if actual != expected:
            raise ValueError("unexpected token identity/order")
        selected = rows
        for row in selected:
            if row.get("Quality Phase") != "final" or row.get("Quality Tasks") != "748":
                raise ValueError("unexpected quality phase/task count")
            if (row.get("Complete"), row.get("Known Only"), row.get("Source Reportable")) != ("False", "True", "False"):
                raise ValueError("unexpected token accounting/reportability flags")
    else:
        keys = [(r.get("Model"), r.get("Retriever"), r.get("Method"), r.get("Dataset")) for r in rows]
        if len(keys) != len(set(keys)):
            raise ValueError("duplicate source identity")
        eligible = [r for r in rows if r.get("Dataset") == "Average" and r.get("Retriever") == "SkillSight"]
        order = [(MODELS[0], "SkillSight")] + [(m, method) for m in MODELS for method in METHODS]
        selected = []
        for model, method in order:
            matches = [r for r in eligible if (r.get("Model"), r.get("Method")) == (model, method)]
            if len(matches) != 1 or matches[0].get("n_tasks") != "748":
                raise ValueError(f"missing/invalid unique 748-task row: {model}/{method}")
            selected.append(matches[0])
    points = []
    for i, row in enumerate(selected):
        point = {k: row[k] for k in ("Model", "Retriever", "Method")}
        point.update(y=finite_metric(row, metric), metric=metric,
                     display_metric="nDCG@1" if metric == "Hit@1" else metric)
        if artifact == TOKEN:
            try:
                tokens = int(row["Total Tokens"])
            except (KeyError, ValueError) as exc:
                raise ValueError("invalid Total Tokens") from exc
            if tokens <= 0:
                raise ValueError("nonpositive Total Tokens")
            point.update(x=tokens / 1_000_000, total_tokens=row["Total Tokens"])
        else:
            point.update(x=i, Dataset=row["Dataset"])
        points.append(point)
    return {"selected_rows": selected, "points": points, "model_order": MODELS.copy(), "method_order": METHODS.copy()}


def read_selection(artifact, source=None):
    directory, expected_hash, _ = SPECS[artifact]
    source = Path(source) if source else ROOT / "BayesGSI/tables" / directory / "results.csv"
    if sha256(source) != expected_hash:
        raise ValueError(f"source drift: {source}")
    with source.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    return source, select_data(artifact, rows)


def validate_alias_evidence(root=ROOT, evidence=None):
    """Fail closed even if an unrelated benchmark file gains an empty gold set."""
    evidence = evidence or json.loads(Path(__file__).with_name("figures6_7_alias_evidence.json").read_text())
    expected = evidence["annotations"]
    files = sorted((root / "BayesGSI/data/bench/instances").glob("*.json"))
    if [str(p.relative_to(root)) for p in files] != [item["path"] for item in expected]:
        raise ValueError("benchmark annotation file set drift")
    seen = set()
    for path, item in zip(files, expected):
        if sha256(path) != item["sha256"]:
            raise ValueError(f"annotation hash drift: {path}")
        rows = json.loads(path.read_text())
        if not isinstance(rows, list) or len(rows) != item["tasks"]:
            raise ValueError("annotation count drift")
        for row in rows:
            task, gold = row.get("instance_id"), row.get("skill_annotations")
            if not isinstance(task, str) or task in seen or not isinstance(row.get("dataset"), str):
                raise ValueError("invalid/duplicate annotation identity")
            if not isinstance(gold, list) or not gold or any(not isinstance(g, str) or not g for g in gold):
                raise ValueError("empty/invalid gold; Hit@1 cannot be aliased")
            seen.add(task)
    if len(seen) != evidence["total_tasks"] or evidence["empty_gold_tasks"] != 0:
        raise ValueError("invalid alias evidence count")
    for item in evidence["source_evaluator_files"]:
        if sha256(root / item["path"]) != item["sha256"]:
            raise ValueError("source annotation/metric evaluator drift")
    return evidence


def render(artifact, selection, display_metric="nDCG@1"):
    """Return live artists for executable point, annotation, and style checks."""
    plt.rcParams.update(RCPARAMS)
    points = selection["points"]
    if artifact == LLMS:
        if len(points) != 7:
            raise ValueError("expected seven baseline/initial/final bars")
        models = selection["model_order"]
        palette = ["#0072B2", "#D55E00", "#009E73"]
        positions = [0, .83, 1.17, 1.83, 2.17, 2.83, 3.17]
        colors = ["#7A7A7A"] + [color for color in palette for _ in range(2)]
        fig, ax = plt.subplots(figsize=(7.0, 3.8), layout="constrained")
        bars = ax.bar(positions, [p["y"] for p in points], width=.30,
                      color=colors, edgecolor="white", linewidth=.6, zorder=3)
        for bar, point in zip(bars, points):
            if point["Method"] == "RouterBSI_init":
                bar.set_hatch("///")
                bar.set_alpha(.55)
            ax.text(bar.get_x() + bar.get_width()/2, point["y"] + .018,
                    f"{point['y']:.3f}", ha="center", va="bottom", fontsize=9)
        ax.set_xticks(range(4), ["SkillSight", *models])
        ax.set_ylabel(display_metric)
        ax.set_ylim(0, 1)
        ax.set_axisbelow(True)
        ax.grid(axis="x", visible=False)
        legend = ax.legend(handles=[Patch(facecolor="#777777", edgecolor="white", hatch="///", alpha=.55, label=r"$\mathrm{RouterBSI}_{\mathrm{init}}$"),
                           Patch(facecolor="#777777", edgecolor="white", label="RouterBSI")],
                  loc="upper center", ncol=2, frameon=False)
        for text in legend.get_texts():
            text.set_math_fontfamily("dejavuserif")
    elif artifact == TOKEN:
        fig, axes = plt.subplots(1, 1, figsize=(6.75, 3.4), squeeze=False, layout="constrained")
        ax = axes.flat[0]
        ax.set_title("Qwen3.5 4B / SkillSight", fontsize=10, pad=10)
        ax.set_ylabel(display_metric)
        for p in points:
            style = STYLES[p["Method"]]
            ax.scatter(p["x"], p["y"], label=p["Method"], color=style["color"], marker=style["marker"], s=65, zorder=3)
        ax.set_xlabel("Total Token Usage (millions)")
        ax.legend(ncol=2, loc="lower right", framealpha=.92)
        ax.margins(x=.12, y=.2)
        lo, hi = ax.get_ylim()
        ax.set_ylim(lo - (hi - lo) * .35, hi)
    else:
        raise ValueError("unsupported artifact")
    return fig, ax


def artist_state(artifact, fig, ax):
    """Serialize actual plotted data, not merely the selector's intended data."""
    state = {"size_inches": fig.get_size_inches().tolist(), "ylabel": ax.get_ylabel(),
             "xlabel": ax.get_xlabel(), "title": ax.get_title(), "ylim": list(ax.get_ylim()),
             "xlim": list(ax.get_xlim()), "xtick_labels": [t.get_text() for t in ax.get_xticklabels()],
             "legend": [t.get_text() for t in ax.get_legend().get_texts()],
             "annotations": [{"text": t.get_text(), "position": list(t.get_position()), "fontsize": t.get_fontsize()} for t in ax.texts]}
    if artifact == TOKEN:
        state["scatter"] = [{"xy": c.get_offsets().tolist(), "color": c.get_facecolors().tolist(),
                             "size": c.get_sizes().tolist(), "marker_vertices": c.get_paths()[0].vertices.tolist()}
                            for c in ax.collections]
    else:
        state["bars"] = [{"x": b.get_x() + b.get_width()/2, "y": b.get_height(), "width": b.get_width(),
                          "color": list(b.get_facecolor()), "hatch": b.get_hatch(), "alpha": b.get_alpha()}
                         for b in ax.patches]
    return state


def generate(artifact):
    # Validate all evidence before writing any target artifact.
    alias_evidence = validate_alias_evidence()
    source, selection = read_selection(artifact)
    out = PAPER / "figs" / artifact
    description = out / "description.text"
    wrapper = out / "table.tex"
    fig, ax = render(artifact, selection)
    state = artist_state(artifact, fig, ax)
    fig.savefig(out / "preview.pdf", metadata={"CreationDate": None, "ModDate": None})
    fig.savefig(out / "preview.png", dpi=300)
    plt.close(fig)
    selected = selection["selected_rows"]
    with (out / "selected_data.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(selected[0]))
        writer.writeheader()
        writer.writerows(selected)
    command = "/usr/bin/python3 RouterBSIPaper/scripts/figures6_7_ndcg1.py --artifact " + artifact
    text = (f"{artifact}: nDCG@1\n\nSource: {relative(source)}\nSource SHA256: {sha256(source)}\n"
            f"Source rows: {SPECS[artifact][2]}; selected rows: {len(selected)}.\nSelection: {SELECTIONS[artifact]}\n"
            "Source metric: Hit@1; display metric: nDCG@1. Exact source identity labels and CSV precision retained.\n"
            f"{ALIAS}\nBenchmark alias evidence: {alias_evidence['total_tasks']} tasks; zero empty-gold tasks; hashes/counts in selection_manifest.json.\n"
            "Scores are fractions, not percentages. Missing/invalid plotted values fail closed, never imputed.\n"
            "Source reportability: non-reportable\nAnalysis-only: source provenance does not certify publication validity.\n"
            f"{CAVEATS[artifact]}\nAggregation: task-instance weighted dataset means, not an equal-dataset mean; no new averaging.\n"
            "Uncertainty: not estimated; no error bars.\n\n"
            f"Scoped independent regeneration from project root:\n  {command}\n"
            "The absolute script path also works from any working directory. Only the named paper figure is written.\n"
            "Current portable provenance: selection_manifest.json beside this figure. The historical snapshot manifest remains unchanged.\n")
    (out / "provenance.text").write_text(text)
    manifest = {
        "schema_version": 1, "artifact": artifact, "artifact_path": relative(out),
        "path_base": "project_skill_selection", "metric": "Hit@1", "display_metric": "nDCG@1",
        "source": record(source), "source_row_count": SPECS[artifact][2], "selected_row_count": len(selected),
        "generator": record(__file__), "alias_evidence_file": record(Path(__file__).with_name("figures6_7_alias_evidence.json")),
        "regenerate": command, "selection": SELECTIONS[artifact], "points": selection["points"],
        "source_reportability": "non-reportable", "analysis_only": True, "caveats": CAVEATS[artifact],
        "metric_alias": ALIAS, "metric_alias_evidence": alias_evidence,
        "aggregation": "stored task-instance-weighted test mean; no new aggregation",
        "precision": "CSV strings preserved; Figure 7 stored means rounded to six decimals; annotations use three decimals",
        "missing_data_policy": "fail closed", "uncertainty_policy": "none estimated",
        "renderer_origin": "research-repo-template/paper/artifact_rendering.py:252-298,337-340,373-375,443-453; faithfully copied target branches",
        "rendered_artists": state,
        "outputs": [record(out / name) for name in ["preview.pdf", "preview.png", "selected_data.csv", "provenance.text"]],
        "manuscript_bindings": [record(description), record(wrapper)],
    }
    (out / "selection_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", choices=list(SPECS), help="default: both scoped figures")
    args = parser.parse_args()
    # Preflight both targets if invoked together, before either target changes.
    targets = [args.artifact] if args.artifact else list(SPECS)
    validate_alias_evidence()
    for artifact in targets:
        read_selection(artifact)
    for artifact in targets:
        manifest = generate(artifact)
        print(f"{artifact}: {manifest['selected_row_count']} Hit@1 values -> nDCG@1; PDF+PNG+CSV+manifest")


if __name__ == "__main__":
    main()
