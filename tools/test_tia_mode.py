"""Test mode truth table, safe edits, and installed control wiring."""

import unittest

from spicelib import AscEditor
from spicelib.editor.base_schematic import TextTypeEnum

from set_tia_mode import ASC, SYMBOLS, make_ops, requests


class ModeTests(unittest.TestCase):
    def test_four_states(self):
        expected = ((1, 0, 0), (0, 1, 0), (1, 1, 0), (1, 1, 1))
        self.assertEqual(tuple(requests(mode) for mode in range(4)), expected)

    def test_invalid_values(self):
        for mode in (-1, 4):
            with self.assertRaises(ValueError):
                requests(mode)
        for value in (0, 30, -1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                make_ops("old", 2, 3, value)

    def test_edit_scope(self):
        ops = make_ops("old", 2, 3, 15)
        self.assertEqual([op["op"] for op in ops], ["remove_directive", "add_directive"])
        self.assertEqual(ops[1]["instruction"], ".param MODE_START=2 MODE_END=3 T_SWITCH=15m")

    def test_schematic_has_no_old_sweep(self):
        AscEditor.set_custom_library_paths(str(SYMBOLS), str(ASC.parent))
        editor = AscEditor(str(ASC))
        active = [d.text for d in editor.directives if d.type == TextTypeEnum.DIRECTIVE]
        self.assertFalse(any(d.lower().startswith(".step") for d in active))
        self.assertEqual(len([d for d in active if d.lower().startswith(".param mode_start=")]), 1)
        self.assertEqual(editor.get_component_value("V1"), "0")
        self.assertIn("V(AB_ENABLE)", editor.get_component_value("BSEL"))
        self.assertIn("3.3-V(AB_ENABLE)", editor.get_component_value("BRESET"))


if __name__ == "__main__":
    unittest.main()
