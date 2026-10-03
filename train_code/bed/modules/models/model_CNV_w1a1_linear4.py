import torch
from torch.nn import BatchNorm1d
from torch.nn import BatchNorm2d
from torch.nn import MaxPool2d
from torch.nn import Module
from torch.nn import ModuleList

from brevitas.core.restrict_val import RestrictValueType
from brevitas.nn import QuantIdentity
from brevitas.nn import QuantConv2d
from brevitas.nn import TruncAvgPool2d
from brevitas.nn import QuantLinear

from brevitas.quant import TruncTo8bit

from .brevitas_example_common import CommonActQuant
from .brevitas_example_common import CommonWeightQuant
from .tensor_norm import TensorNorm

# For Linear Layers at the end of the model
from modules.models.common_imagenet import CommonIntWeightPerTensorQuant
from modules.models.common_imagenet import CommonIntActQuant


import config

    
class CNV_w1a1_linear4(Module):

    def __init__(self, 
                 num_classes=config.NUM_CLASSES, 
                 weight_bit_width=1, 
                 act_bit_width=1, 
                 in_bit_width=8, 
                 in_channels=3):
        super(CNV_w1a1_linear4, self).__init__()

        self.num_classes = num_classes
        self.in_channels = in_channels
        self.return_quant_tensor = False
        
        self.conv_features = ModuleList()
        self.linear_features = ModuleList()

        # Input 224x224x3
        self.conv_features.append(
            QuantIdentity( # for Q1.7 input format -> sign.7bits
                act_quant = CommonActQuant,
                bit_width = in_bit_width,
                min_val = -1.0,
                max_val = 1.0 - 2.0 ** (-7),
                narrow_range = False,
                restrict_scaling_type = RestrictValueType.POWER_OF_TWO))

        # CNNBlock 224x224
            # conv1
        self.conv_features.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=0,
                in_channels=self.in_channels,
                out_channels=32,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        
        self.conv_features.append(MaxPool2d(kernel_size=2, stride=2))

        # CNNBlock 112x112
            # conv2
        self.conv_features.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=0,
                in_channels=32,
                out_channels=16,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features.append(BatchNorm2d(16, eps=1e-4))
        self.conv_features.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        
        self.conv_features.append(MaxPool2d(kernel_size=2, stride=2))

        # CNNBlock 56x56 
            # conv31
        self.conv_features.append(
            QuantConv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=16,
                out_channels=16,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features.append(BatchNorm2d(16, eps=1e-4))
        self.conv_features.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))            
        # conv32
        self.conv_features.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=0,
                in_channels=16,
                out_channels=32,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv33
        self.conv_features.append(
            QuantConv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=32,
                out_channels=32,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv34
        self.conv_features.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=0,
                in_channels=32,
                out_channels=64,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        
        self.conv_features.append(MaxPool2d(kernel_size=2, stride=2))

        # CNNBlock 28x28 
            # conv41
        self.conv_features.append(
            QuantConv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=64,
                out_channels=32,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv42
        self.conv_features.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=0,
                in_channels=32,
                out_channels=64,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv43
        self.conv_features.append(
            QuantConv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=64,
                out_channels=32,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv44
        self.conv_features.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=0,
                in_channels=32,
                out_channels=64,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv45
        self.conv_features.append(
            QuantConv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=64,
                out_channels=32,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv46
        self.conv_features.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=0,
                in_channels=32,
                out_channels=64,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=True))
        
       # Average Pooling
        self.conv_features.append(TruncAvgPool2d(
                kernel_size=20,
                trunc_quant=TruncTo8bit,
                float_to_int_impl_type='FLOOR'))
        # self.conv_features.append(
        #     QuantIdentity(
        #         act_quant=CommonActQuant,
        #         bit_width=4, 
        #         return_quant_tensor=self.return_quant_tensor))

        # Linear 1
        self.linear_features.append(
            QuantLinear(
                in_features=64,
                out_features=16,
                bias=False,
                weight_quant=CommonIntWeightPerTensorQuant,
                weight_bit_width=4))
        self.linear_features.append(BatchNorm1d(16, eps=1e-4))
        self.linear_features.append(
            QuantIdentity(
                act_quant=CommonIntActQuant,
                bit_width=4,
                restrict_scaling_type = RestrictValueType.POWER_OF_TWO,
                return_quant_tensor=self.return_quant_tensor))
        # Linear 2
        self.linear_features.append(
            QuantLinear(
                in_features=16,
                out_features=self.num_classes,
                bias=False,
                weight_quant=CommonIntWeightPerTensorQuant,
                weight_bit_width=4))
        self.linear_features.append(TensorNorm())

        for m in self.modules():
            if isinstance(m, QuantConv2d) or isinstance(m, QuantLinear):
                torch.nn.init.uniform_(m.weight.data, -1, 1)

    def clip_weights(self, min_val, max_val):
        for mod in self.conv_features:
            if isinstance(mod, QuantConv2d):
                mod.weight.data.clamp_(min_val, max_val)
        for mod in self.linear_features:
            if isinstance(mod, QuantLinear):
                mod.weight.data.clamp_(min_val, max_val)

    def forward(self, x):
        x = 2.0 * x - torch.tensor([1.0], device=x.device)
        for mod in self.conv_features:
            x = mod(x)
        x = x.view(x.shape[0], -1)
        for mod in self.linear_features:
            x = mod(x)
        return x

