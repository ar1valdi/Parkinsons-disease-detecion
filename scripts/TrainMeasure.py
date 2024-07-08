import matplotlib.pyplot as plt


class TrainMeasure:
    def __init__(self):
        self.val_acc = 0.0
        self.val_loss = 0.0
        self.train_acc = 0.0
        self.train_loss = 0.0

        self.rem_val_loss = []
        self.rem_val_acc = []
        self.rem_train_loss = []
        self.rem_train_acc = []

    def save_data(self) -> None:
        self.rem_val_loss.append(self.val_loss)
        self.rem_val_acc.append(self.val_acc)
        self.rem_train_loss.append(self.train_loss)
        self.rem_train_acc.append(self.train_acc)

    def reset(self) -> None:
        self.__init__()

    def prepare_figure(self, custom_title: str = None) -> None:
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(self.rem_train_loss, label="train")
        plt.plot(self.rem_val_loss, label="validate")
        plt.title("Loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.ylim(bottom=0)
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(self.rem_train_acc, label="train")
        plt.plot(self.rem_val_acc, label="validate")
        plt.title("Accuracy")
        plt.xlabel("Epoch")
        plt.ylabel("Accuracy")
        plt.legend()
        plt.subplots_adjust(hspace=0.5)
        plt.ylim(bottom=0, top=1)

        if custom_title is not None:
            plt.suptitle(custom_title)

    def plot(self, custom_title: str = None):
        self.prepare_figure(custom_title)
        plt.show()
