from pathlib import Path
import sys
import os
import time
from datetime import datetime
from pathlib import Path
import os
from tqdm import tqdm
from utils.Client import Client
import re

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

dir_path = str(ROOT) + '/face_db/pic_dir'

# 设置SSH连接参数
hostname = '172.16.2.143'
port = 22
username = 'ljw'
password = 'ljw20040917'


def directory_judge(directory_path):
    """
    检查指定目录内是否有文件（不包括子目录）。

    参数:
        directory_path (str): 目录路径。

    返回:
        bool: 如果目录内有文件，则返回True；否则返回False。
    """
    # 检查目录是否存在
    if not os.path.exists(directory_path):
        return False

        # 检查目录是否真的是一个目录
    if not os.path.isdir(directory_path):
        return False

        # 列出目录中的所有项（文件和子目录）
    items = os.listdir(directory_path)
    print(items)
    # 遍历所有项，只检查文件（不包括子目录）
    for item in items:
        # 使用os.path.isfile检查是否为文件
        if os.path.isfile(os.path.join(directory_path, item)):
            return True
            # 如果没有找到任何文件，则返回False
    return False

def delete(directory):
    if os.path.exists(directory):
        # 遍历目录下的所有文件和子目录
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                # 如果它是文件，则删除
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    # 如果它是目录，但你不希望删除目录（只删除文件），则跳过
                # 如果你想递归删除目录及其内容，可以使用shutil.rmtree(file_path)
            except Exception as e:
                print(f"Error while deleting {file_path}. Reason: {e}")
    else:
        print(f"Directory {directory} does not exist.")

if __name__ == '__main__':
    while True:
        if directory_judge(dir_path):
            print("检测到文件...")
            # 远程服务器上的目标目录（你需要在服务器上创建这个目录）
            remote_dir = '/home/ljw/pythonfile/zhian_school/face/face_db/pic_dir'

            client = Client(hostname,port,username,password)

            # 上传文件到服务器
            client.upload_files_to_server(dir_path, remote_dir)

            print("上传服务器成功!")
            # 使用exec_command执行远程服务器上的Python脚本
            stdin , output , stderr = client.show_results(show_err = True)
            print("="*50 , "\n" , output)
            pattern = r'\/home[^\s]+'
            names= client.get_name(output)
            ids = client.get_face_number(output)
            # print("匹配出来的res : " , res)
            # 使用 re.findall 查找所有匹配的路径
            # matches = re.findall(pattern, output)
            # 打印匹配的路径
            # print("matches:",matches)
            # for path in matches:
            #     print(path)
            #     client.download_file_from_server(path , str(ROOT) + '/face_db/pic_dir')
            #     print(f"成功下载到本地文件夹{str(ROOT) + '/face_db/pic_dir'}")

            directory = str(ROOT) + "/face_db/pic_dir"
            delete(directory=directory)
            client.close()

        else:
            print("[Waiting] No file in pic_dir")
            # TODO: 没有文件时，你可以选择记录日志、等待一段时间再检查，或进行其他操作
            time.sleep(5)  # 例如，等待一分钟再检查
