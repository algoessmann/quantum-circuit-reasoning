from qcreason import representation

from qcreason.reasoning.rejection_sampling import filter_results


class HLNForwardCircuitSampler:

    def __init__(self, formulaDict, canParamDict, circuitProvider=representation.standardCircuitProvider,
                 amplificationNum=2, shotNum=1000):
        self.formulaDict = formulaDict
        self.canParamDict = canParamDict

        self.circuitProvider = circuitProvider
        self.amplificationNum = amplificationNum
        self.shotNum = shotNum

    def infer_meanParam(self, formulaKeys, verbose=False):
        circuit = representation.get_amplified_circuit(
            {formulaKey: self.formulaDict[formulaKey] + [self.canParamDict[formulaKey]] for formulaKey in
             self.formulaDict}, self.amplificationNum, atomColors=representation.get_atoms(self.formulaDict),
            circuitProvider=self.circuitProvider)
        circuit.add_measurement(
            [representation.get_formula_string(self.formulaDict[formulaKey]) for formulaKey in formulaKeys] + [
                representation.standardAncillaColor])
        samples = filter_results(circuit.run(shots=self.shotNum))

        if verbose:
            print("Out of {} shots, {} samples have been accepted.".format(self.shotNum, len(samples)))

        return {formulaKey: samples[representation.get_formula_string(self.formulaDict[formulaKey])].mean() for
                formulaKey in formulaKeys}
