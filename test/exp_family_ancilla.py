import qcreason.representation.formulas_to_circuit
from qcreason import engine
from qcreason import representation

import matplotlib.pyplot as plt

circ = engine.get_circuit()(["sledz", "jaszczur", "kaczka"])

weightedFormulas = {
    "f1": ["imp", "sledz", "jaszczur", False],
    "f2": ["and", "jaszczur", "kaczka", True],
    "f3": ["or", "sledz", "kaczka", -1]
}

for formulaKey in weightedFormulas:
    circ = qcreason.representation.formulas_to_circuit.add_formula_to_circuit(circ, weightedFormulas[formulaKey][:-1])

sliceTuples = representation.calculate_angles(representation.get_color_param_dict(weightedFormulas))

headColor = "samplingAncilla"

for sliceTuple in sliceTuples:
    circ.add_controlled_rotation(sliceTuple, headColor)

circ.circuit.draw("mpl")
plt.show()