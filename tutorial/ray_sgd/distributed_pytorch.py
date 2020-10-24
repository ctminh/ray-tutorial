import torch
import torch.nn as nn
from torch.utils.data import DataLoader

import ray
from ray.util.sgd.torch import TrainingOperator
from ray.util.sgd.torch.examples.train_example import LinearDataset
from ray.util.sgd import TorchTrainer

class MyTrainingOperator(TrainingOperator):
    def setup(self, config):
        # setup all components needed for training here. This could include
        # data, models, optimizers, loss & schedulers.

        # setup data loader
        train_dataset, val_dataset = LinearDataset(2, 5), LinearDataset(2, 5)
        train_loader = DataLoader(train_dataset, batch_size=config["batch_size"])
        val_loader = DataLoader(val_dataset, batch_size=config["batch_size"])

        # setup model
        model = nn.Linear(1, 1)

        # setup optimizer
        optimizer = torch.optim.SGD(model.parameters(), lr=config.get("lr", 1e-4))

        # setup loss
        criterion = torch.nn.BCELoss()

        # setup scheduler
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.9)

        # Register all of these components with Ray SGD.
        # This allows Ray SGD to do framework level setup like Cuda, DDP,
        # Distributed Sampling, FP16.
        # We also assign the return values of self.register to instance
        # attributes so we can access it in our custom training/validation
        # methods.
        self.model, self.optimizer, self.criterion, self.scheduler = \
            self.register(models=model, optimizers=optimizer,
                          criterion=criterion,
                          schedulers=scheduler)

# init ray or ray.init(address="auto") to connect to a running cluster.      
ray.init()

# use TorchTrainer to package your model as a ray-object for moving around
trainer = TorchTrainer(
    training_operator_cls=MyTrainingOperator,
    scheduler_step_freq="epoch",  # if scheduler is used
    config={"lr": 0.001, "batch_size": 64},
    # num_workers=100,
    # use_gpu=True
    )

for i in range(10):
    metrics = trainer.train()
    val_metrics = trainer.validate()

