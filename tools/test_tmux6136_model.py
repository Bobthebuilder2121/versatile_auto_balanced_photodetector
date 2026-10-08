"""Source-data regression tests, separate from native LTspice measurements."""

import unittest

import ecdtools.ibis
import numpy as np

from build_tmux6136_model import CIRCUIT


class TMUXModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ibis = ecdtools.ibis.load_file(CIRCUIT / "tmux6136.ibs", transform=True)
        cls.model = cls.ibis.get_model_by_name("input_15p0")
        cls.text = (CIRCUIT / "TMUX6136_extended.lib").read_text()

    def test_clamp_samples_match(self):
        for element, original in (("BGND", self.model.gnd_clamp),
                                  ("BPWR", self.model.power_clamp)):
            line = next(line for line in self.text.splitlines()
                        if line.startswith(element + " "))
            args = line.split("), ", 1)[1].rsplit(")", 1)[0]
            values = np.array([float(v) for v in args.split(",")]).reshape(-1, 2)
            np.testing.assert_allclose(values, np.asarray(original, float)[:, :2],
                                       rtol=1e-12, atol=1e-18)

    def test_external_references(self):
        self.assertIn("BGND SEL_DIE VSS I=table(V(SEL_DIE,VSS)", self.text)
        self.assertIn("BPWR SEL_DIE VDD I=table(V(VDD,SEL_DIE)", self.text)
        self.assertNotIn("V1 PWR_CLAMP_REF", self.text)

    def test_threshold_not_taken_from_reversed_ibis(self):
        self.assertIn("VTH=1.4", self.text)
        self.assertLess(0.8, 1.4)
        self.assertLess(1.4, 2.0)

    def test_capacitance_not_double_counted(self):
        self.assertIn("CIN-CPKG-CCOMP", self.text)
        self.assertAlmostEqual(0.2 + 0.331 + (1.5 - 0.2 - 0.331), 1.5)
        self.assertIn("CON-CSOFF", self.text)
        self.assertAlmostEqual(2.4 + (5.5 - 2.4), 5.5)

    def test_delay_nonoverlap_for_both_edges(self):
        # Test the algebra used by BA/BB; this is not a transistor timing test.
        t = np.linspace(-20e-9, 100e-9, 1201)
        for initial, final in ((0, 1), (1, 0)):
            slow = np.where(t < 58e-9, initial, final)
            fast = np.where(t < 18e-9, initial, final)
            a = np.minimum(slow, fast)
            b = np.minimum(1 - slow, 1 - fast)
            self.assertTrue(np.all(a * b == 0))
            gap = (t >= 18e-9) & (t < 58e-9)
            self.assertTrue(np.all((a[gap] == 0) & (b[gap] == 0)))
            self.assertEqual((a[-1], b[-1]), (final, 1 - final))

    def test_channel_terminal_order(self):
        self.assertIn(".subckt TMUX6136_SPDT SEL SA D SB VSS GND VDD", self.text)
        self.assertIn("NOT an official TI SPICE model", self.text)


if __name__ == "__main__":
    unittest.main()
