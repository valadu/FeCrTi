__all__ = ['Oval']


import typing as t

import numpy as np


class Oval:
    def __init__(self, a: float, b: float) -> None:
        self._a = a
        self._b = b

    def random(self, number: int, seed: t.Optional[int] = None) -> t.Tuple[np.ndarray, np.ndarray]:
        if seed is not None:
            np.random.seed(seed)
        xs = self._a * np.random.random(number)
        ys = self._b * np.random.random(number)
        index = xs**2/self._a**2 + ys**2/self._b**2 < 1
        return xs[index], ys[index]

    def tangent(self, slope: float) -> t.Callable:
        intercept = np.sqrt(self._a**2*slope**2 + self._b**2)
        return lambda x: slope*x + intercept

    def y(self, x: np.ndarray) -> np.ndarray:
        return self._b * np.sqrt(1-x**2/self._a**2)
