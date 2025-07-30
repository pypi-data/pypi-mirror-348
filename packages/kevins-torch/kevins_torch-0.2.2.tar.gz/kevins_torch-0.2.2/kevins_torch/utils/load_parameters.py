import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import importlib
import inspect
import logging
from typing import Dict, List, Optional, Tuple, Type

import torch
import torch.nn as nn
import torch.optim as optim  # 引入優化器模組
import torchvision.models as models
import torchvision.transforms as transforms
import yaml
import argparse

from utils.logger_config import setup_logger

# 設置 logger
logger = setup_logger(__name__)

# 創建控制台處理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 創建格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# 添加處理器到 logger
logger.addHandler(console_handler)

# 根據環境變量設置日誌級別
if os.getenv('DEBUG', 'False').lower() == 'true':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.WARNING)

# Add project root to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def repeat_channels(x: torch.Tensor) -> torch.Tensor:
    """將單通道圖像轉換為三通道圖像。

    Args:
        x: 輸入張量，形狀為 [1, H, W] 或 [3, H, W]

    Returns:
        torch.Tensor: 輸出張量，形狀為 [3, H, W]
    """
    return x.repeat(3, 1, 1) if x.size(0) == 1 else x


def load_transforms(transforms_config: List[Dict]) -> transforms.Compose:
    """從配置中加載數據轉換。

    Args:
        transforms_config: 包含轉換配置的列表，每個配置都是一個字典，
                         包含轉換類型和相關參數

    Returns:
        transforms.Compose: 組合後的轉換函數
    """
    transform_list = []
    for transform in transforms_config:
        if transform["type"] == "Resize":
            transform_list.append(transforms.Resize(tuple(transform["size"])))
        elif transform["type"] == "RandomCrop":
            transform_list.append(
                transforms.RandomCrop(
                    size=tuple(transform["size"]), padding=transform["padding"]
                )
            )
        elif transform["type"] == "ToTensor":
            transform_list.append(transforms.ToTensor())
        elif transform["type"] == "Lambda":
            transform_list.append(transforms.Lambda(repeat_channels))
        elif transform["type"] == "RandomHorizontalFlip":
            transform_list.append(transforms.RandomHorizontalFlip())
        elif transform["type"] == "RandomRotation":
            transform_list.append(
                transforms.RandomRotation(degrees=transform["degrees"])
            )
        elif transform["type"] == "ColorJitter":
            transform_list.append(
                transforms.ColorJitter(
                    brightness=transform["brightness"],
                    contrast=transform["contrast"],
                    saturation=transform["saturation"],
                    hue=transform["hue"],
                )
            )
        elif transform["type"] == "Normalize":
            transform_list.append(
                transforms.Normalize(mean=transform["mean"], std=transform["std"])
            )
        elif transform["type"] == "GaussianBlur":
            transform_list.append(
                transforms.GaussianBlur(
                    kernel_size=transform["kernel_size"], sigma=transform["sigma"]
                )
            )

    return transforms.Compose(transform_list)


def get_local_model_classes() -> Dict[str, Type[nn.Module]]:
    """獲取本地定義的模型類。

    Returns:
        Dict[str, Type[nn.Module]]: 模型名稱到模型類的映射
    """
    models_module = importlib.import_module("models")
    model_classes = {
        name: cls
        for name, cls in inspect.getmembers(models_module, inspect.isclass)
        if issubclass(cls, nn.Module) and cls != nn.Module
    }
    return model_classes


def get_torchvision_model_classes() -> Dict[str, Type[nn.Module]]:
    """獲取torchvision提供的預訓練模型類。

    Returns:
        Dict[str, Type[nn.Module]]: 模型名稱到模型類的映射
    """
    model_classes = {
        name: cls
        for name, cls in inspect.getmembers(models, inspect.isclass)
        if issubclass(cls, nn.Module) and cls != nn.Module
    }
    model_classes["resnet50"] = models.resnet50
    return model_classes


def get_optimizer_classes() -> Dict[str, Type[torch.optim.Optimizer]]:
    """獲取可用的優化器類型。

    Returns:
        Dict[str, Type[torch.optim.Optimizer]]: 優化器名稱到優化器類的映射
    """
    optimizer_classes = {
        name: cls
        for name, cls in inspect.getmembers(optim, inspect.isclass)
        if name != "Optimizer" and issubclass(cls, torch.optim.Optimizer)
    }
    return optimizer_classes


def get_scheduler_classes() -> Dict[str, Type[torch.optim.lr_scheduler._LRScheduler]]:
    """獲取可用的學習率調度器類型。

    Returns:
        Dict[str, Type[torch.optim.lr_scheduler._LRScheduler]]:
            調度器名稱到調度器類的映射
    """
    return {
        name: cls
        for name, cls in inspect.getmembers(
            torch.optim.lr_scheduler,
            inspect.isclass
        )
    }


def get_loss_function_classes() -> Dict[str, Type[nn.Module]]:
    """獲取可用的損失函數類型。

    Returns:
        Dict[str, Type[nn.Module]]: 損失函數名稱到損失函數類的映射
    """
    loss_function_classes = {
        name: cls
        for name, cls in inspect.getmembers(nn, inspect.isclass)
        if name.endswith('Loss') and issubclass(cls, nn.Module)
    }
    return loss_function_classes


def get_local_loss_function_classes() -> Dict[str, Type[nn.Module]]:
    """獲取本地定義的損失函數類。

    Returns:
        Dict[str, Type[nn.Module]]: 損失函數名稱到損失函數類的映射
    """
    try:
        loss_functions_module = importlib.import_module("loss_functions")
        loss_function_classes = {
            name: cls
            for name, cls in inspect.getmembers(loss_functions_module, inspect.isclass)
            if issubclass(cls, nn.Module) and cls != nn.Module
        }
        return loss_function_classes
    except ImportError:
        logger.warning("無法導入 loss_functions 模組")
        return {}


def load_model(model_name: str, model_parameters: Dict) -> nn.Module:
    """根據模型名稱和參數動態構建模型。

    Args:
        model_name: 模型名稱
        model_parameters: 模型參數字典

    Returns:
        nn.Module: 構建的模型實例

    Raises:
        ValueError: 當模型名稱未知時
    """
    local_model_classes = get_local_model_classes()
    torchvision_model_classes = get_torchvision_model_classes()

    if model_name in local_model_classes:
        return local_model_classes[model_name](**model_parameters)
    elif model_name in torchvision_model_classes:
        if "num_classes" in model_parameters:
            original_num_classes = model_parameters["num_classes"]
            model_parameters["num_classes"] = 1000

        model = torchvision_model_classes[model_name](**model_parameters)

        if "num_classes" in model_parameters:
            model.fc = nn.Linear(model.fc.in_features, original_num_classes)

        return model
    else:
        raise ValueError(f"Unknown model name: {model_name}")


def load_optimizer(
    optimizer_config: Dict, model: nn.Module
) -> torch.optim.Optimizer:
    """根據配置加載優化器。

    Args:
        optimizer_config: 優化器配置字典
        model: 要優化的模型

    Returns:
        torch.optim.Optimizer: 配置的優化器實例

    Raises:
        ValueError: 當優化器類型未知時
    """
    optimizer_type = optimizer_config["type"]
    params = optimizer_config["params"]
    optimizer_classes = get_optimizer_classes()

    if optimizer_type in optimizer_classes:
        return optimizer_classes[optimizer_type](model.parameters(), **params)
    else:
        raise ValueError(f"Unknown optimizer type: {optimizer_type}")


def load_scheduler(
    scheduler_config: Dict, optimizer: torch.optim.Optimizer
) -> torch.optim.lr_scheduler._LRScheduler:
    """根據配置加載學習率調度器。

    Args:
        scheduler_config: 調度器配置字典
        optimizer: 要調度的優化器

    Returns:
        torch.optim.lr_scheduler._LRScheduler: 配置的調度器實例

    Raises:
        ValueError: 當調度器類型未知時
    """
    scheduler_type = scheduler_config["type"]
    params = scheduler_config["params"]
    scheduler_classes = get_scheduler_classes()

    if scheduler_type in scheduler_classes:
        return scheduler_classes[scheduler_type](optimizer, **params)
    else:
        raise ValueError(f"Unknown scheduler type: {scheduler_type}")


def load_loss_function(loss_config: Dict, device: torch.device) -> nn.Module:
    """根據配置加載損失函數。

    Args:
        loss_config: 損失函數配置字典
        device: 計算設備（CPU 或 GPU）

    Returns:
        nn.Module: 配置的損失函數實例

    Raises:
        ValueError: 當損失函數類型未知時
    """
    loss_type = loss_config["type"]
    params = loss_config.get("params", {})
    
    # 將 weight 轉換為 Tensor 並移動到指定設備
    if "weight" in params:
        params["weight"] = torch.tensor(params["weight"], dtype=torch.float32).to(device)

    # 獲取內置的損失函數類
    loss_function_classes = get_loss_function_classes()
    
    # 獲取本地自定義的損失函數類
    local_loss_function_classes = get_local_loss_function_classes()

    # 合併兩個損失函數類字典
    combined_loss_function_classes = {**loss_function_classes, **local_loss_function_classes}

    if loss_type in combined_loss_function_classes:
        return combined_loss_function_classes[loss_type](**params).to(device)
    else:
        raise ValueError(f"Unknown loss function type: {loss_type}")


def load_config(config_path: str) -> Tuple[
    nn.Module,
    transforms.Compose,
    transforms.Compose,
    transforms.Compose,
    Dict,
    torch.optim.Optimizer,
    Optional[torch.optim.lr_scheduler._LRScheduler],
    Optional[nn.Module],  # 添加損失函數返回值
]:
    """從 YAML 配置檔案中加載模型、轉換和訓練參數。

    Args:
        config_path: YAML 配置文件的路徑

    Returns:
        tuple: 包含以下元素：
            - model: 神經網絡模型
            - train_transforms: 訓練數據轉換
            - val_transforms: 驗證數據轉換
            - test_transforms: 測試數據轉換
            - training_params: 訓練參數字典
            - optimizer: 優化器
            - scheduler: 學習率調度器（可選）
            - loss_fn: 損失函數（可選）

    Raises:
        ValueError: 當配置文件格式不正確時
    """
    logger.debug(f"正在加載配置文件: {config_path}")
    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        logger.error("配置文件應該是一個字典")
        raise ValueError("配置文件應該是一個字典")

    # 獲取模型配置
    model_config = config["model"]
    model_name = model_config["name"]
    model_parameters = model_config["parameters"]
    logger.debug(f"正在加載模型: {model_name} 參數: {model_parameters}")
    model = load_model(model_name, model_parameters)

    # 加載數據轉換
    logger.debug("正在加載數據轉換")
    train_transforms = load_transforms(config["train_transforms"])
    val_transforms = load_transforms(config["val_transforms"])
    test_transforms = load_transforms(config["test_transforms"])

    # 加載訓練參數
    training_config = config["training"]
    training_params = {
        "batch_size": training_config["batch_size"],
        "num_workers": training_config["num_workers"],
        "learning_rate": training_config["learning_rate"],
        "max_epochs": training_config["max_epochs"],
        "early_stopping_patience": training_config["early_stopping_patience"],
    }
    logger.debug(f"訓練參數: {training_params}")

    # 加載優化器
    logger.debug("正在加載優化器")
    optimizer = load_optimizer(config["optimizer"], model)

    # 加載學習率調度器（如果有的話）
    scheduler = None
    if "scheduler" in config:
        logger.debug("正在加載學習率調度器")
        scheduler = load_scheduler(config["scheduler"], optimizer)
        
    # 獲取計算設備
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 加載損失函數（如果有的話）
    loss_fn = None
    if "loss_function" in config:
        logger.debug("正在加載損失函數")
        loss_fn = load_loss_function(config["loss_function"], device)

    return (
        model,
        train_transforms,
        val_transforms,
        test_transforms,
        training_params,
        optimizer,
        scheduler,
        loss_fn,  # 返回損失函數
    )


"""
YAML 配置例：

configs:
  model:
    name: "CNNModelForCIFAR100"  # 可選擇: CNNModelForCIFAR100, LeNet, VGG, ResNet18
    parameters:
      num_classes: 100
      input_size: 32
  training:
    batch_size: 120
    num_workers: 4
    learning_rate: 0.001
    max_epochs: 1000
    early_stopping_patience: 15
  transforms:
    - type: "Resize"
      size: [32, 32]
    - type: "RandomCrop"
      size: [32, 32]
      padding: 4
    - type: "ToTensor"
    - type: "Lambda"
      function: "repeat_channels"
    - type: "RandomHorizontalFlip"
    - type: "RandomRotation"
      degrees: 30
    - type: "ColorJitter"
      brightness: 0.2
      contrast: 0.2
      saturation: 0.2
      hue: 0.1
    - type: "Normalize"
      mean: [0.4914, 0.4822, 0.4465]
      std: [0.2470, 0.2435, 0.2616]
  optimizer:
    type: "Adam"  # 可選擇: SGD, Adam, RMSprop, Adagrad, AdamW
    params:
      weight_decay: 0.0001
  scheduler:
    type: "StepLR"  # 可選擇: StepLR, ReduceLROnPlateau, ExponentialLR, CosineAnnealingLR
    params:
      step_size: 30
      gamma: 0.1
"""

def main():
    # 解析 args 參數
    args = argparse.ArgumentParser(description='咖啡豆分類訓練程式')
    args.add_argument('--debug', action='store_true', help='啟用除錯模式，顯示詳細資訊')
    args.add_argument('--lookahead', action='store_true', help='使用Lookahead優化器')
    args = args.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)
    # 顯示可用的組件類型
    logger.debug("顯示可用的組件類型")
    logger.debug("模型類型：", get_local_model_classes())
    logger.debug("torchvision模型類型：", get_torchvision_model_classes())
    logger.debug("優化器類型：", get_optimizer_classes())
    logger.debug("調度器類型：", get_scheduler_classes())
    logger.debug("損失函數類型：", get_loss_function_classes())  # 添加損失函數類型顯示

    yaml_file = "train_config_1.yaml"
    logger.debug(f"\n正在讀取設定檔: {yaml_file}")
    logger.debug("-" * 50)

    try:
        with open(yaml_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        if not isinstance(config, dict):
            raise ValueError(f"警告: {yaml_file} 不是有效的配置文件")

        logger.debug(f"模型名稱: {config['model']['name']}")
        logger.debug("模型參數:", config['model']['parameters'])
        logger.debug("訓練參數:", config['training'])
        logger.debug("轉換配置:", config['train_transforms'])
        logger.debug("轉換配置:", config['val_transforms'])
        logger.debug("轉換配置:", config['test_transforms'])
        logger.debug("優化器配置:", config['optimizer'])
        logger.debug("調度器配置:", config['scheduler'])
        logger.debug("損失函數配置:", config['loss_function'])
    except Exception as e:
        raise ValueError(f"處理 {yaml_file} 時發生錯誤: {str(e)}")

if __name__ == "__main__":
    # 顯示可用的組件類型
    print("顯示可用的組件類型")
    print("模型類型：", get_local_model_classes())
    print("torchvision模型類型：", get_torchvision_model_classes())
    print("優化器類型：", get_optimizer_classes())
    print("調度器類型：", get_scheduler_classes())
    print("損失函數類型：", get_loss_function_classes())  # 添加損失函數類型顯示