# import the necessary packages
from threading import Thread
import cv2


class capVideoStream:
    def __init__(self, src=0):
        # 初始化摄像机流并从流中读取第一帧
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        # 初始化用于指示线程是否应该停止的变量
        self.stopped = False

    def start(self):
        # 启动线程从视频流中读取帧
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # 继续无限循环，直到线程停止
        while True:
            # 如果设置了线程指示器变量，则停止线程
            if self.stopped:
                return
            # 否则，从流中读取下一帧
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # 返回最近读取的帧
        return self.frame

    def stop(self):
        # 表示应该停止线程
        self.stopped = True
