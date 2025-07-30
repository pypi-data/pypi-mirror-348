from typing import Sequence

import torch
import torch.nn as nn

from kevins_torch.utils.logger_config import setup_logger
from kevins_torch.models.base import BaseModel
from kevins_torch.models.utils import activation_function_parser

# 設置 logger
logger = setup_logger(__name__)


# 定義 CNN 模型結構
class CNNModel(BaseModel):
    def __init__(
        self,
        input_size: int = 64,
        num_classes: int = 100,
        hidden_layers: Sequence[int] = [256, 128, 64],
        activation_function: str = "LeakyReLU",
        dropout_rate: float = 0.1,
        conv_layers: Sequence[int] = [128, 256, 512, 512],
        using_batch_norm: bool = True,
    ):
        super(CNNModel, self).__init__()

        # 根據字符串選擇激活函數
        self.activation_function = activation_function_parser(activation_function)

        # 捲積層
        conv_sizes = conv_layers
        conv_layers_list = []
        prev_size = 3
        conv_layers_list.append(
            nn.Conv2d(prev_size, conv_sizes[0], kernel_size=3, stride=1, padding=1)
        )
        prev_size = conv_sizes[0]
        for i, conv_size in enumerate(conv_sizes):
            conv_layers_list.append(
                nn.Conv2d(prev_size, conv_size, kernel_size=3, stride=1, padding=1)
            )
            conv_layers_list.append(self.activation_function)
            if using_batch_norm:
                conv_layers_list.append(nn.BatchNorm2d(conv_size))
            conv_layers_list.append(nn.MaxPool2d(kernel_size=2, stride=2))
            prev_size = conv_size
            conv_layers_list.append(nn.Dropout(p=dropout_rate))
        self.conv_layers = nn.Sequential(*conv_layers_list)

        # 使用虛擬張量來計算卷積層的輸出大小
        with torch.no_grad():
            dummy_input = torch.zeros(1, 3, input_size, input_size)
            dummy_output = self.conv_layers(dummy_input)
            conv_output_size = dummy_output.view(1, -1).size(1)

        # 全連接層
        layers = []
        prev_size = conv_output_size

        # 添加隱藏層
        for i, hidden_size in enumerate(hidden_layers):
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(self.activation_function)
            if i < len(hidden_layers) - 1:
                layers.append(nn.Dropout(p=dropout_rate))
            if using_batch_norm:
                layers.append(nn.BatchNorm1d(hidden_size))
            prev_size = hidden_size

        # 添加輸出層
        layers.append(nn.Linear(prev_size, num_classes))

        self.fc_layers = nn.Sequential(*layers)

    def _prepare_input(self, x: torch.Tensor, device: torch.device) -> torch.Tensor:
        """準備模型輸入。

        Args:
            x: 輸入張量
            device: 目標設備

        Returns:
            torch.Tensor: 準備好的輸入張量
        """
        return x.to(device)

    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.fc_layers(x)
        return x

    def predict(self, x):
        """預測單個輸入的類別。

        Args:
            x: 輸入張量，形狀為 [1, 3, H, W]

        Returns:
            int: 預測的類別索引
        """
        self.eval()  # 設置為評估模式
        with torch.no_grad():
            output = self(x)
            _, predicted = output.max(1)
            return predicted.item()
        self.train()  # 恢復為訓練模式


if __name__ == "__main__":
    model = CNNModel()
    print(model)
