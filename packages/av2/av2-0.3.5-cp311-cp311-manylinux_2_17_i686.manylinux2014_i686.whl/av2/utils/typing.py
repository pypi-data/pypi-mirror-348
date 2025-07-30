# <Copyright 2022, Argo AI, LLC. Released under the MIT license.>

"""Types used throughout the package."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Union  # noqa

import numpy as np
import numpy.typing as npt
from upath import UPath

NDArrayNumber = np.ndarray[Any, np.dtype[Union[np.integer[Any], np.floating[Any]]]]
NDArrayBool = npt.NDArray[np.bool]
NDArrayFloat = npt.NDArray[np.floating[Any]]
NDArrayByte = npt.NDArray[np.uint8]
NDArrayInt = npt.NDArray[np.int64]
NDArrayObject = npt.NDArray[np.object_]

PathType = Union[Path, UPath]
