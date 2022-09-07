__all__ = ['Figure']


import typing as t

import matplotlib.pyplot as plt

from matplotlib.axes import Axes
from matplotlib.figure import Figure


class Figure:

    _fig: Figure
    _ax: Axes

    def __init__(self, **kwargs: t.Any) -> None:
        self._fig, self._ax = plt.subplots(1, 1, **kwargs)

    @classmethod
    def show(cls) -> None:
        plt.show()

    @property
    def ax(self) -> Axes:
        return self._ax

    @property
    def fig(self) -> Figure:
        return self._fig

    def annotate(self, x: float, y: float, text: str, **kwargs: t.Any) -> 'Figure':
        self._ax.annotate(text, (x, y), **kwargs)
        return self

    def plot(self, x: t.Any, y: t.Any, **kwargs: t.Any) -> 'Figure':
        self._ax.plot(x, y, **kwargs)
        return self

    def scatter(self, x: t.Any, y: t.Any, **kwargs: t.Any) -> 'Figure':
        self._ax.scatter(x, y, **kwargs)
        return self

    def set(self, **kwargs: t.Any) -> 'Figure':
        self._ax.set(**kwargs)
        return self

    def legend(self, **kwargs: t.Any) -> 'Figure':
        kwargs = {
            'bbox_to_anchor': (1.01, 1.0), 'borderaxespad': 0,
            'loc': 'upper left', 'ncol': 1, **kwargs,
        }
        self._ax.legend(**kwargs)
        return self

    def grid(self, **kwargs: t.Any) -> 'Figure':
        self._ax.grid(**kwargs)
        return self

    def save(self, path: str, **kwargs: t.Any) -> 'Figure':
        kwargs = {'bbox_inches': 'tight', 'transparent': True, **kwargs}
        self._fig.savefig(path, **kwargs)
        return self
