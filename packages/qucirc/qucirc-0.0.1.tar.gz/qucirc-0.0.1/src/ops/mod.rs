use crate::typst::QuillTable;
use downcast_rs::Downcast;
use dyn_clone::DynClone;
use dyn_eq::DynEq;
use dyn_hash::DynHash;
use thiserror::Error;

use super::wire::Wire;

mod misc;
mod op1;
mod op1_with_parameter;
mod op2;

pub use misc::*;
pub use op1::*;
pub use op1_with_parameter::*;
pub use op2::*;

#[derive(Debug, Clone, Eq, PartialEq, derive_more::Display, Error)]
/// This enumeration defines distinct error cases that may occur when working with quantum circuit operations.
/// It captures failures due to type mismatches, incorrect argument counts, or index bounds violations.
///
/// Each variant provides contextual information to aid debugging.
/// One variant indicates that an operation was given inputs of an unexpected type, another signals that the number of provided inputs does not match the expected number, and the third marks an illegal wire index access.
pub enum CircuitError {
    #[display("Type mismatch {_0:?} {_1:?}: {_2}")]
    TypeMismatch(Box<dyn Operation>, Vec<Box<dyn Wire>>, String),
    #[display("Wrong number of arguments for {_0:?}: {_1}")]
    WrongNumberOfArguments(Box<dyn Operation>, usize, String),
    #[display("Index out of bounds: accessing {_0} with {_1} wires")]
    IndexOutOfBounds(usize, usize),
}

#[cfg(feature = "python_api")]
impl From<CircuitError> for pyo3::PyErr {
    /// Converts an error from the quantum circuit domain into a Python exception.
    /// This interface method accepts an error instance and returns a corresponding Python ValueError exception, with its message generated from the original error’s string representation.
    fn from(value: CircuitError) -> Self {
        pyo3::exceptions::PyValueError::new_err(value.to_string())
    }
}

impl CircuitError {
    /// Constructs and returns an error instance representing an incorrect number of arguments provided to an operation.
    ///
    ///
    /// This method accepts an operation reference, a slice of wire references, and a string describing the expected arguments.
    /// It clones the provided operation, captures the count of the supplied wires, and packages these values into an error variant that clearly signifies the argument mismatch.
    pub fn wrong_number_of_arguments(
        operation: &dyn Operation,
        inputs: &[&dyn Wire],
        expected: &str,
    ) -> Self {
        CircuitError::WrongNumberOfArguments(
            dyn_clone::clone_box(operation),
            inputs.len(),
            expected.into(),
        )
    }

    /// Constructs a type mismatch error variant by cloning the provided operation and its input wires while incorporating an expected type description.
    ///
    /// This method takes an operation reference, a slice of wire references, and a string describing the expected input types, then returns an error instance representing a type mismatch.
    /// It ensures that the operation and each input wire are cloned to maintain ownership and integrity of the error information while converting the expected description into an owned string value.
    pub fn type_mismatch(operation: &dyn Operation, inputs: &[&dyn Wire], expected: &str) -> Self {
        CircuitError::TypeMismatch(
            dyn_clone::clone_box(operation),
            inputs.iter().map(|w| dyn_clone::clone_box(*w)).collect(),
            expected.into(),
        )
    }
}

/// A trait representing a quantum circuit operation with support for dynamic cloning, equality checking, hashing, and runtime downcasting.
///
///
/// Provides a method to validate a set of input wires against operation-specific type requirements, returning a standardized error if validation fails.
/// In addition, it offers a helper function to append a formatted representation of the operation into a visualization table based on the provided gate indices, streamlining the integration of operation details into circuit documentation.
pub trait Operation:
    std::fmt::Debug + std::fmt::Display + DynClone + DynEq + DynHash + Downcast + Send + Sync
{
    /// Validates the input wires against the operation-specific type requirements.
    fn type_check(&self, inputs: &[&dyn Wire]) -> Result<(), CircuitError>;

    /// Adds a column to a visualization table by formatting the operation details based on the provided gate indices.
    ///
    /// This method takes a slice of gate indices and a mutable reference to a table, then inserts a new column into the table.
    /// It retrieves the minimum and maximum indices from the slice, formats the operation information, and updates the table with the new column.
    fn add_quill_column(&self, gates: &[usize], table: &mut QuillTable) {
        let min = *gates.iter().min().unwrap();
        let max = *gates.iter().max().unwrap();
        if max == min {
            table.add_column([(min, format!("gate([{}])", self))]);
        } else {
            table.add_column([
                (min, format!("mqgate([{}], n: {})", self, max - min + 1)),
                (max, "1".to_owned()),
            ]);
        }
    }
}

dyn_clone::clone_trait_object!(Operation);
dyn_eq::eq_trait_object!(Operation);
dyn_hash::hash_trait_object!(Operation);
downcast_rs::impl_downcast!(Operation);
