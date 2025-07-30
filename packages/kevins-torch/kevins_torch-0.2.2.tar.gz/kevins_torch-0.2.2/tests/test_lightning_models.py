import unittest
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models
from torch.utils.data import DataLoader
from torchvision.datasets import CIFAR10
from torchvision import transforms

from kevins_torch.utils import LightningModel


class TestLightningModel(unittest.TestCase):
    def setUp(self):
        # 初始化 resnet18 模型
        self.model = models.resnet18(num_classes=10)
        
        # 初始化優化器和學習率調度器
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=5, gamma=0.1)
        
        # 創建 LightningModel 實例
        self.lightning_model = LightningModel(
            num_classes=10,
            model=self.model,
            optimizer=self.optimizer,
            scheduler=self.scheduler,
            show_progress_bar=False,
            show_result_every_epoch=False
        )
        
        # 使用真實 CIFAR10 數據集
        self.batch_size = 32
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])
        self.dataset = CIFAR10(root='./data', train=True, download=True, transform=transform)
        self.loader = DataLoader(self.dataset, batch_size=self.batch_size, shuffle=True)
        
        # 獲取真實批次數據
        self.real_batch = next(iter(self.loader))

    def test_initialization(self):
        self.assertIsInstance(self.lightning_model.model, nn.Module)
        self.assertIsInstance(self.lightning_model.optimizer, optim.Optimizer)
        self.assertIsInstance(self.lightning_model.scheduler, optim.lr_scheduler.StepLR)
        self.assertEqual(self.lightning_model.hparams.num_classes, 10)

    def test_forward_pass(self):
        x = torch.randn(2, 3, 32, 32)  # batch size > 1 避免 batch norm 錯誤
        output = self.lightning_model(x)
        self.assertEqual(output.shape, torch.Size([2, 10]))

    def test_training_step_output(self):
        # 只測試訓練步驟的輸出類型
        with self.assertRaises(RuntimeError):
            # 預期會拋出 RuntimeError 因為沒有 Trainer
            self.lightning_model.training_step(self.real_batch, 0)

    def test_validation_step_output(self):
        # 測試驗證步驟是否能執行
        try:
            self.lightning_model.validation_step(self.real_batch, 0)
            # 檢查是否收集了標籤
            self.assertTrue(len(self.lightning_model.val_true_labels) > 0)
            self.assertTrue(len(self.lightning_model.val_pred_labels) > 0)
        except Exception as e:
            self.fail(f"validation_step() raised {type(e).__name__} unexpectedly")

    def test_test_step_output(self):
        # 測試測試步驟是否能執行
        try:
            self.lightning_model.test_step(self.real_batch, 0)
        except Exception as e:
            self.fail(f"test_step() raised {type(e).__name__} unexpectedly")

    def test_configure_optimizers(self):
        optimizer_config = self.lightning_model.configure_optimizers()
        self.assertIsInstance(optimizer_config["optimizer"], optim.Optimizer)
        self.assertIsInstance(optimizer_config["lr_scheduler"], optim.lr_scheduler.StepLR)
        self.assertEqual(optimizer_config["monitor"], "val_loss")

    def test_confusion_matrix_output(self):
        # 測試混淆矩陣生成函數的輸出
        true_labels = torch.randint(0, 10, (100,))
        pred_labels = torch.randint(0, 10, (100,))
        
        # 測試函數是否能正常執行
        try:
            cm_image, _ = self.lightning_model.get_confusion_matrix_image(
                true_labels, pred_labels
            )
            self.assertIsInstance(cm_image, torch.Tensor)
            self.assertEqual(cm_image.dim(), 3)
        except Exception as e:
            self.fail(f"get_confusion_matrix_image() raised {type(e).__name__} unexpectedly")

    def test_compute_total_grad_norm(self):
        # 模擬梯度
        for param in self.lightning_model.model.parameters():
            param.grad = torch.randn_like(param.data)
        
        grad_norm = self.lightning_model.compute_total_grad_norm()
        self.assertIsInstance(grad_norm, float)
        self.assertGreater(grad_norm, 0)


if __name__ == "__main__":
    unittest.main()
