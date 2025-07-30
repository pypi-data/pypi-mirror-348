# -*- coding: utf-8 -*-
# @Author  : LG
#https://github.com/yatengLG/Focal-Loss-Pytorch/blob/master/Focal_Loss.py
from torch import nn
import torch
from torch.nn import functional as F

class FocalLoss(nn.Module):
    def __init__(self, alpha=None, gamma=2, num_classes=3, size_average=True, multi_label=False):
        """
        focal_loss损失函数
        :param alpha: 类别权重
        :param gamma: 难易样本调节参数
        :param num_classes: 类别数量
        :param size_average: 损失计算方式,默认取均值
        :param multi_label: 是否为多标签分类
        """
        super(FocalLoss, self).__init__()
        self.size_average = size_average
        self.multi_label = multi_label
        if alpha is None:
            self.alpha = torch.ones(num_classes)
        elif isinstance(alpha, list):
            assert len(alpha) == num_classes
            self.alpha = torch.Tensor(alpha)
        else:
            assert alpha < 1
            self.alpha = torch.zeros(num_classes)
            self.alpha[0] += alpha
            self.alpha[1:] += (1-alpha)

        self.gamma = gamma
        
    def forward(self, preds, labels):
        # 基於標籤形狀自動檢測是否為多標籤任務
        is_multilabel = (len(labels.shape) > 1 and labels.shape[1] > 1)
        
        if is_multilabel:
            if preds.shape != labels.shape:
                raise ValueError(f"多標籤模式下，預測形狀 {preds.shape} 應與標籤形狀 {labels.shape} 一致")
            
            # 確保 alpha 在正確的設備上
            alpha = self.alpha.to(preds.device)
            
            # 多標籤版本的實現
            sigmoid_p = torch.sigmoid(preds)
            zeros = torch.zeros_like(sigmoid_p)
            pos_p_sub = torch.where(labels > 0.5, 1.0 - sigmoid_p, zeros)
            neg_p_sub = torch.where(labels <= 0.5, sigmoid_p, zeros)
            
            # 應用gamma聚焦
            pos_loss = labels * torch.pow(pos_p_sub, self.gamma) * torch.log(torch.clamp(sigmoid_p, min=1e-8))
            neg_loss = (1.0 - labels) * torch.pow(neg_p_sub, self.gamma) * torch.log(torch.clamp(1.0 - sigmoid_p, min=1e-8))
            
            # 應用alpha平衡
            if isinstance(alpha, torch.Tensor):
                alpha_pos = alpha.unsqueeze(0).expand_as(pos_loss)
                alpha_neg = 1.0 - alpha_pos
                pos_loss = pos_loss * alpha_pos
                neg_loss = neg_loss * alpha_neg
            
            loss = -(pos_loss + neg_loss)
            
            # 根據 size_average 參數縮減損失
            if self.size_average:
                return loss.mean()
            else:
                return loss.sum()
        else:
            # 單標籤版本
            labels = labels.long()  # 確保標籤是長整型
            
            # 確保 alpha 在正確的設備上
            alpha = self.alpha.to(preds.device)
            
            # 計算交叉熵損失
            preds_logsoft = F.log_softmax(preds, dim=1)
            preds_softmax = torch.exp(preds_logsoft)
            
            # 獲取正確類別的預測概率
            preds_softmax = preds_softmax.gather(1, labels.view(-1, 1))
            preds_logsoft = preds_logsoft.gather(1, labels.view(-1, 1))
            
            # 獲取相應的 alpha 值
            alpha = alpha.gather(0, labels.view(-1))
            
            # 計算 Focal Loss
            loss = -torch.mul(torch.pow((1 - preds_softmax), self.gamma), preds_logsoft)
            
            # 應用 alpha 權重
            loss = alpha * loss.view(-1)
            
            # 根據設置取均值或總和
            if self.size_average:
                return loss.mean()
            else:
                return loss.sum()