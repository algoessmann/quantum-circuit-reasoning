from qcreason import engine
from qcreason import representation
from qcreason import reasoning

import math

circuitProvider = "PennyLaneCircuit" # "QiskitCircuit"

disVariables = ["sledz", "jaszczur", "kaczka", "jaskuka"]
circ = engine.get_circuit(circuitProvider)(disVariables)
circ.add_hadamards(disVariables)

weightedFormulas = {
    "f1": ["imp", "sledz", "jaszczur", True],
    "f2": ["and", "jaszczur", "kaczka", False],
    "f3": ["or", "sledz", "kaczka", -1],
    "f4" : ["lpas", "jaskuka", 1]
}

for formulaKey in weightedFormulas:
    circ = representation.add_formula_to_circuit(circ, weightedFormulas[formulaKey][:-1])

sliceTuples = representation.calculate_angles(representation.get_color_param_dict(weightedFormulas))

headColor = "samplingAncilla"

for sliceTuple in sliceTuples:
    circ.add_controlled_rotation(sliceTuple, headColor)

shotNum = 1000
circ.add_measurement(disVariables + [headColor])
filtered = reasoning.filter_results(circ.run(shotNum)).values

jaskukaTrueCount = len([res for res in filtered if res[3]==1])

print("{} out of {} samples accepted.".format(len(filtered),shotNum))
print("Expectation rate of f4 is {} and estimated by {}.".format(math.e/(math.e+1), jaskukaTrueCount/len(filtered)))

assert abs(jaskukaTrueCount/len(filtered) - math.e/(math.e+1)) < 0.05