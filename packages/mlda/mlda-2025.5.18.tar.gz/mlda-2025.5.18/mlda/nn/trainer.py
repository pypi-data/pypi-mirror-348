import os
import lightning as L
from .. import utils

class Trainer(L.Trainer):
    def __init__(self, log_dirpath='./logs', name='MLDA', accelerator='gpu', min_epochs=1, max_epochs=1000):
        utils.p_header(f'Name: {name}')

        early_stop = L.pytorch.callbacks.early_stopping.EarlyStopping(
            monitor='valid_loss',  # Metric to monitor
            patience=10,          # Wait 3 epochs without improvement
            mode='min',          # Minimize the monitored metric (e.g., loss)
            verbose=True,        # Log when training stops
            min_delta=0.001      # Optional: Minimum change to qualify as improvement
        )

        ckpt_callback = L.pytorch.callbacks.ModelCheckpoint(
            dirpath=log_dirpath, filename=name,
        )

        # Remove the checkpoint file if it exists
        self.ckpt_fpath = os.path.join(log_dirpath, f'{name}.ckpt')
        utils.p_header(f'Checkpoint path: {os.path.abspath(self.ckpt_fpath)}')

        if os.path.exists(self.ckpt_fpath):
            os.remove(self.ckpt_fpath)
        else:
            pass

        super().__init__(
            accelerator=accelerator, devices=1, strategy='auto',
            min_epochs=min_epochs, max_epochs=max_epochs,
            default_root_dir=log_dirpath, callbacks=[early_stop, ckpt_callback]
        )