use crate::{circ::Gate, typst::QuillTable, wire::Wire};

use super::{CircuitError, Operation};

/// Measure a single qubit
#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
pub struct Measure;

impl Operation for Measure {
    /// Checks the types of wires provided for a measurement operation.
    ///
    ///
    /// This method validates that exactly one or two wires are supplied.
    /// It then ensures that the first wire is quantum and, when a second wire is present, that it is also quantum, returning appropriate errors for incorrect argument counts or type mismatches.
    fn type_check(&self, inputs: &[&dyn Wire]) -> Result<(), CircuitError> {
        if inputs.len() != 1 && inputs.len() != 2 {
            return Err(CircuitError::wrong_number_of_arguments(
                self,
                inputs,
                "expecting 1 or 2",
            ));
        }
        if !inputs[0].is_quantum() || inputs.len() == 2 && inputs[1].is_quantum() {
            return Err(CircuitError::type_mismatch(
                self,
                inputs,
                if inputs.len() == 2 {
                    "Measure qubit, bit"
                } else {
                    "Measure qubit"
                },
            ));
        }
        Ok(())
    }

    /// Adds operation details into a visualization table by inserting appropriately formatted column entries based on the supplied gate indices.
    ///
    ///
    /// Determines whether a single gate index or a pair is provided and, accordingly, adds either one column with a "measure()" label or two columns where the first column is labeled with a "meter" operation that computes the relative difference between the two indices and the second with a "ctrl()" label.
    fn add_quill_column(&self, gates: &[usize], table: &mut QuillTable) {
        if gates.len() == 1 {
            table.add_column([(gates[0], format!("measure()"))]);
        } else {
            table.add_column([
                (gates[0], format!("meter(target: {})", gates[1] - gates[0])),
                (gates[1], "ctrl()".to_string()),
            ]);
        }
    }
}

#[cfg(feature = "python_api")]
#[pyo3::pymethods]
impl Measure {
    /// Provides a method that returns a gate configured with the operation and inputs based on the provided qubit specification.
    /// This method accepts a parameter of a discriminated union type that can either be a single index or a tuple of two indices, representing a qubit (and optionally a classical bit), and returns a gate object where the operation is dynamically cloned from the current instance and the inputs vector is populated accordingly.
    fn __getitem__(&self, qubit: either::Either<usize, (usize, usize)>) -> Gate {
        match qubit {
            either::Either::Left(qubit) => Gate {
                operation: dyn_clone::clone_box(self),
                inputs: vec![qubit],
            },
            either::Either::Right((qubit, bit)) => Gate {
                operation: dyn_clone::clone_box(self),
                inputs: vec![qubit, bit],
            },
        }
    }

    /// Returns a duplicate of the instance by cloning it.
    ///  
    ///
    /// Clones the current object without requiring any inputs, producing a new instance identical to the original.
    /// This functionality is particularly useful in contexts where a fresh copy is needed for further independent manipulation.
    fn __call__(&self) -> Self {
        self.clone()
    }

    /// Returns a formatted string representing the operation in a debugging-friendly manner.
    /// It leverages the debug formatting trait to construct a string that succinctly encapsulates the state of the instance, aiding in identification and troubleshooting of the operation when inspected.
    fn __repr__(&self) -> String {
        format!("{:?}", self)
    }

    fn __str__(&self) -> String {
        format!("{}", self)
    }
}

/// Do nothing
#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
pub struct Nop;

impl Operation for Nop {
    /// Checks that the operation receives no wire inputs.
    /// This function validates that the inputs slice is empty and returns an error if any wires are provided, ensuring that no arguments are passed to the no-operation functionality.
    fn type_check(&self, inputs: &[&dyn Wire]) -> Result<(), CircuitError> {
        if inputs.len() != 0 {
            return Err(CircuitError::wrong_number_of_arguments(
                self,
                inputs,
                "expecting 0",
            ));
        }
        Ok(())
    }

    /// Implements a method that does not modify the visualization for this operation.
    ///
    ///
    /// This function accepts an array of gate indices and a mutable reference to a visualization table but intentionally performs no actions, effectively representing a no-operation in the diagram generation process.
    fn add_quill_column(&self, _gates: &[usize], _table: &mut QuillTable) {}
}

#[cfg(feature = "python_api")]
#[pyo3::pymethods]
impl Nop {
    /// Returns a no-operation gate regardless of the qubit parameter provided.
    ///
    ///
    /// This method accepts a qubit identifier, which may be provided either as a single index or as a tuple, and creates a gate structure representing a no-operation by cloning the underlying instance while purposely returning an empty list of inputs.
    fn __getitem__(&self, _qubit: either::Either<usize, (usize, usize)>) -> Gate {
        Gate {
            operation: dyn_clone::clone_box(self),
            inputs: vec![],
        }
    }
    /// Returns a duplicate of the current instance by cloning itself.
    ///
    /// This method supports callable behavior by simply returning a copy of the no-operation entity, enabling compatibility with function call semantics in Python bindings.
    fn __call__(&self) -> Self {
        self.clone()
    }
    /// Returns a string representing the instance via its debug format.
    ///
    /// This method retrieves a textual representation of the object for debugging purposes by formatting it using the Debug trait.
    fn __repr__(&self) -> String {
        format!("{:?}", self)
    }

    fn __str__(&self) -> String {
        format!("{}", self)
    }
}

// /// Reset a single qubit
// #[cfg_attr(
//     feature = "python_api",
//     pyo3_stub_gen::derive::gen_stub_pyclass,
//     pyo3::pyclass(module = "qucirc._.ops")
// )]
// #[derive(Debug, Clone, Eq, PartialEq, Hash)]
// pub struct Reset;

// impl Operation for Reset {
//     fn type_check(&self, inputs: &[&dyn Wire]) -> Result<(), CircuitError> {
//         if inputs.len() != 1 {
//             return Err(CircuitError::wrong_number_of_arguments(
//                 self,
//                 inputs,
//                 "expecting 1",
//             ));
//         }
//         if !inputs[0].is_quantum() {
//             return Err(CircuitError::type_mismatch(self, inputs, "Reset qubit"));
//         }
//         Ok(())
//     }

//     fn add_quill_column(&self, gates: &[usize], table: &mut QuillTable) {
//         table.add_column([(gates[0], format!("reset()"))]);
//     }
// }

// #[cfg(feature = "python_api")]
// #[pyo3::pymethods]
// impl Reset {
//     fn __getitem__(&self, qubit: usize) -> Gate {
//         Gate {
//             operation: dyn_clone::clone_box(self),
//             inputs: vec![qubit],
//         }
//     }

//     fn __repr__(&self) -> String {
//         format!("{}", self)
//     }
// }
