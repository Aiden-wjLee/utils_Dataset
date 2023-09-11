#바로 train validation 폴더에 저장 
import cv2
import os
import re
from tqdm import tqdm
#저장할 때마다 노트에 남기는걸로 바꾸자. 
def check_before_folder(image_folders,save_folder):
    if os.path.isfile(f"{save_folder}image_folder_list.txt"): #if txt file exist(list of image folder)
        read = open(f"{save_folder}image_folder_list.txt", "r")
        for line in read:
            for image_folder in image_folders:
                if line.strip() == image_folder:
                    print(f"{image_folder}는 이미 반영된 폴더입니다.")
                    return False
    return True
def save_txt_list_folder(write_image_folders,save_folder):
    file = open(f"{save_folder}image_folder_list.txt", "a")
    #for i in range (len(image_folders)):
    file.write(write_image_folders+'\n')
    

def dataset_integration(image_folders, save_folder):
    #원래 있던 이미지 탐색
    before_imgs_train = [img for img in os.listdir(save_folder+'train/img') if img.endswith(".png") or img.endswith(".jpg")]
    before_imgs_train.sort(key=lambda x: int(x.split('.')[0]))
    
    before_masks_train = [img for img in os.listdir(save_folder+'train/mask') if img.endswith(".png") or img.endswith(".jpg")]
    before_masks_train.sort(key=lambda x: int(x.split('.')[0]))
    
    before_masks_validation = [img for img in os.listdir(save_folder+'validation/mask') if img.endswith(".png") or img.endswith(".jpg")]
    before_masks_validation.sort(key=lambda x: int(x.split('.')[0]))
    
    before_imgs_validation = [img for img in os.listdir(save_folder+'validation/img') if img.endswith(".png") or img.endswith(".jpg")]
    before_imgs_validation.sort(key=lambda x: int(x.split('.')[0]))
    
    #원래 있던 이미지와 마스크의 개수가 다르면 오류
    print("len(before_images)_train, len(before_masks)_train: ",len(before_imgs_train), len(before_masks_train))
    if (len(before_imgs_train) != len(before_masks_train)):
        print("len(before_images) != len(before_masks)")
        return 0
    print("len(before_images)_validation, len(before_masks)_validation: ",len(before_imgs_validation), len(before_masks_validation))
    if (len(before_imgs_validation) != len(before_masks_validation)):
        print("len(before_images) != len(before_masks)")
        return 0

    #전 이미지 이후에 저장.
    if len(before_imgs_train)!=0 and len(before_masks_train)!=0: #전 이미지가 있으면 마지막 이미지 번호+1부터 저장
        print(before_imgs_train[len(before_imgs_train)-1], before_masks_train[len(before_masks_train)-1])
        start_i_train=int(before_imgs_train[len(before_imgs_train)-1].split('.')[0])+1
    else: #전 이미지가 없으면 0부터 저장
        start_i_train=0
    print("start_i_train: ",start_i_train)
    
    if len(before_imgs_validation)!=0 and len(before_masks_validation)!=0: #전 이미지가 있으면 마지막 이미지 번호+1부터 저장
        print(before_imgs_validation[len(before_imgs_validation)-1], before_masks_validation[len(before_masks_validation)-1])
        start_i_validation=int(before_imgs_validation[len(before_imgs_validation)-1].split('.')[0])+1
    else:
        start_i_validation=0
    print("start_i_validation: ",start_i_validation)
    
    train_img_num=start_i_train
    validation_img_num=start_i_validation 
    
    #
    file_number_each_train=[];   file_number_each_train.append(start_i_train)
    file_number_each_validation=[];   file_number_each_validation.append(start_i_validation)
    #각 이미지 폴더에 적용
    for image_folder in tqdm(image_folders, desc="Converting images to video...", ncols=100):
        print('==============='+image_folder+'===============')
        img_folder = image_folder #+'img/'
        mask_folder = image_folder.replace("img", "mask")
        #mask_folder = image_folder+'mask/'
        
        labeling_imgs=[img for img in os.listdir(img_folder) if img.endswith(".png") or img.endswith(".jpg")]
        labeling_imgs.sort(key=lambda x: int(x.split('.')[0]))
        #labeling_imgs = [img.split('.')[0].zfill(5) + '.' + img.split('.')[1] for img in labeling_imgs] #양식 맞추기 
        
        labeling_masks = [img for img in os.listdir(mask_folder) if img.endswith(".png") or img.endswith(".jpg")]
        labeling_masks.sort(key=lambda x: int(x.split('.')[0]))
        
        img_nums = [int(re.findall('\d+', img)[0]) for img in labeling_imgs]
        mask_nums = [int(re.findall('\d+', mask)[0]) for mask in labeling_masks]
        
        #mask와 img의 개수가 다르면 오류
        for i in range (len(labeling_imgs)):
            if img_nums[i]!=mask_nums[i]:#labeling_imgs[i]!=labeling_masks[i]:
                print("labeling_imgs!=labeling_masks")
                print("i: ", i,"labeling_imgs[i]: ", labeling_imgs[i]), print("labeling_masks[i]: ", labeling_masks[i])
                return 0
        
        print("len(labeling_imgs), len(labeling_masks): ",len(labeling_imgs), len(labeling_masks))
        if(len(labeling_imgs) != len(labeling_masks)):
            print("len(labeling_imgs) != len(labeling_masks)")
            return 0
        #if labeling_imgs.split('.')[0]!=labeling_masks.split('.')[0]:
        #    print("labeling_imgs!=labeling_masks")
        #    print("labeling_imgs[0]: ", labeling_imgs[0]), print("labeling_masks[0]: ", labeling_masks[0])
        #    return 0
        
        total_images = len(labeling_imgs)
        train_end_idx = int(0.8 * total_images)
        
        #train폴더에 대해 읽고, 저장
        for idx, image in enumerate(tqdm(labeling_imgs[:train_end_idx], desc="Integration Train folder", ncols=100)):
            save_image=cv2.imread(os.path.join(img_folder, image))
            save_image_path=os.path.join(save_folder, 'train', 'img', f"{train_img_num}.png")
            if not os.path.isfile(save_image_path):
                cv2.imwrite(save_image_path, save_image)
            

            save_mask=cv2.imread(os.path.join(mask_folder, labeling_masks[idx]))
            save_mask_path=os.path.join(save_folder, 'train', 'mask', f"{train_img_num}.png")
            if not os.path.isfile(save_mask_path):
                cv2.imwrite(save_mask_path, save_mask)
            train_img_num+=1
        
        #validation 폴더에 대해 읽고, 저장
        for idx, image in enumerate(tqdm(labeling_imgs[train_end_idx:], desc="Integration Validation folder", ncols=100)):
            save_image=cv2.imread(os.path.join(img_folder, image))
            save_image_path=os.path.join(save_folder, 'validation', 'img', f"{validation_img_num}.png")
            if not os.path.isfile(save_image_path):
                cv2.imwrite(save_image_path, save_image)
            

            save_mask=cv2.imread(os.path.join(mask_folder, labeling_masks[idx+train_end_idx]))
            save_mask_path=os.path.join(save_folder, 'validation', 'mask', f"{validation_img_num}.png")
            if not os.path.isfile(save_mask_path):
                cv2.imwrite(save_mask_path, save_mask)
            validation_img_num+=1
            
        file_number_each_train.append(train_img_num)
        file_number_each_validation.append(validation_img_num)
        save_txt_list_folder(image_folder,save_folder)
    
    #각 파일에 대한 정보 저장
    file = open(f"{save_folder}train/image_folder_index.txt", "a")
    for i in range (len(image_folders)):
        file.write(f'{image_folders[i]} \t = >  {file_number_each_train[i]}.png ~ {file_number_each_train[i+1]-1}.png \n')
    file = open(f"{save_folder}validation/image_folder_index.txt", "a")
    for i in range (len(image_folders)):
        file.write(f'{image_folders[i]} \t = >  {file_number_each_validation[i]}.png ~ {file_number_each_validation[i+1]-1}.png \n')
    
    print(f"train: {start_i_train}.jpg부터 {train_img_num-1}.jpg까지 저장되었습니다.")
    print(f"validation: {start_i_validation}.jpg부터 {validation_img_num-1}.jpg까지 저장되었습니다.")
    print(f"저장위치 : {save_folder}img/ , {save_folder}mask/ ")
    
    return 0

def main():

    """function:
        image_folders에 있는 이미지들을 intergration_folder에 통합하여 저장하고,
        저장된 이미지들의 정보를 txt파일에 저장한다.
        또, intergration_folder에 저장된 이미지들을 train과 validation으로 나누어 저장한다.
        => 데이터셋 바로 확보.
    method:
        image_folers는 이미지가 저장된 폴더들의 리스트
        integration_folder는 통합된 이미지가 저장될 폴더
    """

    image_folders=[]
    #image_folders.append('D:/OneDrive - Sogang/Sogang/23/papers/segment-anything-main (1)/segment-anything-main/notebooks/result_new/Shelf1_051_1652_select/')

    for i in range (1,2):
        #image_folders.append(f'D:/OneDrive - Sogang/Sogang/23/papers/Track-Anything-master/result/img/water_bot1/') #window
        image_folders.append(f'/media/lee/90182A121829F83C/Dataset/ubuntu_data/back_1/img/') #ubuntu

    intergration_folder='D:/Dataset/water_bot/' #window
    intergration_folder='/media/lee/90182A121829F83C/Dataset/water_bot/' #ubuntu
    
    #image_folders.append('D:/OneDrive - Sogang/Sogang/23/papers/Track-Anything-master/result/img/green3/')
    
    for image_folder in image_folders:
        if not image_folder.endswith('/'):
            print(f"{image_folder}는 '/'로 끝나지 않습니다.")
            return 0
    
    #intergration_folder='/media/lee/90182A121829F83C/Dataset/Water_green/train/'
    if not os.path.isdir(intergration_folder):
        os.mkdir(intergration_folder)
    for sub_folder in ['train', 'validation']:
        if not os.path.isdir(os.path.join(intergration_folder, sub_folder, 'img')):
            os.makedirs(os.path.join(intergration_folder, sub_folder, 'img'))
        if not os.path.isdir(os.path.join(intergration_folder, sub_folder, 'mask')):
            os.makedirs(os.path.join(intergration_folder, sub_folder, 'mask'))

        
    does_not_exist=check_before_folder(image_folders, intergration_folder)
    if does_not_exist:
        dataset_integration(image_folders, intergration_folder)

if __name__ == "__main__":
    main()
