from config import config
from os import path
import pandas as pd
from openpyxl import load_workbook
from util import log


logging = log.getLogger('storage', log.INFO)


class Storage:
    def __init__(self, shop_name):
        self.shop_name = shop_name
        self.output = path.join(config.output, shop_name+'.xlsx')
        return

    def store(self, data, collect_name, distance):
        try:
            logging.info('准备存储: %s' % (self.output))
            writer = ''

            # 只对sheet进行操作, 避免覆盖其他sheet
            if path.exists(self.output):
                book = load_workbook(self.output)
                writer = pd.ExcelWriter(self.output, engine='openpyxl')
                writer.book = book
                writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
            else:
                writer = pd.ExcelWriter(self.output, engine='openpyxl')

            sheet_name = str(distance) + str(
                config.content_zh_CN[collect_name])
            # 如果为空
            if len(data) == 0:
                # 直接进行存储
                data.to_excel(writer, sheet_name=sheet_name)
            else:
                # 选取存储
                columns = config.content_output_map[collect_name].values()
                data.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    columns=columns)

            # 存储
            writer.save()
            logging.info('存储完成')
        except Exception as e:
            logging.error(repr(e))
            logging.info('存储 %s %s 发生错误' % (self.shop_name, collect_name))
            raise e
        return
