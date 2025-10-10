from qcreason import engine, representation
import  matplotlib.pyplot as plt

circuitProvider =  "QiskitCircuit"

disVariables = ["sledz", "jaszczur", "kaczka"]
circ = engine.get_circuit(circuitProvider)(disVariables)
circ = representation.formulas_to_circuit.add_formula_to_circuit(circ, ["imp", "sledz", "jaszczur"])



import qiskit as qk


reflect_0 = qk.QuantumCircuit(*[qk.QuantumRegister(1, name=c) for c in disVariables])
n = len(disVariables)
reflect_0.x(range(n))
reflect_0.h(n-1)
reflect_0.mcx(list(range(n-1)), n-1)
reflect_0.h(n-1)
reflect_0.x(range(n))

composed = circ.circuit.compose(reflect_0).compose(circ.circuit.inverse())

composed.draw("mpl")
plt.show()