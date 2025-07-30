import io

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytorch_lightning as pl
import seaborn as sns
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from PIL import Image
from sklearn.metrics import confusion_matrix
from torchmetrics.classification import Accuracy

matplotlib.use("Agg")  # 使用非 GUI 後端


class LightningModel(pl.LightningModule):
    def __init__(
        self,
        *,
        num_classes: int = 10,
        model: nn.Module,
        optimizer: optim.Optimizer,
        scheduler: optim.lr_scheduler._LRScheduler,
        show_progress_bar: bool = True,
        show_result_every_epoch: bool = False,
    ):
        super().__init__()

        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.accuracy = Accuracy(task="multiclass", num_classes=num_classes)
        self.show_progress_bar = show_progress_bar
        self.show_result_every_epoch = show_result_every_epoch
        self.save_hyperparameters(ignore=["model"])

        # 新增列表來儲存損失和準確度
        self.train_acc = []
        self.train_losses = []
        self.val_losses = []
        self.val_accs = []

        # 初始化用於混淆矩陣的標籤收集
        self.val_true_labels = []  # 初始化
        self.val_pred_labels = []  # 初始化

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = nn.CrossEntropyLoss()(logits, y)
        self.log("train_loss", loss, prog_bar=True)

        # 記錄準確度
        acc = self.accuracy(logits, y)
        self.log("train_acc", acc, prog_bar=True)  # 新增：記錄訓練準確度

        # 記錄學習率
        current_lr = self.optimizers().param_groups[0]["lr"]
        self.log("learning_rate", current_lr)

        # 記錄梯度範數
        total_grad_norm = self.compute_total_grad_norm()
        self.log("grad_norm", total_grad_norm)

        return loss

    def compute_total_grad_norm(self):
        total_norm = 0
        for p in self.parameters():
            if p.grad is not None:
                param_norm = p.grad.detach().data.norm(2)
                total_norm += param_norm.item() ** 2
        return total_norm**0.5

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = nn.CrossEntropyLoss()(logits, y)
        acc = self.accuracy(logits, y)

        # 收集真實標籤和預測標籤用於混淆矩陣
        preds = torch.argmax(logits, dim=1)
        self.val_true_labels.append(y)
        self.val_pred_labels.append(preds)

        # 記錄損失和準確率
        self.log("val_loss", loss, prog_bar=self.show_progress_bar)
        self.log("val_acc", acc, prog_bar=self.show_progress_bar)

    def on_train_epoch_end(self):
        avg_loss = self.trainer.callback_metrics["train_loss"].item()
        self.train_losses.append(avg_loss)

        # 新增：計算並記錄訓練準確度
        avg_train_acc = self.trainer.callback_metrics["train_acc"].item()
        self.log("hp_metric/train_acc", avg_train_acc, on_epoch=True, on_step=False)

        # 紀錄每次 epoch 後的訓練準確度
        self.train_acc.append(avg_train_acc)  # 新增：紀錄訓練準確度

    def on_validation_epoch_end(self):
        avg_val_loss = self.trainer.callback_metrics.get("val_loss", None)
        avg_val_acc = self.trainer.callback_metrics.get("val_acc", None)

        # 確保這些指標存在
        if avg_val_loss is not None:
            self.val_losses.append(avg_val_loss.item())
            self.log(
                "hp_metric/val_loss", avg_val_loss.item(), on_epoch=True, on_step=False
            )
        else:
            print("警告: val_loss 不存在")

        if avg_val_acc is not None:
            self.val_accs.append(avg_val_acc.item())
            self.log(
                "hp_metric/val_acc", avg_val_acc.item(), on_epoch=True, on_step=False
            )
        else:
            print("警告: val_acc 不存在")

        if self.val_true_labels and self.val_pred_labels:
            true_labels = torch.cat(self.val_true_labels)
            pred_labels = torch.cat(self.val_pred_labels)

            # 確保 true_labels 和 pred_labels 不是 None
            if true_labels is not None and pred_labels is not None:
                # 生成混淆矩陣
                confusion_matrix_image, _ = self.get_confusion_matrix_image(
                    true_labels, pred_labels
                )  # 只取原始混淆矩陣

                # 檢查圖像是否成功生成
                if confusion_matrix_image is not None and self.logger is not None:
                    self.logger.experiment.add_image(
                        "Confusion Matrix/Validation",
                        confusion_matrix_image,
                        global_step=self.current_epoch,
                    )
            else:
                print("警告: true_labels 或 pred_labels 為 None")

        # 清除上一個 epoch 的數據
        self.val_true_labels.clear()
        self.val_pred_labels.clear()

    def test_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = nn.CrossEntropyLoss()(logits, y)
        acc = self.accuracy(logits, y)
        self.log("test_loss", loss, prog_bar=self.show_progress_bar)
        self.log("test_acc", acc, prog_bar=self.show_progress_bar)

    def configure_optimizers(self):
        return {
            "optimizer": self.optimizer,
            "lr_scheduler": self.scheduler,
            "monitor": "val_loss",
        }

    def get_confusion_matrix_image(
        self, true_labels, predicted_labels, class_names=None, title="confusion_matrix"
    ):
        """
        生成混淆矩陣的圖像，用於 TensorBoard 可視化

        Args:
            true_labels (torch.Tensor): 真實標籤
            predicted_labels (torch.Tensor): 預測標籤
            class_names (list, optional): 類別名稱列表
            title (str, optional): 圖表標題

        Returns:
            tuple: 包含兩個 torch.Tensor，分別是原始混淆矩陣和標準化混淆矩陣的圖像張量
        """
        # 將 PyTorch 張量轉換為 NumPy 數組
        true_labels = true_labels.cpu().numpy()
        predicted_labels = predicted_labels.cpu().numpy()

        # 計算混淆矩陣
        cm = confusion_matrix(true_labels, predicted_labels)

        # 設置字體大小
        plt.rcParams.update({"font.size": 14})  # 增加全局字體大小

        # 原始混淆矩陣圖像
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=class_names if class_names is not None else range(cm.shape[1]),
            yticklabels=class_names if class_names is not None else range(cm.shape[0]),
            annot_kws={"size": 16},
        )  # 設置熱力圖中數字的字體大小
        plt.title(f"{title} (Raw)", fontsize=18)  # 設置標題字體大小
        plt.xlabel("predicted_labels", fontsize=16)  # 設置x軸標籤字體大小
        plt.ylabel("true_labels", fontsize=16)  # 設置y軸標籤字體大小
        plt.xticks(fontsize=14)  # 設置x軸刻度字體大小
        plt.yticks(fontsize=14)  # 設置y軸刻度字體大小
        plt.tight_layout()

        # 將原始混淆矩陣圖像轉換為張量
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=150)  # 增加DPI以提高圖像質量
        buf.seek(0)
        image_raw = Image.open(buf)
        transform = transforms.ToTensor()
        image_tensor_raw = transform(image_raw)
        plt.close()

        # 標準化混淆矩陣
        cm_normalized = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

        # 標準化混淆矩陣圖像
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            cm_normalized,
            annot=True,
            fmt=".2f",
            cmap="Blues",
            xticklabels=class_names if class_names is not None else range(cm.shape[1]),
            yticklabels=class_names if class_names is not None else range(cm.shape[0]),
            annot_kws={"size": 16},
        )  # 設置熱力圖中數字的字體大小
        plt.title(f"{title} (Normalized)", fontsize=18)  # 設置標題字體大小
        plt.xlabel("predicted_labels", fontsize=16)  # 設置x軸標籤字體大小
        plt.ylabel("true_labels", fontsize=16)  # 設置y軸標籤字體大小
        plt.xticks(fontsize=14)  # 設置x軸刻度字體大小
        plt.yticks(fontsize=14)  # 設置y軸刻度字體大小
        plt.tight_layout()

        # 將標準化混淆矩陣圖像轉換為張量
        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=150)  # 增加DPI以提高圖像質量
        buf.seek(0)
        image_norm = Image.open(buf)
        image_tensor_norm = transform(image_norm)

        plt.close("all")  # 關閉所有 matplotlib 圖形

        return image_tensor_raw, image_tensor_norm
