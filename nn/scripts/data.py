import torch
from torch.utils.data import TensorDataset, random_split
from torch.utils.data.dataset import Subset
import pandas as pd
from sklearn.preprocessing import StandardScaler


def standardize(src: pd.DataFrame) -> pd.DataFrame:
    scaler = StandardScaler()
    stand_data = scaler.fit_transform(src)
    return pd.DataFrame(stand_data, columns=src.columns)


def get_tensor_dataset_from_csv(path: str, data_portion: float = 1, standardize_data: bool = True) -> TensorDataset:
    """
    Loads .csv file into TensorDataset. Assumes target results are in the last column.
    :param standardize_data: if additionally standardize data (excluding last column)
    :param data_portion: portion of data. at least one datapoint is always returned
    :param path: path to csv file
    :return: TensorDataset from csv file
    """
    raw_data = pd.read_csv(path, delimiter=';')

    raw_sample = raw_data.sample(frac=data_portion, random_state=123)
    if len(raw_sample) == 0:
        raw_sample = raw_data.sample(n=1, random_state=123)

    features = raw_sample.iloc[:, :-1]
    if standardize_data:
        features = standardize(features)
    features = features.to_numpy()
    target = raw_sample.iloc[:, -1].to_numpy()

    return TensorDataset(torch.tensor(features).float(), torch.tensor(target).float())


def split_data(data: TensorDataset, train: float, val: float, test: float) -> list[torch.utils.data.dataset.Subset]:
    """
    Splits dataset into train, val and test.
    :param data: dataset
    :param train: portion of train data
    :param val: portion of val data
    :param test: portion of test data
    :return: list of subsets [train, val, test]
    """
    if train + val + test != 1 or (test < 0 or val < 0 or test < 0):
        raise Exception("Split destinations are incorrect")

    data_len = len(data)
    train_len = int(train * data_len)
    val_len = int(val * data_len)
    test_len = data_len - train_len - val_len

    return random_split(data, [train_len, val_len, test_len])


def get_divided_dataset(path: str, train_frac: float, val_frac, test_frac: float,
                        data_portion: float = 1) -> (Subset, Subset, Subset, TensorDataset):
    """
    Creates train, val and test tensor datasets from csv file.
    Assumes target results are in the last column.
    :param path: path of .csv file
    :param test_frac: amount of test data
    :param val_frac: amount of validate data
    :param train_frac: amount of train data
    :param data_portion: portion of data
    :return: List of subsets and full dataset
    """
    dataset = get_tensor_dataset_from_csv(path, data_portion)
    train, val, test = split_data(dataset, train_frac, val_frac, test_frac)
    return train, val, test, dataset



