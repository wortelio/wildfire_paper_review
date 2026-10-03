import torch
import torch.nn as nn
from torch.nn import Conv2d
from torch.nn import ReLU
from torch.nn import Linear
from torch.nn import BatchNorm1d
from torch.nn import BatchNorm2d
from torch.nn import MaxPool2d
from torch.nn import AvgPool2d
from torch.nn import Module
from torch.nn import ModuleList
import math


def conv3x3(inp, oup):
    return [
        Conv2d(inp, oup, 3, 1, 1, bias=False),
        BatchNorm2d(oup),
        ReLU(),
    ]

def conv3x3_maxpool(inp, oup):
    conv3x3_mod = nn.Sequential(*conv3x3(inp, oup))
    conv3x3_mod.add_module("3", MaxPool2d(2))
    return conv3x3_mod    

def conv1x1(inp, oup):
    return [
        Conv2d(inp, oup, 1, 1, 0, bias=False),
        BatchNorm2d(oup),
        ReLU(),
    ]

class ConvBlock(Module):
    def __init__(self, inp_pre, down, up, pooling):
        super(ConvBlock, self).__init__()

        self.conv_1 = nn.Sequential(*self.__conv_mod__(inp_pre, down, up))
        self.conv_2 = nn.Sequential(*self.__conv_mod__(up, down, up))
        self.pooling = MaxPool2d(2) if pooling=="maxpool" else AvgPool2d(7)
     
    def __conv_mod__(self, inp_pre, down, up):
        return [
            *conv1x1(inp_pre, down), 
            *conv3x3(down, up),
        ]   
            
    def forward(self, x):
        x = self.conv_1(x)
        x = x + self.conv_2(x)
        x = self.pooling(x)
        return x
    
    
def linear(inp, oup):
    return nn.Sequential(
        Linear(inp, oup, bias=False),
        BatchNorm1d(oup),
        ReLU(),
    )
        


    
class Torch_CNV_w1a1_Balanced_Resnet_bram(Module):

    def __init__(self, 
                 num_classes=2, 
                 in_channels=3):
        super(Torch_CNV_w1a1_Balanced_Resnet_bram, self).__init__()

        self.num_classes = num_classes
        self.in_channels = in_channels
        
        # [conv3x3, out]
        # [convblk, out_a, out_b, maxpool/avgpool] 
        # [linear, out]
        self.conv_cfgs = [
            ["conv3x3", 8],
            ["conv3x3", 14],
            ["convblk", 16, 28, "maxpool"],
            ["convblk", 30, 60, "maxpool"],
            ["convblk", 60, 120, "maxpool"],
            ["convblk", 120, 240, "avgpool"]
        ]
        self.linear_cfgs = [ 
            ["linear", 120],
            ["linear", 64],
            ["linear", self.num_classes, "classifier"]
        ]
        
        conv_layers = []
        inp = self.in_channels
        for cfg in self.conv_cfgs:
            if cfg[0] == "conv3x3":
                oup = cfg[1]
                conv_layers.append(conv3x3_maxpool(inp, oup))
                inp = oup
            elif cfg[0] == "convblk":
                oup = cfg[2]
                conv_layers.append(ConvBlock(inp, cfg[1], cfg[2], cfg[3]))
                inp = oup
            else:
                raise Exception("Wrong Conv Layer config")
        self.features = nn.Sequential(*conv_layers)
        
        linear_layers = []
        for cfg in self.linear_cfgs:
            if cfg[0] == "linear":
                oup = cfg[1]
                if "classifier" in cfg:
                    linear_layers.append(Linear(inp, self.num_classes))
                else:
                    linear_layers.append(linear(inp, oup))
                    inp = oup
            else:
                raise Exception("Wrong Conv Layer config")
        self.linears = nn.Sequential(*linear_layers)      
        
        self._initialize_weights()

    def forward(self, x):
        x = 2.0 * x - torch.tensor([1.0], device=x.device)
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.linears(x)
        return x
    
    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
                if m.bias is not None:
                    m.bias.data.zero_()
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()
            elif isinstance(m, nn.Linear):
                m.weight.data.normal_(0, 0.01)
                if m.bias is not None:
                    m.bias.data.zero_()

