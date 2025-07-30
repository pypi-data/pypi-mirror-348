use num_rational::Ratio;

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
            table.add_column([(gates[0], $op(self))]);
        }
    };
}

macro_rules! impl_py {
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

/// Phase gate (diag{1, exp(iθ)})
#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
#[display("P({}π)", phase_no_pi)]
pub struct P {
    pub phase_no_pi: Ratio<u64>,
}
impl_py!(P; phase; phase_no_pi);

impl Operation for P {
    impl_type_check1!(P, "P");
    impl_add_quill_column1!(P, |p: &P| format!("gate($P({} π)$)", p.phase_no_pi));
}

/// RX gate (rotation around X axis)
#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
#[display("RX({}π)", angle_no_pi)]
pub struct RX {
    pub angle_no_pi: Ratio<u64>,
}
impl_py!(RX; angle; angle_no_pi);
impl Operation for RX {
    impl_type_check1!(RX, "RX");
    impl_add_quill_column1!(RX, |rx: &RX| format!("gate($R_X({} π)$)", rx.angle_no_pi));
}

/// RY gate (rotation around Y axis)
#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
#[display("RY({}π)", angle_no_pi)]
pub struct RY {
    pub angle_no_pi: Ratio<u64>,
}
impl_py!(RY; angle; angle_no_pi);
impl Operation for RY {
    impl_type_check1!(RY, "RY");
    impl_add_quill_column1!(RY, |ry: &RY| format!("gate($R_Y({} π)$)", ry.angle_no_pi));
}

/// RZ gate (rotation around Z axis)
#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
#[display("RZ({}π)", angle_no_pi)]
pub struct RZ {
    pub angle_no_pi: Ratio<u64>,
}
impl_py!(RZ; angle; angle_no_pi);
impl Operation for RZ {
    impl_type_check1!(RZ, "RZ");
    impl_add_quill_column1!(RZ, |rz: &RZ| format!("gate($R_Z({} π)$)", rz.angle_no_pi));
}
/// U gate (general single-qubit gate)
#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
#[display("U({}π, {}π, {}π)", theta_no_pi, phi_no_pi, lamda_no_pi)]
pub struct U {
    pub theta_no_pi: Ratio<u64>,
    pub phi_no_pi: Ratio<u64>,
    pub lamda_no_pi: Ratio<u64>,
}
impl_py!(U; theta, phi, lamda; theta_no_pi, phi_no_pi, lamda_no_pi);
impl Operation for U {
    impl_type_check1!(U, "U");
    impl_add_quill_column1!(U, |u: &U| format!(
        "gate($U({} π, {} π, {} π)$)",
        u.theta_no_pi, u.phi_no_pi, u.lamda_no_pi
    ));
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
#[display("U1({}π)", lamda_no_pi)]
/// U1 gate (phase gate)
pub struct U1 {
    pub lamda_no_pi: Ratio<u64>,
}
impl_py!(U1; lamda; lamda_no_pi);
impl Operation for U1 {
    impl_type_check1!(U1, "U1");
    impl_add_quill_column1!(U1, |u1: &U1| format!("gate($U_1({} π)$)", u1.lamda_no_pi));
}

/// U2 gate (two-parameter single-qubit gate)
#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
#[display("U2({}π, {}π)", phi_no_pi, lamda_no_pi)]
pub struct U2 {
    pub phi_no_pi: Ratio<u64>,
    pub lamda_no_pi: Ratio<u64>,
}
impl_py!(U2; phi, lamda; phi_no_pi, lamda_no_pi);
impl Operation for U2 {
    impl_type_check1!(U2, "U2");
    impl_add_quill_column1!(U2, |u2: &U2| format!(
        "gate($U_2({} π, {} π)$)",
        u2.phi_no_pi, u2.lamda_no_pi
    ));
}

/// U3 gate (three-parameter single-qubit gate)
#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._.ops")
)]
#[derive(Debug, derive_more::Display, Clone, Eq, PartialEq, Hash)]
#[display("U3({}π, {}π, {}π)", theta_no_pi, phi_no_pi, lamda_no_pi)]
pub struct U3 {
    pub theta_no_pi: Ratio<u64>,
    pub phi_no_pi: Ratio<u64>,
    pub lamda_no_pi: Ratio<u64>,
}
impl_py!(U3; theta, phi, lamda; theta_no_pi, phi_no_pi, lamda_no_pi);
impl Operation for U3 {
    impl_type_check1!(U3, "U3");
    impl_add_quill_column1!(U3, |u3: &U3| format!(
        "gate($U_3({} π, {} π, {} π)$)",
        u3.theta_no_pi, u3.phi_no_pi, u3.lamda_no_pi
    ));
}
