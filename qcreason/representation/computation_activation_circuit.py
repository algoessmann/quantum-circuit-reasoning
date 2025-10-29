from qcreason.representation import m2bp_formulas as mf
from qcreason.representation import activation_circuits as ac
from qcreason.representation import logic_encoding as le
from qcreason.representation import operations_transform as ot

def get_ca_operations(weightedFormulaDict, ancillaPrefix="ancilla_", adjoint=False):
    ops = ot.get_hadamard_gates(le.get_atoms_from_weightedFormulasDict(weightedFormulaDict))
    # for atom in le.get_atoms(weightedFormulaDict): #mf.extract_atoms_from_dict(weightedFormulaDict):
    #     ops.append({"unitary" : "H",
    #                 "targetQubits" : [atom],
    #                 "controlDict" : dict()})
    for formulaKey in weightedFormulaDict:
        ops += mf.generate_formula_operations(weightedFormulaDict[formulaKey][:-1], ajoint=adjoint)
        ops += ac.generate_activation_circuit(canParam=weightedFormulaDict[formulaKey][-1],
                                              statisticColor=mf.get_formula_string(
                                                  weightedFormulaDict[formulaKey][:-1]),
                                              ancillaColor=ancillaPrefix + mf.get_formula_string(
                                                  weightedFormulaDict[formulaKey][:-1]))
    return ops


