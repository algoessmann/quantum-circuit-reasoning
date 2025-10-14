import unittest

from qcreason import representation, engine

circuitProvider = "PennyLaneCircuit"


class PreparationTest(unittest.TestCase):
    def test_statistic_preparation(self):

        circ = engine.get_circuit(circuitProvider)(["a", "b", "c"])
        circ = representation.add_formula_to_circuit(circ, ["and", ["imp", "b", "c"], ["not", "a"]])
        circ.add_measurement(["a", "b", "c", "(not_a)", "(imp_b_c)", "(and_(imp_b_c)_(not_a))"])

        samples = circ.run(shots=100)

        for idx, row in samples.iterrows():
            self.assertTrue(row["(not_a)"] ^ row["a"])
            self.assertTrue(row["(imp_b_c)"] == (not row["b"] or row["c"]))
            self.assertTrue(row["(and_(imp_b_c)_(not_a))"] == (row["(imp_b_c)"] and row["(not_a)"]))

    def test_statistic_ancilla(self):

        disVariables = ["sledz", "jaszczur", "kaczka"]
        weightedFormulas = {
            "f1": ["imp", "sledz", "jaszczur", True],
            "f2": ["and", "jaszczur", "kaczka", False],
            "f3": ["or", "sledz", "kaczka", -1]
        }

        circ = engine.get_circuit(circuitProvider)(disVariables)
        circ = representation.compute_and_activate(circ, weightedFormulas, atomColors=disVariables)
        circ.add_measurement(disVariables + ["(imp_sledz_jaszczur)", "(and_jaszczur_kaczka)"] + ["samplingAncilla"])

        shotNum = 100
        samples = circ.run(shots=shotNum)

        for idx, row in samples.iterrows():
            self.assertTrue(not row["samplingAncilla"] or row["(imp_sledz_jaszczur)"])
            self.assertTrue(not row["samplingAncilla"] or not row["(and_jaszczur_kaczka)"])
