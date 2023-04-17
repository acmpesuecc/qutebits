from Executor import Executor
from QuantumCircuit import *

circ = QuantumCircuit(2)
circ.h(0)
circ.x(1)
circ.y(0)
circ.draw()
exp = Executor(circ)

