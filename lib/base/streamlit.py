__all__ = ['StreamLit']


import functools as f
import types
import typing as t

import streamlit as st

from .. import image


class StreamLit:
    def __init__(self) -> None:
        self._ret = None
        for attr in dir(st._main):
            if not attr.startswith('_'):
                try:
                    setattr(self, attr, self._wrap(st._main, attr))
                except TypeError:
                    pass

    def __getitem__(self, key: str) -> t.Callable:
        return getattr(st, key)

    @property
    def st(self) -> types.ModuleType:
        return st

    @property
    def ret(self) -> t.Any:
        return self._ret

    def auto(self, obj: t.Any, **kwargs: t.Any) -> 'StreamLit':
        if isinstance(obj, image.matplotlib.Figure):
            kwargs = {'bbox_inches': 'tight', 'transparent': True, **kwargs}
            self._ret = st.pyplot(obj.fig, **kwargs)
        elif isinstance(obj, image.seaborn.Figure):
            self.auto(obj.fig)
        elif isinstance(obj, image.plotly.Figure):
            kwargs = {**kwargs}
            self._ret = st.plotly_chart(obj.fig, **kwargs)
        else:
            raise NotImplementedError
        return self

    def _wrap(self, obj: t.Any, attr: str) -> t.Callable:
        method = getattr(obj, attr)

        @f.wraps(method)
        def wrapper(*args: t.Any, **kwargs: t.Any) -> 'StreamLit':
            self._ret = method(*args, **kwargs)
            return self

        return wrapper
