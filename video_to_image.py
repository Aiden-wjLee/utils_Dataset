import cv2
import os

# 영상 로드


def result_original(file_path, image_name, save_path):
    fullname=file_path+image_name


    video = cv2.VideoCapture(str(fullname))
    #video_name=fullname.split('.')[0]
    video_name=image_name.split('.')[0]

    if not os.path.exists(f'{save_path}{str(video_name)}'):
        os.makedirs(f'{save_path}{str(video_name)}')

    else:
        print(f"{fullname} 경로는 이미 존재합니다.")
        exit()
        
    # 비디오 프레임 추출
    count = 0
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            # 프레임 저장
            save_frame_path=f'{save_path}{str(video_name)}/{str(count).zfill(5)}.png'
            if os.path.exists(save_frame_path):
                print(f'{save_frame_path} 이미지가 존재합니다.')
            cv2.imwrite( save_frame_path, frame)
            count += 1
        else:
            break
    video.release()
    print(f'{save_path}{str(video_name)}의 프레임을 추출하였습니다.')
    
def main():
    file_path='D:/OneDrive - Sogang/문서/카카오톡 받은 파일/'
    save_path='D:/Dataset/prior/ '#'./result/img/'
    #image_name='green3.mp4'
    
    # for i in range(14,15):
    #     image_name=f'green{i}.mp4'
    #     result_original(file_path, image_name,save_path)
    
    for i in range(1,2):
        image_name=f'caffe{i}.mp4'
        result_original(file_path, image_name,save_path)
        
        
    #result_original(file_path, image_name)
if __name__=='__main__':
    main()