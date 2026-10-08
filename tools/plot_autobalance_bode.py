#!/usr/bin/env python3
"""Derive the LPF/PI responses with SymPy and save magnitude/phase plots."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp


def positive_number(value: str) -> float:
    number = float(value)
    if not np.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("Value must be finite and positive.")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rin-kohm", type=positive_number, default=100.0)
    parser.add_argument("--rp-kohm", type=positive_number, default=100.0)
    parser.add_argument("--ci-nf", type=positive_number, default=7.97)
    parser.add_argument("--rlp-kohm", type=positive_number, default=15.9)
    parser.add_argument("--clp-nf", type=positive_number, default=10.0)
    parser.add_argument("--fmin", type=positive_number, default=0.1)
    parser.add_argument("--fmax", type=positive_number, default=100000.0)
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path(__file__).resolve().parents[1] / "notes" / "figures",
    )
    args = parser.parse_args()
    if args.fmin >= args.fmax:
        parser.error("--fmin must be less than --fmax.")

    s = sp.symbols("s")
    rin = sp.Rational(str(args.rin_kohm)) * 1000
    rp = sp.Rational(str(args.rp_kohm)) * 1000
    ci = sp.Rational(str(args.ci_nf)) / 10**9
    rlp = sp.Rational(str(args.rlp_kohm)) * 1000
    clp = sp.Rational(str(args.clp_nf)) / 10**9
    tau = rlp * clp
    kp = rp / rin
    ki = 1 / (rin * ci)
    h_lp = 1 / (tau * s + 1)
    h_pi = -(rp + 1 / (s * ci)) / rin
    h_combined = sp.cancel(h_lp * h_pi)

    # Check the expanded polynomials before evaluating their frequency response.
    expected_pi = (-rp * ci * s - 1) / (rin * ci * s)
    expected_combined = (-rp * ci * s - 1) / (
        rin * ci * tau * s**2 + rin * ci * s
    )
    assert sp.simplify(h_pi - expected_pi) == 0
    assert sp.simplify(h_combined - expected_combined) == 0

    fc = float(1 / (2 * sp.pi * tau))
    fz = float(1 / (2 * sp.pi * rp * ci))
    freq = np.logspace(np.log10(args.fmin), np.log10(args.fmax), 3000)
    jw = 2j * np.pi * freq
    definitions = [
        ("H_LP", r"$H_{\rm LP}$", h_lp, "#0072B2", "-"),
        ("H_PI", r"$H_{\rm PI}$", h_pi, "#009E73", "--"),
        ("H_combined", r"$H_{\rm LP}H_{\rm PI}$", h_combined, "#D55E00", "-."),
    ]
    responses = [np.asarray(sp.lambdify(s, item[2], "numpy")(jw)) for item in definitions]
    assert np.allclose(responses[2], responses[0] * responses[1])
    assert all(np.all(np.isfinite(response)) for response in responses)
    lp_at_fc = complex(sp.N(h_lp.subs(s, 2 * sp.pi * sp.I * fc)))
    pi_at_fz = complex(sp.N(h_pi.subs(s, 2 * sp.pi * sp.I * fz)))
    assert np.isclose(abs(lp_at_fc), 1 / np.sqrt(2))
    assert np.isclose(np.angle(lp_at_fc, deg=True), -45)
    assert np.isclose(abs(pi_at_fz), np.sqrt(2) * float(kp))
    assert np.isclose(np.angle(pi_at_fz, deg=True), 135)

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig, axes = plt.subplots(2, 1, figsize=(12, 8.5), sharex=True)
    fig.subplots_adjust(left=0.085, right=0.97, top=0.80, bottom=0.22, hspace=0.12)
    fig.suptitle("Block 3: Tiefpass und invertierender PI-Regler", y=0.97, fontsize=16)
    fig.text(
        0.5, 0.915,
        rf"$H_{{\rm LP}}(s)=\frac{{1}}{{{float(tau):.6g}s+1}}$"
        + r"$\qquad$"
        + rf"$H_{{\rm PI}}(s)=\frac{{-{float(kp):.6g}s-{float(ki):.6f}}}{{s}}$",
        ha="center", fontsize=13,
    )
    fig.text(
        0.5, 0.86,
        rf"$H_3(s)=\frac{{-{float(kp):.6g}s-{float(ki):.6f}}}"
        rf"{{{float(tau):.6g}s^2+s}}$",
        ha="center", fontsize=13,
    )

    columns = [freq]
    names = ["frequency_hz"]
    for (name, label, _, color, style), response in zip(definitions, responses):
        magnitude = 20 * np.log10(np.abs(response))
        phase = np.rad2deg(np.unwrap(np.angle(response)))
        axes[0].semilogx(freq, magnitude, color=color, linestyle=style, linewidth=2, label=label)
        axes[1].semilogx(freq, phase, color=color, linestyle=style, linewidth=2)
        columns.extend([magnitude, phase])
        names.extend([f"{name}_magnitude_db", f"{name}_phase_deg"])

    for axis in axes:
        axis.grid(True, which="major", color="#C8C8C8", linewidth=0.7)
        axis.grid(True, which="minor", color="#E5E5E5", linewidth=0.4)
        axis.set_axisbelow(True)
        axis.set_xlim(args.fmin, args.fmax)
        for corner in (fz, fc):
            if args.fmin <= corner <= args.fmax:
                axis.axvline(corner, color="#666666", linestyle=":", linewidth=1)
    axes[0].axhline(0, color="#888888", linewidth=0.7)
    axes[0].set_ylabel("Betrag [dB]")
    axes[0].legend(loc="upper right", framealpha=1)
    axes[1].set_ylabel("Phase [Grad]")
    axes[1].set_xlabel("Frequenz [Hz]")
    axes[1].set_yticks([-90, -45, 0, 45, 90, 135, 180])
    axes[1].set_ylim(-100, 190)
    for corner, label, alignment in (
        (fz, rf"$f_z={fz:.2f}\,\mathrm{{Hz}}$", "right"),
        (fc, rf"$f_c={fc:.2f}\,\mathrm{{Hz}}$", "left"),
    ):
        if args.fmin <= corner <= args.fmax:
            axes[0].annotate(
                label, xy=(corner, 0.07), xycoords=axes[0].get_xaxis_transform(),
                xytext=(-6 if alignment == "right" else 6, 0), textcoords="offset points",
                ha=alignment, va="bottom", fontsize=10,
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9, "pad": 2},
            )
    fig.text(
        0.085, 0.075,
        "K_AB geschlossen; ideale OPV und Relaiskontakte. Ohne Nachregler und APD/TIA-Regelstrecke.\n"
        "Invertierender PI: Phase +90 bis +180 Grad (180 Grad relativ zum nichtinvertierenden PI).",
        fontsize=10, linespacing=1.5,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    stem = args.output_dir / "autobalance_bode"
    fig.savefig(stem.with_suffix(".png"), dpi=200, facecolor="white")
    fig.savefig(stem.with_suffix(".pdf"), facecolor="white")
    plt.close(fig)
    np.savetxt(
        stem.with_suffix(".csv"), np.column_stack(columns), delimiter=",",
        header=",".join(names), comments="", fmt="%.12g",
    )
    print("Symbolic equivalence, numerical product, corner magnitude/phase: PASS")
    print(f"f_z = {fz:.8f} Hz; f_c = {fc:.8f} Hz; K_P = {float(kp):.8g}; K_I = {float(ki):.8f} s^-1")
    for name, _, transfer, _, _ in definitions:
        print(f"{name}(s) = {sp.cancel(transfer)}")
    print(f"PNG/PDF/CSV: {stem}")


if __name__ == "__main__":
    main()
