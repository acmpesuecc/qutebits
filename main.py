from Executor import Executor
from QuantumCircuit import *

circ = QuantumCircuit(2)
circ.h(0)
circ.h(1)
circ.y(0)
circ.draw()
exp = Executor(circ)
print(exp.get_statevector())
print(exp.get_probs())
counts = exp.measure_all()
print(counts)
