import torch
import torch.nn as nn 
from torchvision.models import mobilenet_v3_small
from torchvision.models import shufflenet_v2_x0_5
from torchvision.models import mobilenet_v2


class PRETRAINED_MODEL(nn.Module):
    def __init__(self, base_model, last_channels, num_classes, in_channels=3):
        super().__init__()
        self.in_channels = in_channels
        self.num_classes = num_classes
        self.last_channels = last_channels
        
        self.base_model = nn.Sequential(*list(base_model.children())[:-1])

        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.linear = nn.Sequential(
            nn.Dropout(p=0.2),
            nn.Linear(in_features=self.last_channels, out_features=32),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(in_features=32, out_features=self.num_classes)
        )
    
    def forward(self, x):
        x = self.base_model(x)
        x = self.pool(x)
        x = torch.flatten(x, start_dim=1)
        x = self.linear(x)
        return x
    
class PRETRAINED_MOBILENETV3_FULL(nn.Module):
    def __init__(self, base_model, num_classes, in_channels=3):
        super().__init__()
        self.in_channels = in_channels
        self.num_classes = num_classes
        
        self.base_model = nn.Sequential(*list(base_model.children())[:-1])

        final_stage = list(base_model.children())[-1]
        self.linear_1 = final_stage[0]
        last_channels = final_stage[0].out_features
        self.hswish = final_stage[1]
        self.dropout = final_stage[2]
        self.classifier = nn.Linear(in_features=last_channels, out_features=self.num_classes)
    
    def forward(self, x):
        x = self.base_model(x)
        x = torch.flatten(x, start_dim=1)
        x = self.linear_1(x)
        x = self.hswish(x)
        x = self.dropout(x)
        x = self.classifier(x)
        return x

class PRETRAINED_MOBILENET_V2(nn.Module):
    def __init__(self, base_model, num_classes, in_channels=3):
        super().__init__()
        self.in_channels = in_channels
        self.num_classes = num_classes
        
        self.base_model = nn.Sequential(*list(base_model.children())[:-1])

        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.linear = nn.Sequential(
            nn.Dropout(p=0.2, inplace=False),
            nn.Linear(in_features=1280, out_features=num_classes),
        )
    
    def forward(self, x):
        x = self.base_model(x)
        x = self.pool(x)
        x = torch.flatten(x, start_dim=1)
        x = self.linear(x)
        return x

# class PRETRAINED_SHUFFLENETv2(nn.Module):
#     def __init__(self, base_model, num_classes, in_channels=3):
#         super().__init__()
#         self.in_channels = in_channels
#         self.num_classes = num_classes
        
#         self.base_model = nn.Sequential(*list(base_model.children())[:-1])
#         self.classifier = nn.Linear(in_features=1024, out_features=num_classes)
    
#     def forward(self, x):
#         x = self.base_model(x)
#         x = x.mean([2, 3]) 
#         x = self.classifier(x)
#         return x
    
    
def setup_model(model_name, num_classes, device):
    if model_name == "MOBILENETV3":
        print("Using MOBILENETV3 Classifier")

        base_model = mobilenet_v3_small(weights='IMAGENET1K_V1')
        print(list(base_model.children())[-1])
        for name, layer in base_model.named_modules():
            if isinstance(layer, nn.Linear):
                last_channels = layer.in_features
                print(f'Model Pretrained has {last_channels} in features in last layer')
                break
        for param in base_model.parameters():
            param.requires_grad = False

        model = PRETRAINED_MODEL(base_model, last_channels=last_channels, num_classes=num_classes).to(device)  
        return model

    elif model_name == "MOBILENETV3_FULL":
        print("Using MOBILENETV3 FULL Classifier")

        base_model = mobilenet_v3_small(weights='IMAGENET1K_V1')
        print(list(base_model.children())[-1])
        for param in base_model.parameters():
            param.requires_grad = False

        model = PRETRAINED_MOBILENETV3_FULL(base_model, num_classes=num_classes).to(device)  
        return model
    
    elif model_name == "MOBILENETV2":
        print("Using MOBILENETV2 FULL Classifier, with V2 Imagenet weights")

        base_model = mobilenet_v2(weights='IMAGENET1K_V2')
        print(list(base_model.children())[-1])
        for param in base_model.parameters():
            param.requires_grad = False

        model = PRETRAINED_MOBILENET_V2(base_model, num_classes=num_classes).to(device)  
        return model
    
    
    elif model_name == "SHUFFLENETV2":
        print("Using SHUFFLE Classifier")

        base_model = shufflenet_v2_x0_5(weights='IMAGENET1K_V1')
        print(list(base_model.children())[-1])
        for name, layer in base_model.named_modules():
            if isinstance(layer, nn.Linear):
                last_channels = layer.in_features
                print(f'Model Pretrained has {last_channels} in features in last layer')
        for param in base_model.parameters():
            param.requires_grad = False

        model = PRETRAINED_MODEL(base_model, last_channels=last_channels, num_classes=num_classes).to(device)   
        return model
    
    else:
        print("Wrong Model")
        raise SystemExit("Wrong Model")
    