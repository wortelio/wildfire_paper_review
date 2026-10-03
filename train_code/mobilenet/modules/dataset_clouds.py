import os
from pathlib import Path
import numpy as np
import math
import random
import torch
from torch.utils.data import Dataset
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2


class Clouds(Dataset):
    '''
    Creates a Pytorch Dataset to train the BED Classifier.
    
    Arguments:
        - img_h:            image height
        - img_w:            image width
        - img_dir:          path to images folder
        - transform:        transformation applied to input images -> Albumentations
        - target_transform: transformation applied to labels -> nothing by default

    Return:
        - img:              1 image of the dataset
        - target:           corresponding label encoded: [0, 0]
    '''

    def __init__(self, img_h, img_w, img_dir, num_classes,
                 ds_len,
                 transform=None, target_transform=None,
                 return_img_filename=False):
        self.img_h = img_h
        self.img_w = img_w
        self.img_dir = img_dir
        self.num_classes = num_classes
        self.ds_len = ds_len
        self.transform = transform
        self.target_transform = target_transform
        self.return_img_filename = return_img_filename
        
        self.except_transform = A.Compose([
                                    A.Resize(self.img_h, self.img_w, p=1),
                                    ToTensorV2(p=1),
                                    ]
                                )

        self.imgs_list = sorted(
            [
                os.path.join(self.img_dir, file_name)
                for file_name in os.listdir(self.img_dir)
                if file_name.endswith(".jpg")
            ]
        )
    
        if ds_len is not None:
            random.seed(123)
            random.shuffle(self.imgs_list)
            self.images_path, self.labels = self.__build_ds__(self.imgs_list[:self.ds_len])
            self.num_samples = len(self.imgs_list[:self.ds_len])
        else:
            self.images_path, self.labels = self.__build_ds__(self.imgs_list)
            self.num_samples = len(self.imgs_list)

    def __len__(self):
        return self.num_samples   

    def __build_ds__(self, imgs_list):
        images = []
        labels = []
        wrong_imgs = 0
                
        for image_path in imgs_list:
                                   
            if cv2.imread(image_path) is None:
                print(f'{image_path} cannot be read by cv2 -> removed')
                wrong_imgs += 1
            
            else:
                label_array = np.zeros((self.num_classes))
                labels.append(label_array)
                images.append(image_path)
        
        print(f'Clouds Dataset Removed wrong images: {wrong_imgs}')

        labels_np = np.array(labels)
        labels_tensor = torch.tensor(labels_np, dtype=torch.float32)
        images_array = np.array(images)
        
        return images_array, labels_tensor

    def __getitem__(self, index):

        # Image processing
        img_file = self.images_path[index]
        img = cv2.imread(img_file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  

        # Labels processing
        label = self.labels[index]
        
        # Data Augmentation
        if self.transform is not None:
            try:
                aug = self.transform(image=img)
                img = aug['image'] / 255.0 #256.0 #255.0
            except:
                #print(f'Error trying to augment image {img_file}')
                aug = self.except_transform(image=img)
                img = aug['image'] / 255.0 #256.0 #255.0
        
        if self.return_img_filename:
            return img, label, img_file    
        else:
            return img, label