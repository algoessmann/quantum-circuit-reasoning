def get_adjoint_circuit(operationsList):
    return [get_adjoint_operation(op) for op in operationsList[::-1]]

def get_adjoint_operation(operationDict):
    if operationDict["unitary"] in ["MCX","MCZ","H"]:
        return operationDict
    elif operationDict["unitary"] == "MCRY":
        adjointOp = operationDict.copy()
        adjointOp["parameters"] = {"angle": -operationDict["parameters"]["angle"]}
        return adjointOp

def get_groundstate_reflexion_operations(qubitColors):
    ops = [{"unitary": "MCX", "targetQubits": [color], "control": {}} for color in qubitColors]
    ops.append({"unitary": "MCZ", "targetQubits": [qubitColors[-1]], "control": {color: 1 for color in qubitColors[:-1]}})
    ops += [{"unitary": "MCX", "targetQubits": [color], "control": {}} for color in qubitColors]
    return ops

def get_hadamard_gates(qubitColors):
    return [{"unitary": "H", "targetQubits": [color]} for color in qubitColors]

# def extract_qubit_colors(operationsList):
#     colors = set()
#     for op in operationsList:
#         if "targetQubits" in op:
#             for color in op["targetQubits"]:
#                 colors.add(color)
#         if "control" in op:
#             for color in op["control"].keys():
#                 colors.add(color)
#     return list(colors)

def amplify_ones_state(preparingOperations, amplificationColors, amplificationNum=1):
    ops = []
    ops += preparingOperations
    for amplificationStep in range(amplificationNum):
        ops += [{"unitary": "MCZ", "targetQubits": [amplificationColors[-1]], "control": {color : 1 for color in amplificationColors[:-1]}}]
        ops += get_adjoint_circuit(preparingOperations)
        ops += get_groundstate_reflexion_operations(amplificationColors)
        ops += preparingOperations
    return ops