import numpy as np

class HybridDataset:

    def __init__(self, datasets, weights, epoch_size=1000):
        self.datasets = datasets
        self.weights = weights
        self.epoch_size = epoch_size

    def __len__(self):
        return self.epoch_size

    def __getitem__(self, idx):
        choice = np.random.choice(len(self.datasets), p=self.weights)
        dataset = self.datasets[choice]
        choice = np.random.choice(len(dataset))
        return dataset[choice]
