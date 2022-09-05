__all__ = ['Figure']


import functools as f
import typing as t

import numpy as np
import pandas as pd

from plotly import graph_objects as go

from ..base.type import KwArgs


class Figure:
    def __init__(self) -> None:
        self._fig = go.Figure()
        self._ret = None
        for attr in dir(self._fig):
            if attr.startswith('add_') or attr.startswith('update_'):
                setattr(self, attr, self._wrap(self._fig, attr))

    @property
    def fig(self) -> go.Figure:
        return self._fig

    @property
    def reet(self) -> t.Any:
        return self._ret

    def surface(self, data: pd.DataFrame, **kwargs: t.Any) -> 'Figure':
        self._surface(data.columns, data.index, data.values, **kwargs)
        return self

    def add_surface_with_mesh(
        self,
        data: pd.DataFrame,
        scatter3d_kwargs: KwArgs = {}, surface_kwargs: KwArgs = {},
    ) -> 'Figure':
        # height, width == len(y:=data.index), len(x:=data.columns) == data.shape
        func = lambda xyz: self._scatter3d(*xyz, mode='lines', **scatter3d_kwargs)
        height, width = data.shape
        x, y, Z = np.arange(width), np.arange(height), data.values
        X, Y = np.meshgrid(x, y)
        list(map(func, zip(X, Y, Z))), list(map(func, zip(X.T, Y.T, Z.T)))
        self._surface(x, y, Z, **surface_kwargs)
        return self.update_scenes(
            xaxis={'ticktext': data.columns, 'tickvals': x},
            yaxis={'ticktext': data.index, 'tickvals': y},
        )

    def _wrap(self, obj: t.Any, attr: str) -> t.Callable:
        method = getattr(obj, attr)

        @f.wraps(method)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> 'Figure':
            self._ret = method(*args, **kwargs)
            return self

        return wrapper

    def _scatter3d(self, x: np.ndarray, y: np.ndarray, z: np.ndarray, **kwargs: t.Any) -> None:
        self._fig.add_scatter3d(x=x, y=y, z=z, **kwargs)

    def _surface(self, x: pd.Index, y: pd.Index, Z: np.ndarray, **kwargs: t.Any) -> None:
        self._fig.add_surface(x=x, y=y, z=Z, **kwargs)
