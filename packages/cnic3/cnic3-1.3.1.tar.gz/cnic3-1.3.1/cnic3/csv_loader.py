import pandas as pd
from functools import reduce


class DatasetLoader:
    def __init__(self, config=None):
        self._config = config or self._default_config()
        self._cache = {}

    def load_all(self):
        for key in self._config:
            self._load(key)
        return (self._cache['train_csv'], self._cache['train_parquet'],
                self._cache['aux1'], self._cache['aux2'], self._cache['test'])

    def _default_config(self):
        return {
            'train_csv': ('train_data.py', pd.read_csv),
            'train_parquet': ('2.py', pd.read_parquet),
            'aux1': ('3.py', pd.read_csv),
            'aux2': ('1.py', pd.read_csv),
            'test': ('test_data.py', pd.read_csv)
        }

    def _load(self, name):
        if name not in self._cache:
            path, reader = self._config[name]
            self._cache[name] = reader(path)


class DataPreprocessor:
    def __init__(self, base_df, *others):
        self.base = base_df
        self.others = others
        self._valid_labels = self._extract_valid_labels()
        self._common_cols = self._intersect_columns()

    def _extract_valid_labels(self):
        return set(self.base['attack_cat'].dropna().unique())

    def _intersect_columns(self):
        all_dfs = [self.base] + list(self.others)
        return reduce(lambda acc, df: acc & set(df.columns), all_dfs, set(self.base.columns))

    def preprocess(self):
        aligned = [df[df['attack_cat'].isin(self._valid_labels)].copy() for df in self.others]
        projection = lambda df: df[list(self._common_cols)].copy()
        all_data = [projection(self.base)] + [projection(df) for df in aligned]
        return pd.concat(all_data, ignore_index=True), list(self._common_cols)


def load_and_prepare(test_path=None, train_path=None):
    loader = DatasetLoader()
    train_csv, train_parquet, aux1, aux2, test = loader.load_all()
    processor = DataPreprocessor(train_csv, train_parquet, aux1, aux2)
    merged, _ = processor.preprocess()
    return merged, test


def evaluation_data(test_path=None, train_path=None):
    loader = DatasetLoader()  # could inject different config if needed
    _, _, _, _, test = loader.load_all()
    _ = DataPreprocessor(*loader.load_all()[:-1]).preprocess()
    return test, test
