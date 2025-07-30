import torch

class TestModel(torch.nn.Module):
    def forward(self, x):
        return x * 2
