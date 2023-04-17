from QuantumCircuit import QuantumCircuit, QGate
import numpy as np
from consts import gate2matrix, cnots
import random

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
                else:
                    gate = QGate.IDENTITY
                g_matrix = gate2matrix[gate]
                # print(f"layer: {i}, qubit: {j}, gate: {gate}")
                layer_matrix = np.kron(layer_matrix, g_matrix)
                # print(layer_matrix)

                if gate in cnots:
                    skip = True
            self.state_vector = layer_matrix@self.state_vector

    def get_statevector(self):
        return self.state_vector

    def get_probs(self):
        probabilities = [np.round(abs(e)**2, 4) for e in self.state_vector]
        return probabilities

    def measure_all(self, shots=8096):
        values = [i for i in range(len(self.state_vector))]
        probabilities = [np.round(abs(e)**2, 4) for e in self.state_vector]
        # cum_probs = [probabilities[0]]
        # for i in range(1, len(probabilities)):
        #     cum_probs.append(cum_probs[i-1]+probabilities[i])
        # # print(probabilities)
        # # print(cum_probs)
        counts = [0 for _ in self.state_vector]
        for _ in range(shots):
            choice = random.choices(values, weights=probabilities, k=1)[0]
            counts[choice]+=1
        return counts


