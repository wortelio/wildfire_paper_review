import config
import modules.dataset_fog as fog
import modules.dataset_fog_4classes as fog_4classes
import modules.dataset_fog_2classes as fog_2classes
import torch
from torch.utils.data import DataLoader
import albumentations as A
from albumentations.pytorch import ToTensorV2

def get_fog_train_loader():
    train_transform = A.Compose([
            A.HorizontalFlip(p=0.5),
            A.OneOf([
                A.RandomBrightnessContrast(p=0.2),
                A.HueSaturationValue(hue_shift_limit=10, p=0.2),
                A.Blur(blur_limit=(3,3), p=0.3),
                A.CLAHE(clip_limit=2.0, p=0.2),
                A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.1),
            ], p=0.9),
            A.ShiftScaleRotate(shift_limit=0.2, scale_limit=0.2, rotate_limit=20, p=0.3),
            A.Resize(config.IMG_H, config.IMG_W, p=1),
            ToTensorV2(p=1),
        ]
    )
    
    # TRAIN DATASET
    print("\n====================\nTRAIN FOG dataset")
    train_fog_dataset = fog_4classes.FOG_SMOKE_4CLASSES(
        img_h = config.IMG_H,
        img_w = config.IMG_W,
        img_dir = config.FOG_TRAIN_IMG_DIR,
        num_classes = config.NUM_CLASSES,
        ds_len = config.DS_LEN,
        transform=train_transform)
    print(f'\nTrain dataset len: {len(train_fog_dataset)}')
   
    train_loader = DataLoader(
        dataset=train_fog_dataset,
        batch_size=config.BATCH_SIZE,
        num_workers=config.NUM_WORKERS,
        pin_memory=config.PIN_MEMORY,
        shuffle=True,
        drop_last=True)
    
    return train_loader 

def get_fog_test_loader():
    val_transform = A.Compose([
        A.Resize(config.IMG_H, config.IMG_W, p=1),
        ToTensorV2(p=1),
        ]
    )
    
    print("\n====================\nTEST FOG dataset")
    test_fog_dataset = fog_4classes.FOG_SMOKE_4CLASSES(
        img_h = config.IMG_H,
        img_w = config.IMG_W,
        img_dir = config.FOG_TEST_IMG_DIR,
        num_classes = config.NUM_CLASSES,
        ds_len = config.DS_LEN,
        transform=val_transform)
    print(f'\nTest dataset len: {len(test_fog_dataset)}')

    test_loader = DataLoader(
        dataset=test_fog_dataset,
        batch_size=config.BATCH_SIZE,
        num_workers=config.NUM_WORKERS,
        pin_memory=config.PIN_MEMORY,
        shuffle=False,
        drop_last=True)
    
    return test_loader

##################################
#       2 CLASSES
##################################
def get_fog_train_loader_2classes():
    train_transform = A.Compose([
            A.HorizontalFlip(p=0.5),
            A.OneOf([
                A.RandomBrightnessContrast(p=0.2),
                A.HueSaturationValue(hue_shift_limit=10, p=0.2),
                A.Blur(blur_limit=(17,17), p=0.3),
                A.CLAHE(clip_limit=2.0, p=0.2),
                A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.1),
            ], p=0.9),
            A.ShiftScaleRotate(shift_limit=0.2, scale_limit=0.2, rotate_limit=20, p=0.3),
            A.Resize(config.IMG_H, config.IMG_W, p=1),
            ToTensorV2(p=1),
        ]
    )
    
    # TRAIN DATASET
    print("\n====================\nTRAIN FOG dataset")
    train_fog_dataset = fog_2classes.FOG_SMOKE_2CLASSES(
        img_h = config.IMG_H,
        img_w = config.IMG_W,
        img_dir = config.FOG_TRAIN_IMG_DIR,
        num_classes = config.NUM_CLASSES,
        ds_len = config.DS_LEN,
        transform=train_transform)
    print(f'\nTrain dataset len: {len(train_fog_dataset)}')
   
    train_loader = DataLoader(
        dataset=train_fog_dataset,
        batch_size=config.BATCH_SIZE,
        num_workers=config.NUM_WORKERS,
        pin_memory=config.PIN_MEMORY,
        shuffle=True,
        drop_last=True)
    
    return train_loader 

def get_fog_test_loader2classes():
    val_transform = A.Compose([
        A.Resize(config.IMG_H, config.IMG_W, p=1),
        ToTensorV2(p=1),
        ]
    )
    
    print("\n====================\nTEST FOG dataset")
    test_fog_dataset = fog_2classes.FOG_SMOKE_2CLASSES(
        img_h = config.IMG_H,
        img_w = config.IMG_W,
        img_dir = config.FOG_TEST_IMG_DIR,
        num_classes = config.NUM_CLASSES,
        ds_len = config.DS_LEN,
        transform=val_transform)
    print(f'\nTest dataset len: {len(test_fog_dataset)}')

    test_loader = DataLoader(
        dataset=test_fog_dataset,
        batch_size=config.BATCH_SIZE,
        num_workers=config.NUM_WORKERS,
        pin_memory=config.PIN_MEMORY,
        shuffle=False,
        drop_last=True)
    
    return test_loader



