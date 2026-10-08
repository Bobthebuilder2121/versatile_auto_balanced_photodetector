#!/usr/bin/env python3
"""Plot the active ASC's single-run mismatch response from native LTspice RAW."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PyLTSpice import RawRead


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "simulations/tia_mcp_check"
raw = RawRead(str(RUN / "tia_check.raw"),
              traces_to_read=["V(vpi)", "V(bias_p)", "V(bias_n)", "V(vout)"])
step = 0
if len(list(raw.get_steps())) > 1:
    matches = [i for i, settings in enumerate(raw.steps) if settings.get("ctrl") == 1]
    if len(matches) != 1:
        raise ValueError("Expected exactly one CTRL=1 step in the simulation.")
    step = matches[0]
t = raw.get_trace("time").get_wave(step)
if t[-1] < 0.0299:
    raise ValueError("The 30 ms transient has not completed.")


def trace(name):
    return raw.get_trace(name).get_wave(step).astype(float)


def cycle_mean(y):
    # Integrate actual variable-step samples, then average each 100 kHz cycle.
    integral = np.r_[0.0, np.cumsum(np.diff(t) * (y[1:] + y[:-1]) / 2)]
    edges = np.arange(0, 0.030000001, 10e-6)
    means = np.diff(np.interp(edges, t, integral)) / np.diff(edges)
    return (edges[1:] + edges[:-1]) / 2, means


vpi = trace("V(vpi)")
tc, vpi_mean = cycle_mean(vpi)
_, bias_mean = cycle_mean(trace("V(bias_p)"))
_, vout_mean = cycle_mean(trace("V(vout)"))
fig, axes = plt.subplots(3, 1, figsize=(9, 8), sharex=True, layout="constrained")
axes[0].plot(t[::5] * 1e3, vpi[::5], color="#D89024", alpha=0.45,
             linewidth=0.6, label="VPI, sampled waveform")
axes[0].plot(tc * 1e3, vpi_mean, color="#0072B2", label="VPI, cycle mean")
axes[0].set_ylabel("PI output (V)")
axes[0].set_title(f"CTRL=1; VPI range {vpi.min():.4f} to {vpi.max():.4f} V; supplies +/-5 V")
axes[1].plot(tc * 1e3, bias_mean, color="#009E73", label="Upper bias, cycle mean")
axes[1].plot(t[::100] * 1e3, -trace("V(bias_n)")[::100], color="#9467BD",
             linestyle="--", label="Lower bias magnitude (-VBIAS_N)")
axes[1].set_ylabel("Bias magnitude (V)")
axes[1].ticklabel_format(axis="y", style="plain", useOffset=False)
axes[2].plot(tc * 1e3, vout_mean * 1e3, color="#D55E00", label="VOUT, cycle mean")
axes[2].axhline(0, color="black", linewidth=0.6)
axes[2].set_ylabel("Mean TIA output (mV)")
axes[2].set_xlabel("Time (ms)")
for ax in axes:
    ax.axvline(10, color="#666666", linestyle=":", linewidth=1)
    ax.set_xlim(0, 30)
    ax.grid(alpha=0.2)
    ax.legend(loc="best", fontsize=8)
fig.suptitle("+20 uA mismatch at 10 ms | fictive diode sensitivity: 100 uA/V")
fig.savefig(RUN / "vpi_response.png", dpi=180, bbox_inches="tight", pad_inches=0.15)
plt.close(fig)
print(RUN / "vpi_response.png")
