class Config:
    def __init__(self):
        self.data_path = ""
        self.train_batch_size = 0
        self.val_batch_size = 0
        self.test_batch_size = 0
        self.epochs = 0
        self.train_frac = 0
        self.val_frac = 0
        self.test_frac = 0
        self.lr = 0
        self.momentum = 0
        self.epochs_per_val = 0

    def load_from_json(self, json_dict: {str, object}) -> None:
        self.data_path = json_dict.get("data_path", "")
        self.train_batch_size = json_dict.get("train_batch_size", 32)
        self.val_batch_size = json_dict.get("val_batch_size", 32)
        self.test_batch_size = json_dict.get("test_batch_size", 32)
        self.train_frac = json_dict.get("train_frac", 0.8)
        self.val_frac = json_dict.get("val_frac", 0.1)
        self.test_frac = json_dict.get("test_frac", 0.1)
        self.lr = json_dict.get("lr", 0.001)
        self.momentum = json_dict.get("momentum", 0.95)
        self.epochs_per_val = json_dict.get("epochs_per_val", 3)
        self.epochs = json_dict.get("epochs", 3)
