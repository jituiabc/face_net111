import math
import os
import time
import torch
import cv2
import numpy as np
from PIL import Image
import os
import shutil
from pathlib import Path


# ---------------------------------------------------#
#   对输入图像进行resize
# ---------------------------------------------------#
def letterbox_image(image, size):
    ih, iw, _ = np.shape(image)
    w, h = size
    scale = min(w / iw, h / ih)
    nw = int(iw * scale)
    nh = int(ih * scale)

    image = cv2.resize(image, (nw, nh))
    new_image = np.ones([size[1], size[0], 3]) * 128
    new_image[(h - nh) // 2:nh + (h - nh) // 2, (w - nw) // 2:nw + (w - nw) // 2] = image
    return new_image


def preprocess_input(image):
    image -= np.array((104, 117, 123), np.float32)
    return image


# ---------------------------------#
#   计算人脸距离
# ---------------------------------#
def face_distance(face_encodings, face_to_compare):
    if len(face_encodings) == 0:
        return np.empty((0))
    # (n, )
    return np.linalg.norm(face_encodings - face_to_compare, axis=1)


# ---------------------------------#
#   比较人脸
# ---------------------------------#
def compare_faces(known_face_encodings, face_encoding_to_check, tolerance=1):
    dis = face_distance(known_face_encodings, face_encoding_to_check)
    return list(dis <= tolerance), dis


# -------------------------------------#
#   人脸对齐
# -------------------------------------#
def Alignment_1(img, landmark):
    # print('landmark.shape[0] : ' , landmark.shape[0])
    if landmark.shape[0] == 68:
        x = landmark[36, 0] - landmark[45, 0]
        y = landmark[36, 1] - landmark[45, 1]
    elif landmark.shape[0] == 5:
        x = landmark[0, 0] - landmark[1, 0]
        y = landmark[0, 1] - landmark[1, 1]
    # print("x : ", x , "y : " , y)
    # 眼睛连线相对于水平线的倾斜角
    if x == 0:
        angle = 0
    else:
        # 计算它的弧度制
        angle = math.atan(y / x) * 180 / math.pi

    center = (img.shape[1] // 2, img.shape[0] // 2)

    RotationMatrix = cv2.getRotationMatrix2D(center, angle, 1)  # 旋转
    # 仿射函数
    new_img = cv2.warpAffine(img, RotationMatrix, (img.shape[1], img.shape[0]))

    RotationMatrix = np.array(RotationMatrix)
    new_landmark = []
    for i in range(landmark.shape[0]):
        pts = []
        pts.append(RotationMatrix[0, 0] * landmark[i, 0] + RotationMatrix[0, 1] * landmark[i, 1] + RotationMatrix[0, 2])
        pts.append(RotationMatrix[1, 0] * landmark[i, 0] + RotationMatrix[1, 1] * landmark[i, 1] + RotationMatrix[1, 2])
        new_landmark.append(pts)
        # print("new_landmarks :" , new_landmark , "pts :" , pts)

    new_landmark = np.array(new_landmark)

    return new_img, new_landmark


def delete_hidden_files(folder_path):
    """
    删除指定文件夹及其子文件夹下所有以'.'开头的文件（隐藏文件）。

    :param folder_path: 要处理的文件夹路径
    """
    # 检查路径是否存在
    if not os.path.exists(folder_path):
        print("提供的路径不存在:", folder_path)
        return

        # 遍历文件夹
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查文件名是否以'.'开头
            if file.startswith('.'):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"已删除: {file_path}")
                except Exception as e:
                    print(f"删除文件时出错: {file_path}。错误: {e}")


def delete_directory_contents(directory):
    # 确保目录存在
    if os.path.exists(directory):
        # 遍历目录下的所有文件和子目录
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                # 如果它是文件或链接，则删除
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    # 如果它是目录，但只想删除文件（不删除目录），则跳过
                # 如果想递归删除目录及其内容，可以使用 shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error while deleting {file_path}. Reason: {e}")
    else:
        print(f"Directory {directory} does not exist.")

    # 指定文件路径，以便可以正确解析ROOT


def capture_photo_from_camera(pic_dir='../face_db/pic_dir'):
    # 检查pic_dir是否存在，如果不存在则创建
    if not os.path.exists(pic_dir):
        os.makedirs(pic_dir)

        # 打开摄像头
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Unable to open camera")
        exit()

    print("Press 's' to capture a photo. Press 'q' to quit.")

    while True:
        # 读取一帧
        ret, frame = cap.read()

        if not ret:
            print("Error: Unable to fetch frame")
            break

            # 显示结果帧
        cv2.imshow('Camera', frame)

        # 等待按键
        k = cv2.waitKey(1) & 0xFF

        # 如果按下's'键，则保存图片
        if k == ord('s'):
            # 获取当前时间，用于生成文件名
            filename = os.path.join(pic_dir, f"photo_{cv2.getTickCount()}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Photo saved as {filename}")

            # 如果按下'q'键，则退出循环
        elif k == ord('q'):
            break

            # 释放摄像头资源
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    while (True):
        path = '/home/ljw/pythonfile/My_Insightface/face' if torch.cuda.is_available() else '/Volumes/ljwdisk/PycharmProject/face_net'
        delete_hidden_files(path)
        time.sleep(60)
    # capture_photo_from_camera()
