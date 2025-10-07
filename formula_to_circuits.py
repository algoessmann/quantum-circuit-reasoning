import qc_from_bpCP as qcfb


def formula_to_circuits(qc, qubitDict, formula):
    """
    Recursively convert a logical formula into a quantum circuit using mod2-basis+ CP decomposition of each connective.
    :param qc:
    :param qubitDict:
    :param formula:
    :return:
    """
    if isinstance(formula, str):
        return qc, qubitDict
    else:
        for subFormula in formula[1:]:
            qc, qubitDict = formula_to_circuits(qc, qubitDict, subFormula)

        connective = formula[0]
        inColors = [get_formula_string(subf) for subf in formula[1:]]
        return qcfb.add_directed_block(qc, qubitDict, get_bpCP(connective, inColors), get_formula_string(formula))


def get_formula_string(formula):
    """
    Generate a string representation of a formula, used for qubit coloring.
    :param formula:
    :return:
    """
    if isinstance(formula, str):
        return formula
    else:
        return "(" + formula[0] + "_" + "_".join(get_formula_string(subf) for subf in formula[1:]) + ")"


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
    elif connectiveKey == "not":
        return [{inColors[0]: 0}]
    else:
        raise ValueError("Unsupported connective: " + connectiveKey)

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    qc, qubitDict = qcfb.initialize_circuit(["a", "b", "c"])
    formula_to_circuits(qc, qubitDict, ["or", ["not", "b"], "c"])

    qc.draw("mpl")
    plt.show()
