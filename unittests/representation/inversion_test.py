import unittest

from qcreason import representation, engine


class InversionTest(unittest.TestCase):
    """
    Implements the Inversion Test on basis encoding states
    """
    def test_same_formula(self):
        self.same_formula_template(formula=["eq", "A", "B"], distributedQubits=["A", "B"])
        self.same_formula_template(formula=["xor", ["not", "sledz"], "jaszczur"],
                                   distributedQubits=["jaszczur", "sledz"])

    def FAILED_test_syntactically_equal(self):
        self.syntactically_equal_template(formula1=["or", ["not", "A"], "B"], formula2=["imp", "A", "B"],
                                          distributedQubits=["A", "B"])

    def same_formula_template(self, formula, distributedQubits):
        self.syntactically_equal_template(formula1=formula, formula2=formula, distributedQubits=distributedQubits)

    def syntactically_equal_template(self, formula1, formula2, distributedQubits, shotNum=10):
        hadamardOperations = [{"unitary": "H", "targetQubits": [dQubit]} for dQubit in distributedQubits]
        operations = (hadamardOperations
                      + representation.generate_formula_operations(formula1, headColor="Y")
                      + representation.generate_formula_operations(formula2, ajoint=True, headColor="Y")
                      + hadamardOperations
                      )
        circuit = engine.get_circuit()(specDict={"operations": operations})
        samples = circuit.run(shotNum)
        for i, row in samples.iterrows():
            self.assertTrue(all([row[dQubit] == 0 for dQubit in distributedQubits]))
