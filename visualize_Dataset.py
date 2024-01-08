#for design project


import numpy as np
import cv2

def main():
    img=cv2.imread('/media/lee/90182A121829F83C/Dataset/Turtlebot_water/train/img/39.png')
    mask=cv2.imread('/media/lee/90182A121829F83C/Dataset/Turtlebot_water/train/mask/39.png')
    print(mask.shape, img.shape)
    print("mask_max: ",np.max(mask))
    print("img_max: ",np.max(img))
    integrated=cv2.addWeighted(img,1,mask,0.5,0)
    cv2.imwrite('integrated_39.png',integrated)
    cv2.imshow('img',integrated)
    cv2.waitKey(0)



if __name__ == '__main__': 
    main()
