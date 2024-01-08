import cv2
import os
from tqdm import tqdm

def main(image_folders, intergration_folder, crop_size):
    """
    Integrate images from multiple folders into a single folder.
    Args:
        image_folders: 이미지가 저장된 폴더들의 리스트
        intergration_folder: 통합된 이미지가 저장될 폴더
    Returns:
        None
    """
    cnt=0
    for img_folder in image_folders:
        imgs=[img for img in os.listdir(img_folder) if img.endswith(".png") or img.endswith(".jpg")]
        print(len(imgs))
        imgs.sort(key=lambda x: int(x.split('.')[0]))
        for img in tqdm(imgs, desc="Converting images to video...", ncols=100):
            image = cv2.imread(os.path.join(img_folder, img))
            image = cv2.resize(image,(crop_size[0],crop_size[1]))
            cv2.imwrite(os.path.join(intergration_folder, str(cnt)+'.png'), image)
            #print(str(os.path.join(img_folder, img)))
            cnt+=1
        

if __name__ == "__main__":
    image_folders=[]
    image_folders.append('E:/dataset/nachi/images_20231027_grid/left/') #왼쪽
    image_folders.append('E:/dataset/nachi/images_20231027_grid/right/') #오른쪽
    intergration_folder='E:/dataset/nachi/images_20231027_grid/origin' ##수정해야하는 사항
    if not os.path.isdir(intergration_folder):
        os.mkdir(intergration_folder)
    main(image_folders, intergration_folder, (1280,512)) #(가로, 세로)