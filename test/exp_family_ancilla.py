import qcreason.representation.formulas_to_circuit
from qcreason import engine
from qcreason import representation

import matplotlib.pyplot as plt

circuitProvider = "QiskitCircuit" # "PennyLaneCircuit"

disVariables = ["sledz", "jaszczur", "kaczka"]
circ = engine.get_circuit(circuitProvider)(disVariables)

weightedFormulas = {
    "f1": ["imp", "sledz", "jaszczur", True],
    "f2": ["and", "jaszczur", "kaczka", False],
    "f3": ["or", "sledz", "kaczka", -1]
}

for formulaKey in weightedFormulas:
    circ = qcreason.representation.formulas_to_circuit.add_formula_to_circuit(circ, weightedFormulas[formulaKey][:-1])

sliceTuples = representation.calculate_angles(representation.get_color_param_dict(weightedFormulas))

headColor = "samplingAncilla"

for sliceTuple in sliceTuples:
    circ.add_controlled_rotation(sliceTuple, headColor)

circ.add_measurement(disVariables + ["(imp_sledz_jaszczur)", "(and_jaszczur_kaczka)"] + [headColor])
circ.visualize()

results = circ.run(shots=100)

for i in range(100):
    assert not results[i][-1] or results[i][-3]
    assert not results[i][-1] or not results[i][-2]

