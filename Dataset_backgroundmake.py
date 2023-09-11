import os
import numpy as np
import cv2
import glob
from tqdm import tqdm

def main(img_folder_path):
    img_folder_name=img_folder_path.split('/')[-2]
    mask_folder_path=img_folder_path.replace('img','mask')

    imgs = glob.glob(img_folder_path+'*.png')+glob.glob(img_folder_path+'*.jpg')
    print(imgs)
    imgs.sort(key=lambda x: int(x.split('/')[-1].split('.')[0]))

    #load and check image size
    img=cv2.imread(imgs[0])
    height, width, _ = img.shape

    for img_path in tqdm(imgs):
        background_img=np.zeros((height,width,3),np.uint8)
        cv2.imwrite(img_path.replace('img', 'mask'), background_img)



if __name__ == "__main__":
    img_folder_path='/media/lee/90182A121829F83C/Dataset/ubuntu_data/back_1/img/'
    main(img_folder_path)