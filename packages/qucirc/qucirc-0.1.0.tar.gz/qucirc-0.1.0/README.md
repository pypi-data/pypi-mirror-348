# qucirc

A lightweight and extensible quantum circuit representation for Python and Rust.

| [crates.io](https://crates.io/crates/qucirc) | [docs.rs](https://docs.rs/qucirc) | [Github](https://github.com/YuantianDing/qucirc) | [PyPI](https://pypi.org/project/qucirc/) | [Documentation](https://yuantianding.github.io/qucirc/) |


## Features

- Support for common quantum gates (H, X, Y, Z, CNOT, etc.) defined in [OpenQASM 3.0 Standard Library](https://openqasm.com/language/standard_library.html#)
- Python API for easy integration
- Extendable circuit visualization using Typst
- DAG Representation of the circuit, easily exported to `petgraph`.
- Support for parameterized gates (RX, RY, RZ, U, etc.)
- Classical bit operations and measurements
- SVG visualization support

## Installation

### Python

```bash
pip install qucirc
```

### Rust
```bash
cargo add qucirc
```

## Usage

### Basic Circuit Creation

```python
from qucirc import Circuit, ops

# Create a new circuit with 2 qubits
circ = Circuit(2)

# Add some gates
circ += ops.H[0]  # Hadamard gate on qubit 0
circ += ops.CNOT[0, 1]  # CNOT gate with control=0, target=1

# Visualize the circuit
print(circ.to_typst())  # Typst representation
print(circ.to_svg())  # SVG visualization
```

### Working with Gates

The library supports various quantum gates:

- Single-qubit gates: H, X, Y, Z, S, T
- Parameterized gates: RX(θ), RY(θ), RZ(θ), P(φ)
- Two-qubit gates: CNOT, CY, CZ, SWAP
- Controlled gates: CH, CP(φ), CRX(θ), CRY(θ), CRZ(θ), CU(θ,φ,λ)

Example with parameterized gates:

```python
from qucirc import Circuit, ops
import math

circuit = Circuit(2)
circuit += ops.RX(math.pi/2)[0]  # Rotation around X axis
circuit += ops.CP(math.pi/4)[0, 1]  # Controlled phase gate

circ
```

### Classical Bits and Measurements

```python
from qucirc import Circuit, ops

circuit = Circuit(2)
# Add a classical bit
bit_index = circuit.new_bits(bitwidth=1, name="c0")
# Add measurement
circuit.add_gate(ops.Measure[0, bit_index])
```

### Circuit Visualization

The library provides multiple ways to visualize circuits:

1. Typst visualization based on Quill:

```python
# Using Jupyter Notebook
import math
import qucirc
from qucirc import ops

circ = qucirc.Circuit()

[q0, q1] = circ.new_qubits("q_0", "q_1")

circ += ops.H[q0]
circ += ops.H[q1]
circ += ops.CNOT[q0, q1]
circ += ops.P(math.pi / 3)[q0]

c0 = circ.new_bits()

circ += ops.Measure[q0, c0]

circ
```

![](https://github.com/YuantianDing/qucirc/blob/main/docs/output.svg)


2. Exporting to Typst (for documentation):

```python
print(circ.to_typst())
```


3. String representation:

```python
print(circ)
```

## DAG-based Symbolic representation

```python
import math
import qucirc
from qucirc import ops

circ1 = qucirc.Circuit()
circ1 += ops.H[0]
circ1 += ops.P(1/3 * math.pi)[1]

circ2 = qucirc.Circuit()
circ2 += ops.P(1/3 * math.pi)[1]
circ2 += ops.H[0]

assert circ1 == circ2
```



## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.






