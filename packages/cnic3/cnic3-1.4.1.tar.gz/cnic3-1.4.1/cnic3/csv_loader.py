import csv
import pandas as pd


def load_data():
    train_csv = pd.read_csv('train_data.py')
    train_parquet = pd.read_parquet('2.py')
    test = pd.read_csv('test_data.csv')
    train_new1 = pd.read_csv('3.py')
    train_new2 = pd.read_csv('1.py')
    return train_csv, train_parquet, train_new1, train_new2, test


def filter_and_align_data(train_csv, *datasets):
    valid_categories = set(train_csv['attack_cat'].dropna().unique())
    filtered = [df[df['attack_cat'].isin(valid_categories)] for df in datasets]
    common_cols = list(set.intersection(*map(set, [train_csv.columns] + [df.columns for df in filtered])))
    aligned = [df[common_cols] for df in [train_csv] + filtered]
    return pd.concat(aligned, ignore_index=True), common_cols


def csv_loader(test_path, train_path):
    train_csv, train_parquet, train_new1, train_new2, test = load_data()
    train, _ = filter_and_align_data(train_csv, train_parquet, train_new1, train_new2)
    return test, train
