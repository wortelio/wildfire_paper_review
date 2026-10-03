import torch
import torch.nn as nn 
from torch.nn import Conv2d
from torch.nn import BatchNorm1d
from torch.nn import BatchNorm2d
from torch.nn import MaxPool2d
from torch.nn import Linear

def conv_3x3_bn_relu(inp, oup):
    return nn.Sequential(
        Conv2d(
            in_channels=inp,
            out_channels=oup,
            kernel_size=3,
            stride=1,
            padding=0,
            bias=False),
        nn.BatchNorm2d(oup),
        nn.ReLU(),
    )

def svd_conv_3x3_bn_relu(inp, mid, oup):
    return nn.Sequential(
        Conv2d(
            in_channels=inp,
            out_channels=mid,
            kernel_size=(3,1),
            stride=1,
            padding=(0,0),
            bias=False),
        nn.BatchNorm2d(mid),
        Conv2d(
            in_channels=mid,
            out_channels=oup,
            kernel_size=(1,3),
            stride=1,
            padding=(0,0),
            bias=False),
        nn.BatchNorm2d(oup),
        nn.ReLU(),
    )


    
def conv_1x1_bn_relu(inp, oup):
    return nn.Sequential(
        Conv2d(
            in_channels=inp,
            out_channels=oup,
            kernel_size=1,
            stride=1,
            padding=0,
            bias=False),
        nn.BatchNorm2d(oup),
        nn.ReLU(),
    )


def svd_conv_1x1_bn_relu(inp, mid, oup):
    return nn.Sequential(
        Conv2d(
            in_channels=inp,
            out_channels=mid,
            kernel_size=(1,1),
            stride=1,
            padding=(0,0),
            bias=False),
        nn.BatchNorm2d(mid),
        Conv2d(
            in_channels=mid,
            out_channels=oup,
            kernel_size=(1,1),
            stride=1,
            padding=(0,0),
            bias=False),
        nn.BatchNorm2d(oup),
        nn.ReLU(),
    )



class TORCH_BED_AIMET_FPGA_MUL4(nn.Module):
    def __init__(self, num_classes=2, model_cfg=None):
        super(TORCH_BED_AIMET_FPGA_MUL4, self).__init__()

        # self.cfgs = [
        #     # [conv3x3/svd_conv3x3/conv1x1/svd_conv1x1/mp, (inp, mid(opt), oup)]
        #     ["svd_conv3x3", (3, 8, 28)],               # conv1
        #     ["mp"],
        #     ["svd_conv3x3", (28, 24, 16)],             # conv2
        #     ["mp"],
        #     ["conv1x1", (16, 16)],                     # conv31
        #     ["conv3x3", (16, 32)],                     # conv32
        #     ["conv1x1", (32, 32)],                     # conv33
        #     ["svd_conv3x3", (32, 52, 56)],             # conv34
        #     ["mp"],
        #     ["conv1x1", (56, 32)],                     # conv41
        #     ["svd_conv3x3", (32, 44, 64)],             # conv42
        #     ["conv1x1", (64, 32)],                     # conv43
        #     ["svd_conv3x3", (32, 32, 64)],             # conv44
        #     ["svd_conv1x1", (64, 12, 32)],             # conv45
        #     ["svd_conv3x3", (32, 8, 64)],              # conv46            
        # ]

        self.cfgs = model_cfg
        
        # Input 224x224x3
        layers = []
        
        for cfg in self.cfgs:
            if len(cfg) == 2:
                layer_type = cfg[0]
                channels = cfg[1] 
                if layer_type == "svd_conv3x3":
                    layers.append(svd_conv_3x3_bn_relu(channels[0], channels[1], channels[2]))   
                elif layer_type== "svd_conv1x1":
                    layers.append(svd_conv_1x1_bn_relu(channels[0], channels[1], channels[2]))   
                elif layer_type == "conv3x3":
                    layers.append(conv_3x3_bn_relu(channels[0], channels[1]))   
                elif layer_type == "conv1x1":
                    layers.append(conv_1x1_bn_relu(channels[0], channels[1]))   
            elif cfg[0] == "mp" and len(cfg) == 1:
                layers.append(MaxPool2d(kernel_size=2, stride=2)) 
            else:
                raise SystemExit("Error in config definition")
            
        self.features = nn.Sequential(*layers)
        
        # building last several layers       
        self.avgpool = nn.AdaptiveAvgPool2d((1,1))

        linears = []
        # Linear 1
        linears.append(Linear(
                in_features=64,
                out_features=32,
                bias=False))
        linears.append(BatchNorm1d(32))
        linears.append(nn.ReLU())
        # Linear 2
        linears.append(Linear(
                in_features=32,
                out_features=num_classes,
                bias=False))

        self.classifier = nn.Sequential(*linears)

        
    def forward(self, x):
        x = 2.0 * x - torch.tensor([1.0], device=x.device)
        x = self.features(x)
        x = self.avgpool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x
