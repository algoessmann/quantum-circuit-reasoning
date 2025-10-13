from qcreason.representation import m2bp_formulas as mf

import numpy as np


def probability_to_angle(prob):
    """
    Calculates an angle alpha, such that R_y(alpha) rotates (1,0) to (sqrt(1-prob), sqrt(prob))
    :param prob:
    :return:
    """
    return 2 * np.arccos(np.sqrt(1 - prob))


def calculate_angles(canParamDict):
    """
    Calculate the angles for controlled rotations implementing a given exponential family distribution.
    :param canParamDict: specifies the distribution by canonical parameters, keys: statistic qubit colors to formulas, values: canonical parameters
    :return:
    """

    controlVariables = list(canParamDict.keys())
    maxValue = np.exp(sum([par for par in canParamDict.values() if par > 0 and not isinstance(par, bool)]))

    angleSlices = []

    for vals in np.ndindex(*(2,) * len(controlVariables)):
        if any([isinstance(canParamDict[controlVariables[i]], bool) and bool(vals[i]) != canParamDict[
            controlVariables[i]] for i in range(len(controlVariables))]):
            ## Then the distribution has no support
            angleSlices.append((0, {var: vals[i] for i, var in enumerate(controlVariables)}))
        else:
            ## Then the sampling probability is the quotient to the maxValue
            angleSlices.append((probability_to_angle(
                np.exp(sum([canParamDict[controlVariables[i]] * val for i, val in enumerate(vals) if
                            not isinstance(canParamDict[controlVariables[i]], bool)])) / maxValue),
                                {var: vals[i] for i, var in enumerate(controlVariables)}))

    return angleSlices

def compute_and_activate(circuit, weightedFormulaDict, ancillaColor="samplingAncilla"):
    ## Compute the statistic formulas
    for formulaKey in weightedFormulaDict:
        circuit = mf.add_formula_to_circuit(circuit, weightedFormulaDict[formulaKey][:-1])
    ## Compute the sampling ancilla for activation
    angleTuples = calculate_angles(get_color_param_dict(weightedFormulaDict))
    for angleTuple in angleTuples:
        circuit.add_controlled_rotation(angleTuple, ancillaColor)
    return circuit

def get_color_param_dict(weightedFormulas):
    return {mf.get_formula_string(weightedFormulas[formulaKey][:-1]): weightedFormulas[formulaKey][-1] for formulaKey in
            weightedFormulas}

#def amplify(circuit, weightedFormulaDict, amplificationNum, ancillaColor="samplingAncilla"):
#    for amplificationStep in range(amplificationNum):
#        circuit = compute_and_activate(circuit, weightedFormulaDict, ancillaColor)
