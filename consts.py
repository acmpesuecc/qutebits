import numpy as np
import math
from QuantumCircuit import QGate as g

GATE_HADAMARD = (1/math.sqrt(2)) * np.array([[1, 1],
                                             [1, -1]])
GATE_PAULI_X = np.array([[0, 1],
                         [1, 0]])

GATE_PAULI_Y = np.array([[0, -1j],
                         [1j, 0]])

GATE_PAULI_Z = np.array([[1, 0],
                         [0, -1]])

GATE_CNOT = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 1],
                      [0, 0, 1, 0]])

GATE_CNOT_OPP = np.array([[1, 0, 0, 0],
                          [0, 0, 0, 1],
                          [0, 0, 1, 0],
                          [0, 1, 0, 1]])

gate2matrix = {
    g.HADAMARD: GATE_HADAMARD,
    g.PAULI_X: GATE_PAULI_X,
    g.PAULI_Y: GATE_PAULI_Y,
    g.PAULI_Z: GATE_PAULI_Z,
    g.CNOT_START: GATE_CNOT,
    g.CNOT_END: GATE_CNOT_OPP
}
