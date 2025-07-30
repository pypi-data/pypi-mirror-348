from __future__ import annotations

import logging
import re
import ast
from typing import Iterable, Any, Type, List

import functools
import gymnasium
import numpy as np
from numpy.typing import NDArray

from .space import Space

LOG = logging.getLogger("palaestrai.types")


class MultiDiscrete(gymnasium.spaces.MultiDiscrete, Space):
    """A series of discrete action spaces

    The multi-discrete action space consists of a series of discrete action
    spaces with different number of actions in each. It is useful to represent
    game controllers or keyboards where each key can be represented as a
    discrete action space. It is parametrized by passing an array of positive
    integers specifying number of actions for each discrete action space.

    For example:

        MultiDiscrete([ 5, 2, 2 ])
    """

    _MULTI_DISCRETE_RE = re.compile(r"MultiDiscrete\(([^)]+)\)")

    def __init__(
        self,
        nvec: NDArray[np.integer[Any]] | List[int],
        dtype: str | Type[np.integer[Any]] = np.int64,
        seed: int | np.random.Generator | None = None,
    ):
        """Constructs a new multi-discrete action space

        :param list[int] nvec: vector of counts of each categorical variable. This will usually be a list of integers. However,
                you may also pass a more complicated numpy array if you'd like the space to have several axes.
        :param dtype: This should be some kind of integer type.
        :param seed: Optionally, you can use this argument to seed the RNG that is used to sample from the space.
        """
        gymnasium.spaces.MultiDiscrete.__init__(self, nvec, dtype, seed)
        Space.__init__(self)

    def to_vector(self, data: np.ndarray, **kwargs) -> np.ndarray:
        """Combine the n data points into a 1D vector.

        :kwargs: as_argmax: whether to turn the data into an argmax representation. I.e.
                    of the form: [0, 0, ... , 0, 1, 0, ... ,0] with [...].argmax() = (n*MX + m*X + x)
                    for a MultiDiscrete([N, M, X]) = [n, m, x];
                    If False the data is given of the form: [0, 0, ..., 0, 1, 0, ..., 0, 1, 0, ..., 0, 1, 0, ..., 0]
                    with the 1s being at n, N+m, N+M+x, respectively, for a MultiDiscrete([N, M, X]) = [n, m, x]
                    default: False

                 value: The value that the non zero entries in the transformed data will have
        """
        as_argmax = kwargs.get("as_argmax", False)
        value = kwargs.get("value", 1)
        if value <= 0:
            LOG.warning(
                "The value given to MultiDiscrete.flatten was lower then 0"
            )
        if as_argmax:
            as_list = [0] * np.prod(self.nvec)
            position = 0
            for idx, v in enumerate(data):
                position += v * (
                    np.prod(self.nvec[idx + 1 :]) if idx < len(data) else 1
                )
            as_list[position] = value
        else:
            as_list = []
            for idx, v in enumerate(data):
                single_list = [0] * self.nvec[idx]
                single_list[v] = value
                as_list.extend(single_list)
        return np.array(as_list)

    def reshape_to_space(self, value: Iterable, **kwargs) -> np.ndarray:
        """Turn data given in a flat form into distinct discrete values.

        The method tries to infer the form of the data from the data, if that is ambiguous it falls back to
        as_argmax.

        :kwargs: as_argmax: Explicitly tell the method to treat the data as if it was produced by
                            MultiDiscrete::flatten, with as_argmax = True; This parameter is required if
                            sum(self.nvec) == product(self.nvec)
                            default: None

        """
        as_argmax = kwargs.get("as_argmax", None)
        as_list = np.array(value)
        length = len(as_list)
        equal = np.prod(self.nvec) == sum(
            self.nvec
        )  # if the sum and the product are equal, we need to rely on an explicit argument
        argmax = False
        if equal and as_argmax is None:
            raise Exception(
                "Cannot derive data format from data, provide the 'as_argmax' parameter to explicitly "
                "define the data format"
            )
        if length == np.prod(self.nvec):
            if not as_argmax and as_argmax is not None:
                raise Exception(
                    "Data is of length for as_argmax conversion, but was explicitly told to not treat the data as such"
                )
            argmax = True
        if length != sum(self.nvec):
            raise Exception(
                f"Data does not match length of any conversion mode; Got {length} expected {np.prod(self.nvec)} or {sum(self.nvec)}"
            )
        elif as_argmax:
            raise Exception(
                "Data is not of length for as_argmax conversion, but was explicitly told to treat the data as such"
            )

        if argmax:
            as_discrete = []
            position = as_list[0]
            for idx, n in enumerate(
                self.nvec
            ):  # we work ourselves backward through the computation
                as_discrete.append(
                    int(
                        position
                        / (
                            np.prod(self.nvec[idx + 1 :])
                            if idx < len(self.nvec)
                            else 1
                        )
                    )
                )
                position -= as_discrete[-1]
        else:
            as_discrete = []
            for n in self.nvec:
                as_discrete.append(np.argmax(as_list[:n]).view(int))
                as_list = as_list[n:]
        return np.array(as_discrete)

    def to_string(self):
        return "MultiDiscrete(%s)" % np.array2string(self.nvec, separator=", ")

    @classmethod
    @functools.cache
    def from_string(cls, s):
        complete_match = MultiDiscrete._MULTI_DISCRETE_RE.match(s)
        if not complete_match:
            raise RuntimeError(
                "String '%s' does not match '%s'"
                % (s, MultiDiscrete._MULTI_DISCRETE_RE)
            )

        inner_str = complete_match[1]
        nvec = np.array(ast.literal_eval(inner_str))
        return MultiDiscrete(nvec)

    def __len__(self, as_argmax=False):
        if as_argmax:
            return np.prod(self.nvec)
        else:
            return np.sum(self.nvec)
