from qcreason.representation.m2bp_connectives import get_bpCP_connective
from qcreason.representation.m2bp_formulas import get_formula_string, add_formula_to_circuit

from qcreason.representation.activation_by_ancilla import calculate_angles, get_color_param_dict, compute_and_activate, \
    amplify

from qcreason.representation.logic_encoding import get_atoms

from qcreason import engine

standardCircuitProvider = "PennyLaneCircuit"
standardAncillaColor = "samplingAncilla"

def get_amplified_circuit(weightedFormulaDict, amplificationNum, atomColors, ancillaColor=standardAncillaColor,
                          circuitProvider=standardCircuitProvider):
    circuit = engine.get_circuit(circuitProvider)(atomColors)
    circuit = compute_and_activate(circuit, weightedFormulaDict, atomColors, ancillaColor)
    circuit = amplify(circuit, weightedFormulaDict, amplificationNum, atomColors, ancillaColor)
    return circuit
