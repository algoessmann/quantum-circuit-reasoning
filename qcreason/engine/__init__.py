def get_circuit(circuitType="QiskitCircuit"):
    if circuitType == "QiskitCircuit":
        from qcreason.engine import qiskit_circuits as qkc
        return qkc.QiskitCircuit
    else:
        raise ValueError(f"Unknown circuit type: {circuitType}")
