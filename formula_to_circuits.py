import qc_from_bpCP as qcfb

import numpy as np


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


aliases = {
    "xor": "neq",
    "lpas": "pas0",
    "id": "pas0",
    "not": "npas0"
}


def get_bpCP(connectiveKey, inColors):
    """
    Generate the basis plus connective decompositions for a given connective and input colors.
    :param connectiveKey: Same connective strings as in tnreason.representation.basisPlus_calculus
    :param inColors: List of input colors
    :return: Mod2-basis+ CP decomposition by a list of slices
    """
    if connectiveKey in aliases:
        connectiveKey = aliases[connectiveKey]

    if connectiveKey == "and":
        return [{c: 1 for c in inColors}]
    elif connectiveKey == "or":
        return [{}, {c: 0 for c in inColors}]
    elif connectiveKey == "eq":
        return [{inColor: 1 for inColor in inColors}, {inColor: 0 for inColor in inColors}]
    elif connectiveKey == "imp":
        return [{}, {**{inColor: 0 for inColor in inColors[:-1]}, inColors[-1]: 0}]
    elif connectiveKey.startswith("pas"):
        pos = int(connectiveKey[3:])
        assert pos < len(inColors)
        return [{inColors[pos]: 0}]
    elif connectiveKey.startswith("n"):
        return [{}] + get_bpCP(connectiveKey[1:], inColors)

    ## Then understood as a Wolfram number
    try:
        int(connectiveKey)
    except:
        raise ValueError("Function {} is not a Wolfram number".format(connectiveKey))

    binDigits = bin(int(connectiveKey))[2:]  # Since have a prefix 0b for binary variables
    order = len(inColors)
    if len(binDigits) != 2 ** order:
        binDigits = "0" * (2 ** order - len(binDigits)) + binDigits  # Fill length of digits to 2 ** order

    return [{inColor: indices[i] for i, inColor in enumerate(inColors)} for indices in
            np.ndindex(*[2 for _ in range(order)]) if
            int(binDigits[2 ** order - 1 - int("".join(map(str, indices)), 2)]) == 1]


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    qc, qubitDict = qcfb.initialize_circuit(["a", "b", "c"])
    formula_to_circuits(qc, qubitDict, ["or", ["not", "b"], "c"])

    qc, qubitDict = qcfb.initialize_circuit(["a", "b", "c"])
    formula_to_circuits(qc, qubitDict, ["01100001", "a",  "b", "c"])

    qc.draw("mpl")
    plt.show()
