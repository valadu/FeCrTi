__all__ = ['Part']


import itertools as it
import random
import types
import typing as t

import numpy as np
import pandas as pd
import plotly.express as px
import scipy as sp

import data
import lib
import model
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

    def sidebar(self, steps: t.Tuple[str, str, str]) -> str:
        with self.st.sidebar:
            self.st.markdown(f'<center><pre><code>{lib.__logo__}</code></pre></center>', unsafe_allow_html=True)
            self.st.markdown('''
            ''')
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
        names = list(map(self._rename, keys))
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
            level = self._slider(f'data_visualization_with_one:1', 2, 64, 8, 'Number of maximum levels:')
            self._st.auto(
                lib.image.seaborn.Figure(figsize=(16, 12))
                    .heatmap_with_contour(df, level=level, contour_kwargs=D(colors='black'), heatmap_kwargs=D(cmap='YlGnBu'))
                    .set(title=name)
            )
        with tabs[2]:
            level = self._slider(f'data_visualization_with_one:2', 2, 64, 8, 'Number of maximum levels:')
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
        ans = self._eval(expression, variables)
        if ans is not None:
            self.data_visualization_with_one(expression, expression, ans)

    def optimization(self, steps: t.Tuple[str, str]) -> None:
        with self.st.sidebar, self.st.form(key='optimization'):
            step = self.st.radio('Which data do you want to visualize?', steps)
            self.st.form_submit_button(label='Ready!')
        return step

    def optimization_references(self) -> None:
        tabs = self.st.tabs(['References', 'Simple Schematic', 'Real-life Example'])
        with tabs[0]:
            self.st.markdown('''
### References
- [多目标优化 - 机器之心](https://www.jiqizhixin.com/graph/technologies/cf8932be-519a-4fd9-84f9-c6ffa997a554)
- [帕累托效率 - 维基百科](https://zh.wikipedia.org/wiki/帕累托效率)
            ''')
        with tabs[1]:
            weight = self.st.slider('Weight (ω):', 0.0, 5.0, 1.0)
            is_pareto_frontier = self.st.checkbox('Pareto Frontier', False)
            #
            o = model.Oval(4.0, 3.0)
            xs_rand, ys_rand = o.random(512, 0)
            xs_line = np.linspace(0.0, 5.0, 100)
            fig = px.scatter(x=xs_rand, y=ys_rand) \
                .add_scatter(x=xs_line, y=o.tangent(-weight)(xs_line), name=f'y + {weight:.03f}x') \
                .update_layout(xaxis=dict(range=[0, 5]), yaxis=dict(range=[0, 5]))
            if is_pareto_frontier:
                xs_pareto = np.linspace(0.0, 4.0, 100)
                fig.add_scatter(x=xs_pareto, y=o.y(xs_pareto), name='Pareto Frontier')
            self.st.plotly_chart(fig)
        with tabs[2]:
            self.st.image('static/mv.png')

    def optimization_getstarted(self) -> None:
        self._title_caption('Specify expressions to be maximized ✨', '')
        with self.st.form(key='optimization_getstarted'):
            expressions = [self.st.text_input(f'{axis}:', 'None') for axis in 'XYZ']
            self.st.form_submit_button(label='Calculate the result.')
        self._namespace(Constant=scope.constants, Function=scope.functions, Variable=data.data)
        # Valid expression(s) and their/its answer(s)
        valids = []
        for expr in expressions:
            ans = self._eval(expr, data.data)
            if isinstance(ans, pd.DataFrame):
                valids.append((expr, ans))
        if len(valids) == 0:
            self.st.error('Please specify one or more of $X$, $Y$, $Z$.')
        elif len(valids) == 1:
            color = self.st.color_picker('Pick a color that indicates maximum:', '#ffff00')
            self.optimization_getstarted_one(*valids[0], color)
        elif len(valids) == 2:
            self.optimization_getstarted_two(*zip(*valids))
        elif len(valids) == 3:
            self.optimization_getstarted_three(*zip(*valids))

    def optimization_getstarted_one(self, expr: str, ans: pd.DataFrame, color: str = '#ffff00') -> None:
        maximum = ans.max().max()
        func = lambda cell: f'background-color: {color}' if cell==maximum else ''
        self.st.dataframe(ans.style.applymap(func))

    def optimization_getstarted_two(
        self,
        expr_xy: t.Tuple[str, str],
        ans_xy: t.Tuple[pd.DataFrame, pd.DataFrame],
    ) -> None:
        scale = self._slider(f'optimization_getstarted_two', 0, 16, 0, 'Scale of spline interpolation:')
        xlabel, ylabel = expr_xy
        xs, ys = ans_xy
        xs_more = sp.ndimage.zoom(xs.values, scale)
        ys_more = sp.ndimage.zoom(ys.values, scale)
        data = {xlabel: [], ylabel: [], 'name': []}
        for column, index in it.product(xs.columns, xs.index):
            data[xlabel].append(xs[column][index])
            data[ylabel].append(ys[column][index])
            data['name'].append(f'{column}{index}')
        fig = px.scatter(pd.DataFrame(data), x=xlabel, y=ylabel, color='name') \
            .update_traces(marker=D(color='DeepSkyBlue', size=12)) \
            .update_layout(showlegend=False) \
            .add_scatter(x=xs_more.flatten(), y=ys_more.flatten(), mode='markers', opacity=0.5, marker=D(color='LightSkyBlue', size=9), hoverinfo='skip')
        self.st.plotly_chart(fig)

    def optimization_getstarted_three(
        self,
        expr_xyz: t.Tuple[str, str, str],
        ans_xyz: t.Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame],
    ) -> None:
        scale = self._slider(f'optimization_getstarted_two', 0, 9, 0, 'Scale of spline interpolation:')
        xlabel, ylabel, zlabel = expr_xyz
        xs, ys, zs = ans_xyz
        xs_more = sp.ndimage.zoom(xs.values, scale)
        ys_more = sp.ndimage.zoom(ys.values, scale)
        zs_more = sp.ndimage.zoom(zs.values, scale)
        data = {xlabel: [], ylabel: [], zlabel: [], 'name': []}
        for column, index in it.product(xs.columns, xs.index):
            data[xlabel].append(xs[column][index])
            data[ylabel].append(ys[column][index])
            data[zlabel].append(zs[column][index])
            data['name'].append(f'{column}{index}')
        fig = px.scatter_3d(pd.DataFrame(data), x=xlabel, y=ylabel, z=zlabel, color='name') \
            .update_traces(marker=D(size=9)) \
            .update_layout(showlegend=False) \
            .add_scatter3d(x=xs_more.flatten(), y=ys_more.flatten(), z=zs_more.flatten(), mode='markers', opacity=0.5, marker=D(size=5), hoverinfo='skip')
        self.st.plotly_chart(fig)

    def _line_break(self, number: int) -> None:
        for _ in range(number):
            self.st.text('')

    def _cataas(self, **kwargs: t.Any) -> str:
        params = '&'.join(f'{k}={v}' for k, v in kwargs.items())
        return f'https://cataas.com/cat?{params}'

    def _title_caption(self, title: str, caption: str) -> None:
        self.st.title(title)
        self.st.caption(caption)

    def _slider(self, key: str, min: int, max: int, value: int, text: str) -> int:
        with self.st.form(key=key):
            level = self.st.slider(text, min, max, value)
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

    def _rename(self, text: str) -> str:
        return text.replace('_', ' ').capitalize()

    def _eval(self, expression: str, variables: t.Dict[str, pd.DataFrame] = data.data) -> t.Optional[pd.DataFrame]:
        try:
            ans = eval(expression, {}, {**scope.constants, **scope.functions, **variables})
        except Exception as e:
            self.st.error(f'**{e.__class__.__name__}**: {e}')
            return None
        else:
            return ans
