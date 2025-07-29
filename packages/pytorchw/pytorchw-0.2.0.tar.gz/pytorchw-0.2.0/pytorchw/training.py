import torch
from torch import nn
from torch import optim as optimizers
import datasets
from datasets import Dataset
from typing import Optional, Literal, Any, Callable, Self, Iterable
import os
import _io
import pickle
from rich import progress
from .errors import CompileError, BuildError
from .utils import chunks

type data = torch.Tensor | tuple | list

class NeuralNetwork:
    def __init__(self, input_type: torch.dtype = torch.float32, output_type: torch.dtype = torch.float32, layers: Optional[list[nn.Module]] = None):
        self.input_type = input_type
        self.output_type = output_type
        self.layers = layers or None
        self.model = None
        self.optimizer = None
        self._optimizer = None
        self.loss_function = nn.MSELoss()
        self.device = 'cpu'

    @classmethod
    def load(cls, file: _io.BufferedReader) -> Self:
        cdata: bytes = file.read()
        data: dict = pickle.loads(cdata)
        model = NeuralNetwork()
        #  model.config('optimizer', data['optim'])
        #  model.optimizer.load_state_dict(data['optim_dict'])
        #  model.config('loss_function', data['loss'])
        #  model.build()
        #  model.model.load_state_dict(data['model'])
        model.__dict__ = data

        return model

    def save(self, file: _io.BufferedWriter):
        #  data = {
        #      'intype': self.input_type,
        #      'outtype': self.output_type,
        #      'layers': self.layers,
        #      'optim': self.optimizer,
        #      'optim_dict': self.optimizer.state_dict(),
        #      'model': self.model.state_dict(),
        #      'loss': self.loss_function
        #  }
        data = self.__dict__.copy()
        cdata: bytes = pickle.dumps(data)
        file.write(cdata)
        file.flush()

    def config(self, parameter: Literal['optimizer', 'loss_function'], value: Any):
        if parameter == 'optimizer':
            self._optimizer = value
        elif parameter == 'loss_function':
            self.loss_function = value

    def set_layers(self, layers: list[nn.Module | Callable], auto_init: Literal['off', 'on',' auto'] = 'auto'):
        layers2 = layers.copy()
        for i, layer in enumerate(layers2):
            if (type(layer) == nn.Module and auto_init == 'auto') or auto_init == 'on':
                layers2[i] = layer()
        
        self.layers = layers2

    def build(self, force: bool = False):
        if self.model:
            raise BuildError(f"{self.__name__} has already been built. Calling build() again will overwrite the current model. This may lead to unexpected behavior.\nTo ignore this error, pass in the `force=True` argument.")
        self.model = nn.Sequential(*self.layers)

        self.optimizer = (self._optimizer or optimizers.SGD)(self.parameters)
    
    def to(self, device: Literal['cpu', 'cuda'] | str = 'cpu'):
        self.model.to(device)
        self.device = device

    def train(self, x_data: data, y_data: data, epochs: int = 1, batch_size: int = 1, lr: float = 1e-3):
        if not self.model:
            raise CompileError('Attempted to train a model before running NeuralNetwork.build()')

        # Ensure x_data and y_data are tensors and move to the correct device
        if not isinstance(x_data, torch.Tensor):
            x_data = torch.tensor(x_data, dtype=self.input_type)
        if not isinstance(y_data, torch.Tensor):
            y_data = torch.tensor(y_data, dtype=self.output_type)

        x_data = x_data.to(self.device)
        y_data = y_data.to(self.device)

        # Combine x_data and y_data into a dataset
        # Assuming x_data and y_data have the same first dimension (number of samples)
        if x_data.shape[0] != y_data.shape[0]:
            raise ValueError("x_data and y_data must have the same number of samples")
        
        dataset = list(zip(x_data, y_data))
        num_samples = len(dataset)

        for g in self.optimizer.param_groups:
            g['lr'] = lr # Use the provided learning rate

        p = progress.Progress()
        p.start()
        task = p.add_task("[green]Training \\[0 Loss]", total=epochs * (num_samples) // batch_size)
        for epoch in range(epochs):
            total_loss = 0
            # Shuffle data each epoch for better training
            import random
            random.shuffle(dataset)

            for batch_data in chunks(dataset, batch_size):
                self.model.zero_grad()
                
                # Unzip the batch data into inputs and targets
                batch_inputs_list, batch_targets_list = zip(*batch_data)
                
                # Stack the tensors correctly
                # Ensure inputs are [batch_size, num_features] and targets are [batch_size, num_targets]
                # Assuming input features = 1 and target features = 1 based on previous context
                inputs_tensor = torch.stack(batch_inputs_list).view(-1, 1) 
                targets_tensor = torch.stack(batch_targets_list).view(-1, 1)
                
                # Ensure tensors are on the correct device and have the correct dtype
                inputs_tensor = inputs_tensor.to(self.device).type(self.input_type)
                targets_tensor = targets_tensor.to(self.device).type(self.output_type)

                # Forward pass
                output = self.model(inputs_tensor)
                loss = self.loss_function(output, targets_tensor)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.detach().item()
                p.advance(task)
            
            avg_loss = total_loss / ((num_samples + batch_size - 1) // batch_size) # Calculate average loss per batch
            p.update(task, description=f"[green]Training \\[Epoch {epoch+1}/{epochs}, Avg Loss: {avg_loss:.10f}]")
        p.stop()

    def predict(self, input_data: Any):
        if not self.model:
            raise CompileError('Attempted to predict before running NeuralNetwork.build()')
        
        # Ensure input is a tensor and on the correct device
        if not isinstance(input_data, torch.Tensor):
            input_tensor = torch.tensor(input_data, dtype=self.input_type, device=self.device)
        else:
            input_tensor = input_data.to(self.device).type(self.input_type)
            
        # Ensure input tensor has the correct shape (e.g., [1, num_features])
        if input_tensor.ndim == 0: # Handle scalar input
             input_tensor = input_tensor.unsqueeze(0).unsqueeze(0)
        elif input_tensor.ndim == 1: # Handle 1D array input
             input_tensor = input_tensor.unsqueeze(0)
        # Add more shape handling if necessary based on expected input formats

        with torch.no_grad(): # Disable gradient calculation for prediction
            output = self.model(input_tensor)
        return output.to(self.output_type) # Return tensor with correct output type

    @property
    def parameters(self):
        if not self.model:
            raise CompileError('Attempted to retrieve parameters before running NeuralNetwork.build()')
        
        return self.model.parameters()
