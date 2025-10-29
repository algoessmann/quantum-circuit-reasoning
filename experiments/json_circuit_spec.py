import json
from qiskit import QuantumCircuit

def load_circuit_from_json(json_data):
    data = json.loads(json_data)
#    qc = QuantumCircuit(len(data["qubits"]), name="json_circuit")
    qubit_map = {name: i for i, name in enumerate(data["qubits"])}

    return data


import json

# Define the circuit structure as a Python dictionary
quantum_circuit = {
    "qubits": ["q0", "q1", "q2"],
    "operations": [
        {
            "unitary": "H",
            "qubits": ["q0"],
            "control": {}
        },
        {
            "unitary": "CNOT",
            "qubits": ["q0", "q1"],
            "control": {}
        },
        {
            "unitary": "RX",
            "qubits": ["q2"],
            "control": {},
            "parameters": {"theta": 1.5708}
        },
        {
            "unitary": "Z",
            "qubits": ["q2"],
            "control": {"q0": 1, "q1": 0}
        },
        {
            "unitary": "MEASURE",
            "qubits": ["q0", "q1", "q2"],
            "control": {}
        }
    ]
}

# Convert the dictionary to a JSON string (pretty printed)
json_string = json.dumps(quantum_circuit, indent=4)

# Print or save it
#print(json_string)
print(load_circuit_from_json(json_string)["operations"])
#print(json_string["operations"])

# Optionally, save to a file
#with open("quantum_circuit.json", "w") as f:
#    json.dump(quantum_circuit, f, indent=4)
