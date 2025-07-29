// Copyright 2019-2020 Portmod Authors
// Distributed under the terms of the GNU General Public License v3

use derive_more::{Display, From};
use pyo3::{
    exceptions::{PyOSError, PyValueError},
    PyErr,
};

#[derive(Debug, Display, From)]
pub enum Error {
    #[display("{_0}: {_1}")]
    IO(String, std::io::Error),
    #[display("{_0}: {_1}")]
    Yaml(String, serde_yaml::Error),
    LanguageIdentifier(unic_langid::LanguageIdentifierError),
    Std(Box<dyn std::error::Error>),
    UnsupportedHashType(String),
    #[display("Error when parsing file {_0}: {_1}")]
    Plugin(String, esplugin::Error),
    #[display("Error when reading/writing index: {_0}")]
    Tantivy(tantivy::TantivyError),
}

impl std::convert::From<Error> for PyErr {
    fn from(err: Error) -> PyErr {
        match err {
            Error::Yaml(file, error) => PyValueError::new_err(format!("In file {file}: {error}")),
            _ => PyOSError::new_err(err.to_string()),
        }
    }
}
