# The quantum circuit file format

The first line specifies the total number of qubits in the circuit.

|keyword|Syntax|Meaning|
|-|-|-|
|**cnot**|`cnot qubit1 qubit2`|Add a cnot gate|
|**x**|`x qubit`|Add an x gate|
|**y**|`y qubit`|Add a y gate|
|**h**|`h qubit`|Add a Hadamard gate|

## Example file
```
1  2
2  h 0
3  x 1
4  cnot 0 1
5  cnot 1 0
```

Line 1 creates a circuit with two qubits.
Line 2 adds a hadamard gate to qubit 0 and line 3 adds an x gate to qubit 0... and so on.

![](new_thing.png)
