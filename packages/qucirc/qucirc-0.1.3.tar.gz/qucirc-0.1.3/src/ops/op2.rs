use num_rational::Ratio;

use super::{CircuitError, Operation};
use crate::circ::Gate;
use crate::typst::QuillTable;
use crate::wire::Wire;

macro_rules! impl_type_check2 {
    ($name:ident, $op:expr) => {
        fn type_check(&self, inputs: &[&dyn Wire]) -> Result<(), CircuitError> {
            if inputs.len() != 2 {
                return Err(CircuitError::wrong_number_of_arguments(self, inputs, $op));
            }

            for input in inputs {
                if !input.is_quantum() && input.bitwidth().unwrap() != 1 {
                    return Err(CircuitError::type_mismatch(self, inputs, $op));
                }
            }

            Ok(())
        }
    };
}

macro_rules! impl_add_quill_column2 {
    ($name:ident, $arg1:expr, $arg2:expr) => {
        fn add_quill_column(&self, gates: &[usize], table: &mut QuillTable) {
            table.add_column([
                (gates[0], $arg1(self, gates)),
                (gates[1], $arg2(self, gates)),
            ]);
        }
    };
}

macro_rules! impl_py {
    ($name:ident) => {
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
                Self
            }

            fn __call__(&self) -> Self {
                self.clone()
            }
            /// Create a new gate from the operation
            fn __getitem__(&self, qubits: (usize, usize)) -> Gate {
                Gate {
                    operation: Box::new(self.clone()),
                    inputs: vec![qubits.0, qubits.1],
                }
            }
            fn __repr__(&self) -> String {
                format!("{}", self)
            }

            fn __str__(&self) -> String {
                format!("{}", self)
            }
        }
    };
    ($name:ident; $($args:ident),*; $($args_no_pi:ident),*) => {
        impl $name {
            pub fn new_f64($($args: f64),*) -> Self {
                $(
                    let $args_no_pi = Ratio::approximate_float_unsigned($args / std::f64::consts::PI)
                        .expect("Angle is not a rational number");
                )*
                Self {
                    $( $args_no_pi ),*
                }
            }
        }

        #[cfg(feature = "python_api")]
        #[pyo3_stub_gen::derive::gen_stub_pymethods]
        #[pyo3::pymethods]
        impl $name {
            #[new]
            fn new_py($($args: f64),*) -> Self {
                $(
                    let $args_no_pi = Ratio::approximate_float_unsigned($args / std::f64::consts::PI)
                        .expect("Angle is not a rational number");
                )*
                Self {
                    $( $args_no_pi ),*
                }
            }

            fn __call__(&self, qubit1: usize, qubit2: usize) -> Gate {
                Gate {
                    operation: Box::new(self.clone()),
                    inputs: vec![qubit1, qubit2],
                }
            }
            fn __repr__(&self) -> String {
                format!("{}", self)
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
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
/// CNOT gate (controlled-NOT gate)
pub struct CNOT;
impl_py!(CNOT);
impl Operation for CNOT {
    impl_type_check2!(CNOT, "CNOT");
    impl_add_quill_column2!(
        CNOT,
        |_: &CNOT, gates: &[usize]| format!("ctrl({})", gates[1] - gates[0]),
        |_: &CNOT, _: &[usize]| "targ()".into()
    );
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
/// CY gate (controlled-Y gate)
pub struct CY;
impl_py!(CY);
impl Operation for CY {
    impl_type_check2!(CY, "CY");
    impl_add_quill_column2!(
        CY,
        |_: &CY, gates: &[usize]| format!("ctrl({})", gates[1] - gates[0]),
        |_: &CY, _: &[usize]| "gate($Y$)".into()
    );
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
/// CZ gate (controlled-Z gate)
pub struct CZ;
impl_py!(CZ);
impl Operation for CZ {
    impl_type_check2!(CZ, "CZ");
    impl_add_quill_column2!(
        CZ,
        |_: &CZ, gates: &[usize]| format!("ctrl({})", gates[1] - gates[0]),
        |_: &CZ, _: &[usize]| "ctrl()".into()
    );
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
/// CH gate (controlled-Hadamard gate)
pub struct CH;
impl_py!(CH);
impl Operation for CH {
    impl_type_check2!(CH, "CH");
    impl_add_quill_column2!(
        CH,
        |_: &CH, gates: &[usize]| format!("ctrl({})", gates[1] - gates[0]),
        |_: &CH, _: &[usize]| "gate($H$)".into()
    );
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
/// CP gate (controlled-phase gate)
pub struct CP {
    pub phase_no_pi: Ratio<u64>,
}
impl_py!(CP; phase; phase_no_pi);

impl Operation for CP {
    impl_type_check2!(CP, "CP");
    impl_add_quill_column2!(
        CP,
        |_: &CP, gates: &[usize]| format!("ctrl({})", gates[1] - gates[0]),
        |cp: &CP, _: &[usize]| format!("gate($P({} π)$)", cp.phase_no_pi)
    );
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
#[display("CRX({}π)", angle_no_pi)]
/// CRX gate (controlled-X gate)
pub struct CRX {
    pub angle_no_pi: Ratio<u64>,
}
impl_py!(CRX; angle; angle_no_pi);

impl Operation for CRX {
    impl_type_check2!(CRX, "CRX");
    impl_add_quill_column2!(
        CRX,
        |_: &CRX, gates: &[usize]| format!("ctrl({})", gates[1] - gates[0]),
        |crx: &CRX, _: &[usize]| format!("gate($R_X({} π)$)", crx.angle_no_pi)
    );
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
#[display("CRY({}π)", angle_no_pi)]
/// CRY gate (controlled-Y gate)
pub struct CRY {
    pub angle_no_pi: Ratio<u64>,
}
impl_py!(CRY; angle; angle_no_pi);

impl Operation for CRY {
    impl_type_check2!(CRY, "CRY");
    impl_add_quill_column2!(
        CRY,
        |_: &CRY, gates: &[usize]| format!("ctrl({})", gates[1] - gates[0]),
        |cry: &CRY, _: &[usize]| format!("gate($R_Y({} π)$)", cry.angle_no_pi)
    );
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
#[display("CRZ({}π)", angle_no_pi)]
/// CRZ gate (controlled-Z gate)
pub struct CRZ {
    pub angle_no_pi: Ratio<u64>,
}
impl_py!(CRZ; angle; angle_no_pi);

impl Operation for CRZ {
    impl_type_check2!(CRZ, "CRZ");
    impl_add_quill_column2!(
        CRZ,
        |_: &CRZ, gates: &[usize]| format!("ctrl({})", gates[1] - gates[0]),
        |crz: &CRZ, _: &[usize]| format!("gate($R_Z({} π)$)", crz.angle_no_pi)
    );
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
#[display("CU({}π, {}π, {}π)", theta_no_pi, phi_no_pi, lamda_no_pi)]
/// CU gate (controlled-U gate)
pub struct CU {
    pub theta_no_pi: Ratio<u64>,
    pub phi_no_pi: Ratio<u64>,
    pub lamda_no_pi: Ratio<u64>,
}
impl_py!(CU; theta, phi, lamda; theta_no_pi, phi_no_pi, lamda_no_pi);

impl Operation for CU {
    impl_type_check2!(CU, "CU");
    impl_add_quill_column2!(
        CU,
        |_: &CU, gates: &[usize]| format!("ctrl({})", gates[1] - gates[0]),
        |cu: &CU, _: &[usize]| format!(
            "gate($U({} π, {} π, {} π)$)",
            cu.theta_no_pi, cu.phi_no_pi, cu.lamda_no_pi
        )
    );
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
/// SWAP gate (swap gate)
pub struct SWAP;
impl Operation for SWAP {
    impl_type_check2!(SWAP, "SWAP");
    impl_add_quill_column2!(
        SWAP,
        |_: &SWAP, gates: &[usize]| format!("swap({})", gates[1] - gates[0]),
        |_: &SWAP, _: &[usize]| "swap()".into()
    );
}
impl_py!(SWAP);
