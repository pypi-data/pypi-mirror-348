mod arrow;

use pyo3::{exceptions::PyValueError, prelude::*};

#[derive(FromPyObject)]
enum Data {
    Bytes(pyo3_bytes::PyBytes), // should be first!
    Arrow(pyo3_arrow::PyArray),
    Channel3(Vec<(u8, u8, u8)>),
    Channel4(Vec<(u8, u8, u8, u8)>),
}

impl Data {
    #[inline]
    fn as_byte_slice(&self) -> PyResult<&[u8]> {
        #[inline]
        fn bytes<T>(slice: &[T]) -> Option<&[u8]> {
            let len: usize = slice.len().checked_mul(size_of::<T>())?;
            Some(unsafe { std::slice::from_raw_parts(slice.as_ptr() as *const u8, len) })
        }

        const ERROR: &str = "image is too big";

        match self {
            Data::Arrow(array) => crate::arrow::py_array_to_slice(array),
            Data::Bytes(bytes) => Ok(bytes.as_slice()),
            Data::Channel3(pixels) => bytes::<(u8, u8, u8)>(pixels)
                .ok_or(ERROR)
                .map_err(PyValueError::new_err),
            Data::Channel4(pixels) => bytes::<(u8, u8, u8, u8)>(pixels)
                .ok_or(ERROR)
                .map_err(PyValueError::new_err),
        }
    }

    #[inline]
    fn pixel_count(&self) -> Option<usize> {
        match self {
            Data::Arrow(array) => crate::arrow::pixel_count(array),
            Data::Bytes(_) => None,
            Data::Channel3(pixels) => Some(pixels.len()),
            Data::Channel4(pixels) => Some(pixels.len()),
        }
    }
}

#[pymodule]
mod _qoi {
    use std::borrow::Cow;

    use pyo3::exceptions::{PyAssertionError, PyValueError};
    use pyo3::{PyErr, PyResult, pyclass, pyfunction, pymethods};
    use pyo3_bytes::PyBytes;
    use qoi::{Channels, ColorSpace, Decoder, Encoder};

    use crate::Data;

    const LINEAR: &str = "linear";
    const SRGB: &str = "SRGB";
    const COLOUR_SPACES: [&str; 2] = [LINEAR, SRGB];

    const RGB: &str = "RGB";
    const RGBA: &str = "RGBA";
    const MODES: [&str; 2] = [RGB, RGBA];

    fn to_py_error(error: qoi::Error) -> PyErr {
        match &error {
            qoi::Error::InvalidChannels { .. }
            | qoi::Error::InvalidColorSpace { .. }
            | qoi::Error::InvalidImageDimensions { .. }
            | qoi::Error::InvalidImageLength { .. }
            | qoi::Error::InvalidMagic { .. }
            | qoi::Error::InvalidPadding
            | qoi::Error::UnexpectedBufferEnd => PyValueError::new_err(error.to_string()),
            qoi::Error::OutputBufferTooSmall { .. } | qoi::Error::IoError(_) => {
                PyAssertionError::new_err(error.to_string())
            }
        }
    }

    #[pyfunction]
    #[pyo3(signature = (data, /, *, width, height, colour_space = None, mode = None))]
    fn encode(
        data: Data,
        width: u32,
        height: u32,
        colour_space: Option<&str>,
        mode: Option<&str>, // channels
    ) -> PyResult<Cow<'static, [u8]>> {
        let mut encoder = {
            let data = data.as_byte_slice()?;

            Encoder::new(data, width, height).map_err(to_py_error)?
        };

        if let Some(mode) = mode {
            let channels = if mode.eq_ignore_ascii_case(RGB) {
                Channels::Rgb
            } else if mode.eq_ignore_ascii_case(RGBA) {
                Channels::Rgba
            } else {
                return Err(PyValueError::new_err(format!(
                    "invalid mode, needs to be one of {MODES:?}"
                )));
            };

            encoder = encoder.with_channels(channels);
        }

        if let Some(pixel_count) = data.pixel_count() {
            if pixel_count != encoder.header().n_pixels() {
                return Err(PyValueError::new_err(format!(
                    "got {pixel_count} pixels, image can't be {width}x{height}"
                )));
            }
        }

        if let Some(colour_space) = colour_space {
            let colour_space = if colour_space.eq_ignore_ascii_case(LINEAR) {
                ColorSpace::Linear
            } else if colour_space.eq_ignore_ascii_case(SRGB) {
                ColorSpace::Srgb
            } else {
                return Err(PyValueError::new_err(format!(
                    "invalid colour space, needs to be one of {COLOUR_SPACES:?}"
                )));
            };

            encoder = encoder.with_colorspace(colour_space);
        }

        encoder.encode_to_vec().map_err(to_py_error).map(Into::into)
    }

    #[pyclass(eq)]
    #[derive(PartialEq)]
    struct Image {
        #[pyo3(get)]
        width: u32,
        #[pyo3(get)]
        height: u32,
        #[pyo3(get)]
        data: Cow<'static, [u8]>,
        channels: Channels,
        colourspace: ColorSpace,
    }

    #[pymethods]
    impl Image {
        #[getter]
        fn mode(&self) -> &'static str {
            match self.channels {
                Channels::Rgb => "RGB",
                Channels::Rgba => "RGBA",
            }
        }

        #[getter]
        fn channels(&self) -> u8 {
            self.channels.as_u8()
        }

        #[getter]
        fn colour_space(&self) -> &'static str {
            match self.colourspace {
                ColorSpace::Linear => LINEAR,
                ColorSpace::Srgb => SRGB,
            }
        }

        fn __repr__(&self) -> PyResult<String> {
            let mode = self.mode();
            let Self { width, height, .. } = self;
            let color_space = self.colour_space();
            let id = self as *const Self;
            Ok(format!(
                "<qoi_rs._qoi.Image colour_space={color_space} mode={mode} size={width}x{height} at {id:?}>"
            ))
        }
    }

    #[pyfunction]
    #[pyo3(signature = (data, /))]
    fn decode(data: PyBytes) -> PyResult<Image> {
        let mut decoder = Decoder::new(&data).map_err(to_py_error)?;

        let header = decoder.header();

        Ok(Image {
            width: header.width,
            height: header.height,
            channels: header.channels,
            colourspace: header.colorspace,
            data: decoder.decode_to_vec().map_err(to_py_error)?.into(),
        })
    }
}
