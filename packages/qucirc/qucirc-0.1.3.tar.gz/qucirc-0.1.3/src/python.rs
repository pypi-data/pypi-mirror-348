use pyo3::prelude::*;
use pyo3_stub_gen::define_stub_info_gatherer;

use crate::{
    circ::{Circuit, Gate},
    wire::{Bits, Qubit, ZeroState},
};

#[pymodule]
#[pyo3(name = "_")]
fn rust_entry(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.setattr("__doc__", include_str!("../README.md"))?;
    m.add_class::<Qubit>()?;
    m.add_class::<Bits>()?;
    m.add_class::<ZeroState>()?;
    m.add_class::<Circuit>()?;
    m.add_class::<Gate>()?;

    ops(m)?;

    Ok(())
}

const OPS_DOC: &str = "
Quantum gate operations:

- Single-qubit gates: H, X, Y, Z, S, T, SDG, TDG, SX
- Parameterized gates: RX(θ), RY(θ), RZ(θ), P(φ)
- Two-qubit gates: CNOT, CY, CZ, SWAP
- Controlled gates: CH, CP(φ), CRX(θ), CRY(θ), CRZ(θ), CU(θ,φ,λ)
";

#[pymodule]
#[pyo3(submodule)]
#[pyo3(module = "qucirc.ops")]
fn ops(m: &Bound<PyModule>) -> PyResult<()> {
    let ops = PyModule::new(m.py(), "ops")?;

    ops.setattr("__doc__", OPS_DOC)?;
    ops.add("H", crate::ops::H)?;
    ops.add("X", crate::ops::X)?;
    ops.add("Y", crate::ops::Y)?;
    ops.add("Z", crate::ops::Z)?;
    ops.add("S", crate::ops::S)?;
    ops.add("T", crate::ops::T)?;
    ops.add("SDG", crate::ops::SDG)?;
    ops.add("TDG", crate::ops::TDG)?;
    ops.add("SX", crate::ops::SX)?;
    ops.add("CNOT", crate::ops::CNOT)?;
    ops.add("CY", crate::ops::CY)?;
    ops.add("CZ", crate::ops::CZ)?;
    ops.add("CH", crate::ops::CH)?;
    ops.add("SWAP", crate::ops::SWAP)?;
    ops.add("Measure", crate::ops::Measure)?;
    ops.add("Nop", crate::ops::Nop)?;

    ops.add_class::<crate::ops::P>()?;
    ops.add_class::<crate::ops::RX>()?;
    ops.add_class::<crate::ops::RY>()?;
    ops.add_class::<crate::ops::RZ>()?;
    ops.add_class::<crate::ops::U>()?;
    ops.add_class::<crate::ops::U1>()?;
    ops.add_class::<crate::ops::U2>()?;
    ops.add_class::<crate::ops::U3>()?;
    ops.add_class::<crate::ops::CP>()?;
    ops.add_class::<crate::ops::CRX>()?;
    ops.add_class::<crate::ops::CRY>()?;
    ops.add_class::<crate::ops::CRZ>()?;
    ops.add_class::<crate::ops::CU>()?;

    pyo3::py_run!(m.py(), ops, "import sys; sys.modules['qucirc._.ops'] = ops");

    m.add_submodule(&ops)?;
    Ok(())
}

define_stub_info_gatherer!(stub_info);
