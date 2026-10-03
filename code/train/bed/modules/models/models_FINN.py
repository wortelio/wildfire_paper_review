import collections
import torch
import torch.nn as nn 
import brevitas.nn as qnn
from brevitas.quant import Int8WeightPerTensorFloat, Uint8ActPerTensorFloat, Int8ActPerTensorFloat
from brevitas.quant import Int8Bias
from brevitas.inject.defaults import TruncTo8bit

import config

# ______________________________________________________________ #
# ___________________    Per Tensor Float   ____________________ #
# ____________________    No Batch Norm     ____________________ #
# ______________________________________________________________ #

class MyIntBias(Int8Bias):    
    """
    8-bit signed int bias quantizer with scale factor equal to the scale factor of the accumulator
    the bias is added to, so typically quant_input_scale * quant_weight_scale.
    """
    bit_width = config.BIAS_BIT_WIDTH
    #pass

class MyInt8Weight(Int8WeightPerTensorFloat):
    #scaling_per_output_channel = True
    #restrict_scaling_type = RestrictValueType.POWER_OF_TWO
    pass

   
class QUANT_PerTensorFloat_NoBN_BED_CLASSIFIER(nn.Module):
    def __init__(self, num_classes, 
                 weight_bw, 
                 big_layers_weight_bw,
                 act_bw, 
                 bias_bw, 
                 in_channels=3):
        super(QUANT_PerTensorFloat_NoBN_BED_CLASSIFIER, self).__init__()
        self.in_channels = in_channels
        self.last_channels = 64
        self.num_classes = num_classes

        self.weight_bw = weight_bw
        self.big_layers_weight_bw = big_layers_weight_bw
        self.act_bw = act_bw
        self.bias_bw = bias_bw
        
        self.model = self.__create_BED__()
        
    def __create_BED__(self):
        BED_model = nn.Sequential(

            collections.OrderedDict(
                [   
                    ("input0", qnn.QuantIdentity(
                                act_quant=Int8ActPerTensorFloat,        
                                return_quant_tensor=True)),
                   
                    # Conv2d [in_channels, out_channels, kernel_size, stride, padding, bias]
          
                    # CNNBlock 224x224
                    ("conv1", qnn.QuantConv2d(
                                self.in_channels, 32, 
                                kernel_size=3, stride=1, padding=1, 
                                weight_bit_width=self.weight_bw,
                                weight_quant=MyInt8Weight,
                                bias=True, 
                                bias_quant=MyIntBias)),
                    ("relu1", qnn.QuantReLU(
                                bit_width=self.act_bw, 
                                act_quant=Uint8ActPerTensorFloat,
                                return_quant_tensor=True)),
                    #("dropout1", nn.Dropout2d(p=0.3)),
        
                    # CNNBlock 112x112
                    ("maxpool2", qnn.QuantMaxPool2d(
                                kernel_size=2, stride=2,
                                return_quant_tensor=True)),
                    ("conv2", qnn.QuantConv2d(
                                32, 16, 
                                kernel_size=3, stride=1, padding=1, 
                                weight_bit_width=self.weight_bw,
                                weight_quant=MyInt8Weight,
                                bias=True, 
                                bias_quant=MyIntBias)),
                    ("relu2", qnn.QuantReLU(
                                bit_width=self.act_bw, 
                                act_quant=Uint8ActPerTensorFloat,
                                return_quant_tensor=True)),
                    #("dropout2",nn.Dropout2d(p=0.3)),

                    # CNNBlock 56x56     
                    ("maxpool3", qnn.QuantMaxPool2d(
                                kernel_size=2, stride=2,
                                return_quant_tensor=True)),
                    ("conv31", qnn.QuantConv2d(
                                16, 16, 
                                kernel_size=1, stride=1, padding=0, 
                                weight_bit_width=self.weight_bw,
                                weight_quant=MyInt8Weight,
                                bias=True, 
                                bias_quant=MyIntBias)),
                    ("relu31", qnn.QuantReLU(
                                bit_width=self.act_bw, 
                                act_quant=Uint8ActPerTensorFloat,
                                return_quant_tensor=True)),
                    
                    ("conv32", qnn.QuantConv2d(
                                16, 32, 
                                kernel_size=3, stride=1, padding=1, 
                                weight_bit_width=self.weight_bw,
                                weight_quant=MyInt8Weight,
                                bias=True,
                                bias_quant=MyIntBias)),
                    ("relu32", qnn.QuantReLU(
                                bit_width=self.act_bw, 
                                act_quant=Uint8ActPerTensorFloat,
                                return_quant_tensor=True)),
                    
                    ("conv33", qnn.QuantConv2d(32, 32, 
                                kernel_size=1, stride=1, padding=0, 
                                weight_bit_width=self.weight_bw,
                                weight_quant=MyInt8Weight,
                                bias=True, 
                                bias_quant=MyIntBias)),
                    ("relu33", qnn.QuantReLU(
                                bit_width=self.act_bw, 
                                act_quant=Uint8ActPerTensorFloat,
                                return_quant_tensor=True)),
                    
                    ("conv34", qnn.QuantConv2d(
                                32, 64, 
                                kernel_size=3, stride=1, padding=1, 
                                weight_bit_width=self.big_layers_weight_bw,
                                weight_quant=MyInt8Weight,
                                bias=True, 
                                bias_quant=MyIntBias)),
                    ("relu34", qnn.QuantReLU(
                                bit_width=self.act_bw, 
                                act_quant=Uint8ActPerTensorFloat,
                                return_quant_tensor=True)),
        
                    # CNNBlock 28x28                                      
                    ("maxpool4", qnn.QuantMaxPool2d(
                                kernel_size=2, stride=2,
                                return_quant_tensor=True)),
                    ("conv41", qnn.QuantConv2d(64, 32, 
                                kernel_size=1, stride=1, padding=0, 
                                weight_bit_width=self.weight_bw,
                                weight_quant=MyInt8Weight,
                                bias=True, 
                                bias_quant=MyIntBias)),
                    ("relu41", qnn.QuantReLU(
                                bit_width=self.act_bw, 
                                act_quant=Uint8ActPerTensorFloat,
                                return_quant_tensor=True)),
                    
                    ("conv42", qnn.QuantConv2d(32, 64, 
                                kernel_size=3, stride=1, padding=1, 
                                weight_bit_width=self.big_layers_weight_bw,
                                weight_quant=MyInt8Weight,
                                bias=True, 
                                bias_quant=MyIntBias)),
                    ("relu42", qnn.QuantReLU(
                                bit_width=self.act_bw, 
                                act_quant=Uint8ActPerTensorFloat,
                                return_quant_tensor=True)),
                    
                    ("conv43", qnn.QuantConv2d(
                                64, 32, 
                                kernel_size=1, stride=1, padding=0, 
                                weight_bit_width=self.weight_bw,
                                weight_quant=MyInt8Weight,
                                bias=True, 
                                bias_quant=MyIntBias)),
                    ("relu43", qnn.QuantReLU(
                                bit_width=self.act_bw, 
                                act_quant=Uint8ActPerTensorFloat,
                                return_quant_tensor=True)),
                    
                    ("conv44", qnn.QuantConv2d(
                                32, 64, 
                                kernel_size=3, stride=1, padding=1, 
                                weight_bit_width=self.big_layers_weight_bw,
                                weight_quant=MyInt8Weight,
                                bias=True, 
                                bias_quant=MyIntBias)),
                    ("relu44", qnn.QuantReLU(
                                bit_width=self.act_bw, 
                                act_quant=Uint8ActPerTensorFloat,
                                return_quant_tensor=True)),
                    
                    ("conv45", qnn.QuantConv2d(64, 32, 
                                kernel_size=1, stride=1, padding=0, 
                                weight_bit_width=self.weight_bw,
                                weight_quant=MyInt8Weight,
                                bias=True, 
                                bias_quant=MyIntBias)),
                    ("relu45", qnn.QuantReLU(
                                bit_width=self.act_bw, 
                                act_quant=Uint8ActPerTensorFloat,
                                return_quant_tensor=True)),
                    
                    ("conv46", qnn.QuantConv2d(
                                32, self.last_channels, 
                                kernel_size=3, stride=1, padding=1, 
                                weight_bit_width=self.big_layers_weight_bw,
                                weight_quant=MyInt8Weight,
                                bias=True, 
                                bias_quant=MyIntBias)),
                    ("relu46", qnn.QuantReLU(
                                bit_width=self.act_bw,
                                act_quant=Uint8ActPerTensorFloat,
                                return_quant_tensor=True)),
        
                    # Output One Head, 2 Neurons
                    ("avgpool5", qnn.TruncAvgPool2d(                  # Adaptive Avg Pool replaced to avoid extra calculations
                                kernel_size=(28, 28),
                                stride=1,
                                trunc_quant=TruncTo8bit,
                                return_quant_tensor=True)),
                    ("flatten5", nn.Flatten(start_dim=1)),
                    #("dropout5", nn.Dropout(p=0.2)),
                    ("linear51", qnn.QuantLinear(
                                in_features=self.last_channels, out_features=16, 
                                bias=True,
                                weight_bit_width=self.weight_bw,
                                weight_quant=MyInt8Weight,
                                bias_quant=MyIntBias)),
                    ("relu5", qnn.QuantReLU(
                                bit_width=self.act_bw,
                                act_quant=Uint8ActPerTensorFloat, 
                                return_quant_tensor=True)),
                    ("linear52", qnn.QuantLinear(
                                in_features=16, out_features=self.num_classes,
                                bias=True,
                                weight_bit_width=self.weight_bw,
                                weight_quant=MyInt8Weight,
                                bias_quant=MyIntBias)),
                ]
            )                    
        )     
        return BED_model


    def forward(self, x):
        x = self.model(x)
        return x


# ______________________________________________________________ #
# ____________________    NO BATCH NORM     ____________________ #
# ______________________________________________________________ #
class FUSED_BED_CLASSIFIER(nn.Module):
    def __init__(self, num_classes, in_channels=3):
        super(FUSED_BED_CLASSIFIER, self).__init__()
        self.in_channels = in_channels
        self.last_channels = 64
        self.num_classes = num_classes
        
        self.model = self.__create_BED__()
        
    def __create_BED__(self):
        BED_model = nn.Sequential(

            collections.OrderedDict(
                [
            # Conv2d [in_channels, out_channels, kernel_size, stride, padding, bias]

                    # CNNBlock 224x224
                    ("conv1", nn.Conv2d(self.in_channels, 32, kernel_size=3, stride=1, padding=1)),
                    ("relu1", nn.ReLU()),
                    ("dropout1", nn.Dropout2d(p=0.3)),
        
                    # CNNBlock 112x112
                    ("maxpool2", nn.MaxPool2d(kernel_size=2, stride=2)),
                    ("conv2", nn.Conv2d(32, 16, kernel_size=3, stride=1, padding=1)),
                    ("relu2", nn.ReLU()),
                    ("dropout2",nn.Dropout2d(p=0.3)),
        
                    # CNNBlock 56x56
                    ("maxpool3", nn.MaxPool2d(kernel_size=2, stride=2)),
                    ("conv31", nn.Conv2d(16, 16, kernel_size=1, stride=1, padding=0)),
                    ("relu31", nn.ReLU()),
                    
                    ("conv32", nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)),
                    ("relu32", nn.ReLU()),
                    
                    ("conv33", nn.Conv2d(32, 32, kernel_size=1, stride=1, padding=0)),
                    ("relu33", nn.ReLU()),
                    
                    ("conv34", nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)),
                    ("relu34", nn.ReLU()),
        
                    # CNNBlock 28x28
                    ("maxpool4", nn.MaxPool2d(kernel_size=2, stride=2)),
                    ("conv41", nn.Conv2d(64, 32, kernel_size=1, stride=1, padding=0)),
                    ("relu41", nn.ReLU()),
                    
                    ("conv42", nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)),
                    ("relu42", nn.ReLU()),
                    
                    ("conv43", nn.Conv2d(64, 32, kernel_size=1, stride=1, padding=0)),
                    ("relu43", nn.ReLU()),
                    
                    ("conv44", nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)),
                    ("relu44", nn.ReLU()),
                    
                    ("conv45", nn.Conv2d(64, 32, kernel_size=1, stride=1, padding=0)),
                    ("relu45", nn.ReLU()),
                    
                    ("conv46", nn.Conv2d(32, self.last_channels, kernel_size=3, stride=1, padding=1)),
                    ("relu46", nn.ReLU()),
        
                    # Output One Head, 2 Neurons
                    ("avgpool5", nn.AdaptiveAvgPool2d((1, 1))),
                    ("flatten5", nn.Flatten(start_dim=1)),
                    ("dropout5", nn.Dropout(p=0.2)),
                    ("linear51", nn.Linear(in_features=self.last_channels, out_features=16)),
                    ("relu5", nn.ReLU()),
                    ("linear52", nn.Linear(in_features=16, out_features=2)),
                ]
            )
        )
        return BED_model
    
    def forward(self, x):
        x = self.model(x)
        return x


