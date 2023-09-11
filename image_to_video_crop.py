def crop_image(image, xywh):
    """
    crop image from original numpy array

    check a value and rotate image if the original image is rotated
    :param image: original numpy array image
    :param xywh: x = start x-axis point(horizontal)
                 y = start y-axis point(vertical)
                 w = the width of cropped image, aligned with x
                 h = the height of cropped image, aligned with y
    :return: the cropped numpy array
    """
    # print("\nStart Cropping Image ...")
    real_h = image.shape[0]
    real_w = image.shape[1]

    x = xywh[0]
    y = xywh[1]
    w = xywh[2]
    h = xywh[3]

    # rotate if h > w
    if real_h > real_w:
        images = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        real_h = images.shape[0]
        real_w = images.shape[1]

    if x + w > real_w:
        # print("insert value under", real_w, image)
        raise ValueError("insert value under", real_w, image)
    if y + h > real_h:
        # print("insert value under", real_h, image)
        raise ValueError("insert value under", real_h, image)

    cropped_image = image[y: y + h, x: x + w]
    return cropped_image




import cv2
import os

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
    height, width, _ = frame.shape

    # VideoWriter 객체를 생성합니다.
    fourcc = cv2.VideoWriter_fourcc(*'XVID') # 코덱 설정 (XVID, MP4V 등)
    out = cv2.VideoWriter(video_name, fourcc, fps, (width, height))

    # 각 이미지를 프레임으로 추가합니다.
    for image in images:
        frame = cv2.imread(os.path.join(image_folder, image))
        if size is not None:
            frame = crop_image(frame, xywh=[16, 0, 2560, 1024])
            frame = cv2.resize(frame,size)
        ##frame = cv2.resize(frame,(255,255))
        out.write(frame)
        

    out.release()
    print(f"{image_folder} : Video saved successfully!")


def main():
    #image_folder = 'D:/OneDrive - Sogang/Sogang/23/papers/segment-anything-main (1)/segment-anything-main/notebooks/result/429_2120/'
    #image_folder='D:/OneDrive - Sogang/Sogang/23/papers/segment-anything-main (1)/segment-anything-main/notebooks/result_new/Shelf5_051_1926/'
    #'D:/C_data/Downloads/test6_video_pred_mask/content/Segment-and-Track-Anything/tracking_results/test6_video/test6_video_masks/'
    #image_folder='D:/Dataset/nachi/images_real_connector/left/'
    #image_folder='D:/OneDrive - Sogang/Sogang/23/papers/Track-Anything-master/result/mask/cross_red/'
    #image_folder='D:/Dataset/nachi_2560_1024/Original_L_2560_1024/'
    image_folder='D:/Dataset/nachi_2560_1024_LR/original_nachi_2560_1024_LR/'
    if not image_folder.endswith('/'):
        image_folder+='/'
    ###video_name = image_folder+'../floor_new_val2.avi'
    video_name= image_folder+'../nachi_2560_1024_LR.mp4' #'../LR_2560_1024.mp4'
    fps = 30
    images_to_video(image_folder, video_name, fps,(1280,512)) #(가로, 세로)

if __name__ == "__main__":
    main()
