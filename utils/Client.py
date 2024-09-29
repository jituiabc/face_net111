import paramiko
import os
from datetime import datetime
import re
import ast
class Client(object):
    def __init__(self , hostname , port , username , passwd ) -> None:
        self.hostname = hostname
        self.port = port
        self.passwd = passwd
        self.username = username
        # 创建SSH客户端
        self.client = self.generate()
        self.sftp = self.client.open_sftp()
        print("初始化成功")

    def generate(self):
        client = paramiko.SSHClient()
        # 自动添加主机密钥
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接远程主机
        client.connect(self.hostname, self.port, self.username, self.passwd)
        return client

    def upload_files_to_server(self , local_dir_path , remote_dir_path) -> None:
        """
        将本地目录中的所有文件上传到远程服务器。

        参数:
        local_dir (str): 本地目录路径。
        remote_dir (str): 远程目录路径。
        """
        if not os.path.exists(local_dir_path):
            print("本地路径不存在...")
            return -1
        
        for item in os.listdir(local_dir_path):
            local_file_path = os.path.join(local_dir_path,item)
            if os.path.isfile(local_file_path):
                # 构建远程文件的完整路径
                remote_path = os.path.join(remote_dir_path, item)
                # 上传文件
                self.sftp.put(local_file_path, remote_path)
        print("上传成功")
        return

    def download_file_from_server(self,remote_dir , local_dir):
        """
            将远程服务器上指定的文件下载到本地，若是文件夹，则将文件夹下的文件进行遍历，并下载到本地
        """

        os.makedirs(local_dir , exist_ok=True)

        if self.remote_is_dir(remote_dir):
            remote_files = self.sftp.listdir(remote_dir)
            
        print(remote_files)

    def upload_one_file(self , local_path , remote_path) -> None:
        self.sftp.put(local_path , remote_path)
    
    def download_one_file(self , local_path , remote_path) -> None:
        self.sftp.get(remote_path , local_path)

    def show_results(self , show_err = False) -> str:
        stdin, stdout, stderr = self.client.exec_command(
                '/home/ljw/anaconda3/envs/py310/bin/python3 /home/ljw/pythonfile/zhian_school/face/face_encoding.py'
            )
        stdin, stdout, stderr = self.client.exec_command(
                '/home/ljw/anaconda3/envs/py310/bin/python3 /home/ljw/pythonfile/zhian_school/face/detect.py'
            )
        output = stdout.read().decode('utf-8')
        print('output:\n  ', output)

        if show_err == True:
            error = stderr.read().decode('utf-8')
            if error:
                print(error)
            else:
                print("没有报错信息！")
        return stdin , output, stderr
        
    def remote_is_dir(self , path) -> bool :
        try:
            self.sftp.listdir()
            return True
        except IOError:
            return False

    @staticmethod
    def get_name(txt):
        # print(txt)
        result = re.findall(r"姓名： (.*)" , txt)
        # name = result.group(0)
        # print(type(result[0]))
        name_lst = ast.literal_eval(result[0])
        # print(type(name_lst))
        return name_lst
    @classmethod
    def get_face_id(cls , txt):
        result = re.findall(r"id (.*)", txt )
        id_lst = ast.literal_eval(result[0])
        return id_lst

    def close(self):
        self.client.close()
        self.sftp.close()


if __name__ == "__main__":
    client = Client(hostname='172.16.2.143',port=22,username='ljw',passwd='ljw20040917')
