import config
import modules.dataset_flame as flame
import torch
from torch.utils.data import DataLoader
import albumentations as A
from albumentations.pytorch import ToTensorV2

def get_flame_test_loader():
    val_transform = A.Compose([
        A.Resize(224, 224, p=1),
        ToTensorV2(p=1),
        ]
    )
    
    print("\n====================\nTEST FLAME dataset")
    test_flame_dataset = flame.FLAME(
        img_h = 224,
        img_w = 224,
        img_dir = config.FLAME_TEST_IMG_DIR,
        num_classes = 1,
        ds_len = None,
        transform=val_transform)
    print(f'\nTest dataset len: {len(test_flame_dataset)}')

    test_loader = DataLoader(
        dataset=test_flame_dataset,
        batch_size=64,
        num_workers=8,
        pin_memory=True,
        shuffle=False,
        drop_last=False)
    
    return test_loader



