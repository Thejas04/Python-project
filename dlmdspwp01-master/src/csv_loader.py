import pandas as pd
import os

from pandas.core.frame import DataFrame

CSV_PATH = '../data'

def load_csv(csv_file) -> DataFrame:
    file_path = os.path.join(os.getcwd(), CSV_PATH, csv_file)
    data = pd.read_csv(file_path)
    return data

if __name__ == '__main__':
    data = load_csv('test.csv')
    print(data)