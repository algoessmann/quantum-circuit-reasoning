from qcreason.representation import m2bp_connectives as mc


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


def add_formula_to_circuit(circ, formula):
    """
    Recursively convert a logical formula into a quantum circuit using mod2-basis+ CP decomposition of each connective.
    :param qc:
    :param qubitDict:
    :param formula:
    :return:
    """
    if isinstance(formula, str):
        return circ
    else:
        for subFormula in formula[1:]:
            circ = add_formula_to_circuit(circ, subFormula)

        connective = formula[0]
        inColors = [get_formula_string(subf) for subf in formula[1:]]
        circ.add_directed_block(mc.get_bpCP_connective(connective, inColors), get_formula_string(formula))
        return circ

