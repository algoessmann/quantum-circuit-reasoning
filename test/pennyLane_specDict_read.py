from qcreason import representation
from qcreason.representation import m2bp_connectives as mc

from qcreason.engine import pennylane_circuits as pc

print(mc.get_connective_operations("not","a","(not_a)")[0])
print(pc.get_operation_from_unitaryDict(mc.get_connective_operations("not","a","(not_a)")[0]))