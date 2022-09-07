__all__ = ['Part']


from asyncio import constants
import random
import types
import typing as t

import pandas as pd

import data
import lib
import scope


D = dict


class Part:
    def __init__(self) -> None:
        self._st = lib.base.streamlit.StreamLit()

    @property
    def st(self) -> types.ModuleType:
        return self._st.st

    def meta(self) -> None:
        self.st.set_page_config(page_title='FeCrTi', page_icon='🌏')

    def sidebar(self, steps: t.List[str]) -> str:
        with self.st.sidebar:
            self.st.markdown(f'<center><pre><code>{lib.__logo__}</code></pre></center>', unsafe_allow_html=True)
            with self.st.form(key='sidebar'):
                step = self.st.radio('Which step do you want to take?', steps)
                self.st.form_submit_button(label='Ready!')
        return step

    def relaxation(self) -> None:
        with self.st.sidebar, self.st.form(key='relaxation'):
            n_rows = self.st.slider('Number of rows:', 2, 8, 4)
            n_cols = self.st.slider('Number of columns:', 2, 8, 4)
            self.st.form_submit_button(label='Reset layout.')
        self._title_caption('Choose your favorite cat 🐱', 'You can display the image in full size by hovering it and clicking the double arrow.')
        for _ in range(n_rows):
            row = self.st.container()
            for col in row.columns(n_cols):
                col.image(self._cataas(width=1200, height=1200, _=random.random()))

    def data_visualization(self) -> None:
        with self.st.sidebar, self.st.form(key='data_visualization'):
            keys = self.st.multiselect('Which data do you want to visualize?', data.data.keys())
            self.st.form_submit_button(label='Reset data.')
        names = [key.replace('_', ' ').capitalize() for key in keys]
        dfs = [data.data[key] for key in keys]
        if len(keys) == 0:
            pass
        elif len(keys) == 1:
            self._title_caption('Choose the type of visualization 📊', 'You can display the image in full size by hovering it and clicking the double arrow.')
            self.data_visualization_with_one(keys[0], names[0], dfs[0])
        else:
            self._title_caption('Custom expression to calculate 🖩', '')
            self.data_visualization_with_more(keys, names, dfs)

    def data_visualization_with_one(self, key: str, name: str, df: pd.DataFrame) -> None:
        tabs = self.st.tabs(['Interactive Table', 'Contour Lines', 'Filled Contours', '3D Surface'])
        with tabs[0]:
            self.st.dataframe(df)
        with tabs[1]:
            level = self._level(f'data_visualization_with_one:1', 2, 64, 8)
            self._st.auto(
                lib.image.seaborn.Figure(figsize=(16, 12))
                    .heatmap_with_contour(df, level=level, contour_kwargs=D(colors='black'), heatmap_kwargs=D(cmap='YlGnBu'))
                    .set(title=name)
            )
        with tabs[2]:
            level = self._level(f'data_visualization_with_one:2', 2, 64, 8)
            self._st.auto(
                lib.image.seaborn.Figure(figsize=(16, 12))
                    .heatmap_with_contourf(df, level=level)
                    .set(title=name)
            )
        with tabs[3]:
            self._st.auto(
                lib.image.plotly.Figure()
                    .new_surface_with_mesh(
                        df,
                        scatter3d_kwargs=D(line=D(color='#000000', width=3)),
                        surface_kwargs=D(name=name, contours=D(z=D(show=True, usecolormap=True, project_z=True))),
                    )
                    .update_layout(showlegend=False)
            )

    def data_visualization_with_more(self, keys: t.List[str], names: t.List[str], dfs: t.List[pd.DataFrame]) -> None:
        expression = self._expression('data_visualization_with_more', ' + '.join(keys))
        variables = dict(zip(keys, dfs))
        self._namespace(Constant=scope.constants, Function=scope.functions, Variable=variables)
        try:
            ans = eval(expression, {}, {**scope.constants, **scope.functions, **variables})
        except Exception as e:
            self.st.error(f'**{e.__class__.__name__}**: {e}')
            self.st.stop()
        self.data_visualization_with_one(expression, expression, ans)

    def line_break(self, number: int) -> None:
        for _ in range(number):
            self.st.text('')

    def _cataas(self, **kwargs: t.Any) -> str:
        params = '&'.join(f'{k}={v}' for k, v in kwargs.items())
        return f'https://cataas.com/cat?{params}'

    def _title_caption(self, title: str, caption: str) -> None:
        self.st.title(title)
        self.st.caption(caption)

    def _level(self, key: str, min: int, max: int, value: int) -> int:
        with self.st.form(key=key):
            level = self.st.slider('Number of maximum levels:', min, max, value)
            self.st.form_submit_button(label='Reset image.')
        return level

    def _expression(self, key: str, default: str) -> str:
        with self.st.form(key=key):
            expression = self.st.text_input('Expression </>', default)
            self.st.form_submit_button(label='Calculate the result.')
        return expression

    def _namespace(self, **kwargs: t.Any) -> None:
        with self.st.expander('View functions and variables available in current namespace.'):
            self.st.write(kwargs)
