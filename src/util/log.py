# -*-coding:utf-8-*-
import logging
import time
import sys


DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR


def getLogger(filename, log_rank=logging.WARNING):
    # 创建Logger
    logger = logging.getLogger(filename)
    logger.setLevel(logging.INFO)
    # 创建Handler
    localdate = time.strftime('%Y-%m-%d_', time.localtime(time.time()))
    fh = logging.FileHandler(localdate+filename, mode='a')
    fh.setLevel(log_rank)
    formatter = logging.Formatter(
        '''%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:
            %(message)s''')
    fh.setFormatter(formatter)
    # 将Logger添加到Handler里面
    logger.addHandler(fh)
    return logger


class Counter:
    def __init__(self, name, length):
        if length < 0:
            length = 0
        self.length = length
        self.name = name
        self.count = 0
        return

    def add(self, num=1):
        if self.count >= self.length:
            return
        else:
            self.count += num

    def show(self):
        sys.stdout.write('\r%s: %d%%' % (self.name,
                                         self.count / self.length * 100))
        sys.stdout.flush()

    def end(self):
        print('Ok')


def getCounter(name, length):
    return Counter(name, length)
