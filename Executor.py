from QuantumCircuit import QuantumCircuit, QGate
import numpy as np
from consts import gate2matrix

cnots = [QGate.CNOT_START, QGate.CNOT_END]


class Executor:
    def __init__(self, qc: QuantumCircuit):
        self.state_vector = np.zeros(2**qc.no_qubits)
        self.state_vector[0] = 1
        skip = False
        max_len = max([len(e) for e in qc.circ])
        for i in range(max_len):
            layer_matrix = np.array([[1]])
            for j in range(qc.no_qubits):
                if skip:
                    skip = False
                    continue

                if i<len(qc.circ[j]):
                    gate = qc.circ[j][i][0]
                    g_matrix = gate2matrix[gate]
                else:
                    gate = None
                    g_matrix = np.eye(2)
                # print(f"layer: {i}, qubit: {j}, gate: {gate}")
                layer_matrix = np.kron(layer_matrix, g_matrix)
                # print(layer_matrix)

                if gate in cnots:
                    skip = True
            self.state_vector = layer_matrix@self.state_vector

    def get_statevector(self):
        return self.state_vector
