import os


def get_pid():
    return os.getpid()


def print_pid():
    print('当前主进程号: %d' % (get_pid()))
