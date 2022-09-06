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

def mean(df: pd.DataFrame) -> float:
    return np.mean(df.values)

def min(df: pd.DataFrame) -> float:
    return np.min(df.values)

def std(df: pd.DataFrame) -> float:
    return np.std(df.values)

def sum(df: pd.DataFrame) -> float:
    return np.sum(df.values)


constants = {
    'PI': np.pi, 'E': np.e,
}
functions = {
    # See above
    'norm': norm,
    'count': count, 'max': max, 'mean': mean, 'min': min, 'std': std, 'sum': sum,
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
