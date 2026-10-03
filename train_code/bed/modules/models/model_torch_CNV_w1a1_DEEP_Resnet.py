import torch
from torch.nn import Conv2d
from torch.nn import ReLU
from torch.nn import Linear
from torch.nn import BatchNorm1d
from torch.nn import BatchNorm2d
from torch.nn import MaxPool2d
from torch.nn import AvgPool2d
from torch.nn import Module
from torch.nn import ModuleList



    
class Torch_CNV_w1a1_DEEP_Resnet(Module):

    def __init__(self, 
                 num_classes=2, 
                 in_channels=3):
        super(Torch_CNV_w1a1_DEEP_Resnet, self).__init__()

        self.num_classes = num_classes
        self.in_channels = in_channels
        
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

        # CNNBlock 224x224
        # conv1
        self.conv_features_0.append(Conv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=self.in_channels,
                out_channels=64,
                bias=False))
        self.conv_features_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_0.append(ReLU())
        
        self.conv_features_0.append(MaxPool2d(kernel_size=2, stride=2))

        # CNNBlock 112x112
        # conv2
        self.conv_features_0.append(Conv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=64,
                out_channels=32,
                bias=False))
        self.conv_features_0.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features_0.append(ReLU())
        
        self.conv_features_0.append(MaxPool2d(kernel_size=2, stride=2))

        # CNNBlock 56x56 
        # conv31
        self.conv_features_1_0.append(Conv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=32,
                out_channels=16,
                bias=False))
        self.conv_features_1_0.append(BatchNorm2d(16, eps=1e-4))
        self.conv_features_1_0.append(ReLU())            
        # conv32
        self.conv_features_1_0.append(Conv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=16,
                out_channels=32,
                bias=False))
        self.conv_features_1_0.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features_1_0.append(ReLU())
        # conv33
        self.conv_features_1_0.append(Conv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=32,
                out_channels=32,
                bias=False))
        self.conv_features_1_0.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features_1_0.append(ReLU())
        # conv34
        self.conv_features_1_1.append(Conv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=32,
                out_channels=64,
                bias=False))
        self.conv_features_1_1.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_1_1.append(ReLU())
        
        self.conv_features_1_1.append(MaxPool2d(kernel_size=2, stride=2))

        # CNNBlock 28x28 
        # conv41
        self.conv_features_2_0.append(Conv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=64,
                out_channels=32,
                bias=False))
        self.conv_features_2_0.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features_2_0.append(ReLU())
        # conv42
        self.conv_features_2_0.append(Conv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=32,
                out_channels=64,
                bias=False))
        self.conv_features_2_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_2_0.append(ReLU())
        # conv43
        self.conv_features_2_0.append(Conv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=64,
                out_channels=32,
                bias=False))
        self.conv_features_2_0.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features_2_0.append(ReLU())
        # conv44
        self.conv_features_2_0.append(Conv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=32,
                out_channels=64,
                bias=False))
        self.conv_features_2_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_2_0.append(ReLU())
        # conv45
        self.conv_features_2_0.append(Conv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=64,
                out_channels=32,
                bias=False))
        self.conv_features_2_0.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features_2_0.append(ReLU())
        # conv46
        self.conv_features_2_0.append(Conv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=32,
                out_channels=64,
                bias=False))
        self.conv_features_2_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_2_0.append(ReLU())

        self.conv_features_2_1.append(MaxPool2d(kernel_size=2, stride=2))

        # CNNBlock 14x14 
        # conv51
        self.conv_features_3_0.append(Conv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=64,
                out_channels=32,
                bias=False))
        self.conv_features_3_0.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features_3_0.append(ReLU())
        # conv52
        self.conv_features_3_0.append(Conv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=32,
                out_channels=64,
                bias=False))
        self.conv_features_3_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_3_0.append(ReLU())
        # conv53
        self.conv_features_3_0.append(Conv2d(
                kernel_size=1, stride=1, padding=0,
                in_channels=64,
                out_channels=32,
                bias=False))
        self.conv_features_3_0.append(BatchNorm2d(32, eps=1e-4))
        self.conv_features_3_0.append(ReLU())
        # conv54
        self.conv_features_3_0.append(Conv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=32,
                out_channels=64,
                bias=False))
        self.conv_features_3_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_3_0.append(ReLU())
        # conv55
        self.conv_features_3_0.append(Conv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=64,
                out_channels=64,
                bias=False))
        self.conv_features_3_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_3_0.append(ReLU())
        # conv56
        self.conv_features_3_0.append(Conv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=64,
                out_channels=64,
                bias=False))
        self.conv_features_3_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_3_0.append(ReLU())

        self.conv_features_3_1.append(MaxPool2d(kernel_size=2, stride=2))


        # CNNBlock 7x7
        # conv61
        self.conv_features_4_0.append(Conv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=64,
                out_channels=64,
                bias=False))
        self.conv_features_4_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_4_0.append(ReLU())
        # conv62
        self.conv_features_4_0.append(Conv2d(
                kernel_size=3, stride=1, padding=1,
                in_channels=64,
                out_channels=64,
                bias=False))
        self.conv_features_4_0.append(BatchNorm2d(64, eps=1e-4))
        self.conv_features_4_0.append(ReLU())
     
        
       # Average Pooling
        self.avg_pool = AvgPool2d(7)

        # Linear 1
        self.linear_features.append(Linear(
                in_features=64,
                out_features=64,
                bias=False))
        self.linear_features.append(BatchNorm1d(64, eps=1e-4))
        self.linear_features.append(ReLU())
        # Linear 2
        self.linear_features.append(Linear(
                in_features=64,
                out_features=32,
                bias=False))
        self.linear_features.append(BatchNorm1d(32, eps=1e-4))
        self.linear_features.append(ReLU())
        # Linear 3
        self.linear_features.append(Linear(
                in_features=32,
                out_features=self.num_classes,
                bias=False))


        self.relu = ReLU()

    def forward(self, x):
        x = 2.0 * x - torch.tensor([1.0], device=x.device)
        for mod in self.conv_features_0:
            x = mod(x)
        
        for i, mod in enumerate(self.conv_features_1_0):
            if i == 0:
                x_res = mod(x)
            else:
                x_res = mod(x_res)
        x = x + x_res
        x = self.relu(x)
        for mod in self.conv_features_1_1:
            x = mod(x)

        for i, mod in enumerate(self.conv_features_2_0):
            if i == 0:
                x_res = mod(x)
            else:
                x_res = mod(x_res)
        x = x + x_res
        x = self.relu(x)
        for mod in self.conv_features_2_1:
            x = mod(x)

        for i, mod in enumerate(self.conv_features_3_0):
            if i == 0:
                x_res = mod(x)
            else:
                x_res = mod(x_res)
        x = x + x_res
        x = self.relu(x)
        for mod in self.conv_features_3_1:
            x = mod(x)
        
        for i, mod in enumerate(self.conv_features_4_0):
            if i == 0:
                x_res = mod(x)
            else:
                x_res = mod(x_res)
        x = x + x_res
        x = self.relu(x)
        
        x = self.avg_pool(x)
        
        x = x.view(x.shape[0], -1)
        for mod in self.linear_features:
            x = mod(x)
        return x

