import unittest

from detection.triage import Triage


class TestTriage(unittest.TestCase):
    def test_decision_maker(self):
        triage = Triage()
        self.assertAlmostEqual(triage.decision_maker(0.54, 0.46), 1)
        self.assertAlmostEqual(triage.decision_maker(0.60, 0.40), 0)
        self.assertAlmostEqual(triage.decision_maker(0.24, 0.76), 0)
        self.assertAlmostEqual(triage.decision_maker(0.76, 0.24), 0)
        self.assertAlmostEqual(triage.decision_maker(0.55, 0.44), 1)
        self.assertAlmostEqual(triage.decision_maker(0.44, 0.55), 1)