from copy import deepcopy

import numpy as np
import json
import matplotlib.pyplot as plt
import torch
from mpl_toolkits.mplot3d import Axes3D

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


def plot_lr_gamma_search_results(lrs_train, gammas_train, loss_train, acc_train, lrs_test, gammas_test, loss_test, acc_test):
    fig = plt.figure(figsize=(12, 10))

    # Train loss subplot
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    ax1.plot_trisurf(lrs_train, gammas_train, loss_train, cmap='viridis', linewidth=0.2)
    ax1.set_title("Train Loss")
    ax1.set_xlabel('Learning Rate')
    ax1.set_ylabel('Gamma')
    ax1.set_zlabel('Loss')
    ax1.legend(['Loss'])

    # Train accuracy subplot
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    ax2.plot_trisurf(lrs_train, gammas_train, acc_train, cmap='viridis', linewidth=0.2)
    ax2.set_title("Train Accuracy")
    ax2.set_xlabel('Learning Rate')
    ax2.set_ylabel('Gamma')
    ax2.set_zlabel('Accuracy')
    ax2.legend(['Accuracy'])

    # Test loss subplot
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    ax3.plot_trisurf(lrs_test, gammas_test, loss_test, cmap='viridis', linewidth=0.2)
    ax3.set_title("Test Loss")
    ax3.set_xlabel('Learning Rate')
    ax3.set_ylabel('Gamma')
    ax3.set_zlabel('Loss')
    ax3.legend(['Loss'])

    # Test accuracy subplot
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    ax4.plot_trisurf(lrs_test, gammas_test, acc_test, cmap='viridis', linewidth=0.2)
    ax4.set_title("Test Accuracy")
    ax4.set_xlabel('Learning Rate')
    ax4.set_ylabel('Gamma')
    ax4.set_zlabel('Accuracy')
    ax4.legend(['Accuracy'])

    plt.tight_layout()
    plt.show()


def look_for_lr_and_gamma(lr_start, lr_end, lr_amount, gamma_start, gamma_end, gamma_amount,
                          my_model, config, train_loader, val_loader, test_loader):
    train_rem = []
    test_rem = []
    progress_done = 0
    all_iters = lr_amount * gamma_amount
    lrs = np.linspace(lr_start, lr_end, lr_amount)
    gammas = np.linspace(gamma_start, gamma_end, gamma_amount)

    print(f"Checking lrs={lrs}")
    print(f"Checking gammas={gammas}")

    for i in range(len(lrs)):
        curr_lr = lrs[i]
        for j in range(len(gammas)):
            curr_gamma = gammas[j]
            train_res = my_model.train(train_loader,
                                       config.epochs,
                                       curr_lr,
                                       config.scheduler_step_size,
                                       curr_gamma,
                                       config.epochs_per_val,
                                       val_loader,
                                       log_progress=False,
                                       plot_results=False)
            progress_done += 1
            print(f"Trained lr={curr_lr:7f}, gamma = {curr_gamma:.7f}, done {progress_done}/{all_iters}")
            test_res = my_model.test(test_loader, log_results=True)
            train_rem.append([curr_lr, curr_gamma, train_res.train_loss, train_res.train_acc])
            test_rem.append([curr_lr, curr_gamma, test_res[0], test_res[1]])

    # [id][lr, gamma, loss, acc]
    min_train_lr = test_rem[0][0]
    min_train_gamma = test_rem[0][1]
    min_train_loss = train_rem[0][2]
    min_train_loss_acc = train_rem[0][3]
    min_test_lr = test_rem[0][0]
    min_test_gamma = test_rem[0][1]
    min_test_loss = test_rem[0][2]
    min_test_loss_acc = test_rem[0][3]

    for i in range(len(test_rem)):
        t = test_rem[i]
        m = train_rem[i]
        print(f'========= lr={t[0]:.7f}, gamma={t[1]:.7f} =========')
        print(f'train : loss={m[2]:.7f}, acc={m[3]:.7f}')
        print(f'test  : loss={t[2]:.7f}, acc={t[3]:.7f}')
        if t[2] < min_test_loss:
            min_test_lr = t[0]
            min_test_gamma = t[1]
            min_test_loss = t[2]
            min_test_loss_acc = t[3]
        if m[2] < min_train_loss:
            min_train_lr = m[0]
            min_train_gamma = m[1]
            min_train_loss = m[2]
            min_train_loss_acc = m[3]

    print(f"min train loss: lr={min_train_lr}, gamma={min_train_gamma}, loss={min_train_loss}, acc={min_train_loss_acc}")
    print(f"min test loss : lr={min_test_lr}, gamma={min_test_gamma}, loss={min_test_loss}, acc={min_test_loss_acc}")

    train_rem = np.array(train_rem)
    test_rem = np.array(test_rem)

    lrs_train = train_rem[:, 0]
    gammas_train = train_rem[:, 1]
    loss_train = train_rem[:, 2]
    acc_train = train_rem[:, 3]
    lrs_test = test_rem[:, 0]
    gammas_test = test_rem[:, 1]
    loss_test = test_rem[:, 2]
    acc_test = test_rem[:, 3]

    plot_lr_gamma_search_results(lrs_train, gammas_train, loss_train, acc_train, lrs_test, gammas_test, loss_test, acc_test)


def training_with_one_datapoint(train, val, test, config, dataset):
    for i in range(20):
        train_one = deepcopy(train)
        train_one.indices = train_one.indices[i:i + 1]
        train_loader = DataLoader(train_one, batch_size=config.train_batch_size, shuffle=True)
        val_loader = DataLoader(val, batch_size=config.train_batch_size, shuffle=True)
        test_loader = DataLoader(test, batch_size=config.train_batch_size, shuffle=True)

        features_num = dataset.tensors[0].shape[1]
        my_model = SequentialModel(features_num)

        m = my_model.train(train_loader,
                           config.epochs,
                           config.lr,
                           config.scheduler_step_size,
                           config.scheduler_gamma,
                           config.epochs_per_val,
                           val_loader,
                           log_progress=False,
                           plot_results=False)
        print(f'{i}: train_loss={m.train_loss}')
        my_model.test(test_loader, log_results=False)


def main():
    config = import_config()

    train, val, test, dataset = data.get_divided_dataset(config.data_path,
                                                         config.train_frac,
                                                         config.val_frac,
                                                         config.test_frac,
                                                         config.data_portion)

    train_loader = DataLoader(train, batch_size=config.train_batch_size, shuffle=True)
    val_loader = DataLoader(val, batch_size=config.train_batch_size, shuffle=True)
    test_loader = DataLoader(test, batch_size=config.train_batch_size, shuffle=True)

    features_num = dataset.tensors[0].shape[1]
    my_model = SequentialModel(features_num)

    m = my_model.train(train_loader,
                       config.epochs,
                       config.lr,
                       config.scheduler_step_size,
                       config.scheduler_gamma,
                       config.epochs_per_val,
                       val_loader,
                       log_progress=True,
                       plot_results=False)
    my_model.test(test_loader, log_results=True)
    m.plot()
    torch.save(my_model.model.state_dict(), 'model.pt')

    # look_for_lr_and_gamma(0.01,
    #                       0.06,
    #                       51,
    #                       0.1,
    #                       0.1,
    #                       1,
    #                       my_model, config, train_loader, val_loader, test_loader)


if __name__ == '__main__':
    main()
