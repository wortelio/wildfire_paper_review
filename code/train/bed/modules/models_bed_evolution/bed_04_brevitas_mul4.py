import torch
import torch.nn as nn 
from torch.nn import BatchNorm1d
from torch.nn import BatchNorm2d
from torch.nn import MaxPool2d

from brevitas.core.restrict_val import RestrictValueType

from brevitas.nn import QuantConv2d
from brevitas.nn import QuantLinear
from brevitas.nn import QuantReLU
from brevitas.nn import QuantIdentity
from brevitas.nn import TruncAvgPool2d
from brevitas.quant import Int32Bias

from brevitas.quant import TruncTo8bit

from modules.models_bed_evolution.brevitas_common import CommonIntWeightPerChannelQuant
#from brevitas_common import CommonIntWeightPerTensorQuant
from modules.models_bed_evolution.brevitas_common import CommonUintActQuant
from modules.models_bed_evolution.brevitas_common import CommonIntActQuant

from modules.models_bed_evolution.tensor_norm import TensorNorm



def conv_3x3_bn_relu(inp, oup, weight_bit_width, act_bit_width, last):
    return_true = True if last == True else False
    return nn.Sequential(
        QuantConv2d(
            in_channels=inp,
            out_channels=oup,
            kernel_size=3,
            stride=1,
            padding=1,
            bias=False,
            weight_quant=CommonIntWeightPerChannelQuant,
            weight_bit_width=weight_bit_width),
        nn.BatchNorm2d(oup),
        QuantReLU(
            act_quant=CommonUintActQuant,
            bit_width=act_bit_width,
            return_quant_tensor=return_true),
    )

def svd_conv_3x3_bn_relu(inp, mid, oup, weight_bit_width, act_bit_width, last):
    return_true = True if last == True else False
    return nn.Sequential(
        QuantConv2d(
            in_channels=inp,
            out_channels=mid,
            kernel_size=(3,1),
            stride=1,
            padding=(1,0),
            bias=False,
            weight_quant=CommonIntWeightPerChannelQuant,
            weight_bit_width=weight_bit_width),
        nn.BatchNorm2d(mid),
        QuantIdentity(
            act_quant = CommonIntActQuant,
            bit_width = act_bit_width,
            narrow_range = False),
        QuantConv2d(
            in_channels=mid,
            out_channels=oup,
            kernel_size=(1,3),
            stride=1,
            padding=(0,1),
            bias=False,
            weight_quant=CommonIntWeightPerChannelQuant,
            weight_bit_width=weight_bit_width),
        nn.BatchNorm2d(oup),
        QuantReLU(
            act_quant=CommonUintActQuant,
            bit_width=act_bit_width,
            return_quant_tensor=return_true),
    )


    
def conv_1x1_bn_relu(inp, oup, weight_bit_width, act_bit_width, last):
    return_true = True if last == True else False
    return nn.Sequential(
        QuantConv2d(
            in_channels=inp,
            out_channels=oup,
            kernel_size=1,
            stride=1,
            padding=0,
            bias=False,
            weight_quant=CommonIntWeightPerChannelQuant,
            weight_bit_width=weight_bit_width),
        nn.BatchNorm2d(oup),
        QuantReLU(
            act_quant=CommonUintActQuant,
            bit_width=act_bit_width,
            return_quant_tensor=return_true),
    )


def svd_conv_1x1_bn_relu(inp, mid, oup, weight_bit_width, act_bit_width, last):
    return_true = True if last == True else False
    return nn.Sequential(
        QuantConv2d(
            in_channels=inp,
            out_channels=mid,
            kernel_size=(1,1),
            stride=1,
            padding=(0,0),
            bias=False,
            weight_quant=CommonIntWeightPerChannelQuant,
            weight_bit_width=weight_bit_width),
        nn.BatchNorm2d(mid),
        QuantIdentity(
            act_quant = CommonIntActQuant,
            bit_width = act_bit_width,
            narrow_range = False),
        QuantConv2d(
            in_channels=mid,
            out_channels=oup,
            kernel_size=(1,1),
            stride=1,
            padding=(0,0),
            bias=False,
            weight_quant=CommonIntWeightPerChannelQuant,
            weight_bit_width=weight_bit_width),
        nn.BatchNorm2d(oup),
        QuantReLU(
            act_quant=CommonUintActQuant,
            bit_width=act_bit_width,
            return_quant_tensor=return_true),
    )



class BED_AIMET_FPGA_MUL4(nn.Module):
    def __init__(self, num_classes=2, 
                 in_bit_width=8,
                 weight_bit_width=4,
                 act_bit_width=4):
        super(BED_AIMET_FPGA_MUL4, self).__init__()

        self.cfgs = [
            # [conv3x3/svd_conv3x3/conv1x1/svd_conv1x1/mp, (inp, mid(opt), oup)]
            ["svd_conv3x3", (3, 8, 28)],               # conv1
            ["mp"],
            ["svd_conv3x3", (28, 24, 16)],             # conv2
            ["mp"],
            ["conv1x1", (16, 16)],                     # conv31
            ["conv3x3", (16, 32)],                     # conv32
            ["conv1x1", (32, 32)],                     # conv33
            ["svd_conv3x3", (32, 52, 56)],             # conv34
            ["mp"],
            ["conv1x1", (56, 32)],                     # conv41
            ["svd_conv3x3", (32, 44, 64)],              # conv42
            ["conv1x1", (64, 32)],                     # conv43
            ["svd_conv3x3", (32, 32, 64)],             # conv44
            ["svd_conv1x1", (64, 12, 32)],             # conv45
            ["svd_conv3x3", (32, 8, 64), "last"],      # conv46            
        ]
        
        # Input 224x224x3
        layers = [
                QuantIdentity( # for Q1.7 input format -> sign.7bits
                act_quant = CommonIntActQuant,
                bit_width = in_bit_width,
                min_val = -1.0,
                max_val = 1.0 - 2.0 ** (-7),
                narrow_range = False, 
                restrict_scaling_type = RestrictValueType.POWER_OF_TWO)
        ]
        
        for cfg in self.cfgs:
            if len(cfg) > 1:
                layer_type = cfg[0]
                channels = cfg[1] 
                if len(cfg) == 2:
                    return_true = False
                elif cfg[2] == "last" and len(cfg) == 3:
                    return_true = True
                else:
                    raise SystemExit("Error in config definition: len > 1")
                if layer_type == "svd_conv3x3":
                    layers.append(svd_conv_3x3_bn_relu(channels[0], channels[1], channels[2], weight_bit_width, act_bit_width, return_true))   
                elif layer_type== "svd_conv1x1":
                    layers.append(svd_conv_1x1_bn_relu(channels[0], channels[1], channels[2], weight_bit_width, act_bit_width, return_true))   
                elif layer_type == "conv3x3":
                    layers.append(conv_3x3_bn_relu(channels[0], channels[1], weight_bit_width, act_bit_width, return_true))   
                elif layer_type == "conv1x1":
                    layers.append(conv_1x1_bn_relu(channels[0], channels[1], weight_bit_width, act_bit_width, return_true))   
            elif cfg[0] == "mp" and len(cfg) == 1:
                layers.append(MaxPool2d(kernel_size=2, stride=2)) 
            else:
                raise SystemExit("Error in config definition")
            
        self.features = nn.Sequential(*layers)
        
        # building last several layers       
        self.avgpool = TruncAvgPool2d(
                kernel_size=28,  
                trunc_quant=TruncTo8bit,
                float_to_int_impl_type='FLOOR')

        linears = []
        # Linear 1
        linears.append(
            QuantLinear(
                in_features=64,
                out_features=16,
                bias=False,
                weight_quant=CommonIntWeightPerChannelQuant,
                weight_bit_width=weight_bit_width))
        linears.append(BatchNorm1d(16))
        linears.append(
            QuantReLU(
                act_quant=CommonUintActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=False))
        # Linear 2
        linears.append(
            QuantLinear(
                in_features=16,
                out_features=num_classes,
                bias=False,
                weight_quant=CommonIntWeightPerChannelQuant,
                weight_bit_width=8))
        linears.append(TensorNorm())

        self.classifier = nn.Sequential(*linears)

        
    def forward(self, x):
        x = 2.0 * x - torch.tensor([1.0], device=x.device)
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x
