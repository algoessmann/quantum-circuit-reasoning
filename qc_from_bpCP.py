import qiskit as qk


def initialize_circuit(inColors):
    registers = [qk.QuantumRegister(1, name=c) for c in inColors]
    qc = qk.QuantumCircuit(*registers)
    qubitDict = {**{inColors[i]: qc.qubits[i] for i in range(len(inColors))}}

    for inColor in inColors:
        qc.h(qubitDict[inColor])

    return qc, qubitDict


def get_bpCP(connectiveKey, inColors):
    """
    Generate the basis plus connective decompositions for a given connective and input colors.
    :param connectiveKey: Same connective strings as in tnreason.application
    :param inColors: List of input colors
    :return: Mod2-basis+ CP decomposition by a list of slices
    """
    if connectiveKey == "and":
        return [{c: 1 for c in inColors}]
    elif connectiveKey == "or":
        return [{}, {c: 0 for c in inColors}]


def add_directed_block(qc, qubitDict, basPlusCP, headColor):
    if headColor not in qubitDict:
        qc.add_register(qk.QuantumRegister(1, name=headColor))
        qubitDict[headColor] = qc.qubits[-1]

    for posDict in basPlusCP:
        add_slice(qc, qubitDict, posDict, headColor)

    return qc, qubitDict


def add_slice(qc, qubitDict, posDict, headColor):
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

    # qc, qubitDict = initialize_circuit(["a", "b"])
    # bpCP = get_bpCP("and", ["a","b"])
    # qc, qubitDict = add_directed_block(qc, qubitDict, bpCP, "cHead")
    # add_measurement(qc, qubitDict, ["c","a","b"])
    #
    # qc.draw("mpl")
    # plt.show()
