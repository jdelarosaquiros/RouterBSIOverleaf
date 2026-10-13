# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib==3.10.8"]
# ///
"""Standalone, offline RouterBSI test trajectory from raw saved predictions.

Run: uv run --script generate.py. Writes only beside this script. No imports
from sibling generators, precomputed tables, model calls, or raw-run writes.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any
import statistics
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ARTIFACT = "routerbsi_test_ndcg@1_std"
SOURCE = ROOT / ".wisc/results/GatedRouter/sra_full_skillsight_f1_i10_l400_qwen3.5_4b"
RUNS = ("run_1", "run_2", "run_3")
CHECKPOINTS = ("initial", *map(str, range(1, 11)), "final")
LABELS = ("Cold\nstart", *map(str, range(1, 11)), "Final")
N_TASKS = 748
COLOR = "#009E73"
CAPTION = (
    "RouterBSI test routing performance from cold start through iterations 1--10 "
    "and the saved final evaluation (Final duplicates iteration 10, not an additional update). "
    "The line shows mean nDCG@1 across three runs; "
    "the shaded band shows one population standard deviation. "
    "Analysis-only: source runs remain non-reportable."
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def object_digest(value):
    return digest(json.dumps(value, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=False, allow_nan=False).encode("utf-8"))


def path_label(path):
    path = Path(path).resolve()
    return str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)


def read_source(path, inputs, jsonl=False) -> Any:
    """Hash the very same bytes that are parsed, not a different file read."""
    path = Path(path)
    require(path.is_file(), f"Missing source: {path}")
    data = path.read_bytes()
    key = path_label(path)
    record = {"sha256": digest(data), "bytes": len(data)}
    require(key not in inputs or inputs[key] == record, f"Source drift: {key}")
    inputs[key] = record
    if jsonl:
        lines = data.decode("utf-8").splitlines()
        require(all(line.strip() for line in lines), f"Blank JSONL record: {path}")
        return [json.loads(line) for line in lines]
    return json.loads(data)


def checkpoint_paths(run, checkpoint):
    require(checkpoint in CHECKPOINTS, f"Unexpected checkpoint {checkpoint}")
    run = Path(run)
    if checkpoint in ("initial", "final"):
        return (run / f"predictions/{checkpoint}_test.jsonl",
                run / f"metrics/{checkpoint}_test.json",
                run / f"conditions_{checkpoint}.json", None)
    folder = run / "iterations" / f"{int(checkpoint):02d}"
    return (folder / f"test_accepted_{int(checkpoint):02d}.jsonl",
            folder / f"test_accepted_{int(checkpoint):02d}.json",
            folder / "conditions_accepted.json", folder / "ledger.json")


def validate_completion(completion):
    require(completion.get("status") == "completed_noncanonical"
            and completion.get("reportable") is False
            and completion.get("analysis_ready") is True
            and completion.get("passed") is True
            and bool(completion.get("nonreportable_reason"))
            and completion.get("split_counts", {}).get("test") == N_TASKS,
            "Missing/changed non-reportable completion metadata")


def id_list(value, name, nonempty=True):
    require(isinstance(value, list) and (bool(value) or not nonempty)
            and all(isinstance(x, str) and x for x in value), f"Invalid {name}")
    require(len(value) == len(set(value)), f"Duplicate {name}")
    return value


def evaluate_records(records, task_ids, policy, reference_gold=None):
    """Binary nDCG@1 = 1[top-ranked ID in nonempty required_ids].

    An empty ranking scores zero; missing/non-list rankings and empty gold fail.
    Policy binding checks all retrieved candidates, not only the top-ranked ID.
    """
    require(len(records) == N_TASKS, "Expected exactly 748 prediction records")
    seen, gold, reciprocal_ranks, hits = set(), {}, [], 0
    library_hash = policy.get("library_hash")
    require(isinstance(library_hash, str) and len(library_hash) == 64,
            "Invalid saved policy library hash")
    require(object_digest(policy.get("conditions")) == library_hash, "Saved policy content hash mismatch")
    conditions = policy.get("conditions", {}).get("sra", {})
    require(bool(conditions), "Missing saved sra conditions")
    for row in records:
        task = row.get("task_id")
        require(isinstance(task, str) and task in task_ids, "Unknown test task")
        require(task not in seen, f"Duplicate test task: {task}")
        seen.add(task)
        require(row.get("tier") == "sra" and row.get("label_source") == "core_gt_ids",
                f"Wrong tier/label source: {task}")
        required = id_list(row.get("required_ids"), "required_ids")
        ranked = id_list(row.get("ranked_ids"), "ranked_ids", nonempty=False)
        candidates = id_list(row.get("candidate_ids"), "candidate_ids")
        require(set(ranked).issubset(candidates), f"Ranking outside candidates: {task}")
        statements = row.get("candidate_statements")
        require(isinstance(statements, list) and len(statements) == len(candidates),
                f"Missing candidate statements: {task}")
        require(row.get("library_hash") == library_hash, f"Policy hash mismatch: {task}")
        require(all(c in conditions and conditions[c] == s
                    for c, s in zip(candidates, statements)), f"Policy statement mismatch: {task}")
        task_hash = row.get("task_hash")
        require(isinstance(task_hash, str) and len(task_hash) == 64, "Invalid task hash")
        gold[task] = {"required_ids": sorted(required), "task_hash": task_hash, "tier": "sra"}
        hits += int(bool(ranked) and ranked[0] in required)
        reciprocal_ranks.append(next((1.0 / i for i, skill in enumerate(ranked[:10], 1)
                                      if skill in required), 0.0))
    require(seen == set(task_ids), "Incomplete test membership")
    if reference_gold is not None:
        require(gold == reference_gold, "Test gold/task identity drift")
    return {"n_tasks": len(records), "hits_at_1": hits, "ndcg1": hits / len(records),
            "mrr10": math.fsum(reciprocal_ranks) / len(records),
            "gold_sha256": object_digest(gold),
            "task_membership_sha256": object_digest(sorted(seen)),
            "policy_binding": "all_candidate_statements_verified"}, gold


def crosscheck_metrics(metrics, values):
    saved = metrics.get("all", {})
    require(saved.get("count") == N_TASKS, "Saved metrics task count mismatch")
    result = {}
    for key, derived, required in (("Hit@1", values["ndcg1"], False),
                                   ("MRR@10", values["mrr10"], True)):
        present = key in saved
        require(present or not required, f"Missing saved {key}")
        value = saved.get(key)
        if present:
            require(isinstance(value, (int, float)) and not isinstance(value, bool)
                    and math.isfinite(value) and 0 <= value <= 1
                    and math.isclose(value, derived, abs_tol=1e-12, rel_tol=0),
                    f"Saved {key} mismatch")
        field = "hit1" if key == "Hit@1" else "mrr10"
        result[f"saved_{field}"] = value
        result[f"{field}_crosscheck"] = "verified" if present else "unavailable_not_stored"
    return result


def aggregate(rows):
    expected = [(run, checkpoint) for run in RUNS for checkpoint in CHECKPOINTS]
    require([(r["run"], r["checkpoint"]) for r in rows] == expected,
            "Expected exact ordered 3 x 12 run/checkpoint coverage")
    points = []
    for x, checkpoint in enumerate(CHECKPOINTS):
        selected = [r for r in rows if r["checkpoint"] == checkpoint]
        vals = [r["ndcg1"] for r in selected]
        require(all(isinstance(v, (float, int)) and math.isfinite(v) and 0 <= v <= 1
                    for v in vals), "Invalid run metric")
        mean = statistics.mean(vals)
        variance = statistics.pvariance(vals)
        sd = math.sqrt(variance)
        points.append({"method": "RouterBSI", "model": "Qwen3.5 4B", "retriever": "SkillSight",
                       "split": "test", "checkpoint": checkpoint, "x": x,
                       "evaluation": "snapshot" if checkpoint in ("initial", "final") else "accepted",
                       "n_runs": 3, "n_tasks_per_run": N_TASKS,
                       **{run: value for run, value in zip(RUNS, vals)},
                       "mean": mean, "population_variance": variance, "population_sd": sd,
                       "lower": mean - sd, "upper": mean + sd})
    return points


def verify_input_hashes(inputs):
    for name, metadata in inputs.items():
        path = ROOT / name
        require(path.is_file() and digest(path.read_bytes()) == metadata["sha256"],
                f"Source drift before publication: {name}")


def load_source(source=SOURCE):
    """Only the 36 specified test evaluations are consumed; no run-wide audit."""
    source = Path(source)
    inputs, rows, runs = {}, [], []
    reference_gold, reference_tasks = None, None
    for run_name in RUNS:
        run = source / run_name
        completion = read_source(run / "completion.json", inputs)
        validate_completion(completion)
        config = read_source(run / "config.json", inputs)
        require(config.get("model") == "Qwen/Qwen3.5-4B"
                and config.get("retrieval_backend") == "sra_skillsight"
                and config.get("iterations") == 10
                and config.get("replay_mbr_enabled") is True
                and config.get("validation_gate_enabled") is True,
                "Unexpected run model/retriever/iteration/condition configuration")
        state = read_source(run / "test_state.json", inputs)
        tasks = id_list(state.get("task_ids"), "test_state.task_ids")
        require(len(tasks) == N_TASKS and state.get("status") == "complete", "Incomplete test state")
        tasks = set(tasks)
        require(reference_tasks is None or tasks == reference_tasks, "Cross-run test membership drift")
        reference_tasks = tasks
        require(sorted(p.name for p in (run / "iterations").iterdir() if p.is_dir())
                == [f"{i:02d}" for i in range(1, 11)], "Missing/unexpected iteration directories")
        previous_hash = None
        for checkpoint in CHECKPOINTS:
            pred_path, metric_path, policy_path, ledger_path = checkpoint_paths(run, checkpoint)
            policy = read_source(policy_path, inputs)
            ledger = read_source(ledger_path, inputs) if ledger_path else None
            if ledger is not None:
                require(ledger.get("iteration") == int(checkpoint)
                        and isinstance(ledger.get("accepted"), bool)
                        and ledger.get("accepted_hash") == policy.get("library_hash")
                        and ledger.get("before_hash") == previous_hash,
                        "Accepted policy/ledger chain mismatch")
            elif checkpoint == "final":
                require(policy.get("library_hash") == previous_hash == state.get("library_hash"),
                        "Final policy does not match last accepted policy/test_state")
            previous_hash = policy.get("library_hash")
            records = read_source(pred_path, inputs, jsonl=True)
            values, gold = evaluate_records(records, tasks, policy, reference_gold)
            if reference_gold is None:
                reference_gold = gold
            values.update(crosscheck_metrics(read_source(metric_path, inputs), values))
            row = {"run": run_name, "checkpoint": checkpoint, "split": "test",
                   "evaluation": "snapshot" if ledger is None else "accepted",
                   **values, "prediction_source": path_label(pred_path),
                   "prediction_sha256": inputs[path_label(pred_path)]["sha256"],
                   "metrics_source": path_label(metric_path),
                   "metrics_sha256": inputs[path_label(metric_path)]["sha256"],
                   "policy_source": path_label(policy_path),
                   "policy_sha256": inputs[path_label(policy_path)]["sha256"],
                   "policy_library_hash": policy["library_hash"],
                   "ledger_source": path_label(ledger_path) if ledger_path else None,
                   "ledger_sha256": inputs[path_label(ledger_path)]["sha256"] if ledger_path else None,
                   "ledger_accepted": ledger["accepted"] if ledger else None,
                   "final_duplicates_iteration10": (inputs[path_label(pred_path)]["sha256"] == rows[-1]["prediction_sha256"]
                                                   if checkpoint == "final" else None),
                   "status": completion["status"], "reportable": completion["reportable"]}
            if checkpoint == "final":
                require(row["final_duplicates_iteration10"], "Final no longer duplicates iteration 10; revise caption explicitly")
            rows.append(row)
        runs.append({"run": run_name, "path": path_label(run), "completion": completion,
                     "seed": config.get("seed"),
                     "initial_skills_cache": config.get("initial_skills_cache"),
                     "config_source": path_label(run / "config.json"),
                     "test_state_source": path_label(run / "test_state.json"),
                     "initial_policy_library_hash": rows[-12]["policy_library_hash"],
                     "final_policy_library_hash": rows[-1]["policy_library_hash"]})
    points = aggregate(rows)
    return points, rows, {"source_root": path_label(source), "inputs": inputs,
                          "source_runs": runs, "diagnostic_only": True, "reportable": False}



def build_figure(points):
    """Twelve equally spaced categorical checkpoints at final column width."""
    require(len(points) == 12 and [p["checkpoint"] for p in points] == list(CHECKPOINTS)
            and [p["x"] for p in points] == list(range(12)), "Invalid plotted coverage/order")
    for point in points:
        vals = [point[run] for run in RUNS]
        require(all(math.isfinite(v) and 0 <= v <= 1 for v in vals), "Invalid plotted run values")
        mean, variance = statistics.mean(vals), statistics.pvariance(vals)
        sd = math.sqrt(variance)
        require((point["mean"], point["population_variance"], point["population_sd"],
                 point["lower"], point["upper"]) == (mean, variance, sd, mean - sd, mean + sd),
                "Renderer inputs disagree with full-precision run statistics")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator

    with plt.rc_context({"font.family": "DejaVu Serif", "font.size": 8,
                         "axes.labelsize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8,
                         "legend.fontsize": 8, "pdf.fonttype": 42, "ps.fonttype": 42,
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.linewidth": .6, "axes.grid": True,
                         "grid.alpha": .22, "grid.linewidth": .5}):
        fig, ax = plt.subplots(figsize=(218 / 72, 154 / 72))
        fig.subplots_adjust(left=.18, right=.90, bottom=.28, top=.86)
        xs = [p["x"] for p in points]
        ax.plot(xs, [p["mean"] for p in points], color=COLOR, marker="D", linestyle="-.",
                label="RouterBSI", linewidth=1.3, markersize=3.0,
                markeredgecolor="white", markeredgewidth=.4)
        ax.fill_between(xs, [p["lower"] for p in points], [p["upper"] for p in points],
                        color=COLOR, alpha=.15, linewidth=0)
        ax.set_xticks(xs, LABELS)
        ax.get_xticklabels()[0].set_horizontalalignment("right")
        ax.get_xticklabels()[-1].set_horizontalalignment("left")
        ax.tick_params(axis="both", length=2.5, width=.6, pad=3)
        ax.set_xlim(-.35, 11.95)
        ax.set_ylim(min(p["lower"] for p in points) - .018,
                    max(p["upper"] for p in points) + .018)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
        ax.set_ylabel("nDCG@1", labelpad=3)
        ax.set_xlabel("Iteration", labelpad=4)
        ax.legend(loc="lower left", bbox_to_anchor=(0, 1.01), borderaxespad=0,
                  frameon=False, handlelength=2.5)
        fig.canvas.draw()
    return fig, ax


def readability_report(fig, ax):
    renderer = fig.canvas.get_renderer()
    texts = [*ax.get_xticklabels(), *ax.get_yticklabels(), ax.xaxis.label, ax.yaxis.label,
             *ax.get_legend().get_texts()]
    visible = [t for t in texts if t.get_visible() and t.get_text()
               and t.get_window_extent(renderer).overlaps(ax.figure.bbox)]
    tick_boxes = [t.get_window_extent(renderer) for t in ax.get_xticklabels()]
    require(all(not a.overlaps(b) for a, b in zip(tick_boxes, tick_boxes[1:])),
            "Category label overlap")
    measurements = []
    for text in visible:
        box = text.get_window_extent(renderer)
        require(box.x0 >= 0 and box.y0 >= 0 and box.x1 <= fig.bbox.width
                and box.y1 <= fig.bbox.height, f"Clipped text: {text.get_text()}")
        measurements.append({"text": text.get_text(), "size_pt": text.get_fontsize(),
                             "bbox_points_bottom_origin": [v * 72 / fig.dpi for v in box.extents]})
    return {"artifact": ARTIFACT,
            "scope": "Current standalone Agg artist measurements; supersedes copied readability metadata. "
                     "No manuscript figure number or composed-TeX validation is asserted.",
            "generator_sha256": digest(Path(__file__).read_bytes()),
            "measurements": {"width_pt": fig.get_figwidth() * 72,
                             "height_pt": fig.get_figheight() * 72,
                             "font_sizes_pt": sorted({t.get_fontsize() for t in visible}),
                             "text": measurements},
            "checks": {"category_labels_nonoverlapping": True, "visible_text_within_canvas": True},
            "actual_artists": {"lines": [{"label": l.get_label(), "x": l.get_xdata().tolist(),
                                           "y": l.get_ydata().tolist(), "color": l.get_color(),
                                           "marker": l.get_marker(), "linestyle": l.get_linestyle()}
                                          for l in ax.lines],
                               "bands": [b.get_paths()[0].vertices.tolist() for b in ax.collections],
                               "xlim": list(ax.get_xlim()), "ylim": list(ax.get_ylim())}}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def generate(output=HERE, source=SOURCE) -> dict[str, Any]:
    """Validate and stage before publication; CLI has no destination override.

    The output/source arguments support local isolated regression fixtures only.
    Python floats use round-trip serialization; integer hits retain exact ratios.
    """
    output = Path(output).resolve()
    require(output == HERE or output.is_relative_to(HERE), "Outputs must stay within this figure folder")
    points, rows, provenance = load_source(source)
    fig, ax = build_figure(points)
    import matplotlib
    import matplotlib.pyplot as plt
    try:
        reading = readability_report(fig, ax)
        output.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".generate-", dir=output) as temp:
            stage = Path(temp)
            with matplotlib.rc_context({"pdf.fonttype": 42, "ps.fonttype": 42}):
                fig.savefig(stage / "preview.pdf", metadata={"CreationDate": None, "ModDate": None})
                fig.savefig(stage / "preview.png", dpi=300)
            write_csv(stage / "selected_data.csv", points)
            write_csv(stage / "per_run_data.csv", rows)
            (stage / "description.text").write_text(CAPTION + "\n", encoding="utf-8")
            (stage / "table.tex").write_text(
                "\\begin{figure}[!htbp]\n\\centering\n"
                f"\\includegraphics[width=\\linewidth]{{figs/{ARTIFACT}/preview.pdf}}\n"
                f"\\caption[RouterBSI test routing trajectory]{{\\input{{figs/{ARTIFACT}/description.text}}}}\n"
                f"\\label{{fig:{ARTIFACT}}}\n\\end{{figure}}\n", encoding="utf-8")
            reasons = sorted({r["completion"]["nonreportable_reason"] for r in provenance["source_runs"]})
            notes = (
                f"Artifact: {ARTIFACT}\nSource root: {provenance['source_root']}\n"
                "Method/model/retriever/split: RouterBSI / Qwen3.5 4B / SkillSight / test.\n"
                "Exact coverage: run_1, run_2, run_3 x initial, 1..10, final = 36 evaluations.\n"
                "Cold start and Final are saved snapshots; 1..10 are accepted-policy test evaluations.\n"
                "Final is a separate saved categorical snapshot, not iteration 11. Its prediction bytes and policy match\n"
                "iteration 10 in all three runs: no extra training update or independent evaluation repeat is implied.\n"
                "No imputation or extrapolation.\n"
                "Metric: binary nDCG@1 = 1[ranked_ids[0] in required_ids]; an empty ranking scores zero.\n"
                "Every task has verified nonempty binary gold, so this equals Hit@1; no claim about empty-gold conventions.\n"
                "Within run: equally weighted mean over exactly 748 unique test tasks. Stable task membership, task hashes,\n"
                "and gold labels are checked across all 36 files. Across runs: arithmetic mean and population SD (ddof=0).\n"
                "The band is mean +/- one population SD without clipping or CSV rounding. Integer hits and full-precision\n"
                "run scores are in per_run_data.csv; selected_data.csv contains exact round-trip float means and moments.\n"
                "This is across-run variation in test performance of the predicate policies, not predicate length,\n"
                "temporal variation, task-level dispersion, standard error, confidence interval, or a significance test.\n"
                "All metrics are derived from raw rankings, never imported from an aggregate figure table.\n"
                "Stored Hit@1 is checked whenever present; absent values are explicitly unavailable_not_stored.\n"
                "Stored MRR@10 is independently recomputed and checked for every evaluation (absolute tolerance 1e-12).\n"
                "All candidate_statements match the saved initial/accepted/final policy, and policy library hashes\n"
                "match predictions; numbered policies are chained through ledger.before_hash/accepted_hash.\n"
                "Three runs, not three seeds: all use seed=20260324 with distinct initial predicate policies/cache files.\n"
                "Run 1 has a different source_manifest_sha256 from runs 2/3 (retained in completion metadata);\n"
                "matching archived task/gold identities does not imply equivalent source builds or independent seeds.\n"
                "Full input-file SHA256 hashes are in selection_manifest.json.\n"
                "Source status: completed_noncanonical; reportable=false; diagnostic_only=true.\n"
                "Analysis-only: complete saved evidence does not establish publication eligibility or validate source audits.\n"
                "Nonreportable reasons: " + " | ".join(reasons) + "\n"
                "Scope: standalone inactive artifact; no manuscript integration or raw-run/sibling changes.\n"
                f"Reproduce: uv run --script RouterBSIPaper/figs/{ARTIFACT}/generate.py\n"
                f"Test: uv run --script RouterBSIPaper/figs/{ARTIFACT}/test_generate.py -v\n"
            )
            (stage / "provenance.text").write_text(notes, encoding="utf-8")
            reading["outputs"] = {n: digest((stage / n).read_bytes()) for n in ("preview.pdf", "preview.png")}
            write_json(stage / "readability_manifest.json", reading)
            verify_input_hashes(provenance["inputs"])
            manifest = dict(provenance, artifact=ARTIFACT,
                            artifact_path=f"RouterBSIPaper/figs/{ARTIFACT}",
                            metric="nDCG@1", equivalent_binary_metric="Hit@1",
                            formula="sum(1[ranked_ids nonempty and ranked_ids[0] in required_ids]) / 748",
                            cutoff=1, gold_policy="all required_ids nonempty; exact stable labels and task hashes",
                            mean_formula="arithmetic mean of 3 run task means",
                            variance_formula="sum((run_mean - mean)**2) / 3",
                            uncertainty="mean +/- population SD, ddof=0; not CI/SE/significance",
                            precision="unrounded float round-trip serialization; exact integer hit counts retained",
                            source_hash_scope="whole bytes of every consumed raw input; rechecked before publication",
                            checkpoint_order=list(CHECKPOINTS), display_labels=list(LABELS),
                            coverage={run: list(CHECKPOINTS) for run in RUNS},
                            selected_row_count=12, evaluation_count=36, n_runs=3, n_tasks_per_evaluation=N_TASKS,
                            evaluations=rows, points=points,
                            source_flags={"ranking_derived": True, "stored_hit1_missing_allowed": True,
                                          "all_mrr10_crosschecks_verified": True, "all_policy_bindings_verified": True},
                            generator_sha256=digest(Path(__file__).read_bytes()),
                            test_sha256=digest((HERE / "test_generate.py").read_bytes()),
                            renderer={"library": "matplotlib", "version": matplotlib.__version__,
                                      "png_dpi": 300, "width_pt": 218, "height_pt": 154,
                                      "color": COLOR, "line_count": 1, "band_count": 1,
                                      "y_limits": list(ax.get_ylim())},
                            output_sha256={f.name: digest(f.read_bytes()) for f in sorted(stage.iterdir())})
            write_json(stage / "selection_manifest.json", manifest)
            for path in sorted(stage.iterdir(), key=lambda p: (p.name == "selection_manifest.json", p.name)):
                path.replace(output / path.name)
        return manifest
    finally:
        plt.close(fig)


if __name__ == "__main__":
    result = generate()
    print(f"PASS: {result['evaluation_count']} raw evaluations -> {result['selected_row_count']} points; "
          "3 runs, 748 test tasks, mean +/- population SD; non-reportable.")
    print(HERE)
    for point in (result["points"][0], result["points"][-1]):
        print(f"{point['checkpoint']}: {point['mean']!r} +/- {point['population_sd']!r}")
