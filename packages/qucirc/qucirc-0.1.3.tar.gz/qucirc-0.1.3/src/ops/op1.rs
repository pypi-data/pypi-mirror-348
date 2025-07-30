use derive_more::Display;

use super::{CircuitError, Operation};
use crate::circ::Gate;
use crate::typst::QuillTable;
use crate::wire::Wire;

macro_rules! impl_type_check1 {
    ($name:ident, $op:expr) => {
        fn type_check(&self, inputs: &[&dyn Wire]) -> Result<(), CircuitError> {
            if inputs.len() != 1 {
                return Err(CircuitError::wrong_number_of_arguments(self, inputs, $op));
            }

            if !inputs[0].is_quantum() && inputs[0].bitwidth().unwrap() != 1 {
                return Err(CircuitError::type_mismatch(self, inputs, $op));
            }

            Ok(())
        }
    };
}

macro_rules! impl_add_quill_column1 {
    ($name:ident, $op:expr) => {
        fn add_quill_column(&self, gates: &[usize], table: &mut QuillTable) {
            table.add_column([(gates[0], format!("gate(${}$)", $op))]);
        }
    };
}

macro_rules! impl_py {
    ($name:ident, $op:expr) => {
        impl $name {
            pub fn new() -> Self {
                Self
            }
        }
        #[cfg(feature = "python_api")]
        #[pyo3_stub_gen::derive::gen_stub_pymethods]
        #[pyo3::pymethods]
        impl $name {
            #[new]
            fn new_py() -> Self {
                $name
            }
            fn __call__(&self) -> Self {
                self.clone()
            }
            /// Create a new gate from the operation
            fn __getitem__(&self, qubit: usize) -> Gate {
                Gate {
                    operation: Box::new(self.clone()),
                    inputs: vec![qubit],
                }
            }
            fn __repr__(&self) -> String {
                format!("{:?}", self)
            }

            fn __str__(&self) -> String {
                format!("{}", self)
            }
        }
    };
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, Display, Clone, Eq, PartialEq, Hash)]
/// Pauli X gate
pub struct X;
impl Operation for X {
    impl_type_check1!(X, "X");
    impl_add_quill_column1!(X, "X");
}
impl_py!(X, "X");

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, Display, Clone, Eq, PartialEq, Hash)]
/// Pauli Y gate
pub struct Y;
impl Operation for Y {
    impl_type_check1!(Y, "Y");
    impl_add_quill_column1!(Y, "Y");
}
impl_py!(Y, "Y");

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, Display, Clone, Eq, PartialEq, Hash)]
/// Pauli Z gate
pub struct Z;
impl Operation for Z {
    impl_type_check1!(Z, "Z");
    impl_add_quill_column1!(Z, "Z");
}
impl_py!(Z, "Z");

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, Display, Clone, Eq, PartialEq, Hash)]
/// Hadamard gate
pub struct H;
impl Operation for H {
    impl_type_check1!(H, "H");
    impl_add_quill_column1!(H, "H");
}
impl_py!(H, "H");

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, Display, Clone, Eq, PartialEq, Hash)]
/// S gate
pub struct S;
impl Operation for S {
    impl_type_check1!(S, "S");
    impl_add_quill_column1!(S, "S");
}
impl_py!(S, "S");

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, Display, Clone, Eq, PartialEq, Hash)]
/// T gate
pub struct T;
impl Operation for T {
    impl_type_check1!(T, "T");
    impl_add_quill_column1!(T, "T");
}
impl_py!(T, "T");

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, Display, Clone, Eq, PartialEq, Hash)]
/// SDG gate (conjugate transpose of S gate)
pub struct SDG;
impl Operation for SDG {
    impl_type_check1!(SDG, "SDG");
    impl_add_quill_column1!(SDG, "S^dagger");
}
impl_py!(SDG, "S^dagger");

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, Display, Clone, Eq, PartialEq, Hash)]
/// TDG gate (conjugate transpose of T gate)
pub struct TDG;
impl Operation for TDG {
    impl_type_check1!(TDG, "TDG");
    impl_add_quill_column1!(TDG, "T^dagger");
}
impl_py!(TDG, "T^dagger");

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, Display, Clone, Eq, PartialEq, Hash)]
/// SX gate (square root of X gate)
pub struct SX;
impl Operation for SX {
    impl_type_check1!(SX, "SX");
    impl_add_quill_column1!(SX, "sqrt(X)");
}
impl_py!(SX, "sqrt(X)");
