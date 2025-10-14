def filter_results(results):
    ## Drop the samples where the sampling ancilla is 0
    return [result[:-1] for result in results if result[-1] == 1]
