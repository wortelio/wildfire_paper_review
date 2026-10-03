import collections
import torch
import torch.nn as nn

# ______________________________________________________________ #
# ____________________   Manually Reduced   ____________________ #
# ____________________         MODEL        ____________________ #
# ______________________________________________________________ #

# After AIMET, manually reorder and reduce 
# some layers to lower MACs,
# keeping the same amount of weights


class BED_CLASSIFIER_FPGA(nn.Module):
    def __init__(self, num_classes=2, in_channels=3):
        super(BED_CLASSIFIER_FPGA, self).__init__()
        self.in_channels = in_channels
        self.last_channels = 64
        self.num_classes = num_classes
        
        self.model = self.__create_BED__()
        
    def __create_BED__(self):
        BED_model = nn.Sequential(

            collections.OrderedDict(
                [
            # Conv2d [in_channels, out_channels, kernel_size, stride, padding, bias]

                    # CNNBlock 230x230
                    ("conv1", nn.Conv2d(self.in_channels, 12, kernel_size=3, stride=1, padding=0,  bias=False)),
                    ("bn1", nn.BatchNorm2d(12)),
                    ("relu1", nn.ReLU()),
        
                    # CNNBlock 114x114
                    ("maxpool2", nn.MaxPool2d(kernel_size=2, stride=2)),
                    ("conv2", nn.Sequential(
                        nn.Conv2d(12, 24, kernel_size=(3, 1), stride=(1, 1), padding=(0,0), bias=False),
                        nn.Conv2d(24, 16, kernel_size=(1, 3), stride=(1, 1), padding=(0,0), bias=False)),
                    ),
                    ("bn2", nn.BatchNorm2d(16)),
                    ("relu2", nn.ReLU()),
        
                    # CNNBlock 56x56
                    ("maxpool3", nn.MaxPool2d(kernel_size=2, stride=2)),
                    ("conv31", nn.Conv2d(16, 16, kernel_size=1, stride=1, padding=0,  bias=False)),
                    ("bn31", nn.BatchNorm2d(16)),
                    ("relu31", nn.ReLU()),
                    
                    ("conv32", nn.Sequential(
                        nn.Conv2d(16, 16, kernel_size=(3, 1), stride=(1, 1), padding=(0,0), bias=False),
                        nn.Conv2d(16, 32, kernel_size=(1, 3), stride=(1, 1), padding=(0,0), bias=False)),
                    ),                    
                    ("bn32", nn.BatchNorm2d(32)),
                    ("relu32", nn.ReLU()),
                    
                    ("conv33", nn.Conv2d(32, 32, kernel_size=1, stride=1, padding=0,  bias=False)),
                    ("bn33", nn.BatchNorm2d(32)),
                    ("relu33", nn.ReLU()),
                    
                    ("conv34", nn.Sequential(
                        nn.Conv2d(32, 42, kernel_size=(3, 1), stride=(1, 1), padding=(0,0), bias=False),
                        nn.Conv2d(42, 64, kernel_size=(1, 3), stride=(1, 1), padding=(0,0), bias=False)),
                    ), 
                    ("bn34", nn.BatchNorm2d(64)),
                    ("relu34", nn.ReLU()),
        
                    # CNNBlock 26x26
                    ("maxpool4", nn.MaxPool2d(kernel_size=2, stride=2)),
                    ("conv41", nn.Conv2d(64, 30, kernel_size=1, stride=1, padding=0,  bias=False)),
                    ("bn41", nn.BatchNorm2d(30)),
                    ("relu41", nn.ReLU()),
                    
                    ("conv42", nn.Conv2d(30, 60, kernel_size=3, stride=1, padding=0,  bias=False)),
                    ("bn42", nn.BatchNorm2d(60)),
                    ("relu42", nn.ReLU()),
                    
                    ("conv43", nn.Conv2d(60, 32, kernel_size=1, stride=1, padding=0,  bias=False)),
                    ("bn43", nn.BatchNorm2d(32)),
                    ("relu43", nn.ReLU()),
                    
                    ("conv44", nn.Sequential(
                        nn.Conv2d(32, 42, kernel_size=(3, 1), stride=(1, 1), padding=(0,0), bias=False),
                        nn.Conv2d(42, 58, kernel_size=(1, 3), stride=(1, 1), padding=(0,0), bias=False)),
                    ), 
                    ("bn44", nn.BatchNorm2d(58)),
                    ("relu44", nn.ReLU()),
                    
                    ("conv45", nn.Conv2d(58, 32, kernel_size=1, stride=1, padding=0,  bias=False)),
                    ("bn45", nn.BatchNorm2d(32)),
                    ("relu45", nn.ReLU()),
                    
                    ("conv46", nn.Sequential(
                        nn.Conv2d(32, 20, kernel_size=(3, 1), stride=(1, 1), padding=(0,0), bias=False),
                        nn.Conv2d(20, 64, kernel_size=(1, 3), stride=(1, 1), padding=(0,0), bias=False)),
                    ), 
                    ("bn46", nn.BatchNorm2d(self.last_channels)),
                    ("relu46", nn.ReLU()),
        
                    # Output One Head, 2 Neurons
                    ("avgpool5", nn.AdaptiveAvgPool2d((1, 1))),
                    ("flatten5", nn.Flatten(start_dim=1)),
                    ("linear51", nn.Linear(in_features=self.last_channels, out_features=32, bias=False)),
                    ("bn51", nn.BatchNorm1d(32)),
                    ("relu5", nn.ReLU()),
                    ("linear52", nn.Linear(in_features=32, out_features=self.num_classes)),
                ]
            )
        )
        return BED_model
    
    

    def __initialize_weights__(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_in',
                    nonlinearity='relu'
                )
                if m.bias is not None:
                        nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)


    def forward(self, x):
        x = self.model(x)
        return x

