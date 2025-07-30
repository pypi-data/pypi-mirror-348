//! A quantum circuit library for Python and Rust.
//!
//! This library provides an abstract representation of quantum circuits, supporting:
//! - Quantum gates and operations
//! - Circuit construction and manipulation
//! - Visualization and documentation
//! - Python bindings for easy integration
//!
//! # Features
//!
//! - Support for common quantum gates (H, X, Y, Z, CNOT, etc.)
//! - Parameterized gates (RX, RY, RZ, U, etc.)
//! - Circuit visualization using Typst
//! - Python API for easy integration
//!

#[macro_export]
macro_rules! pyo3_stub_gen_impl_any {
    ($name:ty) => {
        impl pyo3_stub_gen::PyStubType for $name {
            fn type_output() -> pyo3_stub_gen::TypeInfo {
                pyo3_stub_gen::TypeInfo {
                    name: "typing.Any".to_string(),
                    import: iter::once("typing".into()).collect(),
                }
            }
            fn type_input() -> pyo3_stub_gen::TypeInfo {
                pyo3_stub_gen::TypeInfo {
                    name: "typing.Any".to_string(),
                    import: iter::once("typing".into()).collect(),
                }
            }
        }
    };
}

#[macro_export]
macro_rules! pyo3_wrapper_impl {
    (#$tree:tt $p:vis struct $wrapper:ident($name:ty)) => {
        #[pyo3::pyclass]
        #$tree
        $p struct $wrapper($name);

        impl<'py> pyo3::IntoPyObject<'py> for $name {
            type Target = <$wrapper as pyo3::IntoPyObject<'py>>::Target;
            type Output = <$wrapper as pyo3::IntoPyObject<'py>>::Output;
            type Error = <$wrapper as pyo3::IntoPyObject<'py>>::Error;

            // Required method
            fn into_pyobject(self, py: pyo3::Python<'py>) -> Result<Self::Output, Self::Error> {
                $wrapper(self).into_pyobject(py)
            }
        }

        impl<'py> pyo3::FromPyObject<'py> for $name {
            fn extract_bound(ob: &pyo3::Bound<'_, pyo3::PyAny>) -> pyo3::PyResult<$name> {
                use pyo3::types::PyAnyMethods;
                Ok(ob.extract::<$wrapper>()?.0)
            }
        }
    };
}

/// Quantum circuit structures
pub mod circ;

/// Quantum circuit operations
pub mod ops;

/// Typst circuit visualization
pub mod typst;

/// Quantum circuit wires
pub mod wire;

#[cfg(feature = "python_api")]
/// Python bindings
pub mod python;
