import pandas as pd
import numpy as np
import os

def remove_file(file_path: str):
    try:
        os.remove(file_path)
    except:
        pass

def datadict_to_csv(datadict: dict[str, np.array], file_path: str):
    df = pd.DataFrame.from_dict(datadict)
    df.to_csv(file_path, index=False)

def csv_to_datadict(file_path: str) -> dict[str, np.array]:
    df = pd.read_csv(file_path)

    dict = {}
    for key in df:
        dict[key] = df[key].to_numpy()

    return dict

def to_file(string: str, file_path: str):
    with open(file_path, 'w') as f:
        f.write(string)