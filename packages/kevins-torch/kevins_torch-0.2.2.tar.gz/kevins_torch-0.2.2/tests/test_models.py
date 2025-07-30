import unittest
import torch

from models import CNNModel, LeNetModel


class TestModels(unittest.TestCase):
    """測試 CNNModel 和 LeNetModel 的功能。"""

    def setUp(self):
        """設置測試環境。"""
        self.batch_size = 4
        self.lenet_input_shape = (self.batch_size, 3, 32, 32)
        self.cnn_input_shape = (self.batch_size, 3, 64, 64)
        self.lenet_test_input = torch.randn(self.lenet_input_shape)
        self.cnn_test_input = torch.randn(self.cnn_input_shape)

    def test_lenet_initialization(self):
        """測試 LeNet 模型的初始化。"""
        num_classes = 10
        model = LeNetModel(num_classes=num_classes)
        
        # 測試模型類型
        self.assertIsInstance(model, LeNetModel)
        
        # 測試模型結構
        self.assertTrue(hasattr(model, 'features'))
        self.assertTrue(hasattr(model, 'classifier'))
        
        # 測試輸出形狀
        output = model(self.lenet_test_input)
        self.assertEqual(output.shape, (self.batch_size, num_classes))

    def test_cnn_initialization(self):
        """測試 CNN 模型的初始化。"""
        input_size = 64
        num_classes = 100
        hidden_layers = [256, 128, 64]
        conv_layers = [128, 256, 512, 512]
        
        model = CNNModel(
            input_size=input_size,
            num_classes=num_classes,
            hidden_layers=hidden_layers,
            conv_layers=conv_layers,
            using_batch_norm=True
        )
        
        # 測試模型類型
        self.assertIsInstance(model, CNNModel)
        
        # 測試模型結構
        self.assertTrue(hasattr(model, 'conv_layers'))
        self.assertTrue(hasattr(model, 'fc_layers'))
        
        # 測試輸出形狀
        output = model(self.cnn_test_input)
        self.assertEqual(output.shape, (self.batch_size, num_classes))

    def test_cnn_with_different_activations(self):
        """測試 CNN 模型使用不同的激活函數。"""
        activations = ["ReLU", "LeakyReLU", "ELU", "SELU"]
        for activation in activations:
            model = CNNModel(activation_function=activation)
            output = model(self.cnn_test_input)
            self.assertEqual(output.shape, (self.batch_size, 100))

    def test_cnn_without_batch_norm(self):
        """測試不使用批量歸一化的 CNN 模型。"""
        model = CNNModel(using_batch_norm=False)
        output = model(self.cnn_test_input)
        self.assertEqual(output.shape, (self.batch_size, 100))

    def test_cnn_with_custom_layers(self):
        """測試使用自定義層配置的 CNN 模型。"""
        hidden_layers = [512, 256]
        conv_layers = [64, 128, 256]
        model = CNNModel(
            hidden_layers=hidden_layers,
            conv_layers=conv_layers
        )
        output = model(self.cnn_test_input)
        self.assertEqual(output.shape, (self.batch_size, 100))

    def test_model_predict(self):
        """測試模型的預測功能。"""
        # 測試 LeNet
        lenet = LeNetModel()
        lenet_pred = lenet.predict(self.lenet_test_input[0].unsqueeze(0))
        self.assertIsInstance(lenet_pred, int)
        self.assertTrue(0 <= lenet_pred < 10)

        # 測試 CNN
        cnn = CNNModel()
        cnn_pred = cnn.predict(self.cnn_test_input[0].unsqueeze(0))
        self.assertIsInstance(cnn_pred, int)
        self.assertTrue(0 <= cnn_pred < 100)

    def test_invalid_input_size(self):
        """測試無效的輸入大小。"""
        # 測試 LeNet 的錯誤輸入大小
        lenet = LeNetModel()
        invalid_input = torch.randn(1, 3, 64, 64)  # LeNet 期望 32x32
        with self.assertRaises(RuntimeError):
            lenet(invalid_input)

        # 測試 CNN 的錯誤輸入大小
        cnn = CNNModel(input_size=32)
        invalid_input = torch.randn(1, 3, 64, 64)  # CNN 期望 32x32
        with self.assertRaises(RuntimeError):
            cnn(invalid_input)


if __name__ == "__main__":
    unittest.main()
