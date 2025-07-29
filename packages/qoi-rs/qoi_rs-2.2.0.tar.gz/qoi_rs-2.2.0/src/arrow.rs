use arrow_array::{Array, FixedSizeListArray, UInt8Array};
use pyo3::PyResult;
use pyo3::exceptions::{PyAssertionError, PyTypeError, PyValueError};
use pyo3_arrow::PyArray;

#[inline]
pub fn py_array_to_slice(array: &PyArray) -> PyResult<&[u8]> {
    match array.field().data_type() {
        arrow_schema::DataType::UInt8 => {
            match array.array().as_any().downcast_ref::<UInt8Array>() {
                Some(value) => Ok(value.values().as_ref()),
                None => Err(PyAssertionError::new_err("unable to cast u8 array")),
            }
        }
        arrow_schema::DataType::FixedSizeList(field, size) => match size {
            3 | 4 => match field.data_type() {
                arrow_schema::DataType::UInt8 => {
                    match array.array().as_any().downcast_ref::<FixedSizeListArray>() {
                        Some(value) => {
                            if value.value_offset(1) != *size {
                                Err(PyAssertionError::new_err(
                                    "second element has invalid offset",
                                ))
                            } else if let Some(value) =
                                value.values().as_any().downcast_ref::<UInt8Array>()
                            {
                                Ok(value.values().as_ref())
                            } else {
                                Err(PyAssertionError::new_err("should be unreachable"))
                            }
                        }
                        None => Err(PyAssertionError::new_err("unable to cast u8 array")),
                    }
                }
                inner_type => Err(PyTypeError::new_err(format!(
                    "invalid inner list item type: {inner_type}"
                ))),
            },
            size => Err(PyValueError::new_err(format!(
                "invalid inner list length: {size}"
            ))),
        },
        data_type => Err(PyTypeError::new_err(format!(
            "invalid list item type: {data_type}"
        ))),
    }
}

#[inline]
pub fn pixel_count(array: &PyArray) -> Option<usize> {
    match array.field().data_type() {
        arrow_schema::DataType::FixedSizeList(_, _) => Some(array.array().len()),
        _ => None,
    }
}
