import keras
import warnings
import numpy as np


class TensorBoard(keras.callbacks.TensorBoard):

    def _log_weights(self, epoch):
        with self._train_writer.as_default():
            for layer in self.model.layers:
                for weight in layer.weights:
                    # Use weight.path istead of weight.name to distinguish
                    # weights of different layers.
                    histogram_weight_name = weight.path + "/histogram"
                    self.summary.histogram(
                        histogram_weight_name, weight, step=epoch
                    )
                    if self.write_images:
                        image_weight_name = weight.path + "/image"
                        self._log_weight_as_image(
                            weight, image_weight_name, epoch
                        )
            self._train_writer.flush()


class LearningRateDecay(keras.callbacks.LearningRateScheduler):

    def __init__(self, rate: float, delay: int = 0, **kwargs):

        def lr_schedule(epoch: int, lr: float):
            if epoch < delay:
                return float(lr)
            return float(lr * keras.ops.exp(-rate))
        
        super().__init__(schedule=lr_schedule, **kwargs)


class Rollback(keras.callbacks.Callback):

    def __init__(
        self, 
        frequency: int = None,
        tolerance: float = 0.5, 
        rollback_optimizer: bool = True,
    ):
        super().__init__()
        self.frequency = frequency or 1_000_000_000
        self.tolerance = tolerance
        self.rollback_optimizer = rollback_optimizer

    def on_train_begin(self, logs=None):
        self.rollback_weights = self._get_model_vars()
        self.rollback_optimizer_vars = self._get_optimizer_vars()
        self.rollback_loss = float('inf')

    def on_epoch_end(self, epoch: int, logs: dict = None):
        current_loss = logs.get('val_loss', logs.get('loss'))
        deviation = (current_loss - self.rollback_loss) / self.rollback_loss

        if np.isnan(current_loss) or np.isinf(current_loss):
            self._rollback()
            print("\nRolling back model, found nan or inf loss.\n")
            return 
        
        if deviation > self.tolerance:
            self._rollback()
            print(f"\nRolling back model, found too large deviation: {deviation:.3f}\n")
        
        if epoch and epoch % self.frequency == 0:
            self._rollback()
            print(f"\nRolling back model, {epoch} % {self.frequency} == 0\n")
            return 
        
        if current_loss < self.rollback_loss:
            self._save_state(current_loss)

    def _save_state(self, current_loss: float) -> None:
        self.rollback_loss = current_loss
        self.rollback_weights = self._get_model_vars()
        if self.rollback_optimizer:
            self.rollback_optimizer_vars = self._get_optimizer_vars()

    def _rollback(self) -> None:
        self.model.set_weights(self.rollback_weights)
        if self.rollback_optimizer:
            self.model.optimizer.set_weights(self.rollback_optimizer_vars)

    def _get_optimizer_vars(self):
        return [v.numpy() for v in self.model.optimizer.variables]
    
    def _get_model_vars(self):
        return self.model.get_weights()
    