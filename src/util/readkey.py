# -*-coding:utf-8-*-
import sys


def get_key(id=0):
    data = open('baidu.key', 'r').readlines()
    if (len(data) <= id):
        print('没有 id为%d 的ak_key' % (id))
        sys.exit(1)
    else:
        key = data[id].strip()
        statement = '调用key%d: %s' + '*' * (len(key)-5)
        print(statement % (id, key[0:5]))
        return key
