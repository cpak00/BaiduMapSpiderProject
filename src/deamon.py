# -*-coding:utf-8-*-
from spider import controllor
from baidu.api import ApiError
import pandas as pd
import numpy as np
from config import config
from util import log
from util import readkey
import time
import sys


logging = log.getLogger('deamon.log', log.INFO)


class Deamon:
    def __init__(self):
        logging.info('Deamon初始化')
        self.localday = int(time.strftime('%d', time.localtime()))
        self.ak_key = readkey.get_key()
        self.shop_filename = config.shop_filename
        self.complete_filename = config.complete_filename
        self._read_list()
        self.main_controller = controllor.Controller(self.ak_key)
        logging.info('Deamon初始化完毕')
        return

    # 等待日期变化
    def wait_day(self):
        i = 0
        while True:
            current_day = int(time.strftime('%d', time.localtime()))
            if current_day == self.localday:
                # 等待一小时
                self.s_print('\r等待日期变化: %dh' % (i))
                time.sleep(60 * 60)
                i += 1
            else:
                self.s_print('\n日期变化为%d' % (current_day))
                self.localday = current_day
                break

    def _read_list(self):
        logging.info('开始读取待爬信息和已爬信息')
        self.shop = pd.read_excel(self.shop_filename)
        self.complete = pd.read_excel(self.complete_filename)
        logging.info('待爬信息和已爬信息读取完毕')
        return

    # 获取以完成的结果
    def get_successful(self, real_name):
        result = self.complete.loc[self.complete['实际'] == real_name]
        if len(result) != 0:
            return str(result.loc[result.index[0], '已完成']).split(',')
        else:
            return []

    # 存储以完成的结果
    def save_successful(self, real_name, successful):
        result = self.complete.loc[self.complete['实际'] == real_name]
        successful = ','.join(successful)
        if len(result) != 0:
            self.complete.loc[result.index, '已完成'] = successful
        else:
            self.complete = self.complete.append({
                '实际': real_name,
                '已完成': successful
            }, ignore_index=True)
        self.complete.to_excel(config.complete_filename)

    # 守护api执行, 出错作出处理
    def main(self):
        while True:
            try:
                self.s_print('当前日期: %s\n' % (self.localday))
                self.run()
            except ApiError as e:
                self.s_print('意外终止\n')
                reason = e.get_message()
                self.s_print('终止原因: %s\n' % (reason))
                if '配额超限' in reason:
                    self.wait_day()
                else:
                    break

    def run(self):
        logging.info('deamon开始运行')
        successful = []
        successful_num = 0
        error_num = 0
        for i in range(len(self.shop)):
            # 基础信息读取
            shop_name = self.shop['查找'][i]
            real_name = self.shop['实际'][i]
            location = self.shop['坐标'][i]

            if location is np.nan:
                logging.info('%s 没有有效地址' % (shop_name))
                continue

            try:
                logging.info('%s 就绪, 地图名称: %s, 坐标(%s)' % (shop_name, real_name,
                                                          location))

                # 获取已完成结果
                successful = self.get_successful(real_name)
                if len(successful) != 0:
                    logging.info('已完成: %s' % (successful))

                successful = self.main_controller.run(
                    shop_name, real_name, location, self.save_successful,
                    successful)
                logging.info('%s 完成, 成功: %s' % (shop_name, successful))

                # 存储已完成结果
                self.save_successful(real_name, successful)
                successful_num += 1

                if set(successful) == set(config.content.keys()):
                    logging.info('%s 全部完成' % (shop_name))
                else:
                    logging.info('%s 继续' % (shop_name))
                    i = i - 1

            except Exception as e:
                logging.error(repr(e))
                # 记录错误并继续
                logging.info('%s 发生错误, 跳过\n地图名称: %s, 坐标: (%s)' %
                             (shop_name, real_name, location))
                error_num += 1
                continue
        logging.info('deamon运行结束, 共成功%d个, 失败%d个' % (successful_num, error_num))
        return

    # 安全print
    def s_print(self, *args, **kwargs):
        try:
            sys.stdout.write(*args, **kwargs)
            sys.stdout.flush()
        except Exception:
            return


if __name__ == '__main__':
    deamon = Deamon()
    deamon.main()
