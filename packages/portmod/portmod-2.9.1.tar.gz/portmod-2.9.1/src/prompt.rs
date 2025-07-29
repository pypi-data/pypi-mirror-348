use inquire::{InquireError, MultiSelect};
use pyo3::exceptions::{PyException, PyIOError, PyKeyboardInterrupt};
use pyo3::prelude::*;

#[derive(Debug)]
/// Error that wraps `InquireError`s
pub struct PromptErr(InquireError);

impl From<PromptErr> for PyErr {
    fn from(value: PromptErr) -> Self {
        match value.0 {
            InquireError::NotTTY => {
                PyException::new_err("the input device is not a TTY; unable to read input")
            }
            InquireError::InvalidConfiguration(e) => PyException::new_err(format!(
                "the given prompt configuration is not valid: {}",
                e
            )),
            InquireError::IO(e) => PyIOError::new_err(e),
            InquireError::OperationCanceled => PyKeyboardInterrupt::new_err("Operation canceled"),
            InquireError::OperationInterrupted => {
                PyKeyboardInterrupt::new_err("Operation interupted")
            }
            InquireError::Custom(e) => PyException::new_err(e.to_string()),
        }
    }
}

impl From<InquireError> for PromptErr {
    fn from(other: InquireError) -> Self {
        Self(other)
    }
}

#[pyfunction]
#[pyo3(signature = (question, options, help_message=None))]
/// A prompt that allows the user to select one or more options
pub fn multi_select_prompt(
    question: &str,
    options: Vec<PyObject>,
    help_message: Option<&str>,
) -> Result<Vec<PyObject>, PromptErr> {
    let mut prompt = MultiSelect::new(question, options);
    if let Some(help_message) = help_message {
        prompt = prompt.with_help_message(help_message)
    }
    Ok(prompt.prompt()?)
}
