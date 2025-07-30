import unittest
import torch
from kevins_torch.models.pretrained import PretrainedModel


class TestPretrainedModel(unittest.TestCase):
    """測試 PretrainedModel 類的功能。"""

    def setUp(self):
        """設置測試環境。"""
        self.batch_size = 4
        self.num_classes = 2
        self.input_shape = (self.batch_size, 3, 224, 224)
        self.test_input = torch.randn(self.input_shape)

    def test_resnet_model_initialization(self):
        """測試 ResNet 模型的初始化。"""
        model = PretrainedModel(
            model_name="resnet50",
            num_classes=self.num_classes,
            weights="DEFAULT",
            freeze_features=True,
            unfreeze_layers=0
        )
        
        # 測試模型類型
        self.assertIsInstance(model, PretrainedModel)
        
        # 測試輸出形狀
        output = model(self.test_input)
        self.assertEqual(
            output.shape,
            (self.batch_size, self.num_classes)
        )
        
        # 測試參數凍結
        layers = [model.model.layer1, model.model.layer2, model.model.layer3, model.model.layer4]
        for layer in layers:
            for param in layer.parameters():
                self.assertFalse(param.requires_grad)
        
        # 測試分類層未凍結
        self.assertTrue(model.model.fc.weight.requires_grad)
        self.assertTrue(model.model.fc.bias.requires_grad)

    def test_vgg_model_initialization(self):
        """測試 VGG 模型的初始化。"""
        model = PretrainedModel(
            model_name="vgg16",
            num_classes=self.num_classes,
            weights="DEFAULT",
            freeze_features=True,
            unfreeze_layers=0
        )
        
        # 測試模型類型
        self.assertIsInstance(model, PretrainedModel)
        
        # 測試輸出形狀
        output = model(self.test_input)
        self.assertEqual(output.shape, (self.batch_size, self.num_classes))
        
        # 測試參數凍結
        for param in model.model.features.parameters():
            self.assertFalse(param.requires_grad)
        
        # 測試分類層未凍結
        self.assertTrue(model.model.classifier[-1].weight.requires_grad)
        self.assertTrue(model.model.classifier[-1].bias.requires_grad)

    def test_model_unfreezing(self):
        """測試模型參數解凍功能。"""
        model = PretrainedModel(
            model_name="resnet50",
            num_classes=self.num_classes,
            weights="DEFAULT",
            freeze_features=True,
            unfreeze_layers=2
        )
        
        # 測試部分參數解凍
        unfrozen_params = 0
        for layer in [model.model.layer4]:
            for param in layer.parameters():
                if param.requires_grad:
                    unfrozen_params += 1
        
        self.assertGreater(unfrozen_params, 0)

    def test_invalid_model_name(self):
        """測試無效的模型名稱。"""
        with self.assertRaises(ValueError):
            PretrainedModel(model_name="invalid_model")

    def test_default_parameters(self):
        """測試默認參數。"""
        model = PretrainedModel()
        
        # 測試默認模型名稱
        self.assertEqual(model.model_name, "resnet18")
        
        # 測試默認類別數
        output = model(self.test_input)
        self.assertEqual(output.shape, (self.batch_size, 2))

    def test_model_saving_and_loading(self):
        """測試模型保存和加載。"""
        # 創建並保存模型
        model = PretrainedModel(
            model_name="resnet50",
            num_classes=self.num_classes
        )
        torch.save(model.state_dict(), "test_model.pth")
        
        # 創建新模型並加載權重
        new_model = PretrainedModel(
            model_name="resnet50",
            num_classes=self.num_classes
        )
        new_model.load_state_dict(torch.load("test_model.pth", weights_only=True))
        
        # 測試加載後的模型輸出是否一致
        with torch.no_grad():
            original_output = model(self.test_input)
            new_output = new_model(self.test_input)
            self.assertTrue(torch.allclose(original_output, new_output))
        
        # 清理測試文件
        import os
        os.remove("test_model.pth")


if __name__ == "__main__":
    unittest.main()
