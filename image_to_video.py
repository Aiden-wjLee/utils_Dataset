

import cv2
import os
from tqdm import tqdm
def images_to_video(image_folder, video_name, fps, size=None):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png") or img.endswith(".jpg")]
    images.sort(key=lambda x: int(x.split('.')[0]))
    print(images)
    print("len(images): ", len(images))
    # 첫 번째 이미지를 읽어, 비디오 해상도를 결정합니다.
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    if size is not None:
        frame = cv2.resize(frame,size)
    print("frame.shape: ",frame.shape)
    #cv2.imshow('frame',frame)
    #cv2.waitKey(0)
    height, width, _ = frame.shape
    print("height",height)

    # VideoWriter 객체를 생성합니다.
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # 코덱 설정 (XVID, MP4V 등)
    out = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    # 각 이미지를 프레임으로 추가합니다.
    for image in tqdm(images, desc="Converting images to video...", ncols=100):
        frame = cv2.imread(os.path.join(image_folder, image))
        if size is not None:
            frame = cv2.resize(frame,size)
        ##frame = cv2.resize(frame,(255,255))
        out.write(frame)
        

    out.release()
    print(f"{image_folder} : Video saved successfully!")


def main():
    """
    Args:
        image_folder (str): path to image folder.
        video_name (str): path to video name.
    """
    #'D:/C_data/Downloads/test6_video_pred_mask/content/Segment-and-Track-Anything/tracking_results/test6_video/test6_video_masks/'
    #image_folder='D:/Dataset/nachi/images_real_connector/left/'
    #image_folder = '/media/lee/90182A121829F83C/Dataset/Water_real_floor/train/img/'
    #image_folder ='D:/Dataset/nachi_new_view/origin/'
    image_folder = 'E:/dataset/nachi/images_20231028_manual/right/'  #origin/
    if not image_folder.endswith('/'):
        image_folder+='/'
    ###video_name = image_folder+'../floor_new_val2.avi'
    video_name= image_folder+'../images_20231028_manual_right.mp4' #'../LR_2560_1024.mp4'
    fps = 30
    images_to_video(image_folder, video_name, fps,(1280,512)) #(가로, 세로)

if __name__ == "__main__":
    main()