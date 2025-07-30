use derive_more::{Index, IndexMut};
use std::fmt;

/// A table of typst quill circuit. The first `Vec` is the row, and the second `Vec` is the column.
///
#[derive(Debug, Clone, Eq, PartialEq, Hash, Index, IndexMut)]
pub struct QuillTable(pub Vec<Vec<String>>);

impl QuillTable {
    /// Create a new `QuillTable` with `n` rows and `n` columns.
    ///
    /// # Arguments
    ///
    /// * `n` - The number of rows.
    ///
    pub fn new(n: usize) -> Self {
        QuillTable(vec![vec![]; n])
    }

    /// Add a column to the table. Fill the column with "1" if the index is not in the items.
    ///
    /// # Arguments
    ///
    /// * `items` - A list of tuples, where the first element is the index of the row, and the second element is the item to add.
    ///
    /// # Example
    ///
    /// ```rust
    /// // This will be transformed using `add_column`:
    /// let table = QuillTable(vec![
    ///     vec!["gate($H$)"],
    ///     vec!["1"        , "1" ,]    ,     
    ///     vec!["1"        , "1" , "1"],     
    ///     vec!["nwire(2)"],     
    ///     vec!["1"        , "1"],     
    /// ])
    ///
    /// table.add_column([(1, "$a$"), (3, "$b$"), (4, "$c$")]);
    ///
    /// // The table will be transformed to:
    /// assert_eq!(table.0, vec![
    ///     vec!["gate($H$)"],    
    ///     vec!["1"         , "1", "1", "$a$"],
    ///     vec!["1"         , "1", "1", "1"]  ,
    ///     vec!["nwire(2)"  , "1", "1", "$b$"],
    ///     vec!["1"         , "1", "1", "$c$"],
    /// ])
    /// ```
    ///
    pub fn add_column(&mut self, items: impl IntoIterator<Item = (usize, String)>) {
        let items = items.into_iter().collect::<Vec<_>>();
        let min = *items.iter().map(|(i, _)| i).min().unwrap();
        let max = *items.iter().map(|(i, _)| i).max().unwrap();
        let max_len = (min..=max).map(|v| self.0[v].len()).max().unwrap();

        for i in min..=max {
            while self.0[i].len() < max_len {
                self.0[i].push("1".to_owned());
            }

            if let Some((_, item)) = items.iter().find(|(a, _)| *a == i) {
                self.0[i].push(item.clone());
            } else {
                self.0[i].push("1".to_owned());
            }
        }
    }
}

impl std::fmt::Display for QuillTable {
    /// Formats the table into a typst-formatted representation for quantum circuits.
    ///
    /// It writes a series of lines that include an import statement, page configuration values, and a quantum circuit directive, iterating over each row to output the circuit details with consistent spacing.
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "#import \"@preview/quill:0.7.0\": *")?;
        writeln!(f, "#set page(width: auto, margin: 0pt, height: auto)")?;

        writeln!(f, "#quantum-circuit(")?;
        let max_len = self.0.iter().map(|p| p.len()).max().unwrap();

        for (i, row) in self.0.iter().enumerate() {
            if i == self.0.len() - 1 {
                writeln!(f, "    {}, {}, ", row.join(", "), max_len - row.len() + 1)?;
            } else {
                writeln!(
                    f,
                    "    {}, {}, [\\ ], ",
                    row.join(", "),
                    max_len - row.len() + 1
                )?;
            }
        }
        writeln!(f, ")")
    }
}
