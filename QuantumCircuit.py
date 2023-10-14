from enum import Enum, auto
import io

class QGate(Enum):
    HADAMARD = "H"
    PAULI_X = "X"
    PAULI_Y = "Y"
    PAULI_Z = "Z"
    CNOT_START = "."
    CNOT_END = "x"
    IDENTITY = "I"
    START = "0"

cnots = [QGate.CNOT_START, QGate.CNOT_END]


class QuantumCircuit:
    def __init__(self, no_qubits):
        self.no_qubits = no_qubits
        self.circ = [[] for _ in range(no_qubits)]

    def __str__(self):
        out = io.StringIO()
        for qubit_gates in self.circ:
            print("|0>", end="", file=out)
            for gate in qubit_gates:
                gate = gate[0]
                if gate == QGate.IDENTITY:
                    print("-----", end="", file=out)
                else:
                    print(f"-|{gate.value}|-", end="", file=out)
            print("\n", file=out)
            # print(2*" ", end="", file = out)
            # for i, gate in enumerate(qubit_gates):
            #     gate = gate[0]
            #     if gate in cnots:
            #         print(5*i*" ", "  |  ", file = out)
        return out.getvalue()

    def draw(self):
        print(end=self.__str__())

    def h(self, index):
        self.circ[index].append((QGate.HADAMARD,))

    def x(self, index):
        self.circ[index].append((QGate.PAULI_X,))

    def y(self, index):
        self.circ[index].append((QGate.PAULI_Y,))

    def z(self, index):
        self.circ[index].append((QGate.PAULI_Z,))

    def cx(self, start, end):
        if start+1 != end and start-1 != end:
            raise NotImplementedError(
                "CNOT for non adjacent qubits not implemented yet")

        insert_index = max(len(self.circ[start]), len(self.circ[end]))

        while len(self.circ[start]) < insert_index:
            self.circ[start].append((QGate.IDENTITY,))
        self.circ[start].append((QGate.CNOT_START, end))

        while len(self.circ[end]) < insert_index:
            self.circ[end].append((QGate.IDENTITY,))
        self.circ[end].append((QGate.CNOT_END, start))
