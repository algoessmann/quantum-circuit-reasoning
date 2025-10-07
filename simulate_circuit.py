import qc_from_bpCP as qcfb
import qiskit as qk

qc, qubitDict = qcfb.initialize_circuit(["a", "b"], "c")
qc = qcfb.add_directed_block(qc, qubitDict, [{"a": 1, "b": 0}, {"b": 1}], ["a", "b"], "c")

from qiskit_aer import AerSimulator
sim = AerSimulator()
tqc = qk.transpile(qc, sim)

# Run the transpiled circuit on the simulator
job = sim.run(tqc, shots=1000)
result = job.result()

# Get the counts of the results
counts = result.get_counts(tqc)
print("\nTotal counts are:", counts)