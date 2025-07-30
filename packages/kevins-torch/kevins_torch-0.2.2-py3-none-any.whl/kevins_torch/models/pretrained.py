import torch
import torch.nn as nn
import torchvision.models as models

from kevins_torch.utils.logger_config import setup_logger
from kevins_torch.models.base import BasePretrainedModel

# 設置 logger
logger = setup_logger(__name__)

# 定義支持的模型類型
SUPPORTED_MODELS = {
    # ResNet 系列
    "resnet18": models.resnet18,
    "resnet34": models.resnet34,
    "resnet50": models.resnet50,
    "resnet101": models.resnet101,
    "resnet152": models.resnet152,
    "resnext50_32x4d": models.resnext50_32x4d,
    "resnext101_32x8d": models.resnext101_32x8d,
    "wide_resnet50_2": models.wide_resnet50_2,
    "wide_resnet101_2": models.wide_resnet101_2,
    # VGG 系列
    "vgg16": models.vgg16,
    "vgg19": models.vgg19,
}


class PretrainedModel(BasePretrainedModel):
    """通用的預訓練模型類。

    這個類封裝了各種預訓練的模型（如 ResNet、VGG 等），並允許微調最後幾層。

    Args:
        model_name: 模型名稱，可選值見 SUPPORTED_MODELS
        num_classes: 輸出類別數量
        weights: 預訓練權重類型，默認為 'DEFAULT'
        freeze_features: 是否凍結特徵提取層，默認為 True
        unfreeze_layers: 要解凍的層數，如果為 0 則保持所有特徵提取層凍結
    """

    def __init__(
        self,
        model_name: str = "resnet18",
        num_classes: int = 2,
        weights: str = "DEFAULT",
        freeze_features: bool = True,
        unfreeze_layers: int = 0,
    ) -> None:
        super().__init__()
        logger.debug(f"初始化 {model_name} 模型，類別數: {num_classes}")
        
        self.model_name = model_name

        if model_name not in SUPPORTED_MODELS:
            raise ValueError(
                f"不支持的模型名稱: {model_name}。"
                f"可用的模型: {list(SUPPORTED_MODELS.keys())}"
            )

        # 載入預訓練模型
        logger.debug(f"加載 {model_name} 模型")
        self.model = SUPPORTED_MODELS[model_name](weights=weights)

        # 修改最後一層以適應新的分類數量
        if hasattr(self.model, "fc"):  # ResNet 系列
            num_features = self.model.fc.in_features
            self.model.fc = nn.Linear(num_features, num_classes)
        elif hasattr(self.model, "classifier"):  # VGG 系列
            num_features = self.model.classifier[-1].in_features
            self.model.classifier[-1] = nn.Linear(num_features, num_classes)
        else:
            raise ValueError(f"不支持的模型架構: {model_name}")

        # 凍結特徵提取層
        if freeze_features:
            logger.debug("凍結特徵提取層參數")
            if hasattr(self.model, "features"):  # VGG 系列
                for param in self.model.features.parameters():
                    param.requires_grad = False
            elif hasattr(self.model, "layer1"):  # ResNet 系列
                layers = [
                    self.model.layer1,
                    self.model.layer2,
                    self.model.layer3,
                    self.model.layer4,
                ]
                for layer in layers:
                    for param in layer.parameters():
                        param.requires_grad = False
            else:
                raise ValueError(f"不支持的模型架構: {model_name}")

        # 解凍指定層數
        if unfreeze_layers > 0:
            self.unfreeze_features(unfreeze_layers)

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
            x: 輸入張量，形狀為 [batch_size, 3, H, W]

        Returns:
            torch.Tensor: 輸出張量，形狀為 [batch_size, num_classes]
        """
        logger.debug(f"輸入張量形狀: {x.shape}")
        output = self.model(x)
        logger.debug(f"輸出張量形狀: {output.shape}")
        return output

    def unfreeze_features(self, num_layers: int = 0) -> None:
        """解凍最後 num_layers 層的參數進行微調。

        Args:
            num_layers: 要解凍的層數，如果為 0 則保持所有特徵提取層凍結
        """
        if num_layers > 0:
            logger.debug(f"解凍最後 {num_layers} 層參數")
            if hasattr(self.model, "features"):  # VGG 系列
                children = list(self.model.features.children())
            elif hasattr(self.model, "layer4"):  # ResNet 系列
                children = list(self.model.layer4.children())
            else:
                raise ValueError("不支持的模型架構")

            for child in children[-num_layers:]:
                for param in child.parameters():
                    param.requires_grad = True
        else:
            logger.debug("保持所有特徵提取層凍結")


if __name__ == "__main__":
    # 測試 ResNet
    resnet_model = PretrainedModel(
        model_name="resnet50",
        num_classes=2,
        weights="DEFAULT",
        freeze_features=True,
        unfreeze_layers=0
    )
    print("ResNet Model:", resnet_model)

    # 測試 VGG
    vgg_model = PretrainedModel(
        model_name="vgg16",
        num_classes=2,
        weights="DEFAULT",
        freeze_features=True,
        unfreeze_layers=0
    )
    print("VGG Model:", vgg_model)
