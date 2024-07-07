from typing import Callable

import torch
import torchmetrics
from torch import nn, optim
from torch.utils.data import DataLoader
from torchmetrics.classification import BinaryAccuracy

# TODO: add normalization step
# TODO: try Adam optimizer
# TODO: add learning rate scheduler

# TODO: add check for class imbalance
# TODO: normalize data in .csv
# TODO: monitor gradients during training (exploading, vanishing)

class SequentialModel:
    def __init__(self,
                 n_in: int) -> None:
        self.criterion = nn.BCELoss()
        self.epochs_per_validate = 3
        self.model = nn.Sequential(
            nn.Linear(n_in, 50).cuda(),
            nn.LeakyReLU().cuda(),
            nn.Linear(50, 70).cuda(),
            nn.LeakyReLU().cuda(),
            nn.Linear(70, 20).cuda(),
            nn.LeakyReLU().cuda(),
            nn.Linear(20, 1).cuda(),
            nn.Sigmoid().cuda()
        )
        self.optimizer = optim.SGD(
            self.model.parameters(),
            lr=0.001,
            momentum=0.95)

    def validate(self, val_loader: DataLoader) -> (float, float):
        val_loss = 0.0
        val_acc = 0.0
        acc_metric = BinaryAccuracy().cuda()
        self.model.eval()

        with torch.no_grad():
            for features, targets in val_loader:
                features, targets = features.cuda(), targets.cuda()
                prediction = self.model(features).squeeze()

                loss = self.criterion(prediction, targets)
                acc = acc_metric(prediction, targets)
                val_loss += loss.item()
                val_acc += acc.item()

        self.model.train()
        return val_loss/len(val_loader), val_acc/len(val_loader)

    def train(self, train_loader: DataLoader, epochs: int, lr: float, momentum: float,
              epochs_per_val: int, val_loader: DataLoader) -> None:
        val_counter = epochs_per_val
        self.optimizer = optim.SGD(self.model.parameters(), lr=lr, momentum=momentum)
        acc_metric = BinaryAccuracy().cuda()
        val_loss, val_acc = 0.0, 0.0

        for epoch in range(epochs):
            train_loss, train_acc = 0.0, 0.0
            val_counter += 1

            for features, targets in train_loader:
                features, targets = features.cuda(), targets.cuda()

                self.optimizer.zero_grad()

                prediction = self.model(features).squeeze()
                loss = self.criterion(prediction, targets)
                loss.backward()
                self.optimizer.step()

                acc = acc_metric(prediction, targets)

                train_loss += loss
                train_acc += acc

            if val_counter >= epochs_per_val and val_loader is not None:
                val_loss, val_acc = self.validate(val_loader)
                val_counter = 0

            train_loss = train_loss/len(train_loader)
            train_acc = train_acc/len(train_loader)
            print(f'==========Epoch {epoch + 1}==========')
            print(f'Train: loss={train_loss:5f}, acc={train_acc:5f}')
            print(f'Valid: loss={val_loss:5f}, acc={val_acc:5f}')

        print('Training done')

    def test(self, test_loader):
        return self.validate(test_loader)

    def predict(self, features) -> int:
        self.model.eval()
        with torch.no_grad():
            pred = self.model(features).squeeze()
        self.model.train()
        if pred > 0.5:
            return 1
        return 0

