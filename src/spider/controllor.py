# -*-coding:utf-8-*-
from config import config
from spider import collector
from spider import storage
from util import log


logging = log.getLogger('controller.log', log.INFO)


class Controller:
    def __init__(self, ak_key):
        # 读取配置
        self.content = config.content
        self.collector = collector.Collector(ak_key)
        pass

    def run(self, shop_name, real_name, shop_location, save_handler,
            filter=[]):
        # 成功爬取的结果
        successful_result = filter
        # 构造存储器
        self.storage = storage.Storage(shop_name)
        for key in self.content:
            try:
                collect_name = key
                # 如果当前待爬内容在filter过滤器中, 跳过
                if collect_name in filter:
                    continue
                # 遍历所需内容
                logging.info('开始爬取 店名: %s, 待爬内容: %s' % (shop_name, key))
                distance = self.content[collect_name]
                # 开始爬取数据
                data = self.collector.run(collect_name, shop_name,
                                          shop_location, distance)
                if data is not None:
                    # 数据不为空, 则进行存储
                    self.storage.store(data, collect_name, distance)
                    logging.info('爬取完成 店名: %s, 待爬内容: %s' % (shop_name, key))
                    # 成功爬取
                    successful_result.append(collect_name)
                    save_handler(real_name, successful_result)
                else:
                    logging.error('待爬内容不存在')
            except Exception as e:
                logging.error(repr(e))
                continue

        return successful_result
