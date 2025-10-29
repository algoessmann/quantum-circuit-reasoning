import numpy as np


def probability_to_angle(prob):
    """
    Calculates an angle alpha, such that R_y(alpha) rotates (1,0) to (sqrt(1-prob), sqrt(prob))
    :param prob:
    :return:
    """
    return 2 * np.arccos(np.sqrt(1 - prob))


def generate_activation_circuit(canParam, statisticColor, ancillaColor="samplingAncilla"):
    """
    Prepares the activation circuit for a single activation tensor of the HLN parametrized by a canonical parameter.
    :param canParam:
    :param statisticColor:
    :param ancillaColor:
    :return:
    """

    if isinstance(canParam, bool):
        return [{"unitary": "MCX", "targetQubits": [ancillaColor], "control": {statisticColor: int(canParam)}}]
    else:
        maxValue = np.exp(max(0, canParam))
        return [{"unitary": "MCRY", "targetQubits": [ancillaColor], "control": {statisticColor: val},
                 "parameters": {"angle": probability_to_angle(np.exp(val * canParam) / maxValue)}} for val in [0, 1]]
