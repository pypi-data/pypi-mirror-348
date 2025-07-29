import torch
from torch import nn
import torch.nn.functional as F

class AdvLinear(nn.Module):
    def __init__(self, in_features, out_features, bias=True, dtype=torch.float32):
        super(AdvLinear, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.exponents = nn.Parameter(torch.ones(in_features, dtype=dtype))
        self.lin = nn.Linear(in_features, out_features, bias=bias, dtype=dtype)

    def forward(self, x):
        x = x ** self.exponents
        return self.lin(x)

class ActiveLinear(nn.Module):
    def __init__(self, in_features, out_features, active_params: int | None = None, inputs_per_active_param: int | None = None, bias=True, dtype=torch.float32):
        super(ActiveLinear, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        if self.active_params is None:
            self.active_params = in_features
        else:
            self.active_params = active_params

        # Set minimum and maximum bounds for inputs_per_active_param
        min_inputs = 1
        max_inputs = min(100, self.in_features)  # Cap at 100 or in_features, whichever is smaller
        
        if inputs_per_active_param is None:
            self.inputs_per_active_param = nn.Parameter(torch.tensor([1.0]), dtype=torch.int32, requires_grad=True)
        else:
            # Validate and clamp the input value
            clamped_value = max(min_inputs, min(inputs_per_active_param, max_inputs))
            if clamped_value != inputs_per_active_param:
                print(f"Warning: inputs_per_active_param clamped from {inputs_per_active_param} to {clamped_value}")
            self.inputs_per_active_param = nn.Parameter(torch.tensor([clamped_value]), dtype=torch.int32, requires_grad=False)

        self.normal_lin = nn.Linear(in_features, out_features - self.active_params, bias=bias, dtype=dtype)
        self.active_lin = nn.Linear(self.inputs_per_active_param, self.active_params, bias=bias, dtype=dtype)

    def forward(self, x):
        normal = self.normal_lin(x[:, :self.in_features - self.active_params])
        active = self.active_lin(x[:, self.in_features - self.active_params:])
        return torch.cat([normal, active], dim=1)
