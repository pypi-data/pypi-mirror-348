use std::collections::HashSet;

use crate::wire::{Bits, Wire, ZeroState};
use crate::{
    ops::{CircuitError, Operation},
    wire::Qubit,
};
use petgraph::{
    Direction,
    graph::{DiGraph, NodeIndex},
    visit::EdgeRef,
};

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._")
)]
#[derive(Clone, Debug, derive_more::Display, Eq, Hash)]
#[display("{}[{}]", operation, inputs.iter().map(|i| format!("{}", i)).collect::<Vec<_>>().join(","))]
/// Encapsulates a quantum gate that couples an operation with its input wire indices.
///
/// This structure holds a boxed operation implementing the required interface for quantum operations and a list of indices that identify the corresponding input wires, allowing for structured management and manipulation within a quantum circuit.
pub struct Gate {
    pub operation: Box<dyn Operation>,
    pub inputs: Vec<usize>,
}

impl PartialEq for Gate {
    /// Compares two instances by evaluating whether both the operation and the input indices are equal.
    ///
    ///
    /// Returns a boolean value indicating equality, with the implementation directly comparing the operation field and the inputs vector to determine if the two instances represent the same logical gate.
    fn eq(&self, other: &Self) -> bool {
        &self.operation == &other.operation && self.inputs == other.inputs
    }
}

#[cfg(feature = "python_api")]
#[pyo3_stub_gen::derive::gen_stub_pymethods]
#[pyo3::pymethods]
impl Gate {
    /// Returns a string representation of the instance using its debug formatting.
    ///
    ///
    /// Formats the current instance with the Debug trait, producing a string that can be used for display or debugging purposes.
    pub fn __repr__(&self) -> String {
        format!("{:?}", self)
    }

    pub fn __str__(&self) -> String {
        format!("{}", self)
    }
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._")
)]
#[derive(Clone, derive_more::Debug)]
/// A structure representing a quantum circuit with its associated components is defined.
///
/// This type organizes the circuit’s state by maintaining a vector of wires, a directed acyclic graph where nodes correspond to quantum gates and edges represent connections via wire indices, and a vector that tracks the current output node for each input wire.
pub struct Circuit {
    /// The inputs of the circuit. The index of the input is the index of the input wire.
    pub wires: Vec<Box<dyn Wire>>,
    /// The graph of the circuit. The nodes are the gates and the edges are the wires.
    graph: DiGraph<Gate, usize>,
    /// The outputs of the circuit. The index of the output is the index of the input wire.
    current_wires: Vec<Option<NodeIndex>>,
}

impl Circuit {
    /// Creates a new circuit instance with empty wires, graph, and current wires.
    ///
    /// This function initializes and returns a circuit by constructing empty collections for wires, the underlying graph structure, and the current wire tracking, providing a clean starting state for circuit building.
    pub fn new() -> Self {
        Self {
            wires: vec![],
            graph: DiGraph::new(),
            current_wires: vec![],
        }
    }

    /// Creates a new circuit instance pre-populated with a specified number of qubits.
    ///
    /// This function initializes the circuit by constructing a vector of wires, each representing a qubit with a unique identifier based on its index, and sets up an empty directed acyclic graph along with a vector tracking the current wire outputs for each qubit.
    pub fn new_with_qubits(qubits: usize) -> Self {
        Self {
            wires: (0..qubits)
                .map(|i| Qubit::new(format!("q_{}", i)))
                .collect(),
            graph: DiGraph::new(),
            current_wires: vec![None; qubits],
        }
    }

    /// Adds a new wire to the circuit and returns its index.
    ///
    /// This method takes ownership of a boxed wire trait object, appends it to the internal collection of wires, and updates the output tracking vector by inserting a corresponding placeholder.
    pub fn new_wire(&mut self, wire: Box<dyn Wire>) -> usize {
        let i = self.wires.len();
        self.wires.push(wire);
        self.current_wires.push(None);
        i
    }

    /// Adds a new gate operation to the circuit and returns the index of the added node. (Short-hand for `push`)
    ///
    /// This function accepts an operation and an array of input wire indices, converts the inputs to a vector, and appends a new gate to the circuit by delegating to the push method.
    pub fn perform<const N: usize>(
        &mut self,
        operation: impl Operation,
        inputs: [usize; N],
    ) -> NodeIndex {
        self.push(Gate {
            operation: Box::new(operation),
            inputs: inputs.to_vec(),
        })
        .unwrap()
    }

    /// Adds a gate to the quantum circuit by validating its inputs, performing a type check on the associated wires, and updating the circuit’s internal graph and current wire outputs.
    ///
    ///
    /// Checks that each input index is within bounds, then validates the operation against the referenced wires.
    /// On success, creates a new node in the circuit’s graph representing the gate, updates the output tracking for each input wire accordingly, and returns the node index.
    /// If any input index is invalid or the type check fails, an error is returned.
    pub fn push(&mut self, gate: Gate) -> Result<NodeIndex, CircuitError> {
        if gate.inputs.iter().any(|i| *i >= self.wires.len()) {
            return Err(CircuitError::IndexOutOfBounds(
                *gate.inputs.iter().max().unwrap(),
                self.wires.len(),
            ));
        }

        let Gate { operation, inputs } = gate;

        let input_wires: Vec<_> = inputs.iter().map(|i| &*self.wires[*i]).collect();
        operation.type_check(&input_wires)?;

        let node = self.graph.add_node(Gate {
            operation,
            inputs: inputs.clone(),
        });
        for inp in inputs {
            if let Some(output) = self.current_wires[inp] {
                self.graph.add_edge(node, output, inp);
            }
            self.current_wires[inp] = Some(node);
        }
        Ok(node)
    }

    /// Returns a reference to the underlying directed acyclic graph used internally for representing the circuit.
    ///
    /// This accessor function provides read-only access to the graph structure where nodes correspond to quantum gates and edges represent the connectivity between gates and wires.
    pub fn graph(&self) -> &DiGraph<Gate, usize> {
        &self.graph
    }

    pub fn into_graph(self) -> DiGraph<Gate, usize> {
        self.graph
    }

    /// Returns an iterator over references to all gate objects contained within the circuit's internal structure.
    ///
    /// This method accesses the underlying graph representation of the circuit and retrieves an iterator over its stored gate elements, allowing for read-only traversal and inspection of each gate's configuration within the circuit.
    pub fn gates(&self) -> impl Iterator<Item = &Gate> {
        self.graph.node_weights()
    }

    /// Returns a mutable iterator over the circuit’s gates.
    ///  
    /// Allows in-place modifications to each gate by iterating through the mutable references of gate nodes stored in the underlying graph.
    pub fn gates_mut(&mut self) -> impl Iterator<Item = &mut Gate> {
        self.graph.node_weights_mut()
    }

    /// Returns a hash set containing a cloned boxed copy of each operation present in the circuit's internal structure.
    ///
    /// This function collects the operation from every gate linked to the circuit, ensuring that the resulting set represents the unique operations applied throughout the circuit.
    pub fn operation_set(&self) -> HashSet<Box<dyn Operation>> {
        self.gates().map(|g| g.operation.clone()).collect()
    }

    #[cfg(feature = "typst")]
    pub fn to_typst(&self) -> String {
        format!("{}", crate::typst::QuillTable::from(self))
    }
}

#[cfg(feature = "python_api")]
#[pyo3_stub_gen::derive::gen_stub_pymethods]
#[pyo3::pymethods]
impl Circuit {
    #[new]
    #[pyo3(signature = (qubits=0,))]
    /// Creates a new circuit instance with a specified number of qubits.
    ///
    ///
    /// Initializes a circuit by delegating to the constructor that sets up the internal qubit wires, allowing the user to immediately work with a circuit configured with the desired number of qubits.
    pub fn construct(qubits: usize) -> Self {
        Self::new_with_qubits(qubits)
    }

    #[pyo3(name = "new_wire")]
    /// Adds a new wire to the circuit and returns its index.
    /// This method takes ownership of a boxed wire trait object, appends it to the internal collection of wires, and updates the output tracking vector by inserting a corresponding placeholder.
    pub fn new_wire_py(&mut self, wire: Box<dyn Wire>) -> usize {
        let i = self.wires.len();
        self.wires.push(wire);
        self.current_wires.push(None);
        i
    }

    #[getter]
    /// Returns a vector containing cloned boxed wire trait objects from the circuit's internal collection.
    ///
    /// This accessor function retrieves all wires by cloning the internal list, ensuring that the caller receives an independent copy of the wires for inspection or further manipulation.
    pub fn wires(&self) -> Vec<Box<dyn Wire>> {
        self.wires.clone()
    }

    /// Retrieves the index of a wire based on its string representation.
    ///
    ///
    /// Searches through the internal collection of wires and returns the position of the first wire whose debug format matches the provided name, returning None if no match is found.
    pub fn get_wire(&self, name: &str) -> Option<usize> {
        self.wires.iter().position(|w| format!("{:?}", w) == name)
    }

    #[pyo3(signature = (name="".into(),))]
    /// Creates and registers a new qubit wire within the circuit.
    ///
    /// This function accepts a mutable string for the qubit's name and, if the provided name is empty, automatically generates a unique identifier.
    /// It appends a new qubit to the circuit's collection of wires and returns the index corresponding to the newly added wire.
    ///
    pub fn new_qubit(&mut self, mut name: String) -> usize {
        if name.is_empty() {
            name = (0..)
                .map(|i| format!("q_{}", i))
                .filter(|name| self.get_wire(name).is_none())
                .next()
                .unwrap();
        }

        let i = self.wires.len();
        self.wires.push(Qubit::new(name));
        self.current_wires.push(None);
        i
    }

    #[pyo3(signature = (*args))]
    /// Creates several new qubit wires from a vector of names and returns their indices.
    /// This method iterates over each provided name, cloning it as necessary, and calls the routine responsible for initializing a new qubit wire for each entry; the resulting indices are then collected and returned as a vector.
    pub fn new_qubits(&mut self, args: Vec<String>) -> Vec<usize> {
        // match args {
        //     Either::Left((name,)) => name
        //         .split(',')
        //         .map(|name| self.new_qubit(name.into()))
        //         .collect(),
        //     Either::Right(names) => names
        //         .iter()
        //         .map(|name| self.new_qubit(name.clone()))
        //         .collect(),
        // }
        args.iter()
            .map(|name| self.new_qubit(name.clone()))
            .collect()
    }

    #[pyo3(signature = (count=1, name="".into()))]
    /// Creates a set of new qubits and returns their indices as a vector.
    ///
    /// This method accepts a count and a name, and for each qubit to be created, it delegates to the single qubit creation function.
    /// If the provided name is empty or equals "q", it automatically generates a unique identifier; otherwise, it uses the provided name for every qubit created.
    ///
    pub fn new_qubits_n(&mut self, count: usize, name: String) -> Vec<usize> {
        if name.is_empty() || &*name == "q" {
            (0..count).map(|_| self.new_qubit("".into())).collect()
        } else {
            (0..count).map(|_| self.new_qubit(name.clone())).collect()
        }
    }

    /// Constructs and appends a new zero state wire to the circuit, returning the index of the added wire.
    ///  
    ///
    /// Adds a zero state wire by inserting it into the circuit’s collection of wires and initializes its corresponding output placeholder, thereby expanding and managing the circuit’s internal state.
    pub fn new_zerostate(&mut self) -> usize {
        let i = self.wires.len();
        self.wires.push(ZeroState::new());
        self.current_wires.push(None);
        i
    }
    #[pyo3(signature = (bitwidth=1, name="".into()))]
    /// Creates and adds a new wire representing bits to the circuit.
    ///
    ///
    /// Adds a wire with a specified bitwidth and name to the circuit.
    /// If the provided name is empty, a default name is generated automatically to ensure uniqueness.
    /// The wire is appended to the list of circuit wires, and the corresponding output is initialized to None, returning the index of the newly added wire.
    pub fn new_bits(&mut self, bitwidth: usize, mut name: String) -> usize {
        if name.is_empty() {
            name = (0..)
                .map(|i| format!("c_{}", i))
                .filter(|name| self.get_wire(name).is_none())
                .next()
                .unwrap();
        }
        let i = self.wires.len();
        self.wires.push(Bits::new(name, bitwidth));
        self.current_wires.push(None);
        i
    }

    /// Returns a vector containing all the gates that compose the circuit.
    /// This method extracts the gate entries from the underlying circuit structure, clones each one, and collects them into a list for subsequent use.
    pub fn to_gates(&self) -> Vec<Gate> {
        self.gates().map(|g| g.clone()).collect()
    }
    /// Converts the circuit into a typst-formatted string representation.
    ///
    ///
    /// Transforms the circuit's internal state into a typst document string, enabling further rendering or integration into documentation.
    #[cfg(feature = "typst")]
    #[pyo3(name = "to_typst")]
    pub fn to_typst_py(&self) -> String {
        self.to_typst()
    }

    /// Returns a string representation of the circuit using debug formatting.
    /// This method enables the conversion of the circuit's state into a debug-friendly string, facilitating inspection and logging.
    fn __repr__(&self) -> String {
        format!("{:?}", self)
    }

    fn __str__(&self) -> String {
        format!("{}", self)
    }

    #[cfg(feature = "typst")]
    /// Returns an SVG representation of the circuit as a string.
    /// This method converts the circuit into its SVG depiction and returns the resulting string, providing a visual output intended for environments that support SVG format.
    fn _repr_svg_(&self) -> String {
        self.to_svg().unwrap()
    }

    /// Adds a gate to the circuit in place by appending the given gate and updating the circuit's graph structure.
    /// Returns a successful result upon appending the gate or an error if the operation fails during insertion.
    fn __iadd__(&mut self, other: Gate) -> Result<(), CircuitError> {
        self.push(other).map(|_| ())
    }

    /// Compares two instances for equality.
    /// This method determines if the current instance is equal to another by delegating to the underlying equality implementation.
    fn __eq__(&self, other: &Self) -> bool {
        self == other
    }
}

#[cfg(feature = "typst")]
impl Circuit {
    /// Converts the quantum circuit into an SVG formatted string using a typesetting conversion utility.
    /// It returns a Result that encapsulates either the SVG representation as a String or an error indicating a failure during conversion.
    pub fn to_svg(&self) -> Result<String, typst_as_lib::TypstAsLibError> {
        crate::typst::QuillTable::from(self).to_svg()
    }
}

impl PartialEq for Circuit {
    /// Compares two circuit instances for structural equivalence.
    ///
    ///
    /// Checks if the internal wires are equal, confirms the current outputs have matching lengths, and recursively compares the corresponding segments of the underlying graphs to determine if the circuits are equivalent in structure and gate assignments.
    fn eq(&self, other: &Self) -> bool {
        self.wires == other.wires
            && self.current_wires.len() == other.current_wires.len()
            && self
                .current_wires
                .iter()
                .zip(other.current_wires.iter())
                .all(|(a, b)| match (a, b) {
                    (Some(a), Some(b)) => dag_eq(&self.graph, *a, &other.graph, *b),
                    (None, None) => true,
                    _ => false,
                })
    }
}

impl std::fmt::Display for Circuit {
    /// Formats the circuit into a string representation by converting it to a list of gates and rendering that list using debug formatting.
    ///
    ///
    /// Invoked during formatting operations, this function writes the debug representation of the circuit's gate list into the provided formatter, returning the result of the write operation.
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{}",
            self.gates()
                .map(|g| format!("{}", g))
                .collect::<Vec<_>>()
                .join("\n")
        )
    }
}

/// Compares two nodes from separate directed acyclic graphs to determine structural and operational equivalence.
/// This function recursively verifies that the nodes, as well as their outgoing edges, have matching gate operations and identical edge weights, ensuring the entire subgraphs are equivalent.
fn dag_eq(
    graph: &DiGraph<Gate, usize>,
    node1: NodeIndex,
    other: &DiGraph<Gate, usize>,
    node2: NodeIndex,
) -> bool {
    if graph.node_weight(node1).unwrap() != other.node_weight(node2).unwrap() {
        return false;
    }

    let mut edges1: Vec<_> = graph.edges_directed(node1, Direction::Outgoing).collect();
    let mut edges2: Vec<_> = other.edges_directed(node2, Direction::Outgoing).collect();

    if edges1.len() != edges2.len() {
        return false;
    }
    if !edges1.is_sorted_by(|a, b| a.weight() < b.weight()) {
        println!("edges1 is not sorted");
    }
    if !edges2.is_sorted_by(|a, b| a.weight() < b.weight()) {
        println!("edges2 is not sorted");
    }

    edges1.sort_by(|a, b| a.weight().cmp(b.weight()));
    edges2.sort_by(|a, b| a.weight().cmp(b.weight()));
    for (edge1, edge2) in edges1.iter().zip(edges2.iter()) {
        if edge1.weight() != edge2.weight() {
            return false;
        }

        if !dag_eq(graph, edge1.target(), other, edge2.target()) {
            return false;
        }
    }
    true
}

impl Eq for Circuit {}
