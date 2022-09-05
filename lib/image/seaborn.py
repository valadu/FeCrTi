__all__ = ['Figure']


import typing as t

import numpy as np
import pandas as pd
import scipy as sp
import seaborn as sns

from . import matplotlib
from ..base.type import KwArgs


class Figure:
    def __init__(self, **kwargs: t.Any) -> None:
        self._fig = matplotlib.Figure(**kwargs)

    @property
    def fig(self) -> matplotlib.Figure:
        return self._fig

    def set(self, **kwargs: t.Any) -> 'Figure':
        self._fig.set(**kwargs)
        return self

    def heatmap(self, data: pd.DataFrame, **kwargs: t.Any) -> 'Figure':
        kwargs = {'annot': True, 'fmt': '.03f', **kwargs}
        sns.heatmap(data, ax=self._fig.ax, **kwargs)
        return self

    def heatmap_with_contour(
        self,
        data: pd.DataFrame, level: int = 5, scale: float = 5.0,
        contour_kwargs: KwArgs = {}, heatmap_kwargs: KwArgs = {},
    ) -> 'Figure':
        height, width = data.shape
        Z = sp.ndimage.zoom(data.to_numpy(), scale)
        self._fig.ax.contour(
            np.linspace(0, width, round(width*scale)),
            np.linspace(0, height, round(height*scale)),
            Z, levels=self._levels(data, level), **contour_kwargs,
        )
        return self.heatmap(data, **heatmap_kwargs)

    def heatmap_with_contourf(
        self,
        data: pd.DataFrame, level: int = 5, scale: float = 5.0,
        contour_kwargs: KwArgs = {}, heatmap_kwargs: KwArgs = {},
    ) -> 'Figure':
        height, width = data.shape
        Z = sp.ndimage.zoom(data.to_numpy(), scale)
        cntr = self._fig.ax.contourf(
            np.linspace(0, width, round(width*scale)),
            np.linspace(0, height, round(height*scale)),
            Z, levels=self._levels(data, level), **contour_kwargs,
        )
        self._fig.fig.colorbar(cntr, ax=self._fig.ax)
        return self.heatmap(data, alpha=0, cbar=False, **heatmap_kwargs)

    def save(self, path: str, **kwargs: t.Any) -> 'Figure':
        self._fig.save(path, **kwargs)
        return self

    def _levels(self, data: pd.DataFrame, level: int) -> np.ndarray:
        min = np.floor(data.min().min())
        max = np.ceil(data.max().max())
        return np.linspace(min, max, level+1)
