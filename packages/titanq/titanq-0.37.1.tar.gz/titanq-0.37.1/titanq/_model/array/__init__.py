# Copyright (c) 2025, InfinityQ Technology, Inc.

"""
The Array module defines the structure for array management within the TitanQ SDK.

`ArrayBuilder` is an interface that enables its subclasses to construct arrays for use with the TitanQ SDK.

`ArrayLike` is an interface for objects that are considered "array-like." It provides a set of methods that
can be implemented by any class—whether it's a numpy.ndarray or a specialized type (such as scipy's coo_array)
to ensure compatibility with the expected behaviors of the SDK.

`ArrayLike` instances are created through the `ArrayLikeFactory`, ensuring consistency and simplicity across the SDK.

`Array` is an alias for the raw data arrays supported by TitanQ, meaning the array module can directly interact with
these types of arrays.
"""

from typing import Union

import numpy as np
from scipy.sparse import coo_array, csr_array


# Alias for the supported array types in the TitanQ SDK
Array = Union[np.ndarray, coo_array, csr_array]

# dtype to use for any numpy array like
_TITANQ_DTYPE = np.float32