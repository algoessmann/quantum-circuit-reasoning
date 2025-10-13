
from qcreason import engine
from qcreason import representation

circuitProvider = "PennyLaneCircuit" # "QiskitCircuit"

disVariables = ["sledz", "jaszczur", "kaczka"]
weightedFormulas = {
    "f1": ["imp", "sledz", "jaszczur", True],
    "f2": ["and", "jaszczur", "kaczka", False],
    "f3": ["or", "sledz", "kaczka", -1]
}

circ = engine.get_circuit(circuitProvider)(disVariables)
circ.add_hadamards(disVariables)
circ = representation.compute_and_activate(circ, weightedFormulas, atomColors=disVariables)
circ = representation.amplify(circ, weightedFormulas, 1, atomColors=disVariables)
circ.add_measurement(disVariables + ["(imp_sledz_jaszczur)", "(and_jaszczur_kaczka)"] + ["samplingAncilla"])
#circ.visualize()

shotNum = 100
results = circ.run(shots=shotNum)
satisfactionRate = [result[-1] for result in results].count(1)/shotNum
print("Satisfaction rate is {}.".format(satisfactionRate))

for i in range(shotNum):
    ## When sampling ancilla is true, the hard formulas must be satisfied
    assert not results[i][-1] or results[i][-3]
    assert not results[i][-1] or not results[i][-2]

