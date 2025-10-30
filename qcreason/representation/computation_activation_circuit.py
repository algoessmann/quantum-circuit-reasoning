from qcreason.representation import m2bp_formulas as mf
from qcreason.representation import activation_circuits as ac
from qcreason.representation import logic_encoding as le
from qcreason.representation import operations_transform as ot

def get_hln_ca_operations(weightedFormulaDict, ancillaPrefix="ancilla_"):
    """

    :param weightedFormulaDict:
    :param ancillaPrefix:
    :return:
    """
    ops = ot.get_hadamard_gates(le.get_atoms_from_weightedFormulasDict(weightedFormulaDict))
    for formulaKey in weightedFormulaDict:
        ops += mf.generate_formula_operations(weightedFormulaDict[formulaKey][:-1])
        ops += ac.single_canParam_to_activation_circuit(canParam=weightedFormulaDict[formulaKey][-1],
                                              statisticColor=mf.get_formula_string(
                                                  weightedFormulaDict[formulaKey][:-1]),
                                              ancillaColor=ancillaPrefix + mf.get_formula_string(
                                                  weightedFormulaDict[formulaKey][:-1]))
    return ops


