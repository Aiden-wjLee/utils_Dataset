import os
import shutil
import random
from tqdm import tqdm

def integrate_datasets(dataset_folder1, dataset_folder2, integrated_folder):
    # 각 데이터셋의 디렉토리 경로를 설정합니다.
    train_img_dirs = [os.path.join(dataset_folder1, 'train/img'), os.path.join(dataset_folder2, 'train/img')]
    train_mask_dirs = [os.path.join(dataset_folder1, 'train/mask'), os.path.join(dataset_folder2, 'train/mask')]
    val_img_dirs = [os.path.join(dataset_folder1, 'validation/img'), os.path.join(dataset_folder2, 'validation/img')]
    val_mask_dirs = [os.path.join(dataset_folder1, 'validation/mask'), os.path.join(dataset_folder2, 'validation/mask')]

    # 통합 디렉토리 경로를 설정합니다.
    integrated_train_img = os.path.join(integrated_folder, 'train/img')
    integrated_train_mask = os.path.join(integrated_folder, 'train/mask')
    integrated_val_img = os.path.join(integrated_folder, 'validation/img')
    integrated_val_mask = os.path.join(integrated_folder, 'validation/mask')

    print("len of train_img_dirs: ", len(train_img_dirs))
    print("len of val_img_dirs: ", len(val_img_dirs))
    # 필요한 디렉토리들을 생성합니다.
    for path in [integrated_train_img, integrated_train_mask, integrated_val_img, integrated_val_mask]:
        os.makedirs(path, exist_ok=True)

    # 이미지와 마스크를 쌍으로 섞고, 복사하는 함수를 정의합니다.
    def integrate_and_shuffle(image_dirs, mask_dirs, integrated_image_dir, integrated_mask_dir, scale1, scale2):
        paired_files = []
        len1=len(os.listdir(image_dirs[0]))
        len2=len(os.listdir(image_dirs[1]))

        # 데이터셋 1에 대한 처리
        images1 = [f for f in os.listdir(image_dirs[0]) if f.endswith('.png' or '.jpg')]
        images1.sort()
        selected_images1 = random.sample(images1, int(len(images1) * scale1))  # Scale1에 따라 샘플링
        paired_files.extend([(img, os.path.join(image_dirs[0], img), os.path.join(mask_dirs[0], img)) for img in selected_images1])

        # 데이터셋 2에 대한 처리
        images2 = [f for f in os.listdir(image_dirs[1]) if f.endswith('.png')]
        images2.sort()
        selected_images2 = random.sample(images2, int(len(images2) * scale2))  # Scale2에 따라 샘플링
        paired_files.extend([(str(int(img.split('.')[0])+int(len1))+'.png', os.path.join(image_dirs[1], img), os.path.join(mask_dirs[1], img)) \
                             for img in selected_images2])

        print("len of paired_files: ", len(paired_files))
        # 파일 쌍을 무작위로 섞습니다.
        random.shuffle(paired_files)

        # 파일 쌍을 통합 디렉토리로 복사합니다. 
        for i,( img_name, img_path, mask_path) in tqdm(enumerate(paired_files), desc=f'Integrating dataset to {integrated_image_dir}', ncols=100):
            img_name_i=str(i)+'.png'
            shutil.copy(img_path, os.path.join(integrated_image_dir, img_name_i))
            shutil.copy(mask_path, os.path.join(integrated_mask_dir, img_name_i))

    # 트레이닝 데이터에 대한 통합 및 무작위 섞기를 수행합니다.
    integrate_and_shuffle(train_img_dirs, train_mask_dirs, integrated_train_img, integrated_train_mask, 0.5, 1)
    
    # 검증 데이터에 대한 통합 및 무작위 섞기를 수행합니다.
    integrate_and_shuffle(val_img_dirs, val_mask_dirs, integrated_val_img, integrated_val_mask, 0.5, 1)

    print('Dataset integration and shuffling completed.')

# 스크립트를 실행합니다.
if __name__ == "__main__":
    dataset_folder1 = './nachi_grid_1027'
    dataset_folder2 = './nachi_manual_1028'
    integrated_folder = './nachi_grid_integrated_12_4'
    
    integrate_datasets(dataset_folder1, dataset_folder2, integrated_folder)