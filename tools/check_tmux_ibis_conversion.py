"""Generate locally corrected pybis2spice outputs and audit against TI IBIS."""

import hashlib
import importlib.metadata
import json
import re
from pathlib import Path

import ecdtools.ibis
import numpy as np
from pybis2spice import pybis2spice, subcircuit


ROOT = Path(__file__).resolve().parents[1]
CIRCUIT = ROOT / "simulations/tia_mcp_check"
OUTPUT = CIRCUIT / "ibis_conversion/pybis2spice"
CORNERS = ("Typical", "WeakSlow", "FastStrong")


def table_from_output(text, element):
    line = next(line for line in text.splitlines() if line.startswith(element + " "))
    args = line.split("table(V(DIE),", 1)[1].rsplit(")", 1)[0]
    numbers = [float(value) for value in args.split(",")]
    return np.asarray(numbers).reshape(-1, 2)


def main():
    source = CIRCUIT / "tmux6136.ibs"
    original_lib = CIRCUIT / "tmux6136.lib"
    active = CIRCUIT / "tia_check.asc"
    active_hash = hashlib.sha256(active.read_bytes()).hexdigest()
    parsed = ecdtools.ibis.load_file(source, transform=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    report = {
        "ecdtools": importlib.metadata.version("ecdtools"),
        "pybis2spice": importlib.metadata.version("pybis2spice"),
        "upstream_commit": "546618633b50d1bc0bdfd21e6250d835d122d59d",
        "local_fix": "GND clamp absolute voltage = table voltage + reference",
        "ibis_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "old_lib_sha256": hashlib.sha256(original_lib.read_bytes()).hexdigest(),
        "active_asc_sha256": active_hash,
        "models": [],
    }
    old_text = original_lib.read_text()
    for model_name in parsed.model_names:
        data = pybis2spice.DataModel(parsed, model_name, "TMUX6136PW")
        if data.model_type != "Input":
            raise ValueError(f"Unexpected model type: {data.model_type}")
        for index, corner in enumerate(CORNERS):
            destination = OUTPUT / f"{model_name}_{corner}.lib"
            result = subcircuit.generate_spice_model(
                "Input", "LTSpice", data, corner, str(destination)
            )
            if result != 0:
                raise RuntimeError(f"Conversion failed: {model_name}/{corner}")
            subcircuit.create_ltspice_symbol(data, corner, str(destination), "Input")
            text = destination.read_text()
            ground = table_from_output(text, "B2")
            power = table_from_output(text, "B1")
            gref = float(data.gnd_clamp_ref[index])
            pref = float(data.pwr_clamp_ref[index])
            # Ground table voltages are relative to GND Clamp Reference.
            expected_ground_x = data.iv_gnd_clamp[:, 0] + gref
            expected_power_x = np.flip(pref - data.iv_pwr_clamp[:, 0])
            ground_current = np.allclose(
                ground[:, 1], data.iv_gnd_clamp[:, index + 1], rtol=1e-10, atol=1e-18
            )
            power_current = np.allclose(
                power[:, 1], np.flip(data.iv_pwr_clamp[:, index + 1]),
                rtol=1e-10, atol=1e-18,
            )
            power_axis = np.allclose(power[:, 0], expected_power_x, atol=1e-12)
            ground_axis = np.allclose(ground[:, 0], expected_ground_x, atol=1e-12)
            assert ground_current and power_current and power_axis and ground_axis
            for name, values in (("R_pkg", data.r_pkg), ("L_pkg", data.l_pkg),
                                 ("C_pkg", data.c_pkg), ("C_comp", data.c_comp)):
                value = float(re.search(rf"^\.param {name} = (\S+)", text, re.M)[1])
                assert np.isclose(value, float(values[index]), rtol=1e-12, atol=0)
            suffix = ("TYP", "MIN", "MAX")[index]
            old_name = f"TMUX6136PW_{model_name.upper()}_{suffix}"
            old_match = re.search(
                rf"\.SUBCKT {old_name}\b(.*?)\.ENDS", old_text, re.S | re.I
            )
            if old_match is None:
                raise ValueError(f"Missing previous subcircuit: {old_name}")
            old_tables = re.findall(
                r"^G(?:GND|PWR)_CLAMP[^\n]*\n((?:\+[^\n]*\n)+)",
                old_match[1], re.M,
            )
            old_currents = [float(line.split(",")[-1])
                            for table in old_tables for line in table.splitlines()]
            assert len(old_tables) == 2 and len(old_currents) == 6
            report["models"].append({
                "model": model_name, "corner": corner,
                "ground_table_rows": len(ground), "power_table_rows": len(power),
                "current_tables_preserved": bool(ground_current and power_current),
                "power_voltage_axis_correct": bool(power_axis),
                "ground_voltage_axis_correct": bool(ground_axis),
                "ground_voltage_axis_offset_v": float(ground[0, 0] - expected_ground_x[0]),
                "ground_reference_v": gref, "power_reference_v": pref,
                "old_clamp_rows_each": 3,
                "old_clamp_currents_all_zero": all(value == 0 for value in old_currents),
                "analog_switch_path_present": False,
            })
    assert hashlib.sha256(active.read_bytes()).hexdigest() == active_hash
    report["active_asc_unchanged"] = True
    (OUTPUT.parent / "audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"Generated {len(report['models'])} input models and symbols in {OUTPUT}")
    for item in report["models"]:
        print(f"{item['model']:12} {item['corner']:10}: "
              f"GND/PWR={item['ground_table_rows']}/{item['power_table_rows']} rows; "
              f"GND axis offset={item['ground_voltage_axis_offset_v']:g} V")
    print("Current tables and R/L/C match source; active ASC unchanged.")
    print("Generated models are audit artifacts, NOT full analog-switch models.")


if __name__ == "__main__":
    main()
