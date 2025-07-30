# Kevin's Torch Utils

[![PyPI version](https://badge.fury.io/py/kevins_torch.svg)](https://badge.fury.io/py/kevins_torch)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

這是一個用於圖像 AI 訓練的 PyTorch 工具組 (`kevins_torch`)，旨在提供一系列實用的功能來簡化深度學習模型的開發、訓練和評估過程。

## 主要功能模組

*   **`models`**:
    *   `base.py`: 提供模型的基本結構。
    *   `cnn.py`: 包含通用的卷積神經網路實現。
    *   `lenet.py`: LeNet 模型的實現。
    *   `pretrained.py`: 處理和載入預訓練模型的工具。
    *   `utils/activation_function_parser.py`: 解析活化函數配置。
*   **`utils`**:
    *   `load_parameters.py`: 從設定檔載入模型和訓練參數。
    *   `lightning_models.py`: 與 PyTorch Lightning 整合的相關工具。
    *   `logger_config.py`: 設定日誌記錄器。
    *   `repeat_channels.py`: 用於調整輸入圖像通道數的工具。
    *   `dataset/coffee_bean_dataset.py`: 針對特定咖啡豆資料集的處理。
*   **`examples`**:
    *   `settings.yaml`: 範例設定檔。
    *   `train_configs_generator.py`: 產生訓練設定檔的腳本。
*   **`tests`**:
    *   包含對各個模組的單元測試。

## 安裝

您可以透過 pip 安裝此套件：

```bash
pip install kevins_torch
```

## 使用範例

```python
import torch
from kevins_torch import models
from kevins_torch.utils import load_parameters

# 載入設定檔中的參數
config_path = 'examples/settings.yaml' # 假設您的設定檔路徑
params = load_parameters(config_path)

# 根據設定檔建立模型
# (假設您的設定檔中有模型定義)
# model = models.build_model(params['model_config']) # 實際函數可能不同

# 或者直接使用預定義的模型
model = models.LeNet(num_classes=10)

# 準備輸入數據 (範例)
dummy_input = torch.randn(1, 1, 28, 28) # LeNet 通常用於 MNIST (1x28x28)

# 進行預測
output = model(dummy_input)
print("模型輸出:", output.shape)
```

## 開發設定

如果您想為此專案貢獻，請先設定開發環境：

1.  複製儲存庫：
    ```bash
    git clone https://github.com/yourusername/kevins_torch # 請替換成實際的儲存庫 URL
    cd kevins_torch
    ```
2.  安裝開發依賴：
    ```bash
    pip install -r dev-requirements.txt
    ```
3.  設定 pre-commit hooks (建議)：
    ```bash
    pre-commit install
    ```

## 執行測試

使用 pytest 執行測試：

```bash
pytest tests/
```

## 貢獻

歡迎透過 Pull Requests 或 Issues 提出問題和改進建議！

## 授權

本專案採用 MIT License 授權。
