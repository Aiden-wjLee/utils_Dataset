from PIL import Image
import os
import glob
import numpy as np
import torchvision.transforms as transforms
import torch
from tqdm import tqdm

import cv2
def calculate_mean_std(image_folder):
    transform_to_tensor = transforms.ToTensor()
    
    num_images = 0
    sum_mean = torch.zeros(3)
    sum_std = torch.zeros(3)
    
    image_files = glob.glob(os.path.join(image_folder, '*.jpg')) + glob.glob(os.path.join(image_folder, '*.png'))

    for count, image_file in enumerate(tqdm(image_files)):
        image = cv2.cvtColor(cv2.imread(image_file), cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        #image = Image.open(image_file)

        #if count==37:
        #    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        #    cv2.imshow('image', np.array(cv_image))
        #    cv2.waitKey(0)

        image_tensor = transform_to_tensor(image)
        
        # 이미지 별로 mean과 std를 계산
        image_mean = torch.mean(image_tensor, dim=(1, 2))
        image_std = torch.std(image_tensor, dim=(1, 2))
        
        sum_mean += image_mean
        sum_std += image_std
        num_images += 1
    
    # 전체 이미지에 대한 mean과 std를 계산
    overall_mean = sum_mean / num_images
    overall_std = sum_std / num_images
    
    return overall_mean.tolist(), overall_std.tolist()

#image_folder = "D:/Dataset/nachi_new_view1/origin"  # 실제 이미지 폴더 경로로 변경해주세요.
# \ to /
image_folder='D:/Dataset/nachi_grid_1027/train/img'

#image_folder = "/media/lee/90182A121829F83C/Dataset/Turtlebot_water/train/img/"
mean, std = calculate_mean_std(image_folder)
print(f"Calculated mean: {mean}")
print(f"Calculated std: {std}")