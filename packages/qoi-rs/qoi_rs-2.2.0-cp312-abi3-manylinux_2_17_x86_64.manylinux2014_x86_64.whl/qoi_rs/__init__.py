from collections.abc import Buffer
from typing import TYPE_CHECKING

from . import types

__all__ = "encode", "decode", "encode_pillow", "decode_pillow"

if TYPE_CHECKING:

    def encode(
        data: types.Data,
        /, *,
        width: int,
        height: int,
        colour_space: types.ColourSpace = None,
        mode: types.Mode = None,
    ) -> bytes:
        pass

    def decode(data: Buffer, /) -> types.Image:
        pass

else:
    from ._qoi import encode, decode


def encode_pillow(
    image: types.PillowImage,
    /, *,
    colour_space: types.ColourSpace = None,
    mode: types.Mode = None,
):
    return encode(
        image.tobytes(), # TODO: use image directly: https://github.com/python-pillow/Pillow/issues/8329
        width=image.width,
        height=image.height,
        colour_space=colour_space,
        mode=mode or image.mode,
    )


def decode_pillow(data: Buffer) -> types.PillowImage:
    from PIL import Image
    image = decode(data)
    return Image.frombytes(
        image.mode,
        (image.width, image.height),
        image.data,
    )
