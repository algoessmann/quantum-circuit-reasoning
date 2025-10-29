import unittest

from qcreason import representation, engine

circuitProvider = "PennyLaneCircuit"


class PreparationTest(unittest.TestCase):
    def test_statistic_preparation_amplification_free(self):
        operations = representation.get_hadamard_gates(["a","b","c"]) + representation.generate_formula_operations(["and", ["imp", "b", "c"], ["not", "a"]])
        circ = engine.get_circuit(circuitProvider)(specDict={"operations" : operations})
        circ.add_measurement(circ.colors)

        samples = circ.run(shots=100)
        for idx, row in samples.iterrows():
            self.assertTrue(row["(not_a)"] ^ row["a"])
            self.assertTrue(row["(imp_b_c)"] == (not row["b"] or row["c"]))
            self.assertTrue(row["(and_(imp_b_c)_(not_a))"] == (row["(imp_b_c)"] and row["(not_a)"]))

    def test_statistic_preparation_with_amplification(self):
        weightedFormulaDict = {"f1": ["and", ["imp", "b", "c"], ["not", "a"], True]}
        for amplificationNum in [0, 1, 5]:
            circ = engine.get_circuit(circuitProvider)(specDict={"operations": representation.amplify_ones_state(
                representation.get_ca_operations(weightedFormulaDict), amplificationColors=["ancilla_(and_(imp_b_c)_(not_a))"], amplificationNum=amplificationNum
            )})
            circ.add_measurement(circ.colors)
            samples = circ.run(shots=10)
            for idx, row in samples.iterrows():
                self.assertTrue(row["(not_a)"] ^ row["a"])
                self.assertTrue(row["(imp_b_c)"] == (not row["b"] or row["c"]))
                self.assertTrue(row["(and_(imp_b_c)_(not_a))"] == (row["(imp_b_c)"] and row["(not_a)"]))

    def test_statistic_ancillas(self):
        weightedFormulas = {
            "f1": ["imp", "sledz", "jaszczur", True],
            "f2": ["and", "jaszczur", "kaczka", False],
            "f3": ["or", "sledz", "kaczka", -1]
        }
        circ = engine.get_circuit(circuitProvider)(specDict={"operations": representation.amplify_ones_state(
            representation.get_ca_operations(weightedFormulas),
            amplificationColors=["ancilla_(and_(imp_b_c)_(not_a))"], amplificationNum=0
        )})
        ancillaVariables = ['ancilla_(or_sledz_kaczka)', 'ancilla_(imp_sledz_jaszczur)', 'ancilla_(and_jaszczur_kaczka)']
        circ.add_measurement(["(imp_sledz_jaszczur)", "(and_jaszczur_kaczka)"] + ancillaVariables)

        shotNum = 100
        samples = circ.run(shots=shotNum)

        for idx, row in samples.iterrows():
            ## Hard formulas need to be satisfied when sampling ancillas are 1
            self.assertTrue(not all([row[ancilla] for ancilla in ancillaVariables]) or (row["(imp_sledz_jaszczur)"] and not row["(and_jaszczur_kaczka)"]))

    def test_wolfram_codes(self):
        operations = representation.get_hadamard_gates(["a","b","c"]) + representation.generate_formula_operations(["8", ["11", "a", "c"], ["1", "b"]])
        circ = engine.get_circuit(circuitProvider)(specDict={"operations" : operations})
        circ.add_measurement(circ.colors)

        shotNum = 10
        results = circ.run(shots=shotNum)
        for idx, row in results.iterrows():
            self.assertTrue(row["b"] == (not row["(1_b)"]))  # 1 is not
            self.assertTrue(row["(11_a_c)"] == (not row["a"] or row["c"]))  # 11 is imp
            self.assertTrue(row["(8_(11_a_c)_(1_b))"] == (row["(11_a_c)"] and row["(1_b)"]))  # 8 is and
