def filter_results(results, ancillaColors = ["samplingAncilla"]):
    ## Drop the samples where the sampling ancilla is 0
    if len(ancillaColors) == 1: ## OLD behavior for single ancilla
        return results[results[ancillaColors[0]]==1]
    return results[results[ancillaColors].sum(axis=1)==len(ancillaColors)]


def compute_satisfaction(resultDf, weightedFormulas):
    from tnreason import application as tnapp
    from tnreason import engine as tneng

    empDistribution = tnapp.get_empirical_distribution(sampleDf=resultDf)
    satDict = dict()
    for formulaKey in weightedFormulas:
        satDict[formulaKey] = tneng.contract(
            {**empDistribution.create_cores(),
             **tnapp.create_cores_to_expressionsDict({formulaKey : weightedFormulas[formulaKey][:-1]})},
            openColors=[])[:] / empDistribution.get_partition_function()
    return satDict