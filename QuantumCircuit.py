from enum import Enum, auto

class QGate(Enum):
	HADAMARD = "H"

class QuantumCircuit:
	def __init__(self, no_qubits):
		self.no_qubits = no_qubits
		self.circ = [[] for _ in range(no_qubits)]

	def draw(self):
		for i in range(self.no_qubits):
			print("|0>", end="")
			for j in i:
				print(f"-|{J}|-")

	def h(self, index):
		self.circ[index].append(QGate.HADAMARD)

