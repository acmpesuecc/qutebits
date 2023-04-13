from enum import Enum, auto

class QGate(Enum):
	HADAMARD = "H"
	PAULI_X  = "X"
	PAULI_Y = "Y"
	PAULI_Z = "Z"

class QuantumCircuit:
	def __init__(self, no_qubits):
		self.no_qubits = no_qubits
		self.circ = [[] for _ in range(no_qubits)]

	def draw(self):
		for qubit_gates in self.circ:
			print("|0>", end="")
			for gate in qubit_gates:
				print(f"-|{gate.value}|-", end="")
			print()

	def h(self, index):
		self.circ[index].append(QGate.HADAMARD)

	def x(self, index):
		self.circ[index].append(QGate.PAULI_X)

	def y(self, index):
		self.circ[index].append(QGate.PAULI_Y)

