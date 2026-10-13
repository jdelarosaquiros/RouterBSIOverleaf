# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib==3.10.8"]
# ///
"""Standalone diagnostic test nDCG@1 figure; run: uv run --script generate.py.

Reads only the exact all-splits CSV and its manifest. No imports from sibling
renderers, no inference, no recomputation from rounded precision/recall, and no
publication-eligibility promotion. The CLI writes only beside this script.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
from pathlib import Path
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ARTIFACT = "mbr_replay_test_ndcg@1_std"
SOURCE = ROOT / "BayesGSI/tables/routing_performance_by_iteration_std_all_splits/results.csv"
SOURCE_MANIFEST = SOURCE.with_name("manifest.json")
METHODS = ("Both Enabled", "Both Disabled", "Only MBR", "Only Gate")
CHECKPOINTS = ("initial", *map(str, range(1, 11)))
IDENTITY = {"Model": "Qwen3.5 4B", "Retriever": "SkillSight", "Split": "test", "Dataset": "Average"}
SOURCE_FIELDS = ("Model", "Retriever", "Method", "Split", "Evaluation", "Dataset",
                 "n_tasks", "Iteration", "n_runs", "Hit@1_mean", "Hit@1_variance")
STYLES = {
    "Both Enabled": dict(color="#009E73", marker="D", linestyle="-."),
    "Both Disabled": dict(color="#7A7A7A", marker="^", linestyle=":"),
    "Only MBR": dict(color="#0072B2", marker="o", linestyle="-"),
    "Only Gate": dict(color="#D55E00", marker="s", linestyle="--"),
}
CAPTION = (
    "Routing performance with MBR replay and held-out validation gating enabled or disabled. "
    "Lines show task-weighted test nDCG@1 (Hit@1) averaged across three runs; "
    "shaded bands indicate one population standard deviation. "
    "Iteration 0 denotes initialization. Analysis-only: source runs remain non-reportable."
)


def select_rows(rows):
    """Require the complete 4 x 11 selection; retain exact source CSV strings."""
    selected = {}
    for row_number, row in enumerate(rows, start=2):
        if not all(row.get(key) == value for key, value in IDENTITY.items()):
            continue
        method, iteration = row.get("Method"), row.get("Iteration")
        if method not in METHODS:
            raise ValueError(f"Unexpected condition at CSV row {row_number}: {method!r}")
        if iteration == "final":
            if row.get("Evaluation") != "snapshot":
                raise ValueError(f"Final must be a snapshot at CSV row {row_number}")
            continue
        if iteration not in CHECKPOINTS:
            raise ValueError(f"Unexpected checkpoint at CSV row {row_number}: {iteration!r}")
        key = method, iteration
        if key in selected:
            raise ValueError(f"Duplicate checkpoint: {key}")
        stage = "snapshot" if iteration == "initial" else "accepted"
        if row.get("Evaluation") != stage:
            raise ValueError(f"Wrong evaluation stage for {key}: expected {stage}")
        if row.get("n_tasks") != "748" or row.get("n_runs") != "3":
            raise ValueError(f"Expected 748 tasks and 3 runs for {key}")
        try:
            point = {field: row[field] for field in SOURCE_FIELDS}
            mean, variance = float(row["Hit@1_mean"]), float(row["Hit@1_variance"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Missing/invalid nDCG@1 fields for {key}") from exc
        if not math.isfinite(mean) or not 0 <= mean <= 1:
            raise ValueError(f"Invalid Hit@1_mean for {key}: {mean}")
        # Bounded [0,1] scores have Var <= mean * (1 - mean). Allow only
        # the documented six-decimal CSV rounding at that upper boundary.
        if not math.isfinite(variance) or variance < 0 or variance > mean * (1 - mean) + 1e-6:
            raise ValueError(f"Invalid Hit@1_variance for {key}: {variance}")
        point.update(x=CHECKPOINTS.index(iteration), source_csv_row=row_number,
                     Hit1_std=math.sqrt(variance))
        selected[key] = point
    expected = [(method, iteration) for method in METHODS for iteration in CHECKPOINTS]
    missing = [key for key in expected if key not in selected]
    if missing:
        raise ValueError(f"Missing test/Average checkpoints: {missing}")
    return [selected[key] for key in expected]


def load_source(source=SOURCE, source_manifest=SOURCE_MANIFEST):
    """Validate the consumed bytes against manifest before any output write."""
    source, source_manifest = Path(source), Path(source_manifest)
    csv_bytes = source.read_bytes()
    manifest_bytes = source_manifest.read_bytes()
    manifest = json.loads(manifest_bytes)
    digest = hashlib.sha256(csv_bytes).hexdigest()
    output = manifest.get("output", {})
    if output.get("sha256") != digest or output.get("bytes") != len(csv_bytes):
        raise ValueError("Source CSV hash/size disagrees with source manifest")
    if manifest.get("diagnostic_only") is not True:
        raise ValueError("Expected source diagnostic_only=true; do not silently promote reportability")
    reader = csv.DictReader(io.StringIO(csv_bytes.decode("utf-8"), newline=""))
    fields = reader.fieldnames or []
    if len(fields) != len(set(fields)) or not set(SOURCE_FIELDS).issubset(fields):
        raise ValueError("Missing or duplicate required source CSV columns")
    rows = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError("Malformed CSV row width")
    if manifest.get("row_count") != len(rows):
        raise ValueError("Source manifest row_count disagrees with CSV")
    points = select_rows(rows)
    runs = []
    for method in METHODS:
        matching = [run for run in manifest.get("runs", [])
                    if run.get("Model") == IDENTITY["Model"]
                    and run.get("Retriever") == IDENTITY["Retriever"]
                    and run.get("Method") == method]
        paths = [run.get("path") for run in matching]
        if len(matching) != 3 or len(set(paths)) != 3 or not all(paths):
            raise ValueError(f"Source manifest requires 3 distinct runs for {method}")
        for run in matching:
            completion = run.get("completion", {})
            if (run.get("split_sizes", {}).get("test") != 748
                    or run.get("iterations") != list(range(1, 11))):
                raise ValueError(f"Wrong manifest task/checkpoint coverage for {method}")
            if (not isinstance(completion, dict) or completion.get("reportable") is not False
                    or completion.get("status") != "completed_noncanonical"
                    or not completion.get("nonreportable_reason")):
                raise ValueError(f"Missing/changed non-reportable completion metadata for {method}")
            runs.append({key: run[key] for key in
                         ("Model", "Retriever", "Method", "path", "split_sizes", "iterations", "completion")})
    provenance = {
        "source": str(source.relative_to(ROOT)) if source.is_relative_to(ROOT) else str(source),
        "source_sha256": digest,
        "source_manifest": str(source_manifest.relative_to(ROOT)) if source_manifest.is_relative_to(ROOT) else str(source_manifest),
        "source_manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "source_csv_hash_verified_against_manifest": True,
        "source_row_count": len(rows),
        "diagnostic_only": True,
        "reportable": False,
        "source_runs": runs,
        "source_definitions": manifest.get("definitions", {}),
    }
    return points, provenance


def build_figure(points):
    """Match the original four-series styling; plot nDCG@1 mean +/- population SD."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Recheck coverage and moments even for callers using the renderer directly.
    checked = select_rows(points)
    for point, verified in zip(points, checked):
        if (point["Method"], point["Iteration"], point["x"], point["Hit1_std"]) != (
                verified["Method"], verified["Iteration"], verified["x"], verified["Hit1_std"]):
            raise ValueError("Renderer inputs must match selected order, x and exact sqrt(variance)")
    with plt.rc_context({
        "font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 10, "axes.labelsize": 11, "legend.fontsize": 9,
        "pdf.fonttype": 42, "ps.fonttype": 42, "axes.spines.top": False,
        "axes.spines.right": False, "axes.grid": True, "grid.alpha": .22,
        "grid.linewidth": .5,
    }):
        fig, ax = plt.subplots(figsize=(6.75, 3.4), layout="constrained")
        lower_bounds, upper_bounds = [], []
        for method in METHODS:
            group = [point for point in points if point["Method"] == method]
            xs = [p["x"] for p in group]
            ys = [float(p["Hit@1_mean"]) for p in group]
            lower = [y - p["Hit1_std"] for y, p in zip(ys, group)]
            upper = [y + p["Hit1_std"] for y, p in zip(ys, group)]
            ax.plot(xs, ys, label=method, linewidth=1.8, markersize=4.5,
                    markeredgewidth=.6, markeredgecolor="white", **STYLES[method])
            ax.fill_between(xs, lower, upper, color=STYLES[method]["color"], alpha=.13, linewidth=0)
            lower_bounds.extend(lower)
            upper_bounds.extend(upper)
        ax.set_title("Qwen3.5 4B / SkillSight", fontsize=10, pad=10)
        ax.set_xlabel("Iteration (0 = initial)")
        ax.set_ylabel("nDCG@1")
        ax.set_xticks(range(0, 11, 2))
        # Do not clip or truncate uncertainty bands to the metric's [0,1] range.
        ax.set_ylim(min(lower_bounds) - .06, max(upper_bounds) + .04)
        ax.legend(ncol=2, loc="lower right", framealpha=.92)
        fig.canvas.draw()
    return fig, ax


def generate(output=HERE, source=SOURCE, source_manifest=SOURCE_MANIFEST):
    """Validate first, stage outputs, then publish only the local artifact set.

    Path arguments are for isolated test fixtures; the CLI has no overrides.
    Validation failures leave all previously published files byte-identical.
    """
    points, provenance = load_source(source, source_manifest)
    fig, ax = build_figure(points)
    import matplotlib
    import matplotlib.pyplot as plt

    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix=".generate-", dir=output) as temporary:
            stage = Path(temporary)
            with matplotlib.rc_context({"pdf.fonttype": 42, "ps.fonttype": 42}):
                fig.savefig(stage / "preview.pdf", bbox_inches="tight",
                            metadata={"CreationDate": None, "ModDate": None})
                fig.savefig(stage / "preview.png", bbox_inches="tight", dpi=300)
            with (stage / "selected_data.csv").open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=list(points[0]))
                writer.writeheader()
                writer.writerows(points)
            (stage / "description.text").write_text(CAPTION + "\n", encoding="utf-8")
            (stage / "table.tex").write_text(
                "\\begin{figure}[!htbp]\n\\centering\n"
                f"\\includegraphics[width=\\linewidth]{{figs/{ARTIFACT}/preview.pdf}}\n"
                f"\\caption[Replay and validation-gate ablation: test nDCG@1]{{\\input{{figs/{ARTIFACT}/description.text}}}}\n"
                f"\\label{{fig:{ARTIFACT}}}\n\\end{{figure}}\n", encoding="utf-8")
            reasons = sorted({run["completion"]["nonreportable_reason"] for run in provenance["source_runs"]})
            notes = (
                f"Artifact: {ARTIFACT}\n"
                f"Source: {provenance['source']}\nSource SHA256: {provenance['source_sha256']}\n"
                f"Source manifest: {provenance['source_manifest']}\n"
                f"Source manifest SHA256: {provenance['source_manifest_sha256']}\n"
                "The consumed CSV bytes/size are verified against source manifest output.sha256/bytes.\n"
                f"Source rows: {provenance['source_row_count']}; selected rows: {len(points)}.\n"
                "Selection: exact Model=Qwen3.5 4B, Retriever=SkillSight, Split=test, Dataset=Average.\n"
                "Conditions: Both Enabled, Both Disabled, Only MBR, Only Gate; 3 runs and 748 tasks per point.\n"
                "Coverage: initial/snapshot at x=0, then 1--10/accepted; final snapshots excluded.\n"
                "Metric: Hit@1 displayed as nDCG@1 (equal under binary relevance), from Hit@1_mean; population variance from Hit@1_variance (ddof=0).\n"
                "Band: Hit@1_mean +/- sqrt(Hit@1_variance), using CSV-rounded variance, not raw-run recomputation.\n"
                "Hit1_std retains the full Python float sqrt result; no further rounding or clipping.\n"
                "Within-run Average is task-weighted over 748 test tasks (dataset means weighted by n_tasks); "
                "the table then takes the mean and population variance across three runs. "
                "This is not temporal variation, "
                "task-level dispersion, a standard error, or a confidence interval.\n"
                "No imputation, interpolation, or extrapolation. Source metric keys remain Hit@1; display label is nDCG@1.\n"
                "Source reportability: diagnostic_only=true; reportable=false; completed_noncanonical.\n"
                "Analysis-only, non-reportable: this rendering does not establish publication eligibility.\n"
                "Nonreportable reason(s): " + " | ".join(reasons) + "\n"
                "Scope: manuscript integration; no publication-eligibility promotion or sibling changes.\n"
                "Reproduce from project_skill_selection: uv run --script "
                f"RouterBSIPaper/figs/{ARTIFACT}/generate.py\n"
            )
            (stage / "provenance.text").write_text(notes, encoding="utf-8")
            manifest = dict(
                provenance, artifact=ARTIFACT, metric="Hit@1", display_metric="nDCG@1",
                metric_equivalence="Binary relevance: nDCG@1 equals Hit@1", mean_field="Hit@1_mean",
                variance_field="Hit@1_variance", std_formula="sqrt(Hit@1_variance)",
                uncertainty="mean +/- one population SD (ddof=0); not a confidence interval",
                variance_precision="source CSV-rounded variance; no additional rounding",
                filters=IDENTITY, coverage={method: list(CHECKPOINTS) for method in METHODS},
                evaluation_by_checkpoint={i: "snapshot" if i == "initial" else "accepted" for i in CHECKPOINTS},
                excluded="final snapshots and all other model/retriever/split/dataset rows",
                n_runs_per_point=3, n_tasks_per_point=748, selected_row_count=len(points),
                points=points, styles=STYLES, y_limits=list(ax.get_ylim()),
                generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                renderer={"library": "matplotlib", "version": matplotlib.__version__, "png_dpi": 300},
                output_sha256={path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                               for path in sorted(stage.iterdir())},
            )
            (stage / "selection_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
            # Publish manifest last so it never certifies files still in staging.
            for path in sorted(stage.iterdir(), key=lambda p: (p.name == "selection_manifest.json", p.name)):
                path.replace(output / path.name)
    finally:
        plt.close(fig)
    return manifest


if __name__ == "__main__":
    result = generate()
    print(f"PASS: {result['selected_row_count']} test nDCG@1 points, 4 conditions, initial + 1..10; "
          "source hash verified; diagnostic-only/non-reportable.")
    for name in ("description.text", "preview.pdf", "preview.png", "provenance.text",
                 "selected_data.csv", "table.tex", "selection_manifest.json"):
        print(HERE / name)
