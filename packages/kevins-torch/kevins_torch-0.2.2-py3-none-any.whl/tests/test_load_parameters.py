import os
import sys
import pytest
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
# Add project root to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from kevins_torch.utils.load_parameters import (  # noqa: E402
    load_transforms,
    load_model,
    load_optimizer,
    load_scheduler,
    load_config,
)
from kevins_torch.models.cnn import CNNModel  # noqa: E402

# Test data
TEST_YAML = """
model:
  name: "CNNModel"
  parameters:
    num_classes: 100
    input_size: 32
training:
  batch_size: 120
  num_workers: 4
  learning_rate: 0.001
  max_epochs: 1000
  early_stopping_patience: 15
train_transforms:
- type: Resize
  size:
  - 256
  - 256
- type: ToTensor
- type: Lambda
  function: repeat_channels
- type: RandomHorizontalFlip
  p: 0.5
- type: RandomVerticalFlip
  p: 0.5
- type: RandomRotation
  degrees: 360
  p: 0.5
- type: RandomPerspective
  distortion_scale: 0.5
  p: 0.5
- type: RandomAffine
  degrees: 360
  translate: 0.2
  scale: 0.2
  shear: 10
  p: 0.5
- type: ColorJitter
  brightness: 0.3
  contrast: 0.3
  saturation: 0.3
  hue: 0.2
  p: 0.5
- type: GaussianBlur
  kernel_size: 5
  sigma: 1.0
  p: 0.5
- type: Normalize
  mean: &id001
  - 0.5314157605171204
  - 0.49074479937553406
  - 0.3935178518295288
  std: &id002
  - 0.30881452560424805
  - 0.28827348351478577
  - 0.2249414622783661
val_transforms:
- type: Resize
  size:
  - 256
  - 256
- type: ToTensor
- type: Lambda
  function: repeat_channels
- type: Normalize
  mean: *id001
  std: *id002
test_transforms:
- type: Resize
  size:
  - 256
  - 256
- type: ToTensor
- type: Lambda
  function: repeat_channels
- type: Normalize
  mean: *id001
  std: *id002
optimizer:
  type: "Adam"
  params:
    weight_decay: 0.0001
scheduler:
  type: "StepLR"
  params:
    step_size: 30
    gamma: 0.1
"""

TEST_YAML_NO_SCHEDULER = """
model:
  name: "CNNModel"
  parameters:
    num_classes: 100
    input_size: 32
training:
  batch_size: 120
  num_workers: 4
  learning_rate: 0.001
  max_epochs: 1000
  early_stopping_patience: 15
train_transforms:
- type: Resize
  size:
  - 256
  - 256
- type: ToTensor
- type: Lambda
  function: repeat_channels
- type: RandomHorizontalFlip
  p: 0.5
- type: RandomVerticalFlip
  p: 0.5
- type: RandomRotation
  degrees: 360
  p: 0.5
- type: RandomPerspective
  distortion_scale: 0.5
  p: 0.5
- type: RandomAffine
  degrees: 360
  translate: 0.2
  scale: 0.2
  shear: 10
  p: 0.5
- type: ColorJitter
  brightness: 0.3
  contrast: 0.3
  saturation: 0.3
  hue: 0.2
  p: 0.5
- type: GaussianBlur
  kernel_size: 5
  sigma: 1.0
  p: 0.5
- type: Normalize
  mean: &id001
  - 0.5314157605171204
  - 0.49074479937553406
  - 0.3935178518295288
  std: &id002
  - 0.30881452560424805
  - 0.28827348351478577
  - 0.2249414622783661
val_transforms:
- type: Resize
  size:
  - 256
  - 256
- type: ToTensor
- type: Lambda
  function: repeat_channels
- type: Normalize
  mean: *id001
  std: *id002
test_transforms:
- type: Resize
  size:
  - 256
  - 256
- type: ToTensor
- type: Lambda
  function: repeat_channels
- type: Normalize
  mean: *id001
  std: *id002
optimizer:
  type: "Adam"
  params:
    weight_decay: 0.0001
"""


@pytest.fixture
def mock_config_file(tmp_path):
    config_file = tmp_path / "test_config.yaml"
    config_file.write_text(TEST_YAML)
    return str(config_file)


def test_load_transforms():
    transforms_config = [
        {"type": "Resize", "size": [32, 32]},
        {"type": "ToTensor"},
        {"type": "Normalize", "mean": [0.5, 0.5, 0.5], "std": [0.5, 0.5, 0.5]}
    ]
    transform = load_transforms(transforms_config)
    assert isinstance(transform, transforms.Compose)
    assert len(transform.transforms) == 3


def test_load_model():
    model = load_model("CNNModel", {"num_classes": 100, "input_size": 32})
    assert isinstance(model, nn.Module)


def test_load_optimizer():
    model = CNNModel(num_classes=10)
    optimizer = load_optimizer(
        {"type": "Adam", "params": {"weight_decay": 0.0001}},
        model
    )
    assert isinstance(optimizer, optim.Adam)
    assert optimizer.param_groups[0]["weight_decay"] == 0.0001


def test_load_scheduler():
    model = CNNModel(num_classes=10)
    optimizer = optim.Adam(model.parameters())
    scheduler = load_scheduler(
        {"type": "StepLR", "params": {"step_size": 30, "gamma": 0.1}},
        optimizer
    )
    assert isinstance(scheduler, optim.lr_scheduler.StepLR)


def test_load_config(mock_config_file):
    (
        model,
        train_transforms,
        val_transforms,
        test_transforms,
        training_params,
        optimizer,
        scheduler,
    ) = load_config(mock_config_file)

    assert isinstance(model, nn.Module)
    assert isinstance(train_transforms, transforms.Compose)
    assert isinstance(val_transforms, transforms.Compose)
    assert isinstance(test_transforms, transforms.Compose)
    assert isinstance(optimizer, optim.Adam)
    assert isinstance(scheduler, optim.lr_scheduler.StepLR)


def test_load_config_without_scheduler(tmp_path):
    no_scheduler_yaml = TEST_YAML_NO_SCHEDULER
    config_file = tmp_path / "no_scheduler.yaml"
    config_file.write_text(no_scheduler_yaml)

    (
        model,
        train_transforms,
        val_transforms,
        test_transforms,
        training_params,
        optimizer,
        scheduler,
    ) = load_config(str(config_file))

    assert scheduler is None


def test_load_torchvision_model():
    # 測試實際的torchvision模型
    model = load_model("PretrainedModel", {"model_name": "resnet18", "num_classes": 100})
    assert isinstance(model, nn.Module)


def test_load_invalid_model():
    with pytest.raises(ValueError):
        load_model("InvalidModel", {})


def test_load_invalid_optimizer():
    from models.cnn import CNNModel
    model = CNNModel(num_classes=10)
    with pytest.raises(ValueError):
        load_optimizer({"type": "InvalidOptimizer", "params": {}}, model)


def test_load_invalid_scheduler():
    from models.cnn import CNNModel
    model = CNNModel(num_classes=10)
    optimizer = optim.Adam(model.parameters())
    with pytest.raises(ValueError):
        load_scheduler({"type": "InvalidScheduler", "params": {}}, optimizer)
