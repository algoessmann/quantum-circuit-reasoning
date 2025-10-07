from qcreason import engine
from qcreason import representation

circ = engine.get_circuit("PennyLaneCircuit")(["a", "b", "c"])

circ = representation.add_formula_to_circuit(circ, ["0100", ["imp", "a", "c"], ["not", "b"]])
circ.add_measurement(["b","(not_b)"])
#circ.visualize()

# Run the circuit
results = circ.run(shots=10000)

for i in range(10):
    assert (results[i][0] == 1 and results[i][1] == 0) or (results[i][0] == 0 and results[i][1] == 1)