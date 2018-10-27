from os import path
import os

# 将工作目录设置为守护进程所在目录
chdir_path = path.dirname(path.abspath(__file__))
os.chdir(chdir_path)


def print_chdir():
    print('当前工作目录: %s' % (chdir_path))