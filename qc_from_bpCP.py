import qiskit as qk


def initialize_circuit(inColors):
    registers = [qk.QuantumRegister(1, name=c) for c in inColors]
    qc = qk.QuantumCircuit(*registers)
    qubitDict = {**{inColors[i]: qc.qubits[i] for i in range(len(inColors))}}

    for inColor in inColors:
        qc.h(qubitDict[inColor])

    return qc, qubitDict


def add_directed_block(qc, qubitDict, basPlusCP, headColor):
    if headColor not in qubitDict:
        qc.add_register(qk.QuantumRegister(1, name=headColor))
        qubitDict[headColor] = qc.qubits[-1]

    for posDict in basPlusCP:
        add_slice(qc, qubitDict, posDict, headColor)

    return qc, qubitDict


def add_slice(qc, qubitDict, posDict, headColor):
    if len(posDict) == 0:
        qc.x(qubitDict[headColor])
        return

    for inColor in posDict:
        if posDict[inColor] == 0:
            qc.x(qubitDict[inColor])

    qc.mcx([qubitDict[inColor] for inColor in posDict], qubitDict[headColor])

    for inColor in posDict:
        if posDict[inColor] == 0:
            qc.x(qubitDict[inColor])


def add_measurement(qc, qubitDict, tbMeasured):
    cr = qk.ClassicalRegister(len(tbMeasured), name="measure")
    qc.add_register(cr)
    qc.measure([qubitDict[c] for c in tbMeasured], range(len(tbMeasured)))


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    qc, qubitDict = initialize_circuit(["a", "b"])
    bpCP = [{"a": 1, "b": 0}, {"b": 1}]
    qc, qubitDict = add_directed_block(qc, qubitDict, bpCP, "c")
    add_measurement(qc, qubitDict, ["c", "a", "b"])

    qc.draw("mpl")
    plt.show()


