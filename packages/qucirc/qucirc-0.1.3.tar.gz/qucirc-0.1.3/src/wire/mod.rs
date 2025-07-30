use std::iter;

use downcast_rs::Downcast;
use dyn_clone::DynClone;
use dyn_eq::DynEq;
use dyn_hash::DynHash;

/// Defines a trait that abstracts common behaviors for wires in a quantum circuit.
///  
///
/// Extends functionalities for cloning, equality, hashing, downcasting, and ensuring thread safety.
/// Provides methods to determine if a wire is quantum, query its bitwidth, and generate a vector of formatted strings that can be used for visualizing or initializing the wire's state.
pub trait Wire:
    std::fmt::Debug + std::fmt::Display + DynClone + DynEq + DynHash + Downcast + Send + Sync
{
    fn is_quantum(&self) -> bool;
    fn bitwidth(&self) -> Option<usize>;

    fn quill_wire_start(&self) -> Vec<String> {
        let mut result = Vec::new();
        if self.is_quantum() {
            result.push(format!("lstick(${:?}$)", self));
        } else {
            result.push(format!("lstick(${:?}$), setwire(2)", self));
        }

        if self.bitwidth().map_or(false, |bitwidth| bitwidth > 1) {
            result.push(format!("nwire({})", self.bitwidth().unwrap()));
        }

        result
    }
}

dyn_clone::clone_trait_object!(Wire);
dyn_eq::eq_trait_object!(Wire);
dyn_hash::hash_trait_object!(Wire);
downcast_rs::impl_downcast!(Wire);

#[cfg(feature = "python_api")]
crate::pyo3_stub_gen_impl_any!(Box<dyn Wire>);

#[cfg(feature = "python_api")]
crate::pyo3_wrapper_impl!(
    #[derive(Clone, derive_more::Deref, derive_more::DerefMut)]
    pub struct PyWirePtr(Box<dyn Wire>)
);

#[cfg(feature = "python_api")]
#[pyo3::pymethods]
impl PyWirePtr {
    /// Returns a boolean indicating whether the encapsulated wire represents a quantum element.
    /// This method delegates the check to the underlying wire, enabling a consistent query for quantum status across the interface.
    fn is_quantum(&self) -> bool {
        self.0.is_quantum()
    }
    /// Returns the bitwidth of the underlying wire object.
    /// This method extracts the stored wire’s bitwidth by invoking the corresponding function on the internal wire reference and returns it as an optional usize value.
    fn bitwidth(&self) -> Option<usize> {
        self.0.bitwidth()
    }
    /// Generates a string representation for debugging by returning a formatted string of the underlying wire.
    /// This function implements the Python __repr__ method and outputs a detailed textual description constructed with debug formatting, ensuring that the object's internal state can be easily inspected when used from Python.
    fn __repr__(&self) -> String {
        format!("{:?}", self.0)
    }
    /// Converts the contained wire object into a string using its Display implementation.
    ///
    ///
    /// Generates a string representation that can be used within Python to expose a human-readable description of the underlying wire object.
    /// This method leverages standard formatting to ensure consistent output.
    fn __str__(&self) -> String {
        format!("{}", self.0)
    }
    /// Checks for equality between two Python wire pointer objects by comparing their underlying wire representations.
    ///
    ///
    /// Determines if the inner values of the two wrappers are equivalent by invoking the equality logic defined for the encapsulated wire trait, thereby enabling Python-side comparisons of wire objects using the __eq__ method.
    fn __eq__(&self, other: &PyWirePtr) -> bool {
        self.0 == other.0
    }
    /// Implements the Python special method to determine inequality between two wire pointer wrappers.
    /// This method compares the inner wire objects of the two wrappers, returning true if they differ and false otherwise, thereby facilitating Python-side inequality checks consistent with the underlying Rust semantics.
    fn __ne__(&self, other: &PyWirePtr) -> bool {
        self.0 != other.0
    }
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._")
)]
#[derive(derive_more::Display, Debug, Clone, Eq, PartialEq, Hash)]
#[display("{_0}")]
/// A simple wrapper type encapsulating a quantum bit identifier using a string.
///
/// This type primarily serves to distinguish quantum bits from other wire representations by wrapping a string value that acts as its identifier.
/// Its design promotes clear type usage in the context of quantum circuits while supporting the trait object interface defined for wires.
pub struct Qubit(pub String);

impl Qubit {
    /// Creates a new instance representing a quantum bit wire.
    /// This function accepts a string parameter to label the quantum element and returns it as a boxed dynamic trait object, enabling it to be used polymorphically wherever the wire abstraction is required.
    pub fn new(name: String) -> Box<dyn Wire> {
        Box::new(Self(name))
    }
}

impl Wire for Qubit {
    /// Checks if the wire represents a quantum state by always returning true.
    ///
    ///
    /// Returns a boolean indicating the quantum nature of the wire, confirming that the wire is indeed a quantum bit.
    fn is_quantum(&self) -> bool {
        true
    }
    /// Returns the constant bitwidth value of one for this quantum wire.
    ///
    /// Ensures that when queried, the bitwidth is provided as an Option containing the value one, indicating that the wire represents a single quantum bit regardless of any external parameters.
    fn bitwidth(&self) -> Option<usize> {
        Some(1)
    }
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._")
)]
#[derive(derive_more::Display, Debug, Clone, Eq, PartialEq, Hash)]
#[display("|0>")]
/// A unit structure representing a quantum wire initialized to a zero state.
///
///
/// This item embodies a specialized wire used within quantum circuit implementations, ensuring compatibility with interface expectations for quantum wires while serving as a straightforward, marker-like type.
/// It is intended for use in contexts where the initialization of a quantum bit to a zero state is required.
pub struct ZeroState;

impl ZeroState {
    /// Returns a boxed trait object encapsulating a quantum wire in the zero state.
    /// This constructor function instantiates the zero state wire, enabling its use within contexts where trait objects conforming to the wire interface are required.
    pub fn new() -> Box<dyn Wire> {
        Box::new(Self)
    }
}

impl Wire for ZeroState {
    /// Returns a boolean indicating the wire represents a quantum state.
    /// This function consistently returns true, confirming that the associated wire is indeed quantum in nature.
    fn is_quantum(&self) -> bool {
        true
    }
    /// Returns an optional bit width, always indicating a width of one.
    ///
    /// Determines that the wire is associated with a single bit by unconditionally returning an option containing the value one.
    fn bitwidth(&self) -> Option<usize> {
        Some(1)
    }
}

#[cfg_attr(
    feature = "python_api",
    pyo3_stub_gen::derive::gen_stub_pyclass,
    pyo3::pyclass(module = "qucirc._")
)]
#[derive(derive_more::Display, Debug, Clone, Eq, PartialEq, Hash)]
#[display("{_0}")]
/// A structure encapsulating a classical wire characterized by an identifier and a bitwidth.
///
/// This type represents a classical wire by wrapping a string label with its corresponding number of bits, facilitating its use in contexts where explicit bit specifications and identifier management are required.
pub struct Bits(pub String, pub usize);

impl Bits {
    /// Creates and returns a new classical wire instance with the specified identifier and bitwidth.
    /// This function constructs a new wire with the provided name and number of bits, then boxes it for dynamic dispatch over the underlying wire interface.
    pub fn new(name: String, bitwidth: usize) -> Box<dyn Wire> {
        Box::new(Self(name, bitwidth))
    }
}

impl Wire for Bits {
    /// Determines whether the wire represents a quantum bit.
    ///
    ///
    /// This method always indicates a non-quantum nature by returning false, ensuring that classical wires are correctly identified within the system.
    fn is_quantum(&self) -> bool {
        false
    }
    /// Computes and returns an optional bitwidth reflecting the number of bits for the entity.
    ///
    ///
    /// This function retrieves the internally stored bitwidth, encapsulated as a usize value, and wraps it in an Option.
    fn bitwidth(&self) -> Option<usize> {
        Some(self.1)
    }
}

#[cfg(feature = "python_api")]
#[pyo3::pymethods]
impl Qubit {
    /// Creates a new instance representing a quantum bit wire.
    /// This function accepts a string parameter to label the quantum element and returns it as a boxed dynamic trait object, enabling it to be used polymorphically wherever the wire abstraction is required.
    #[staticmethod]
    #[pyo3(name = "new")]
    pub fn new_py(name: String) -> Box<dyn Wire> {
        Box::new(Self(name))
    }
}

#[cfg(feature = "python_api")]
#[pyo3::pymethods]
impl ZeroState {
    /// Returns a boxed trait object encapsulating a quantum wire in the zero state.
    /// This constructor function instantiates the zero state wire, enabling its use within contexts where trait objects conforming to the wire interface are required.
    #[staticmethod]
    #[pyo3(name = "new")]
    pub fn new_py() -> Box<dyn Wire> {
        Box::new(Self)
    }
}

#[cfg(feature = "python_api")]
#[pyo3::pymethods]
impl Bits {
    /// Creates and returns a new classical wire instance with the specified identifier and bitwidth.
    /// This function constructs a new wire with the provided name and number of bits, then boxes it for dynamic dispatch over the underlying wire interface.
    #[staticmethod]
    #[pyo3(name = "new")]
    pub fn new_py(name: String, bitwidth: usize) -> Box<dyn Wire> {
        Box::new(Self(name, bitwidth))
    }
}
