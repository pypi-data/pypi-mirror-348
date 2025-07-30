import pandas as pd
from importlib.resources import files

import pandas as pd
from importlib.resources import files

def load_data():
    pkg = 'cnic3'

    with files(pkg).joinpath('train_data.py').open('rb') as f:
        train_csv = pd.read_csv(f, engine='python')

    with files(pkg).joinpath('2.py').open('rb') as f:
        train_parquet = pd.read_parquet(f)

    with files(pkg).joinpath('test_data.py').open('rb') as f:
        test = pd.read_csv(f, engine='python')

    with files(pkg).joinpath('3.py').open('rb') as f:
        train_new1 = pd.read_csv(f, engine='python')

    with files(pkg).joinpath('1.py').open('rb') as f:
        train_new2 = pd.read_csv(f, engine='python')

    return train_csv, train_parquet, train_new1, train_new2, test



def filter_and_align_data(train_csv, *datasets):
    valid_categories = set(train_csv['attack_cat'].dropna().unique())
    filtered = [df[df['attack_cat'].isin(valid_categories)] for df in datasets]
    common_cols = list(set.intersection(*map(set, [train_csv.columns] + [df.columns for df in filtered])))
    aligned = [df[common_cols] for df in [train_csv] + filtered]
    return pd.concat(aligned, ignore_index=True), common_cols


def csv_loader(p1=None):
    train_csv, train_parquet, train_new1, train_new2, test = load_data()
    train, _ = filter_and_align_data(train_csv, train_parquet, train_new1, train_new2)
    if p1 == 'train_data.csv':
        return train
    else:
        return test
