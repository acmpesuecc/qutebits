# Qutebits Documentation

There are 2 main classes: `QuantumCircuit` and `Executor`, and an enum `QGate` :

`QuantumCircuit` - used to define a new Quantum Circuit and add `QGate`s to the `QuantumCircuit`.

`Executor` - actually executes the `QuantumCircuit`

`QGate` is an enum which has options of all the gates supported.



## `QGate`

is a Enum whihc can be one of the following values:

```python
class QGate(Enum):
    HADAMARD = "H"
    PAULI_X = "X"
    PAULI_Y = "Y"
    PAULI_Z = "Z"
    CNOT_START = "."
    CNOT_END = "x"
    IDENTITY = "I"

```

## `QuantumCircuit`

**Initializer:**

````python
QuantumCircuit(no_qubits: int)
````

`no_qubits` - Number of qubits in the Quantum Circuit. It is assumed that same number of classical bits wills be there for use in measurement.

**Methods:**

```python
draw()
```

Print out the quantum circuit using basic ascii text

```python
cx(start, end)
```

Applies a Controlled NOT gate on the`QuantumCircuit` with the `start` index as the control qubit and the `end` qubit as the target qubit where both `start` and `end` are the indices of the qubits in the `QuantumCircuit` which be in the range `0` to `no_qubits-1`

Note: Applying CNOT gate on non-adjacent qubits is not yet supported

```python
h(index)
```

Applies a Hadamard gate on the qubit at index `index`

```python
x(index)
```

Applies a X gate on the qubit at index `index`

```
y(index)
```

Applies a Y gate on the qubit at index `index`

```
z(index)
```

Applies a Z gate on the qubit at index `index`



## `Executor`

**Initializer:**

```python
Executor(qc: QuantumCircuit)
```

`qc` - The `QuantumCircuit` Object to be executed

**Methods:**

```
get_statevector()
```

returns the final statevector of the Quantum Circuit as a list

```
get_probs()
```

returns the probabilities of all computational basis state as a list

```
measure_all(shots=8096)
```

`shots` - the number of times the circuit is executed, default value is 8096.

Executes the quantum circuit `shots` number of times and returns a `counts` list where the i-th element represents the number of times the Quantum State collapsed to i-th bitstring state.