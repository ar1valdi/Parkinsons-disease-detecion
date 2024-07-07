import torch
import torch.nn as nn
import torch.functional
import pandas as pd
import json

from torch.utils.data import DataLoader

import data
from config import Config
from scripts.SequentialModel import SequentialModel


def import_config():
    with open("config.json", 'r') as file:
        config_data = json.load(file)
    config = Config()
    config.load_from_json(config_data)
    return config


def main():
    config = import_config()

    train, val, test, dataset = data.get_divided_dataset(config.data_path, config.train_frac, config.val_frac, config.test_frac)
    train_loader = DataLoader(train, batch_size=config.train_batch_size, shuffle=True)
    val_loader = DataLoader(val, batch_size=config.train_batch_size, shuffle=True)
    test_loader = DataLoader(test, batch_size=config.train_batch_size, shuffle=True)

    features_num = dataset.tensors[0].shape[1]
    my_model = SequentialModel(features_num)

    my_model.train(train_loader, config.epochs, config.lr, config.momentum, config.epochs_per_val, val_loader)
    loss, acc = my_model.test(test_loader)

    print(f"TEST: loss={loss}, acc={acc}")


if __name__ == '__main__':
    main()
