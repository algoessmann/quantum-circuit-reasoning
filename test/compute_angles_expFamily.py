import numpy as np


def calculate_angles(canParamDict):
    """
    Calculate the angles for controlled rotations implementing a given exponential family distribution.
    :param canParamDict: specifies the distribution by
    :return:
    """

    controlVariables = list(canParamDict.keys())
    maxValue = np.exp(sum([canparam for canparam in canParamDict.values() if canparam > 0]))


    return [(np.arccos(
        np.sqrt(np.exp(sum([canParamDict[controlVariables[i]] * val for i, val in enumerate(vals)])) / maxValue)),
             {var: vals[i] for i, var in enumerate(controlVariables)})
            for vals in np.ndindex(*(2,) * len(controlVariables))]


if __name__ == "__main__":
    canParamDict = {
        "sledz": 0.1,
        "jaszczur": 2,
        "kaczka": -1
    }
    print(calculate_angles(canParamDict))
