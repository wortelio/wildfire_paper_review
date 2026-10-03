import torch
import torch.nn as nn
from torch.nn import BatchNorm1d
from torch.nn import BatchNorm2d
from torch.nn import MaxPool2d
from torch.nn import Module
from torch.nn import ModuleList

from brevitas.quant_tensor import QuantTensor

from brevitas.core.restrict_val import RestrictValueType
from brevitas.nn import QuantIdentity
from brevitas.nn import QuantConv2d
from brevitas.nn import QuantReLU # -> replaced by QuantIdentity -> Bipolar Network. Kept for Linears
from brevitas.nn import TruncAvgPool2d
from brevitas.nn import QuantLinear

from brevitas.quant import TruncTo8bit

from modules.models.brevitas_example_common import CommonActQuant
from modules.models.brevitas_example_common import CommonWeightQuant
from modules.models.tensor_norm import TensorNorm

# For Linear Layers at the end of the model
from modules.models.common_imagenet import CommonIntWeightPerTensorQuant
from modules.models.common_imagenet import CommonIntActQuant
from modules.models.common_imagenet import CommonUintActQuant


def conv3x3(inp, oup, conv_bit_width):
    return [
        QuantConv2d(
            kernel_size=3, stride=1, padding=1,
            in_channels=inp,
            out_channels=oup,
            bias=False,
            weight_quant=CommonWeightQuant,
            weight_bit_width=conv_bit_width),
        BatchNorm2d(oup, eps=1e-4),
        QuantIdentity(
            act_quant=CommonActQuant,
            bit_width=conv_bit_width, 
            return_quant_tensor=True)
    ]

def conv3x3_maxpool(inp, oup, conv_bit_width=1):
    conv3x3_mod = nn.Sequential(*conv3x3(inp, oup, conv_bit_width))
    conv3x3_mod.add_module("3", MaxPool2d(2))
    return conv3x3_mod    

def conv1x1(inp, oup):
    return [
        QuantConv2d(
            kernel_size=1, stride=1, padding=0,
            in_channels=inp,
            out_channels=oup,
            bias=False,
            weight_quant=CommonWeightQuant,
            weight_bit_width=1),
        BatchNorm2d(oup, eps=1e-4),
        QuantIdentity(
            act_quant=CommonActQuant,
            bit_width=1, 
            return_quant_tensor=False)
    ]

class ConvBlock(Module):
    def __init__(self, inp_pre, down, up, pooling):
        super(ConvBlock, self).__init__()

        self.conv_1 = nn.Sequential(*self.__conv_mod__(inp_pre, down, up))
        self.conv_2 = nn.Sequential(*self.__conv_mod__(up, down, up))
        self.quant_add = QuantIdentity(
            act_quant=CommonActQuant,
            bit_width=1, 
            return_quant_tensor=True)
        avg_pool = TruncAvgPool2d(
            kernel_size=7,
            trunc_quant=TruncTo8bit,
            float_to_int_impl_type='FLOOR')
        self.pooling = MaxPool2d(2) if pooling=="maxpool" else avg_pool
     
    def __conv_mod__(self, inp_pre, down, up):
        return [
            *conv1x1(inp_pre, down), 
            *conv3x3(down, up),
        ]   
            
    def forward(self, x):
        x = self.conv_1(x)
        x_res = self.conv_2(x)
        assert isinstance(x, QuantTensor), "Perform add among QuantTensors"
        assert isinstance(x_res, QuantTensor), "Perform add among QuantTensors"
        x = x + x_res
        x = self.quant_add(x)
        x = self.pooling(x)
        return x
    

class MyWeightsQuant_PerTensor(CommonIntWeightPerTensorQuant):
    restrict_scaling_type = RestrictValueType.POWER_OF_TWO
    
def linear(inp, oup):
    return nn.Sequential(
        QuantLinear(
            in_features=inp,
            out_features=oup,
            bias=False,
            weight_quant=MyWeightsQuant_PerTensor,
            weight_bit_width=4), 
        BatchNorm1d(oup),
        QuantReLU(
            act_quant=CommonUintActQuant,
            bit_width=4, 
            restrict_scaling_type = RestrictValueType.POWER_OF_TWO, 
            return_quant_tensor=False)
    )
        

class CNV_w1a1_Balanced_Resnet_bram(Module):

    def __init__(self, 
                 num_classes=2, 
                 in_channels=3):
        super(CNV_w1a1_Balanced_Resnet_bram, self).__init__()

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

        # CONV layers
        conv_layers = []
        conv_layers.append(QuantIdentity( # for Q1.7 input format -> sign.7bits
                act_quant = CommonIntActQuant,
                bit_width = 8,
                min_val = -1.0,
                max_val = 1.0 - 2.0 ** (-7),
                narrow_range = False,
                restrict_scaling_type = RestrictValueType.POWER_OF_TWO))
        inp = self.in_channels
        for cfg in self.conv_cfgs:
            if cfg[0] == "conv3x3":
                oup = cfg[1]
                conv_layers.append(conv3x3_maxpool(inp, oup, conv_bit_width=4))
                inp = oup
            elif cfg[0] == "convblk":
                oup = cfg[2]
                conv_layers.append(ConvBlock(inp, cfg[1], cfg[2], cfg[3]))
                inp = oup
            else:
                raise Exception("Wrong Conv Layer config")
        self.features = nn.Sequential(*conv_layers)

        # LINEAR layers
        linear_layers = []
        for cfg in self.linear_cfgs:
            if cfg[0] == "linear":
                oup = cfg[1]
                if "classifier" in cfg:
                    linear_layers.append(QuantLinear(
                        in_features=inp,
                        out_features=self.num_classes,
                        bias=False,
                        weight_quant=MyWeightsQuant_PerTensor,
                        weight_bit_width=4))
                    linear_layers.append(TensorNorm())
                else:
                    linear_layers.append(linear(inp, oup))
                    inp = oup
            else:
                raise Exception("Wrong Conv Layer config")
        self.linears = nn.Sequential(*linear_layers)   

        # INIT Weights
        self._initialize_weights()

    
    def clip_weights(self, min_val, max_val):
        for mod in self.features:
            if isinstance(mod, QuantConv2d):
                mod.weight.data.clamp_(min_val, max_val)

                
    def forward(self, x):
        x = 2.0 * x - torch.tensor([1.0], device=x.device)
        x = self.features(x)
        x = x.view(x.size(0), -1)
        x = self.linears(x)
        return x

    
    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, QuantConv2d):
                torch.nn.init.uniform_(m.weight.data, -1, 1)
            # elif isinstance(m, nn.BatchNorm2d):
            #     m.weight.data.fill_(1)
            #     m.bias.data.zero_()
            # elif isinstance(m, QuantLinear):
            #     m.weight.data.normal_(0, 0.01)
