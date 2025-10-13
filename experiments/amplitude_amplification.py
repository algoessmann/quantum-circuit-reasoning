from qcreason import engine, representation
import  matplotlib.pyplot as plt

circuitProvider =  "PennyLaneCircuit"

disVariables = ["sledz", "jaszczur", "kaczka", "jaskuka", "pstrag"]
weightedFormulas = {"f1": ["imp", "sledz", "jaszczur", -3],
                    "f2": ["id", "kaczka", False],
                    "f3": ["id", "jaskuka", True],
                    "f4": ["id", "pstrag", 0.5]}

def acceptanceRate(results):
    return sum([result[-1] for result in results])/len(results)

for amiplitNum in range(20):
    circ = engine.get_circuit(circuitProvider)(disVariables)
    circ = representation.compute_and_activate(circ, weightedFormulas)
    circ = representation.amplify(circ, weightedFormulas, amiplitNum)
    circ.add_measurement(disVariables + ["samplingAncilla"])
    #circ.visualize()
    shotNum = 10000
    results = circ.run(shots=shotNum)
    print(acceptanceRate(results))
    #print(results)

    #for result in results: ## Check the first formula: Needs to be hard!
    #    assert not result[-1] or (result[0] and not result[1])