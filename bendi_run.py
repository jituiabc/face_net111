import cv2
import os
from datetime import datetime
import time

# 确保face_db/pic_dir文件夹存在  
directory = 'face_db/pic_dir'
if not os.path.exists(directory):
    os.makedirs(directory)

# 初始化摄像头  
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Cannot open camera.")
    exit()

# 标志变量，用于控制是否保存图片  
save_image = False

# 定时器，用于控制拍摄频率（以秒为单位）  
capture_interval = 3
last_capture_time = time.time()

while True:
    # 读取一帧  
    ret, frame = cap.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

        # 显示画面
    cv2.imshow('Camera', frame)

    # 检查是否有按键输入  
    key = cv2.waitKey(1) & 0xFF

    # 检查是否到了拍摄时间间隔，并且用户按下了's'键来保存图片  
    current_time = time.time()
    if (current_time - last_capture_time >= capture_interval) or (key == ord('s')):
        # 格式化当前时间作为文件名  
        file_name = os.path.join(directory, datetime.now().strftime("%Y-%m-%d_%H-%M-%S.jpg"))

        # 保存图片  
        cv2.imwrite(file_name, frame)
        print(f"Photo saved as {file_name}")

        # 更新上次拍摄时间  
        last_capture_time = current_time

        # 可选：如果用户已经保存了图片，我们可以重置定时器，但在这里我们保持它继续计时  
        # 因为用户可能想要在下一个间隔再次保存图片，而不必等待整个间隔过去  

    # 检查是否按下了'q'键来退出循环  
    if key == ord('q'):
        break

    # 释放摄像头和关闭所有OpenCV窗口
cap.release()
cv2.destroyAllWindows()