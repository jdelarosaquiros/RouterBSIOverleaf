#!/usr/bin/env python3
"""Render ONLY Figures 3,5,6,7 at 218 PDF points from frozen paper evidence.

Run: python scripts/render_acl_readable_figures.py
Requires matplotlib, numpy, PyMuPDF. No external evidence is loaded, no experiments
are run, no captions/TeX/selected data/historical provenance are rewritten.
Each target receives preview.pdf, preview.png and readability_manifest.json.
The latter supersedes only historical rendering/output metadata, not evidence.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import tempfile
from typing import Any, cast

import fitz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba
from matplotlib.patches import Patch
from matplotlib.text import Text
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RET = "average_retention_degradation"
REPLAY = "mbr_replay_test_ndcg@1_std"
TOKEN = "performance_token_usage"
LLMS = "routing_performance_across_llms_init"
SPECS = {
    RET: (3, "selection.json", "8fcc09dc76b3172d925e8068cc130e82d8885dbe1aaacdf17fb0d2685a2a25f0", 114),
    REPLAY: (5, "selected_data.csv", "d9a19451782771fb3d17f6a5a3b4fd74af72fea225d825021413f891c00d1f5e", 112),
    TOKEN: (6, "selected_data.csv", "ba0fc6824888296f67d550a1a579254728eb13e1a3705203bfb448ad82f48e67", 112),
    LLMS: (7, "selected_data.csv", "f9e157ff71f44b356f7f4ef5d000d79ba8ebd25bf3eef78811a61d29ea6fa9ce", 120),
}
METHODS = ("Both Enabled", "Both Disabled", "Only MBR", "Only Gate")
STYLES: dict[str, dict[str, Any]] = {
    "Both Enabled": dict(color="#009E73", marker="D", linestyle="-."),
    "Both Disabled": dict(color="#7A7A7A", marker="^", linestyle=":"),
    "Only MBR": dict(color="#0072B2", marker="o", linestyle="-"),
    "Only Gate": dict(color="#D55E00", marker="s", linestyle="--"),
}
RET_METHODS = ("Retriever baseline", "LLM Select", "SkillRouter", "SkillDAG", "Skill-Pro", "RouterBSI")
RET_COLORS = ("#777777", "#0072B2", "#E69F00", "#009E73", "#CC79A7", "#D55E00")
RET_MARKERS = ("o", "s", "^", "D", "v", "P")
RET_STYLES = (":", "--", "-.", "--", "-.", "-")
POSITIONS = [0, .80, 1.32, 2.12, 2.64, 3.44, 3.96]
BAR_COLORS = ["#7A7A7A", "#0072B2", "#0072B2", "#D55E00", "#D55E00", "#009E73", "#009E73"]
RC = {"font.family": "serif", "font.serif": ["Times New Roman", "DejaVu Serif"],
      "font.size": 8, "axes.labelsize": 9, "axes.titlesize": 9, "legend.fontsize": 8,
      "xtick.labelsize": 8, "ytick.labelsize": 8, "pdf.fonttype": 42,
      "ps.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False,
      "axes.linewidth": .55, "xtick.major.width": .5, "ytick.major.width": .5,
      "xtick.major.size": 2, "ytick.major.size": 2,
      "xtick.major.pad": 2, "ytick.major.pad": 2, "axes.labelpad": 2,
      "axes.grid": True, "grid.alpha": .22, "grid.linewidth": .5,
      "savefig.bbox": None, "mathtext.fontset": "dejavuserif"}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(artifact):
    _, filename, expected, _ = SPECS[artifact]
    path = ROOT / "figs" / artifact / filename
    if sha(path) != expected:
        raise ValueError(f"Frozen selection changed: {path}")
    if artifact == RET:
        rows = json.loads(path.read_text())["points"]
        assert len(rows) == 30
        assert [r["Method"] for r in rows] == [m for m in RET_METHODS for _ in range(5)]
        for m in RET_METHODS:
            group = [r for r in rows if r["Method"] == m]
            assert [r["x"] for r in group] == [50, 25, 10, 5, 1]
            assert [r["position"] for r in group] == list(range(5))
    else:
        with path.open(newline="") as handle:
            rows = list(csv.DictReader(handle))
        assert len(rows) == {REPLAY: 44, TOKEN: 4, LLMS: 7}[artifact]
        if artifact == REPLAY:
            assert [(r["Method"], int(r["x"])) for r in rows] == [(m, x) for m in METHODS for x in range(11)]
            for r in rows:
                assert float(r["Hit1_std"]) == math.sqrt(float(r["Hit@1_variance"]))
                assert r["Split"] == "test" and r["n_runs"] == "3"
        elif artifact == TOKEN:
            assert [r["Method"] for r in rows] == list(METHODS)
        else:
            assert [r["Method"] for r in rows] == ["SkillSight"] + ["RouterBSI_init", "RouterBSI"] * 3
    return rows


def build(artifact, rows):
    height = SPECS[artifact][3]
    rc = dict(RC)
    if artifact == RET:
        rc.update({"font.family": "DejaVu Sans", "mathtext.fontset": "dejavusans"})
    with plt.rc_context(cast(Any, rc)):
        fig = plt.figure(figsize=(218 / 72, height / 72))
        # Explicit page-size geometry: no tight cropping / implicit rescaling.
        bottom, top = (26, 83) if artifact == RET else (25, 77)
        if artifact == LLMS:
            bottom, top = 27, 101
        left = 36 if artifact == RET else 34
        ax = fig.add_axes((left / 218, bottom / height, (215 - left) / 218, (top - bottom) / height))
        ax.set_axisbelow(True)
        if artifact == RET:
            for i, method in enumerate(RET_METHODS):
                group = [p for p in rows if p["Method"] == method]
                ax.plot([p["position"] for p in group], [p["y"] for p in group],
                        label=method, color=RET_COLORS[i], marker=RET_MARKERS[i], linestyle=RET_STYLES[i],
                        linewidth=1.3 if method == "RouterBSI" else .85,
                        markersize=4 if method == "RouterBSI" else 2.7,
                        zorder=5 if method == "RouterBSI" else 2)
            ax.set_xticks(range(5), ["50", "25", "10", "5", "1"])
            ax.set_ylim(30, 105)
            ax.set_yticks([30, 50, 75, 100])
            assert ax.get_ylim() == (30, 105)
            ax.set_xlabel("Top k")
            ax.set_ylabel(r"Ret@$k$ (%)")
            ax.grid(axis="x", visible=False)
            ax.grid(axis="y", color="#dddddd", linewidth=.6, alpha=1)
            # Preserve wording; a line break saves width without tiny type.
            handles, labels = ax.get_legend_handles_labels()
            labels[0] = "Retriever\nbaseline"
            fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(.53, 1.01),
                       ncol=3, frameon=False, columnspacing=.65, handlelength=1.25,
                       handletextpad=.35, borderpad=.1, labelspacing=.2, fontsize=8)
        elif artifact in (REPLAY, TOKEN):
            if artifact == REPLAY:
                low, high = [], []
                for method in METHODS:
                    group = [r for r in rows if r["Method"] == method]
                    xs = np.array([int(p["x"]) for p in group])
                    ys = np.array([float(p["Hit@1_mean"]) for p in group])
                    sd = np.array([float(p["Hit1_std"]) for p in group])
                    ax.plot(xs, ys, label=method, linewidth=.95, markersize=2.8,
                            markeredgewidth=.35, markeredgecolor="white", **STYLES[method])
                    ax.fill_between(xs, ys - sd, ys + sd, color=STYLES[method]["color"], alpha=.13, linewidth=0)
                    low.extend(ys - sd)
                    high.extend(ys + sd)
                ax.set_ylim(min(low) - .06, max(high) + .04)
                ax.set_xticks(range(0, 11, 2))
                ax.set_xlabel("Iteration")
            else:
                for p in rows:
                    style = STYLES[p["Method"]]
                    ax.scatter(int(p["Total Tokens"]) / 1_000_000, float(p["Hit@1"]),
                               label=p["Method"], color=style["color"], marker=style["marker"], s=24, zorder=3)
                ax.margins(x=.12, y=.2)
                lo, hi = ax.get_ylim()
                ax.set_ylim(lo - (hi - lo) * .35, hi)
                ax.set_xticks([800, 1000, 1200])
                ax.set_xlabel("Total Token Usage (millions)")
            ax.set_yticks([.5, .6, .7])
            ax.set_ylabel("nDCG@1")
            fig.legend(*ax.get_legend_handles_labels(), loc="upper center", bbox_to_anchor=(.57, .89),
                       ncol=2, frameon=False, columnspacing=1.0, handlelength=1.8,
                       handletextpad=.4, borderpad=0, labelspacing=.15, fontsize=8)
        else:
            bars = ax.bar(POSITIONS, [float(p["Hit@1"]) for p in rows], width=.40,
                          color=BAR_COLORS, edgecolor="white", linewidth=.6, zorder=3)
            for bar, point in zip(bars, rows):
                y = float(point["Hit@1"])
                initial = point["Method"] == "RouterBSI_init"
                if initial:
                    bar.set_hatch("///")
                    bar.set_alpha(.55)
                # Positive point offsets keep every value above its bar.
                ax.annotate(f"{y:.3f}", (bar.get_x() + bar.get_width()/2, y),
                            xytext=(0, 9.5 if point["Method"] == "RouterBSI" and point["Model"] == "GPT-OSS 120B" else 2),
                            textcoords="offset points", ha="center", va="bottom", fontsize=8)
            ax.set_xticks([0, 1.06, 2.38, 3.70], ["SkillSight", "Qwen3.5\n4B", "Qwen3.8\n27B", "GPT-OSS\n120B"])
            ax.set_xlim(-.30, 4.26)
            ax.tick_params(axis="x", labelsize=8)
            ax.set_ylabel("nDCG@1")
            ax.set_ylim(0, 1)
            ax.set_yticks([0, .5, 1])
            ax.grid(axis="x", visible=False)
            fig.legend(handles=[Patch(facecolor="#777777", edgecolor="white", hatch="///", alpha=.55,
                                      label=r"$\mathrm{RouterBSI}_{\mathrm{init}}$"),
                                Patch(facecolor="#777777", edgecolor="white", label="RouterBSI")],
                       loc="upper center", bbox_to_anchor=(.57, 1.015), ncol=2, frameon=False,
                       handlelength=1.25, handletextpad=.35, columnspacing=.8, fontsize=9)
        fig.canvas.draw()
        verify_artists(artifact, rows, ax)
        return fig, ax


def verify_artists(artifact, rows, ax):
    """Assert actual coordinates, uncertainty vertices, colors and encodings."""
    if artifact in (REPLAY, TOKEN):
        assert not ax.figure.texts and not ax.get_title(), "Unexpected in-image title"
    if artifact in (RET, REPLAY):
        methods = RET_METHODS if artifact == RET else METHODS
        assert len(ax.lines) == len(methods)
        for i, (line, method) in enumerate(zip(ax.lines, methods)):
            group = [r for r in rows if r["Method"] == method]
            xs = [r["position"] if artifact == RET else int(r["x"]) for r in group]
            ys = [r["y"] if artifact == RET else float(r["Hit@1_mean"]) for r in group]
            np.testing.assert_array_equal(line.get_xdata(), xs)
            np.testing.assert_array_equal(line.get_ydata(), ys)
            style = dict(color=RET_COLORS[i], marker=RET_MARKERS[i], linestyle=RET_STYLES[i]) if artifact == RET else STYLES[method]
            assert to_rgba(line.get_color()) == to_rgba(style["color"])
            assert line.get_marker() == style["marker"] and line.get_linestyle() == style["linestyle"]
            if artifact == REPLAY:
                band = ax.collections[i]
                assert band.get_alpha() == .13
                np.testing.assert_array_equal(band.get_facecolors()[0], to_rgba(style["color"], .13))
                vertices = band.get_paths()[0].vertices
                for x, y, row in zip(xs, ys, group):
                    actual = vertices[vertices[:, 0] == x, 1]
                    sd = float(row["Hit1_std"])
                    assert actual.min() == y - sd and actual.max() == y + sd
                    assert ax.get_ylim()[0] <= y - sd <= y + sd <= ax.get_ylim()[1]
        assert len(ax.collections) == (4 if artifact == REPLAY else 0)
    elif artifact == TOKEN:
        assert len(ax.collections) == 4
        for collection, row in zip(ax.collections, rows):
            np.testing.assert_array_equal(collection.get_offsets(), [[int(row["Total Tokens"]) / 1_000_000, float(row["Hit@1"])]])
            np.testing.assert_array_equal(collection.get_facecolors()[0], to_rgba(STYLES[row["Method"]]["color"]))
    else:
        assert len(ax.patches) == 7 and len(ax.texts) == 7
        for bar, text, row, x, color in zip(ax.patches, ax.texts, rows, POSITIONS, BAR_COLORS):
            assert bar.get_height() == float(row["Hit@1"])
            assert bar.get_x() + bar.get_width()/2 == x
            assert text.get_text() == f"{float(row['Hit@1']):.3f}"
            alpha = .55 if row["Method"] == "RouterBSI_init" else 1
            np.testing.assert_array_equal(bar.get_facecolor(), to_rgba(color, alpha))
            assert bar.get_hatch() == ("///" if alpha == .55 else None)
        verify_bar_label_layout(ax)


def verify_bar_label_layout(ax):
    """Check drawn value boxes against every bar/text and return point gaps."""
    fig = ax.figure
    # savefig can leave text transforms at its export DPI; refresh before measuring.
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    pt = 72 / fig.dpi
    labels = list(ax.texts)
    boxes = [text.get_window_extent(renderer) for text in labels]
    bars = [bar.get_window_extent(renderer) for bar in ax.patches]
    legends = [legend.get_window_extent(renderer) for legend in fig.legends]
    other_text = [text.get_window_extent(renderer) for text in fig.findobj(Text)
                  if text not in labels and text.get_visible() and text.get_text()]

    def gap(a, b):
        # Euclidean distance between disjoint display-coordinate rectangles.
        return math.hypot(max(a.x0 - b.x1, b.x0 - a.x1, 0),
                          max(a.y0 - b.y1, b.y0 - a.y1, 0)) * pt

    above, bar_gaps, text_gaps, legend_gaps = [], [], [], []
    for i, (text, box, bar) in enumerate(zip(labels, boxes, bars)):
        assert text.get_ha() == "center" and text.get_va() == "bottom"
        assert text.get_position()[0] == 0 and text.get_position()[1] > 0
        assert abs((box.x0 + box.x1 - bar.x0 - bar.x1) / 2) < 1e-6
        above.append((box.y0 - bar.y1) * pt)
        assert above[-1] > 0, (text.get_text(), "not above own bar")
        for boundary in (fig.bbox, ax.bbox):
            assert boundary.x0 <= box.x0 <= box.x1 <= boundary.x1, text.get_text()
            assert boundary.y0 <= box.y0 <= box.y1 <= boundary.y1, text.get_text()
        for targets, distances in ((bars, bar_gaps),
                                   (boxes[i+1:] + other_text, text_gaps),
                                   (legends, legend_gaps)):
            for target in targets:
                distances.append(gap(box, target))
                assert distances[-1] > 0, (text.get_text(), "display-coordinate collision")
    pair_gaps = [(bars[i+1].x0 - bars[i].x1) * pt for i in (1, 3, 5)]
    assert min(pair_gaps) > 0
    group_gaps = [(bars[i+1].x0 - bars[i].x1) * pt for i in (0, 2, 4)]
    assert min(group_gaps) >= 3 * max(pair_gaps), "LLM groups must be visually distinct"
    return {"min_own_bar_clearance_pt": min(above),
            "min_label_bar_gap_pt": min(bar_gaps),
            "min_label_text_gap_pt": min(text_gaps),
            "min_label_legend_gap_pt": min(legend_gaps),
            "min_paired_bar_gap_pt": min(pair_gaps),
            "min_between_group_gap_pt": min(group_gaps),
            "label_offsets_pt": [list(text.get_position()) for text in labels]}


def artist_record(artifact, ax):
    record = {"lines": [{"label": l.get_label(), "x": l.get_xdata().tolist(), "y": l.get_ydata().tolist(),
                         "color": l.get_color(), "marker": l.get_marker(), "linestyle": l.get_linestyle()} for l in ax.lines],
              "xlim": list(ax.get_xlim()), "ylim": list(ax.get_ylim())}
    if artifact == REPLAY:
        record["bands"] = [c.get_paths()[0].vertices.tolist() for c in ax.collections]
    if artifact == TOKEN:
        record["scatter"] = [c.get_offsets().tolist() for c in ax.collections]
    if artifact == LLMS:
        record["bars"] = [{"x": b.get_x()+b.get_width()/2, "height": b.get_height(), "rgba": b.get_facecolor(), "hatch": b.get_hatch()} for b in ax.patches]
    return record


def measure(pdf):
    with fitz.open(pdf) as doc:
        page = doc[0]
        text = cast(dict[str, Any], page.get_text("dict"))
        spans = [s for b in text["blocks"] if "lines" in b for l in b["lines"] for s in l["spans"]]
        assert spans
        return {"width_pt": page.rect.width, "height_pt": page.rect.height,
                "font_sizes_pt": sorted({round(s["size"], 4) for s in spans}),
                "text": [{"text": s["text"], "size_pt": s["size"], "bbox": list(s["bbox"])} for s in spans]}


def render(artifact, rows):
    directory = ROOT / "figs" / artifact
    protected = {str(p.relative_to(ROOT)): sha(p) for p in directory.iterdir() if p.is_file() and p.name not in {"preview.pdf", "preview.png", "readability_manifest.json"}}
    fig, ax = build(artifact, rows)
    texts = [t for t in fig.findobj(Text) if t.get_visible() and t.get_text()]
    assert min(t.get_fontsize() for t in texts) >= 8
    with tempfile.TemporaryDirectory(prefix="acl-readability-") as temp:
        temp = Path(temp)
        fig.savefig(temp / "preview.pdf", bbox_inches=None, metadata={"CreationDate": None, "ModDate": None})
        fig.savefig(temp / "preview.png", dpi=300, bbox_inches=None)
        metrics = measure(temp / "preview.pdf")
        assert abs(metrics["width_pt"] - 218) < .01
        assert abs(metrics["height_pt"] - SPECS[artifact][3]) < .01
        assert min(metrics["font_sizes_pt"]) >= 6
        assert all(s >= 8 or (artifact == LLMS and abs(s - 6.3) < .01) for s in metrics["font_sizes_pt"])
        for span in metrics["text"]:
            x0, y0, x1, y1 = span["bbox"]
            assert 0 <= x0 <= x1 <= metrics["width_pt"], span
            assert 0 <= y0 <= y1 <= metrics["height_pt"], span
        for name in ("preview.pdf", "preview.png"):
            (directory / name).write_bytes((temp / name).read_bytes())
    assert all(sha(ROOT / name) == digest for name, digest in protected.items())
    manifest = {"artifact": artifact, "figure_number": SPECS[artifact][0],
                "scope": "formatting only; frozen paper selection, unchanged authored caption and label",
                "regenerate": "python scripts/render_acl_readable_figures.py --artifact " + artifact,
                "generator": {"path": str(Path(__file__).relative_to(ROOT)), "sha256": sha(__file__)},
                "versions": {"matplotlib": matplotlib.__version__, "numpy": np.__version__, "pymupdf": fitz.VersionBind},
                "frozen_input": {"path": str((directory / SPECS[artifact][1]).relative_to(ROOT)), "sha256": SPECS[artifact][2]},
                "protected_hashes": protected, "measurements": metrics,
                "actual_artists": artist_record(artifact, ax),
                "checks": {"numerical_artist_equality": True, "uncertainty_vertices": artifact == REPLAY,
                           "colors_and_series_preserved": True, "captions_labels_and_evidence_unchanged": True},
                "historical_metadata": "Existing selection/provenance records remain immutable evidence. This manifest supersedes their PDF/PNG hashes and rendering settings only; it does not promote reportability.",
                "outputs": {name: sha(directory / name) for name in ("preview.pdf", "preview.png")}}
    if artifact == LLMS:
        manifest["label_layout"] = verify_bar_label_layout(ax)
    elif artifact in (REPLAY, TOKEN):
        manifest["checks"]["in_image_title_absent"] = True
    (directory / "readability_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    plt.close(fig)
    print(f"Figure {SPECS[artifact][0]}: {metrics['width_pt']} x {metrics['height_pt']} pt; fonts {metrics['font_sizes_pt']}; numeric artists PASS")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", choices=list(SPECS))
    args = parser.parse_args()
    targets = [args.artifact] if args.artifact else list(SPECS)
    # All frozen hashes are verified before any output is replaced.
    selected = {a: load(a) for a in targets}
    for artifact, rows in selected.items():
        render(artifact, rows)


if __name__ == "__main__":
    main()
