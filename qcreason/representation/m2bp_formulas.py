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


# def extract_atoms_from_dict(weightedFormulaDict):
#     return list(
#         set().union(*[extract_atoms(weightedFormulaDict[formulaKey][:-1]) for formulaKey in weightedFormulaDict]))
#
#
# def extract_atoms(formula):
#     if isinstance(formula, str):
#         return {formula}
#     else:
#         return set().union(*[extract_atoms(subf) for subf in formula[1:]])


def generate_formula_operations(formula, ajoint=False):
    """
    Generate the list of operations (connectives) in a formula in order of application.
    :param formula:
    :return:
    """
    if isinstance(formula, str):
        return []

    elif not ajoint:
        ops = []
        for subFormula in formula[1:]:
            ops = ops + generate_formula_operations(subFormula)

        ops += mc.get_connective_operations(formula[0], [get_formula_string(subf) for subf in formula[1:]],
                                                get_formula_string(formula))
        return ops
    else:
        ops = []
        ops += mc.get_connective_operations(formula[0], [get_formula_string(subf) for subf in formula[1:]],
                                                get_formula_string(formula))
        for subFormula in formula[::-1][:-1]:
            ops += generate_formula_operations(subFormula)

        return ops


def add_formula_to_circuit(circ, formula, adjoint=False):
    """
    Recursively convert a logical formula into a quantum circuit using mod2-basis+ CP decomposition of each connective.
    :param qc:
    :param qubitDict:
    :param formula:
    :return:
    """
    if isinstance(formula, str):
        return circ
    elif adjoint:  ## Do the same, but in reverse order, use that cnot is self-adjoint
        connective = formula[0]
        inColors = [get_formula_string(subf) for subf in formula[1:]]
        circ.add_directed_block(mc.get_bpCP_connective(connective, inColors), get_formula_string(formula))
        for subFormula in formula[::-1][:-1]:
            circ = add_formula_to_circuit(circ, subFormula, adjoint=True)
        return circ
    else:
        for subFormula in formula[1:]:
            circ = add_formula_to_circuit(circ, subFormula)

        connective = formula[0]
        inColors = [get_formula_string(subf) for subf in formula[1:]]
        circ.add_directed_block(mc.get_bpCP_connective(connective, inColors), get_formula_string(formula))
        return circ
