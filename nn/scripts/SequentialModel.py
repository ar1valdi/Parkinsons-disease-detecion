import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from torchmetrics.classification import BinaryAccuracy
import matplotlib.pyplot as plt
import numpy as np

from scripts.TrainMeasure import TrainMeasure


def _log_train_progress(epoch: int, measure: TrainMeasure) -> None:
    print(f'==========Epoch {epoch + 1}==========')
    print(f'Train: loss={measure.train_loss:5f}, acc={measure.train_acc:5f}')
    print(f'Valid: loss={measure.val_loss:5f}, acc={measure.val_acc:5f}')


class SequentialModel(nn.Module):
    def __init__(self,
                 n_in: int) -> None:
        super(SequentialModel, self).__init__()
        self.criterion = nn.BCELoss()
        self.epochs_per_validate = 3
        self.model = nn.Sequential(
            nn.Linear(n_in, 10),#.cuda(),
            nn.LeakyReLU(),#.cuda(),
            nn.Dropout(p=0.2),
            nn.Linear(10, 1),#.cuda(),
            nn.Sigmoid()#.cuda()
        )#.cuda()

    def validate(self, val_loader: DataLoader) -> (float, float):
        val_loss = 0.0
        val_acc = 0.0
        acc_metric = BinaryAccuracy()#.cuda()
        self.model.eval()

        with torch.no_grad():
            for features, targets in val_loader:
                features, targets = features, targets
                prediction = self.model(features).squeeze()

                loss = self.criterion(prediction, targets)
                acc = acc_metric(prediction, targets)
                val_loss += loss.item()
                val_acc += acc.item()

        self.model.train()
        return val_loss / len(val_loader), val_acc / len(val_loader)

    def train(self, train_loader: DataLoader, epochs: int, lr: float, sc_step_size: int,
              sc_gamma: float, epochs_per_val: int, val_loader: DataLoader,
              log_progress: bool = False, plot_results: bool = True) -> TrainMeasure:
        val_counter = epochs_per_val
        acc_metric = BinaryAccuracy()#.cuda()
        measure = TrainMeasure()

        optimizer = optim.Adam(self.model.parameters(), lr=lr)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=sc_step_size, gamma=sc_gamma)

        for epoch in range(epochs):
            epoch_loss, epoch_acc = 0.0, 0.0

            # training epoch
            for features, targets in train_loader:
                features, targets = features, targets

                optimizer.zero_grad()
                prediction = self.model(features).squeeze(dim=1)
                loss = self.criterion(prediction, targets)
                acc = acc_metric(prediction, targets)
                loss.backward()
                optimizer.step()

                epoch_loss += loss.item()
                epoch_acc += acc.item()

            scheduler.step()

            # validation
            val_counter += 1
            if val_counter >= epochs_per_val and val_loader is not None:
                measure.val_loss, measure.val_acc = self.validate(val_loader)
                val_counter = 0

            # measures
            measure.train_loss = epoch_loss / len(train_loader)
            measure.train_acc = epoch_acc / len(train_loader)
            measure.save_data()

            # logs
            if log_progress:
                _log_train_progress(epoch, measure)

        print('Training done')
        if plot_results:
            measure.plot()

        return measure

    def test(self, test_loader, log_results: bool = True):
        loss, acc = self.validate(test_loader)
        if log_results:
            print(f'TEST: loss={loss:.5f}, acc={acc:.5f}')
        return loss, acc

    def predict(self, features) -> (int, float):
        self.model.eval()
        with torch.no_grad():
            pred = self.model(features).squeeze()
        self.model.train()
        if pred > 0.5:
            return 1, pred
        return 0, 1 - pred

    def print_devices(self):
        for param in self.model.parameters():
            print(f'param: {param.device}')
