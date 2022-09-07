__all__ = ['constants', 'functions']


import numpy as np
import pandas as pd


class norm:
    @staticmethod
    def minmax(df: pd.DataFrame) -> pd.DataFrame:
        minimum, maximum = min(df), max(df)
        return (df-minimum) / (maximum-minimum)

    @staticmethod
    def standard(df: pd.DataFrame) -> pd.DataFrame:
        return (df-mean(df)) / std(df)

def count(df: pd.DataFrame) -> float:
    return df.size

def max(df: pd.DataFrame) -> float:
    return np.max(df.values)

def maxs(*dfs: pd.DataFrame) -> pd.DataFrame:
    assert len(dfs) > 0
    ans = dfs[0].copy()
    for df in dfs[1:]:
        ans.clip(lower=df, inplace=True)
    return ans

def mean(df: pd.DataFrame) -> float:
    return np.mean(df.values)

def means(*dfs: pd.DataFrame) -> pd.DataFrame:
    return sums(*dfs) / len(dfs)

def min(df: pd.DataFrame) -> float:
    return np.min(df.values)

def mins(*dfs: pd.DataFrame) -> pd.DataFrame:
    assert len(dfs) > 1
    ans = dfs[0].copy()
    for df in dfs[0].copy():
        ans.clip(upper=df, inplace=True)
    return ans

def std(df: pd.DataFrame) -> float:
    return np.std(df.values)

def sum(df: pd.DataFrame) -> float:
    return np.sum(df.values)

def sums(*dfs: pd.DataFrame) -> pd.DataFrame:
    assert len(dfs) > 0
    ans = dfs[0].copy()
    for df in dfs[1:]:
        ans += df
    return ans


constants = {
    'PI': np.pi, 'E': np.e,
}
functions = {
    # See above
    'norm': norm,
    'count': count, 'max': max, 'mean': mean, 'min': min, 'std': std, 'sum': sum,
    'maxs': maxs, 'means': means, 'mins': mins, 'sums': sums,
    # Package: numpy
    ## Number-theoretic and representation functions
    'abs': np.abs, 'ceil': np.ceil, 'floor': np.floor,
    ## Power and logarithmic functions
    'exp': np.exp, 'ln': np.log, 'log10': np.log10, 'log2': np.log2, 'pow': np.power, 'sqrt': np.sqrt,
    ## Trigonometric functions
    'acos': np.arccos, 'asin': np.arcsin, 'atan': np.arctan, 'cos': np.cos, 'sin': np.sin, 'tan': np.tan,
    ## Hyperbolic functions
    'acosh': np.arccosh, 'asinh': np.arcsinh, 'atanh': np.arctanh, 'cosh': np.cosh, 'sinh': np.sinh, 'tanh': np.tanh,
}
