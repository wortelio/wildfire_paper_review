import torch
from torch.nn import BatchNorm1d
from torch.nn import BatchNorm2d
from torch.nn import MaxPool2d
from torch.nn import Module
from torch.nn import ModuleList

from brevitas.quant_tensor import QuantTensor

from brevitas.core.restrict_val import RestrictValueType
from brevitas.nn import QuantIdentity
from brevitas.nn import QuantConv2d
from brevitas.nn import QuantReLU # -> replaced by QuantIdentity -> Bipolar Network
from brevitas.nn import TruncAvgPool2d
from brevitas.nn import QuantLinear

from brevitas.quant import TruncTo8bit

from modules.models.brevitas_example_common import CommonActQuant
from modules.models.brevitas_example_common import CommonWeightQuant
from modules.models.tensor_norm import TensorNorm

# For Linear Layers at the end of the model
from modules.models.common_imagenet import CommonIntWeightPerTensorQuant
from modules.models.common_imagenet import CommonIntWeightPerChannelQuant
from modules.models.common_imagenet import CommonIntActQuant
from modules.models.common_imagenet import CommonUintActQuant


#import config

class MyWeightsQuant_PerTensor(CommonIntWeightPerTensorQuant):
    restrict_scaling_type = RestrictValueType.POWER_OF_TWO

class MyWeightsQuant_PerChannel(CommonIntWeightPerChannelQuant):
    restrict_scaling_type = RestrictValueType.POWER_OF_TWO

    
class CNV_w1a1_DEEP_Resnet_V3_NOMAXPOOL(Module):

    def __init__(self, 
                 num_classes=2, 
                 weight_bit_width=1, 
                 act_bit_width=1, 
                 in_bit_width=8, 
                 in_channels=3):
        super(CNV_w1a1_DEEP_Resnet_V3_NOMAXPOOL, self).__init__()

        self.num_classes = num_classes
        self.in_channels = in_channels
        self.return_quant_tensor = False
        self.return_quant_tensor_add_pool = True
        
        self.conv_features_0 = ModuleList()
        # Residual Block 1
        self.conv_features_1_0 = ModuleList()
        self.conv_features_1_1 = ModuleList()
        # Residual Block 2
        self.conv_features_2_0 = ModuleList()
        self.conv_features_2_1 = ModuleList()
        # Residual Block 3
        self.conv_features_3_0 = ModuleList()
        self.conv_features_3_1 = ModuleList()
        # Residual Block 4
        self.conv_features_4_0 = ModuleList()
        
        self.linear_features = ModuleList()

        # Input 224x224x3
        self.conv_features_0.append(
            QuantIdentity( # for Q1.7 input format -> sign.7bits
                act_quant = CommonActQuant,
                bit_width = in_bit_width,
                min_val = -1.0,
                max_val = 1.0 - 2.0 ** (-7),
                narrow_range = False,
                restrict_scaling_type = RestrictValueType.POWER_OF_TWO))

        # CNNBlock 224x224
        # conv1
        self.conv_features_0.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=self.in_channels,
                out_channels=64,
                bias=False,
                weight_quant=MyWeightsQuant_PerChannel,
                weight_bit_width=4))
        self.conv_features_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_0.append(
            QuantReLU(
                act_quant=CommonUintActQuant,
                bit_width=4, 
                restrict_scaling_type = RestrictValueType.POWER_OF_TWO, 
                return_quant_tensor=self.return_quant_tensor))
        
        self.conv_features_0.append(MaxPool2d(kernel_size=2, stride=2))

        # CNNBlock 112x112
        # conv2
        self.conv_features_0.append(
            QuantConv2d(
                kernel_size=3, stride=2, padding=1,
                in_channels=64,
                out_channels=32,
                bias=False,
                weight_quant=MyWeightsQuant_PerChannel,
                weight_bit_width=4))
        self.conv_features_0.append(BatchNorm2d(32, eps=1e-4))
        # Quantize BIPOLAR to enter residuals part
        self.conv_features_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor_add_pool))
        
        # self.conv_features_0.append(MaxPool2d(kernel_size=2, stride=2))

        # CNNBlock 56x56 
        # conv31
        self.conv_features_1_0.append(
            QuantConv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=32,
                out_channels=16,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_1_0.append(BatchNorm2d(16, eps=1e-4))
        self.conv_features_1_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))            
        # conv32
        self.conv_features_1_0.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=16,
                out_channels=32,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_1_0.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features_1_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv33
        self.conv_features_1_0.append(
            QuantConv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=32,
                out_channels=32,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_1_0.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features_1_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor_add_pool))
        # conv34
        self.conv_features_1_1.append(
            QuantConv2d(
                kernel_size=3, stride=2, padding=1,
                in_channels=32,
                out_channels=64,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_1_1.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_1_1.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor_add_pool))
        
        # self.conv_features_1_1.append(MaxPool2d(kernel_size=2, stride=2))

        # CNNBlock 28x28 
        # conv41
        self.conv_features_2_0.append(
            QuantConv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=64,
                out_channels=32,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_2_0.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features_2_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv42
        self.conv_features_2_0.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=32,
                out_channels=64,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_2_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_2_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv43
        self.conv_features_2_0.append(
            QuantConv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=64,
                out_channels=32,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_2_0.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features_2_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv44
        self.conv_features_2_0.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=32,
                out_channels=64,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_2_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_2_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv45
        self.conv_features_2_0.append(
            QuantConv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=64,
                out_channels=64,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_2_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_2_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor_add_pool))
        # conv46
        self.conv_features_2_1.append(
            QuantConv2d(
                kernel_size=3, stride=2, padding=1,
                in_channels=64,
                out_channels=96,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_2_1.append(BatchNorm2d(96, eps=1e-4))
        self.conv_features_2_1.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor_add_pool))

        # self.conv_features_2_1.append(MaxPool2d(kernel_size=2, stride=2))

        # CNNBlock 14x14 
        # conv51
        self.conv_features_3_0.append(
            QuantConv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=96,
                out_channels=48,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_3_0.append(BatchNorm2d(48, eps=1e-4))
        self.conv_features_3_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv52
        self.conv_features_3_0.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=48,
                out_channels=96,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_3_0.append(BatchNorm2d(96, eps=1e-4))
        self.conv_features_3_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv53
        self.conv_features_3_0.append(
            QuantConv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=96,
                out_channels=48,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_3_0.append(BatchNorm2d(48, eps=1e-4))
        self.conv_features_3_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv54
        self.conv_features_3_0.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=48,
                out_channels=96,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_3_0.append(BatchNorm2d(96, eps=1e-4))
        self.conv_features_3_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv55
        self.conv_features_3_0.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=96,
                out_channels=96,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_3_0.append(BatchNorm2d(96, eps=1e-4))
        self.conv_features_3_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor_add_pool))
        # conv56
        self.conv_features_3_1.append(
            QuantConv2d(
                kernel_size=3, stride=2, padding=1,
                in_channels=96,
                out_channels=128,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_3_1.append(BatchNorm2d(128, eps=1e-4))
        self.conv_features_3_1.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor_add_pool))

        # self.conv_features_3_1.append(MaxPool2d(kernel_size=2, stride=2))

        # CNNBlock 7x7
        # conv61
        self.conv_features_4_0.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=128,
                out_channels=128,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_4_0.append(BatchNorm2d(128, eps=1e-4))
        self.conv_features_4_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor))
        # conv62
        self.conv_features_4_0.append(
            QuantConv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=128,
                out_channels=128,
                bias=False,
                weight_quant=CommonWeightQuant,
                weight_bit_width=weight_bit_width))
        self.conv_features_4_0.append(BatchNorm2d(128, eps=1e-4))
        self.conv_features_4_0.append(
            QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor_add_pool))
     
        
       # Average Pooling
        self.avg_pool = TruncAvgPool2d(
                kernel_size=7,
                trunc_quant=TruncTo8bit,
                float_to_int_impl_type='FLOOR')

        # Linear 1
        self.linear_features.append(
            QuantLinear(
                in_features=128,
                out_features=64,
                bias=False,
                weight_quant=MyWeightsQuant_PerTensor,
                weight_bit_width=4)) 
        self.linear_features.append(BatchNorm1d(64, eps=1e-4))
        self.linear_features.append(
            QuantReLU(
                act_quant=CommonUintActQuant,
                bit_width=4, 
                restrict_scaling_type = RestrictValueType.POWER_OF_TWO, # added for linear4 in cnv_w1a1_deep_resnet
                return_quant_tensor=self.return_quant_tensor))
        # Linear 2
        self.linear_features.append(
            QuantLinear(
                in_features=64,
                out_features=32,
                bias=False,
                weight_quant=MyWeightsQuant_PerTensor,
                weight_bit_width=4)) 
        self.linear_features.append(BatchNorm1d(32, eps=1e-4))
        self.linear_features.append(
            QuantReLU(
                act_quant=CommonUintActQuant,
                bit_width=4, 
                restrict_scaling_type = RestrictValueType.POWER_OF_TWO, # added for linear4 in cnv_w1a1_deep_resnet
                return_quant_tensor=self.return_quant_tensor))
        # Linear 3
        self.linear_features.append(
            QuantLinear(
                in_features=32,
                out_features=self.num_classes,
                bias=False,
                weight_quant=MyWeightsQuant_PerTensor,
                weight_bit_width=4)) 
        self.linear_features.append(TensorNorm())

        # Residuals Quantizers
        self.id_res_0 = QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor_add_pool)
        self.id_res_1 = QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor_add_pool)
        self.id_res_2 = QuantIdentity(
                act_quant=CommonActQuant,
                bit_width=act_bit_width, 
                return_quant_tensor=self.return_quant_tensor_add_pool)
        # self.id_res_3 = QuantIdentity(
        #         act_quant=CommonActQuant,
        #         bit_width=act_bit_width, 
        #         return_quant_tensor=self.return_quant_tensor_add_pool)
        self.id_res_3 = QuantReLU(
                act_quant=CommonUintActQuant,
                bit_width=4, 
                restrict_scaling_type = RestrictValueType.POWER_OF_TWO, 
                return_quant_tensor=self.return_quant_tensor_add_pool)

        for m in self.modules():
            if isinstance(m, QuantConv2d) or isinstance(m, QuantLinear):
                torch.nn.init.uniform_(m.weight.data, -1, 1)

    def clip_weights(self, min_val, max_val):
        # for mod in self.conv_features_0:
        #     if isinstance(mod, QuantConv2d):
        #         mod.weight.data.clamp_(min_val, max_val)
        for mod in self.conv_features_1_0:
            if isinstance(mod, QuantConv2d):
                mod.weight.data.clamp_(min_val, max_val)
        for mod in self.conv_features_1_1:
            if isinstance(mod, QuantConv2d):
                mod.weight.data.clamp_(min_val, max_val)
        for mod in self.conv_features_2_0:
            if isinstance(mod, QuantConv2d):
                mod.weight.data.clamp_(min_val, max_val)
        for mod in self.conv_features_2_1:
            if isinstance(mod, QuantConv2d):
                mod.weight.data.clamp_(min_val, max_val)
        for mod in self.conv_features_3_0:
            if isinstance(mod, QuantConv2d):
                mod.weight.data.clamp_(min_val, max_val)
        for mod in self.conv_features_3_1:
            if isinstance(mod, QuantConv2d):
                mod.weight.data.clamp_(min_val, max_val)
        for mod in self.conv_features_4_0:
            if isinstance(mod, QuantConv2d):
                mod.weight.data.clamp_(min_val, max_val)
        
        # Do not clip Linear if bit_width != 1
        # for mod in self.linear_features:
        #     if isinstance(mod, QuantLinear):
        #         mod.weight.data.clamp_(min_val, max_val)

    def forward(self, x):
        x = 2.0 * x - torch.tensor([1.0], device=x.device)
        for mod in self.conv_features_0:
            x = mod(x)
        
        for i, mod in enumerate(self.conv_features_1_0):
            if i == 0:
                x_res = mod(x)
            else:
                x_res = mod(x_res)
        assert isinstance(x, QuantTensor), "Perform add among QuantTensors"
        assert isinstance(x_res, QuantTensor), "Perform add among QuantTensors"
        x = x + x_res
        x = self.id_res_0(x)
        for mod in self.conv_features_1_1:
            x = mod(x)

        for i, mod in enumerate(self.conv_features_2_0):
            if i == 0:
                x_res = mod(x)
            else:
                x_res = mod(x_res)
        assert isinstance(x, QuantTensor), "Perform add among QuantTensors"
        assert isinstance(x_res, QuantTensor), "Perform add among QuantTensors"
        x = x + x_res
        x = self.id_res_1(x)
        for mod in self.conv_features_2_1:
            x = mod(x)

        for i, mod in enumerate(self.conv_features_3_0):
            if i == 0:
                x_res = mod(x)
            else:
                x_res = mod(x_res)
        assert isinstance(x, QuantTensor), "Perform add among QuantTensors"
        assert isinstance(x_res, QuantTensor), "Perform add among QuantTensors"
        x = x + x_res
        x = self.id_res_2(x)
        for mod in self.conv_features_3_1:
            x = mod(x)
        
        for i, mod in enumerate(self.conv_features_4_0):
            if i == 0:
                x_res = mod(x)
            else:
                x_res = mod(x_res)
        assert isinstance(x, QuantTensor), "Perform add among QuantTensors"
        assert isinstance(x_res, QuantTensor), "Perform add among QuantTensors"
        x = x + x_res
        x = self.id_res_3(x)
        
        x = self.avg_pool(x)
        
        x = x.view(x.shape[0], -1)
        for mod in self.linear_features:
            x = mod(x)
        return x

