#!/usr/bin/env python3
"""Create and evaluate LTspice experiment snapshots.

The script copies the current LTspice case into Experiments/<name>/ and writes a
small Markdown report with repeatable signal metrics.
"""

from __future__ import annotations

import argparse
import math
import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PyLTSpice import RawRead


DEFAULT_SIGNALS = ["I(I_in)", "V(vout)", "V(vin)", "V(vpbs)", "V(vnbs)", "I(B1)", "I(B2)"]
COPY_EXTENSIONS = {".asc", ".net", ".log", ".raw", ".plt", ".lib"}


def read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff") or b"\x00" in raw[:200]:
        return raw.decode("utf-16le", errors="ignore")
    return raw.decode(errors="ignore")


def copy_case(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        if item.is_file() and item.suffix.lower() in COPY_EXTENSIONS:
            shutil.copy2(item, destination / item.name)


def get_wave(raw: RawRead, name: str) -> np.ndarray:
    return np.asarray(raw.get_trace(name).get_wave(), dtype=float)


def signal_metrics(time: np.ndarray, wave: np.ndarray, start: float) -> dict[str, float]:
    mask = time >= start
    if not mask.any():
        mask = np.ones_like(time, dtype=bool)
    t = time[mask]
    y = wave[mask]
    duration = max(float(t[-1] - t[0]), 0.0)
    return {
        "mean": float(np.mean(y)),
        "min": float(np.min(y)),
        "max": float(np.max(y)),
        "pp": float(np.max(y) - np.min(y)),
        "rms_ac": float(np.sqrt(np.mean((y - np.mean(y)) ** 2))),
        "duration": duration,
    }


def estimate_phase(time: np.ndarray, x: np.ndarray, y: np.ndarray, freq: float, start: float) -> float | None:
    mask = time >= start
    if not mask.any() or freq <= 0:
        return None
    t = time[mask]
    x = x[mask] - np.mean(x[mask])
    y = y[mask] - np.mean(y[mask])
    sin_ref = np.sin(2 * math.pi * freq * t)
    cos_ref = np.cos(2 * math.pi * freq * t)

    def phase(sig: np.ndarray) -> float:
        a = float(np.dot(sig, cos_ref))
        b = float(np.dot(sig, sin_ref))
        return math.atan2(b, a)

    delta = math.degrees(phase(y) - phase(x))
    while delta > 180:
        delta -= 360
    while delta < -180:
        delta += 360
    return delta


def plot_signals(
    exp_dir: Path,
    time: np.ndarray,
    waveforms: dict[str, np.ndarray],
    start: float,
    end: float | None,
) -> list[Path]:
    plot_dir = exp_dir / "plots"
    plot_dir.mkdir(exist_ok=True)
    mask = time >= start
    if end is not None:
        mask &= time <= end
    if not mask.any():
        mask = np.ones_like(time, dtype=bool)

    t_ms = time[mask] * 1e3
    plots: list[Path] = []

    groups = [
        ("signal_path.png", ["I(I_in)", "V(vout)", "V(vin)"], "Signal path overview"),
        ("rails.png", ["V(vpbs)", "V(vnbs)", "V(vout)", "V(vref)"], "Flying rails and output"),
        ("photocurrents.png", ["I(B1)", "I(B2)", "I(I_in)"], "Photocurrents and differential input current"),
    ]

    for filename, names, title in groups:
        available = [name for name in names if name in waveforms]
        if not available:
            continue
        fig, ax1 = plt.subplots(figsize=(10, 5), constrained_layout=True)
        ax2 = ax1.twinx()
        used_ax2 = False
        colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
        for idx, name in enumerate(available):
            y = waveforms[name][mask]
            color = colors[idx % len(colors)]
            if name.startswith("I("):
                ax2.plot(t_ms, y * 1e3, label=f"{name} [mA]", linewidth=1.2, color=color)
                used_ax2 = True
            else:
                ax1.plot(t_ms, y, label=f"{name} [V]", linewidth=1.2, color=color)
        ax1.set_title(title)
        ax1.set_xlabel("Time [ms]")
        ax1.set_ylabel("Voltage [V]")
        ax1.grid(True, alpha=0.3)
        lines1, labels1 = ax1.get_legend_handles_labels()
        if used_ax2:
            ax2.set_ylabel("Current [mA]")
            lines2, labels2 = ax2.get_legend_handles_labels()
        else:
            lines2, labels2 = [], []
            ax2.set_yticks([])
        ax1.legend(lines1 + lines2, labels1 + labels2, loc="best")
        out = plot_dir / filename
        fig.savefig(out, dpi=160)
        plt.close(fig)
        plots.append(out)

    return plots


def log_summary(path: Path) -> tuple[int, int, list[str], list[str]]:
    if not path.exists():
        return 0, 0, [], []
    text = read_text_auto(path)
    warnings = [line.strip() for line in text.splitlines() if "warning" in line.lower()]
    errors = [line.strip() for line in text.splitlines() if "error" in line.lower()]
    return len(warnings), len(errors), warnings[:10], errors[:10]


def write_report(
    exp_dir: Path,
    source: Path,
    question: str,
    change: str,
    freq: float,
    settle: float,
    plot_end: float | None,
) -> None:
    raw_files = sorted(exp_dir.glob("*.raw"))
    raw_path = next((p for p in raw_files if not p.name.endswith(".op.raw")), None)
    if raw_path is None:
        raise FileNotFoundError(f"No transient .raw file found in {exp_dir}")

    raw = RawRead(str(raw_path))
    time = get_wave(raw, "time")
    traces = set(raw.get_trace_names())
    waveforms = {name: get_wave(raw, name) for name in traces if name in set(DEFAULT_SIGNALS + ["V(vref)"])}
    rows = []
    metrics = {}
    for name in DEFAULT_SIGNALS:
        if name in traces:
            m = signal_metrics(time, waveforms[name], settle)
            metrics[name] = m
            rows.append((name, m))

    zin = None
    if "V(vout)" in metrics and "I(I_in)" in metrics and metrics["I(I_in)"]["pp"] != 0:
        zin = metrics["V(vout)"]["pp"] / metrics["I(I_in)"]["pp"]

    phase = None
    if "I(I_in)" in traces and "V(vout)" in traces:
        phase = estimate_phase(time, waveforms["I(I_in)"], waveforms["V(vout)"], freq, settle)

    log_path = exp_dir / raw_path.with_suffix(".log").name
    warn_count, err_count, warnings, errors = log_summary(log_path)
    plot_paths = plot_signals(exp_dir, time, waveforms, settle, plot_end)

    report = exp_dir / "notes.md"
    with report.open("w", encoding="utf-8") as f:
        f.write(f"# {exp_dir.name}\n\n")
        f.write(f"Source case: `{source}`\n\n")
        f.write("## Question\n\n")
        f.write(f"{question or 'TBD'}\n\n")
        f.write("## Circuit Change\n\n")
        f.write(f"{change or 'TBD'}\n\n")
        f.write("## Simulation Health\n\n")
        f.write(f"- Warnings: {warn_count}\n")
        f.write(f"- Errors: {err_count}\n")
        for line in errors:
            f.write(f"- Error detail: `{line}`\n")
        for line in warnings[:5]:
            f.write(f"- Warning detail: `{line}`\n")
        f.write("\n## Metrics\n\n")
        f.write(f"Metrics measured after `{settle:g} s`.\n\n")
        f.write("| Signal | Mean | Min | Max | Peak-to-peak | AC RMS |\n")
        f.write("| --- | ---: | ---: | ---: | ---: | ---: |\n")
        for name, m in rows:
            f.write(
                f"| `{name}` | {m['mean']:.6g} | {m['min']:.6g} | {m['max']:.6g} | "
                f"{m['pp']:.6g} | {m['rms_ac']:.6g} |\n"
            )
        f.write("\n## Derived Results\n\n")
        if zin is not None:
            f.write(f"- Transimpedance estimate `V(vout)_pp / I(I_in)_pp`: `{zin:.6g} Ohm`\n")
        if phase is not None:
            f.write(f"- Phase estimate of `V(vout)` relative to `I(I_in)` at `{freq:g} Hz`: `{phase:.3f} deg`\n")
        if plot_paths:
            f.write("\n## Plots\n\n")
            for plot_path in plot_paths:
                rel = plot_path.relative_to(exp_dir)
                f.write(f"![{plot_path.stem}]({rel.as_posix()})\n\n")
        f.write("\n## Observation\n\n")
        f.write("TBD\n\n")
        f.write("## Decision\n\n")
        f.write("TBD\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Experiment folder name, e.g. E01_baseline_no_cpd")
    parser.add_argument("--source", type=Path, required=True, help="LTspice case folder to snapshot")
    parser.add_argument("--question", default="", help="Experiment question")
    parser.add_argument("--change", default="", help="Single circuit change for this experiment")
    parser.add_argument("--freq", type=float, default=100_000.0, help="Signal frequency for phase estimate")
    parser.add_argument("--settle", type=float, default=0.003, help="Ignore data before this time")
    parser.add_argument("--plot-end", type=float, default=None, help="Optional end time for plots")
    args = parser.parse_args()

    root = Path.cwd()
    exp_dir = root / "Experiments" / args.name
    copy_case(args.source, exp_dir)
    write_report(exp_dir, args.source, args.question, args.change, args.freq, args.settle, args.plot_end)
    print(exp_dir)
    print(exp_dir / "notes.md")


if __name__ == "__main__":
    main()
