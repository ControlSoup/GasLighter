import numpy as np

def pretty_key_val(key: str, value, round_places: int = 3):

    if isinstance(value, float) or isinstance(value, np.ndarray):
        val = np.round(value, round_places)
    else:
        val = value

    return f"|{key}| = {val}"
