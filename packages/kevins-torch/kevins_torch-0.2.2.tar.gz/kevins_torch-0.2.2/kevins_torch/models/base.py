"""
基礎模型模組
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple, Union
from pytorch_lightning import LightningModule

import torch
import torch.nn as nn
import torch.nn.functional as F

from kevins_torch.utils.logger_config import setup_logger

# 設置 logger
logger = setup_logger(__name__)


class BaseModel(ABC, nn.Module):
    """
    所有模型的抽象基類
    """

    def __init__(self):
        super().__init__()
        self.class_names: Optional[list] = None

    @abstractmethod
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        模型的前向傳播

        Args:
            x: 輸入張量
        """
        pass

    def predict(
        self, x: torch.Tensor, return_probs: bool = False
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """
        通用預測方法，適用於所有分類模型

        Args:
            x: 輸入張量
            return_probs: 是否返回預測概率
        """
        self.eval()
        device = next(self.parameters()).device
        x = self._prepare_input(x, device)

        try:
            with torch.no_grad():
                logits = self(x)
                return self._process_output(logits, return_probs)
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise

    def predict_single(self, x: torch.Tensor) -> Dict[str, Union[int, float]]:
        """
        預測單個樣本

        Args:
            x: 單個樣本的輸入張量
        """
        predictions, probs = self.predict(x, return_probs=True)
        return self._format_single_prediction(predictions[0], probs[0])

    @abstractmethod
    def _prepare_input(self, x: torch.Tensor, device: torch.device) -> torch.Tensor:
        """
        準備模型輸入

        Args:
            x: 輸入張量
            device: 目標設備
        """
        pass

    def _process_output(
        self, logits: torch.Tensor, return_probs: bool
    ) -> Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """
        處理模型輸出

        Args:
            logits: 模型輸出的 logits
            return_probs: 是否返回概率
        """
        probs = F.softmax(logits, dim=1)
        predictions = torch.argmax(probs, dim=1)

        if return_probs:
            max_probs = torch.max(probs, dim=1)[0]
            return predictions, max_probs
        return predictions

    def _format_single_prediction(
        self, pred: torch.Tensor, prob: torch.Tensor
    ) -> Dict[str, Union[int, float]]:
        """
        格式化單個預測結果

        Args:
            pred: 預測類別
            prob: 預測概率
        """
        result = {"class": pred.item(), "probability": prob.item()}
        if self.class_names is not None:
            result["class_name"] = self.class_names[result["class"]]
        return result


class BasePretrainedModel(LightningModule):
    """
    所有預訓練模型的抽象基類
    """
    
    @staticmethod
    def load_model_from_ckpt(self, ckpt_path):
        checkpoint = torch.load(ckpt_path)
        new_state_dict = {}
        for key in checkpoint["state_dict"]:
            new_key = key.replace("model.model.", "model.")  # 去掉多餘的前綴
            new_state_dict[new_key] = checkpoint["state_dict"][key]
        self.load_state_dict(new_state_dict)
