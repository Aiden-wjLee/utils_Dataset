import cv2
import os
import re
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
    before_imgs = [img for img in os.listdir(save_folder+'img') if img.endswith(".png") or img.endswith(".jpg")]
    before_imgs.sort(key=lambda x: int(x.split('.')[0]))
    
    
    before_masks = [img for img in os.listdir(save_folder+'mask') if img.endswith(".png") or img.endswith(".jpg")]
    before_masks.sort(key=lambda x: int(x.split('.')[0]))
    
    
    #원래 있던 이미지와 새로운 이미지의 개수가 다르면 오류
    print("len(before_images), len(before_masks): ",len(before_imgs), len(before_masks))
    if (len(before_imgs) != len(before_masks)):
        print("len(before_images) != len(before_masks)")
        return 0
    
    #전 이미지 이후에 저장.
    if len(before_imgs)!=0 and len(before_masks)!=0: #전 이미지가 있으면 마지막 이미지 번호+1부터 저장
        print(before_imgs[len(before_imgs)-1], before_masks[len(before_masks)-1])
        start_i=int(before_imgs[len(before_imgs)-1].split('.')[0])+1
    else: #전 이미지가 없으면 0부터 저장
        start_i=0
    print("start_i: ",start_i)
    img_num=start_i ; mask_num=start_i
    
    #
    file_number_each=[]
    file_number_each.append(start_i)
    #각 이미지 폴더에 적용
    for image_folder in image_folders:
        print('==============='+image_folder+'===============')
        img_folder = image_folder#+'img/'
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
        
        #img폴더에 대해 읽고, 저장
        for image in (labeling_imgs):
            save_image=cv2.imread(os.path.join(img_folder, image))
            save_image_path=save_folder+'img/'+str(img_num)+'.png'
            if not os.path.isfile(save_image_path):
                cv2.imwrite(save_image_path, save_image)
            img_num+=1
        
        #mask 폴더에 대해 읽고, 저장
        for image in (labeling_masks):
            save_mask=cv2.imread(os.path.join(mask_folder, image))
            save_mask_path=save_folder+'mask/'+str(mask_num)+'.png'
            if not os.path.isfile(save_mask_path):
                cv2.imwrite(save_mask_path, save_mask)
            mask_num+=1
        print (f'{image_folder} 폴더의 이미지 저장 완료 :  ~  {img_num-1}.png')
        file_number_each.append(img_num)
        save_txt_list_folder(image_folder,save_folder)
    
    #각 파일에 대한 정보 저장
    file = open(f"{save_folder}image_folder_index.txt", "a")
    for i in range (len(image_folders)):
        file.write(f'{image_folders[i]} \t = >  {file_number_each[i]}.png ~ {file_number_each[i+1]-1}.png \n')
    
    print(f"{start_i}.jpg부터 {img_num-1}.jpg까지 저장되었습니다.")
    print(f"저장위치 : {save_folder}img/ , {save_folder}mask/ ")
    
    return 0

def main():
    image_folders=[]
    #image_folders.append('D:/OneDrive - Sogang/Sogang/23/papers/segment-anything-main (1)/segment-anything-main/notebooks/result_new/Shelf1_051_1652_select/')

    #for i in range (1,4):
    #    image_folders.append(f'D:/OneDrive - Sogang/Sogang/23/papers/Track-Anything-master/result/img/floor{i}/') #window
        #image_folders.append(f'D:/Dataset/prior/result/img/floor{i}/') ##수정해야하는사항
        
    image_folders.append('D:/Dataset/nachi_error/images_error/left/')
    image_folders.append('D:/Dataset/nachi_error/images_error/right/')
    intergration_folder='D:/Dataset/Water_real_floor/train/' ##수정해야하는 사항
    
    
    #image_folders.append('D:/OneDrive - Sogang/Sogang/23/papers/Track-Anything-master/result/img/green3/')
    
    for image_folder in image_folders:
        if not image_folder.endswith('/'):
            print(f"{image_folder}는 '/'로 끝나지 않습니다.")
            return 0
    
    #intergration_folder='/media/lee/90182A121829F83C/Dataset/Water_green/train/'
    if not os.path.isdir(intergration_folder):
        os.mkdir(intergration_folder)
    if not os.path.isdir(intergration_folder+'img/'):
        os.mkdir(intergration_folder+'img/')
    if not os.path.isdir(intergration_folder+'mask/'):
        os.mkdir(intergration_folder+'mask/')
        
    does_not_exist=check_before_folder(image_folders, intergration_folder)
    if does_not_exist:
        dataset_integration(image_folders, intergration_folder)

if __name__ == "__main__":
    main()
