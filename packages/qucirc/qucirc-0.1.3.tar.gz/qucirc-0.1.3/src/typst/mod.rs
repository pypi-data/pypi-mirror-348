use crate::circ::{Circuit, Gate};

mod quill_table;

pub use quill_table::QuillTable;

/// Generates a textual representation of a quantum circuit by building up a quill table from its wires and gates.
///
/// This function initializes a table based on the number of wires in the circuit, populates each row with the initial state of the corresponding wire, and then iteratively updates the table with each gate operation.
/// Finally, it returns the complete table as a formatted string.
///
impl From<&Circuit> for QuillTable {
    fn from(circuit: &Circuit) -> Self {
        let mut quill_table = QuillTable::new(circuit.wires.len());

        for (i, input) in circuit.wires.iter().enumerate() {
            quill_table[i].extend(input.quill_wire_start())
        }

        for gate in circuit.gates() {
            let Gate { operation, inputs } = gate;
            operation.add_quill_column(&inputs, &mut quill_table);
        }

        quill_table
    }
}

#[cfg(feature = "typst")]
impl QuillTable {
    /// Converts a quantum circuit into a Scalable Vector Graphics (SVG) image.
    ///
    ///
    /// Transforms the provided circuit by first converting it into a formatted textual representation, then leverages a document rendering engine to compile this representation into an SVG format.
    /// Returns the resulting SVG string or an error if the transformation fails.
    pub fn to_svg(&self) -> Result<String, typst_as_lib::TypstAsLibError> {
        use typst_as_lib::TypstEngine;
        use typst_library::layout::Abs;

        let engine = TypstEngine::builder()
            .main_file(format!("{}", self))
            .with_package_file_resolver()
            .fonts(FONTS.iter().map(|a| a.as_ref()).collect::<Vec<_>>())
            .build();

        Ok(typst_svg::svg_merged(
            &engine.compile().output?,
            Abs::zero(),
        ))
    }
}

#[cfg(feature = "typst")]
const FONTS_URLS: &[&str] = &[
    "https://mirrors.ctan.org/fonts/newcomputermodern/otf/NewCMMath-Regular.otf",
    "https://mirrors.ctan.org/fonts/newcomputermodern/otf/NewCMMath-Book.otf",
    "https://mirrors.ctan.org/fonts/newcomputermodern/otf/NewCMMath-Bold.otf",
];

#[cfg(feature = "typst")]
lazy_static::lazy_static! {
    static ref FONTS: Vec<Box<[u8]>> = {
        use std::io::Read;

        FONTS_URLS.iter().map(|url| {
            let response = ureq::get(*url).call().expect("Failed to download font from CTAN.");
            let mut bytes = Vec::new();
            response.into_body().into_reader().read_to_end(&mut bytes).expect("Failed to read font from CTAN.");
            bytes.into_boxed_slice()
        }).collect()
    };
}

#[cfg(test)]
mod tests {
    use std::{fs::File, io::Write};

    use crate::ops;

    use super::*;

    #[cfg(feature = "typst")]
    #[test]
    fn test_to_svg() {
        let mut circuit = Circuit::new_with_qubits(2);
        circuit.perform(ops::H, [0]);
        circuit.perform(ops::CNOT, [0, 1]);
        println!("{}", circuit.to_typst());
        let svg = circuit.to_svg().unwrap();
        let mut file = File::create("test.svg").unwrap();
        file.write_all(svg.as_bytes()).unwrap();
    }
}
