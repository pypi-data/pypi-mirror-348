import re
from typing import Any, override

import torch.nn as nn
from torch import Tensor

from .base import Connector


class MLPConnector(Connector):
    ACTIVATION_MAP: dict[str, type[nn.Module]] = {
        "relu": nn.ReLU,
        "gelu": nn.GELU,
        "silu": nn.SiLU,
        "tanh": nn.Tanh,
        "sigmoid": nn.Sigmoid,
    }

    @override
    def __init__(
        self,
        config: Any,
        image_hidden_size: int,
        text_hidden_size: int,
    ) -> None:
        self.num_layers: int = 2
        self.activation_name: str = "gelu"

        self._parse_config_name(config.name)

        super().__init__(config, image_hidden_size, text_hidden_size)

    def _parse_config_name(self, name: str) -> None:
        pattern = r"mlp_(\d+)_(\w+)"
        match = re.match(pattern, name)

        if match:
            self.num_layers = int(match.group(1))
            self.activation_name = match.group(2)

    @override
    def _build_projection_layer(self) -> nn.Module:
        if self.num_layers < 1:
            raise ValueError(f"Number of layers must be at least 1, got {self.num_layers}")

        activation_class = self.ACTIVATION_MAP.get(self.activation_name)
        if activation_class is None:
            raise ValueError(
                f"Unsupported activation: {self.activation_name}.\nSupported activations: {list(self.ACTIVATION_MAP.keys())}"
            )

        layers: list[Any] = []
        for i in range(self.num_layers):
            if i == 0:
                layers.append(nn.Linear(self.image_hidden_size, self.text_hidden_size))
            else:
                layers.append(nn.Linear(self.text_hidden_size, self.text_hidden_size))

            if i < self.num_layers - 1:
                layers.append(activation_class())

        return nn.Sequential(*layers)

    @override
    def projection(self, visual_features: Tensor) -> Tensor:
        return self.projection_layer(visual_features)
