import shutil

import pandas as pd
from face_detected.retinaface import Retinaface
import cv2
import os
from pathlib import Path
from tqdm import tqdm
from datetime import datetime
from utils.write_to_csv import write_to_csv

"""
0，定义常量信息
"""
ROOT = "/home/ljw/pythonfile/zhian_school/face/"  # 图像根目录
face_db_path = Path(ROOT) / 'face_db'  # 人脸数据库路径
pic_dir = face_db_path / 'pic_dir'  # 要检测的文件夹路径
save_dir = face_db_path / 'face_save'  # 图片保存的路径
log_dir = face_db_path / 'log'  # 检测完图像转移到log文件夹
IS_UNKNOWN = False
# 确保保存和日志目录存在
os.makedirs(save_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

# 文件名列表
file_names = os.listdir(pic_dir)

"""
1，实例化对象
"""
retinaface: Retinaface = Retinaface()

s = 'cuda' if Retinaface._defaults['cuda'] else 'cpu'
print("Using device : " + s)

"""
2，检测识别人脸信息
"""



for file_name in tqdm(file_names):
    if file_name[0] == '.':
        continue

    if file_name.lower().endswith(
            ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
        file_path = str(pic_dir) + '/' + file_name
        # print(file_path)
        img = cv2.imread(file_path)

        if img is None:
            print(f"无法读取文件: {file_path}")
            continue

        try:
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            r_image, face_names, face_ids, conf, face_number, reg_time , _ = retinaface.detect_image(img)
            r_image = cv2.cvtColor(r_image, cv2.COLOR_BGR2RGB)
            conf = float(conf)

            print("检测到的人脸数量", face_number)
            print("姓名：", face_names)

            """
            这段代码是保存内容到csv文件中的
            """
            # TODO： 如果连续三张图片都检测到是同一个人，则把它写进表格里
            for i in range(len(face_names)):
                for id, name in zip(face_names, face_ids):
                    write_to_csv(id, name, reg_time, conf)
            """
            保存检测完成的图片
            """
            # 使用时间戳和文件名作为保存的文件名，以避免冲突
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
            save_path = str(save_dir) + '/' + f"{file_name.split('.')[0]}_{timestamp}.jpg"
            cv2.imwrite(save_path, r_image)
            # print("已保存，图片保存路径为：", save_path)

        except Exception as e:
            print(f"处理文件 {file_name} 时发生错误: {e}")

for file_name in os.listdir(pic_dir):
    file_path = pic_dir / file_name
    new_file_path = log_dir / file_name
    shutil.move(file_path, new_file_path)
    print(f"已将文件 {file_name} 移动到 {log_dir}/{file_name}")

# 清空 pic_dir
for file_name in os.listdir(pic_dir):
    file_path = pic_dir / file_name
    try:
        if file_path.is_file() or file_path.is_symlink():
            os.unlink(file_path)
        elif file_path.is_dir():
            shutil.rmtree(file_path)
    except Exception as e:
        print(f'无法删除 {file_path}. 原因: {e}')
