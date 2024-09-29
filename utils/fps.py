# 导入必要的包
import datetime


class FPS:
    def __init__(self):
        # 存储开始时间、结束时间和在开始和结束间隔之间检查的帧总数
        self._start = None  # 当我们开始读取帧时的开始时间戳。
        self._end = None  # 当我们停止读取帧时的结束时间戳。
        self._numFrames = 0  # 在 _start 和 _end 间隔期间读取的帧总数。

    def start(self):
        # 启动计时器
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # 停止计时器
        self._end = datetime.datetime.now()

    def update(self):
        # 增加开始和结束间隔期间检查的帧总数
        self._numFrames += 1

    def elapsed(self):
        # 返回开始和结束间隔之间的总秒数
        return (self._end - self._start).total_seconds()

    def fps(self):
        # 计算（近似）每秒帧数
        return self._numFrames / self.elapsed()
