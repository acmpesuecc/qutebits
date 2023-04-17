from enum import Enum, auto


class QGate(Enum):
    HADAMARD = "H"
    PAULI_X = "X"
    PAULI_Y = "Y"
    PAULI_Z = "Z"
    CNOT_START = "."
    CNOT_END = "x"


class QuantumCircuit:
    def __init__(self, no_qubits):
        self.no_qubits = no_qubits
        self.circ = [[] for _ in range(no_qubits)]

    def draw(self):
        for qubit_gates in self.circ:
            print("|0>", end="")
            for gate in qubit_gates:
                gate = gate[0]
                print(f"-|{gate.value}|-", end="")
            print("\n")

    def h(self, index):
        self.circ[index].append((QGate.HADAMARD,))

    def x(self, index):
        self.circ[index].append((QGate.PAULI_X,))

    def y(self, index):
        self.circ[index].append((QGate.PAULI_Y,))

    def cx(start, end):
        if start+1 != end and start-1 != end:
            raise NotImplementedError(
                "CNOT for non adjacent qubits not implemente yet")
        self.circ[start].append((QGate.CNOT_START, end))
        self.circ[end].append((QGate.CNOT_END, start))
