import math
import argparse
from pathlib import Path
import sys
import os
from face_detected.retinaface import Retinaface
import cv2
import time
import datetime
import csv
from pathlib import Path
import pandas as pd
from tqdm import tqdm

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

EXCEL_PATH = str(ROOT) + '/existed_name.csv'
VIDEOCAP = 'rtsp://ljw:040917@192.168.18.225:8554/live'
dir_origin_path = ROOT / 'face_db/pic_dir'
dir_save_path = ROOT / 'face_db/face_save'
"""

This is a test


"""

"""
    绝对转相对
"""
FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH


# ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative path

def write2csv(**kwargs):
    print(kwargs)
    # with open('existed_name.csv' , 'a+' , encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     writer.writerow([
    #         kwargs['stu_name'],
    #         kwargs['stu_id'],
    #         kwargs['reg_time']
    #     ])


def show(face_names, face_ids, conf, reg_time, t, r_image):
    print("detecting image successfully!")
    print("face_names: ", face_names)
    print("face_ids: ", face_ids)
    print(f"conf : {conf * 100} %")
    # reg_time = datetime.datetime.now()
    print("签到时间：", reg_time)
    print("检测用时：", t)
    r_image = cv2.cvtColor(r_image, cv2.COLOR_RGB2BGR)
    # cv2.imshow("after",r_image)
    cv2.imwrite(f"face_db/face_save/face_result_{datetime.datetime.now()}.jpg", r_image)
    print("image saved successfully!")


"""
检查检测到的学生是否在excel里
"""


def check_stu_is_in_excel(student_id):
    file_path = EXCEL_PATH
    try:
        # 读取Excel文件
        df = pd.read_csv(file_path)
        if '学号' in df.columns:
            # 检查学生学号是否存在于'学号'列中
            if student_id in df['学号'].values:
                return True
            else:
                return False
        else:
            print("Excel文件中没有名为'学号'的列。")
            return False
    except Exception as e:
        print(f"读取Excel文件时发生错误: {e}")
        return False


def Main(opt):
    retinaface = Retinaface()
    print("现在使用的权重: ", Retinaface._defaults['retinaface_model_path'])
    print("现在使用的主干网络: ", Retinaface._defaults['retinaface_backbone'])
    mode = opt.mode
    # mode = opt.mode[0]
    face_names = []
    face_ids = []
    reg_time = 0.0
    if isinstance(mode, list):
        mode = mode[0]
    if mode == "predict":
        '''
        predict.py有几个注意点
        1、无法进行批量预测，如果想要批量预测，可以利用os.listdir()遍历文件夹，利用cv2.imread打开图片文件进行预测。
        2、如果想要保存，利用cv2.imwrite("img.jpg", r_image)即可保存。
        3、如果想要获得框的坐标，可以进入detect_image函数，读取(b[0], b[1]), (b[2], b[3])这四个值。
        4、如果想要截取下目标，可以利用获取到的(b[0], b[1]), (b[2], b[3])这四个值在原图上利用矩阵的方式进行截取。
        5、在更换facenet网络后一定要重新进行人脸编码，运行encoding.py。
        '''

        while True:
            img = input('Input image filename:')
            # img = '/Users/guosiqi/vippython/face_net/face_db/test_datasets/ljw3.jpg'
            image = cv2.imread(img)
            if image is None:
                print('Open Error! Try again!')
                ans = int(input('Please enter next'))
                if ans == 0:
                    break
                continue
            else:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                conf = 0
                try:
                    t1 = time.time()
                    r_image, face_names, face_ids, conf, face_number, reg_time = retinaface.detect_image(image)
                    # if face_names:  # 如果检测到人脸
                    #     # 将人脸数据上传到数据库
                    #     for name, face_id, time1 in zip(face_names, face_ids, reg_time):
                    #         if name and face_id:  # 确保有检测到的人脸和对应的ID
                    #             # 插入数据到数据库
                    #             # insert_sql = "INSERT INTO student (name, face_id, registered_time) VALUES (%s, %s, %s)"
                    #             # /Volumes/ljwdisk/PycharmProject/face_net/face_db/test_datasets/IMG_7379.JPG
                    #             querys("INSERT INTO student (name, stu_id, reg_time) VALUES (%s, %s, %s)",
                    #                    [name, face_id, time1])
                    #             print("已插入到数据库")
                    if not check_stu_is_in_excel(face_ids):
                        # 如果检测到的学号不在Excel里，则添加
                        write2csv()
                        pass

                    else:
                        # 如果检测到的学号在Excel里，则更新时间
                        pass
                    conf = float(conf)

                except ValueError as v:
                    r_image = retinaface.detect_image((image))
                    # print(v)
                if not face_names:
                    print("没有检测到人脸！")
                else:
                    t2 = time.time()
                    show(face_names, face_ids, conf, reg_time, t2 - t1, r_image)

    elif mode == 'video':
        cap = cv2.VideoCapture(opt.video_path)
        if opt.video_save_path != "":
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
            size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            print(cv2.CAP_PROP_FRAME_WIDTH)
            print(cv2.CAP_PROP_FRAME_HEIGHT)
            out = cv2.VideoWriter(f'face_db/video_save/output_{datetime.datetime.now()}.avi', fourcc, opt.video_fps,
                                  (640, 480))  # 尺寸要一样
        # fps = cap.get(cv2.CAP_PROP_FPS)
        # total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print("-" * 50)
        current_frame = 0
        cnt = 0
        while cap.isOpened():
            cnt += 1
            ret, frame = cap.read()
            frame = cv2.resize(frame, (640, 480))
            if not ret:
                break
            # color = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            try:
                frame, name, face_ids, conf, face_number, reg_time = retinaface.detect_image(frame)
                print(name)
                # print(name[0])
                if name[0] != 'Unknown' and name[0] not in face_names:
                    face_names.append(name)
                # frame = cv2.cvtColor(frame , cv2.COLOR_RGB2BGR)
                conf = float(conf)
                print("检测到的人脸数量", face_number)
                print("successfully detected")
            except:
                frame = retinaface.detect_image(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if not face_names:
                print("没有检测到人脸！")
            else:
                # print("帧率:", fps)
                # print("总帧数:", total_frames)
                print("detecting image successfully!")
                print("face_names: ", face_names)
                print("face_ids: ", face_ids)
                print(f"conf : {conf * 100} %")
                # reg_time = datetime.datetime.now()
                print("签到时间：", reg_time)
                print("-" * 50)
                # for i in range(face_number):
                #     cv2.putText(frame, f"Name: {face_names[i]}, ID: {face_ids[i]}", (50, 50 + i * 30),
                #                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow("video", frame)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break
            if opt.video_save_path is not None:
                out.write(frame)
                # cv2.imwrite(f'face_db/face_save/video_result_{datetime.datetime.now()}.mp4' , frame)
                print("保存成功！！！！！！！")
        cap.release()
        if opt.video_save_path != "":
            print("Save processed video to the path :" + opt.video_save_path)
            out.release()
        cv2.destroyAllWindows()

    elif mode == 'dir_predict':
        img_names = os.listdir(dir_origin_path)
        for img_name in tqdm(img_names):
            if img_name.lower().endswith(
                    ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                image_path = os.path.join(dir_origin_path, img_name)
                image = cv2.imread(image_path)
                # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                try:
                    r_image, face_names, face_ids, conf, face_number, reg_time = retinaface.detect_image(image)
                    print(r_image)
                    conf = float(conf)
                    print("检测到的人脸数量", face_number)
                # r_image = retinaface.detect_image(image)
                except:
                    r_image = retinaface.detect_image((image))
                # r_image = cv2.cvtColor(r_image, cv2.COLOR_RGB2BGR)
                if not os.path.exists(dir_save_path):
                    os.makedirs(dir_save_path)
                cv2.imwrite(os.path.join(dir_save_path, img_name), r_image)

    elif mode == "fps":
        img = cv2.imread('face_db/test_datasets/obama.jpg')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        tact_time = retinaface.get_FPS(img, opt.test_interval)
        print(str(tact_time) + ' seconds, ' + str(1 / tact_time) + ' FPS')

    elif mode == 'register':
        print(retinaface.known_face_IDs)
        name = input("请输入您的姓名...\n")
        number = input("请输入您的学号...\n")
        if number in retinaface.known_face_IDs:
            print("您的信息已经录入过了！")
            Main(opt)
        # name = "刘珈玮"
        # number = "220102050135"
        capture = cv2.VideoCapture(VIDEOCAP)
        cnt = 0
        while True:
            ret, frame = capture.read()
            if not ret:
                print("There was an error while using capture...")
                break
            cv2.imshow("register", frame)
            cv2.putText(frame, "请在做好准备（准确看向摄像头后）按下's'拍照.", (0, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5,
                        (255, 0, 0))
            img_path = "../face_db/train_datasets/" + name + '_' + number + '_' + str(datetime.datetime.now()) + '.jpg'
            if cv2.waitKey(1) & 0xFF == ord('s'):
                cv2.imwrite(img_path, frame)
                print("保存成功!")
                break
            if cv2.waitKey(0) & 0xFF == ord('q'):
                print("正常退出！")
            print(img_path)
        capture.release()
        cv2.destroyAllWindows()
        try:
            retinaface.encode_face_dataset([img_path], name, number)
            print("人脸编码成功！")
            print(f"姓名：{name} , 学号：{number} 已成功载入...")
            wf = open(r"../existed_name.csv", 'a+', encoding='utf-8')
            csv_writer = csv.writer(wf, delimiter=',')
            csv_writer.writerow([name, number])
        except BaseException as b:
            print("人脸载入失败！")
            print("ERROR:", b)

        '''
            在更换facenet网络后一定要重新进行人脸编码，运行face_encoding.py。
        '''
    elif mode == 'encoding':
        encoding()
    elif mode == 0:
        quit(0)

    print(face_names)


'''
在更换facenet网络后一定要重新进行人脸编码，运行encoding。
'''


def encoding():
    retinaface = Retinaface()

    list_dir = os.listdir(ROOT / "face_db/train_datasets")
    print(list_dir)
    image_paths = []
    names = []
    student_IDs = []
    print(list_dir)
    for name in list_dir:
        if name == ".DS_Store":
            continue
        image_paths.append(str(ROOT) + "/face_db/train_datasets/" + name)
        names.append(name.split("_")[0])
        student_IDs.append(name.split("_")[1])
    print(image_paths)
    print(names)
    print(student_IDs)
    retinaface.encode_face_dataset(image_paths, names, student_ID=student_IDs)
    print("face_encoding successful!")


# XXX : 优化方式有待商榷
# def create_student_signin_record(students):
#     """
#
#     :param students: 学生列表，包括姓名，学号，签到时间等
#     :return:
#     """
#     # 创建一个工作簿
#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Student sign-in record"
#
#     # 设置列标题
#     headers = ['姓名', '学号', '第一节课上签到', '第一节课下签到',
#                '第二节课上签到', '第二节课下签到',
#                '第三节课上签到', '第三节课下签到',
#                '第四节课上签到', '第四节课下签到', '晚修']
#
#     # 字体样式
#     bold_font = Font(name='宋体', size=11, bold=True)
#
#     # 设置列宽
#     for col in headers:
#         ws.column_dimensions[chr(ord('A') + headers.index(col))].width = 20
#
#         # 添加并格式化表头
#     for col_num, value in enumerate(headers, 1):
#         cell = ws.cell(row=1, column=col_num, value=value)
#         cell.font = bold_font
#         cell.alignment = Alignment(horizontal='center', vertical='center')
#
#         # 填充学生信息
#     for row_num, student in enumerate(students, 2):
#         for col_num, data in enumerate(student, 1):
#             ws.cell(row=row_num, column=col_num, value=data)
#
#             # 保存工作簿
#     wb.save("Student sign-in record.xlsx")


def parse_opt():
    parse = argparse.ArgumentParser()
    parse.add_argument('-m', '--mode', nargs='+', type=str, default='encoding',
                       help='choose mode : predict,video,fps,dir_predict,register,encoding')
    parse.add_argument('-vp', '--video_path', type=str, default=0, help='指定视频的路径，当video_path=0时表示本地摄像头')
    parse.add_argument('-vs', '--video_save_path', type=str,
                       default=f'face_db/video_save/output_{datetime.datetime.now()}.mp4',
                       help="视频保存的路径，当video_save_path="" 时表示不保存 想要保存视频，则设置如video_save_path = 'yyy.mp4' 即可，代表保存为根目录下的yyy.mp4文件")
    parse.add_argument('-vf', '--video_fps', type=float, default=10.0, help='保存的视频的fps')
    parse.add_argument('-i', '--test_interval', type=int, default=100,
                       help=' test_interval用于指定测量fps的时候，图片检测的次数 理论上test_interval越大，fps越准确')
    opt = parse.parse_args()
    return opt


if __name__ == '__main__':
    # print(__doc__)
    opt = parse_opt()
    Main(opt)

# if __name__ == '__main__':
#     # print(check_stu_is_in_excel('220102050135'))
#     write2csv(name='刘珈玮', id='220102050135', reg_time='2024-7-31')
