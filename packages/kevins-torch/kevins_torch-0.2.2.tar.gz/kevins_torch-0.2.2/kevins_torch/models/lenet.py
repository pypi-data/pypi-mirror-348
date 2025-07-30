import torch
import torch.nn as nn

from kevins_torch.utils.logger_config import setup_logger
from kevins_torch.models.base import BaseModel

# 設置 logger
logger = setup_logger(__name__)


class LeNetModel(BaseModel):
    """LeNet-5 卷積神經網絡模型。

    這個類實現了 LeNet-5 架構，適用於圖像分類任務。

    Args:
        num_classes: 輸出類別數量，默認為10
    """
    def __init__(self, num_classes: int = 10) -> None:
        super().__init__()
        logger.debug(f"初始化 LeNet 模型，類別數: {num_classes}")
        
        self.features = nn.Sequential(
            nn.Conv2d(3, 6, kernel_size=5),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(6, 16, kernel_size=5),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        
        self.classifier = nn.Sequential(
            nn.Linear(16 * 5 * 5, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, num_classes),
        )

    def _prepare_input(self, x: torch.Tensor, device: torch.device) -> torch.Tensor:
        """準備模型輸入。

        Args:
            x: 輸入張量
            device: 目標設備

        Returns:
            torch.Tensor: 準備好的輸入張量
        """
        return x.to(device)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """前向傳播。

        Args:
            x: 輸入張量，形狀為 [batch_size, 3, 32, 32]

        Returns:
            torch.Tensor: 輸出張量，形狀為 [batch_size, num_classes]
        """
        logger.debug(f"輸入張量形狀: {x.shape}")
        x = self.features(x)
        logger.debug(f"特徵提取後形狀: {x.shape}")
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        logger.debug(f"分類後形狀: {x.shape}")
        return x

    def predict(self, x: torch.Tensor) -> int:
        """預測單個輸入的類別。

        Args:
            x: 輸入張量，形狀為 [1, 3, 32, 32]

        Returns:
            int: 預測的類別索引
        """
        self.eval()  # 設置為評估模式
        with torch.no_grad():
            output = self(x)
            _, predicted = output.max(1)
            return predicted.item()
        self.train()  # 恢復為訓練模式
