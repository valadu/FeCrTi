__all__ = ['data']


import pathlib as p

import numpy as np
import pandas as pd


root = p.Path(__file__).absolute().parent
data = {
    path.stem: pd.read_json(path).applymap(np.average)
    for path in root.iterdir()
    if path.suffix == '.json'
}
