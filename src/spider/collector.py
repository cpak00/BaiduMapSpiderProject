# -*-coding:utf-8-*-
import baidu.api as api
import pandas as pd
from config import config
from util import log


logging = log.getLogger('collector', log.INFO)


# 安全的map取值
def s_get(map, key):
    if key in map:
        return map[key]
    else:
        return ''


class Collector:
    def __init__(self, ak_key):
        # 初始化
        self.map_handler = api.Handler(ak_key)

    def run(self, collect_name, shop_name, shop_location, distance):
        # 运行某个收集器
        if collect_name == 'house':
            return self.collect_house(shop_name, shop_location, distance)
        elif collect_name == 'hotel':
            return self.collect_hotel(shop_name, shop_location, distance)
        elif collect_name == 'metro':
            return self.collect_metro(shop_name, shop_location, distance)
        elif collect_name == 'bus':
            return self.collect_bus(shop_name, shop_location, distance)
        else:
            return None

    def collect_house(self, shop_name, shop_location, distance):
        # 构造解析器
        output_map = config.content_output_map['house']
        house_parser = api.Parse(output_map)

        house_results = self.map_handler.circle_search('小区', '房地产',
                                                       shop_location, distance)

        # 计数器
        counter = log.getCounter('%s 小区' % (shop_name), len(house_results))
        # 获取房价信息
        results = []

        # 记录个数, 为0 直接返回
        logging.info('%s %s: %s个' % (shop_name, '小区', len(house_results)))
        if len(house_results) == 0:
            return pd.DataFrame(columns=['个数为0'])

        for result in house_results:
            result['location'] = house_parser.location_parse(
                result['location'])
            if result['detail'] == 1:
                url = s_get(result['detail_info'], 'detail_url')
                house_info = house_parser.house_parse(url)
                result.update(house_info)
            results.append(result)
            # print(result['name'] + ' done')
            counter.add()
            counter.show()
        counter.end()

        # 获取距离信息
        houses_info = pd.DataFrame(results)
        houses_location = houses_info['location']

        paths = self.map_handler.path_search('walking', shop_location,
                                             houses_location)
        path_results = []
        for path in paths:
            path_results.append(path['distance']['value'])

        houses_info['duration'] = path_results
        house_parser.df_parse(houses_info)

        return houses_info
        # houses_info.to_csv('{0}_house_{1}m.csv'.format(shop_name, distance))
        # print('{0} done'.format(shop_name))

    def collect_hotel(self, shop_name, shop_location, distance):
        # 构造解析器
        output_map = config.content_output_map['hotel']
        hotel_parser = api.Parse(output_map)

        hotel_results = self.map_handler.circle_search(
            '酒店', '酒店', shop_location, distance, filter="酒店")

        # 计数器
        counter = log.getCounter('%s 酒店' % (shop_name), len(hotel_results))
        # 获取酒店信息
        results = []

        # 记录个数, 为0 直接返回
        logging.info('%s %s: %s个' % (shop_name, '酒店', len(hotel_results)))
        if len(hotel_results) == 0:
            return pd.DataFrame(columns=['个数为0'])

        for result in hotel_results:
            result['tag'] = s_get(result['detail_info'], 'tag')
            result['location'] = hotel_parser.location_parse(
                result['location'])
            url = s_get(result['detail_info'], 'detail_url')
            hotel_info = hotel_parser.hotel_parse(url)
            result.update(hotel_info)
            results.append(result)
            # print(result['name'] + ' done')
            counter.add()
            counter.show()
        counter.end()

        # 获取距离信息
        hotels_info = pd.DataFrame(results)
        hotels_location = hotels_info['location']

        paths = self.map_handler.path_search('walking', shop_location,
                                             hotels_location)
        path_results = []
        for path in paths:
            path_results.append(path['distance']['value'])

        hotels_info['duration'] = path_results
        hotel_parser.df_parse(hotels_info)

        return hotels_info
        # hotels_info.to_csv('{0}_hotel_{1}m.csv'.format(shop_name, distance))
        # print('{0} done'.format(shop_name))

    def collect_metro(self, shop_name, shop_location, distance):
        # 构造解析器
        output_map = config.content_output_map['metro']
        metro_parser = api.Parse(output_map)

        metro_results = self.map_handler.circle_search(
            '地铁站', '地铁站', shop_location, distance, filter='地铁站')

        # 计数器
        counter = log.getCounter('%s 地铁' % (shop_name), len(metro_results))
        # 获取房价信息
        results = []

        # 记录个数, 为0 直接返回
        logging.info('%s %s: %s个' % (shop_name, '地铁', len(metro_results)))
        if len(metro_results) == 0:
            return pd.DataFrame(columns=['个数为0'])

        for result in metro_results:
            result['location'] = metro_parser.location_parse(
                result['location'])
            results.append(result)
            # print(result['name'] + ' done')
            counter.add()
            counter.show()
        counter.end()

        # 获取距离信息
        metros_info = pd.DataFrame(results)
        metros_location = metros_info['location']

        paths = self.map_handler.path_search('walking', shop_location,
                                             metros_location)
        path_results = []
        for path in paths:
            path_results.append(path['distance']['value'])

        metros_info['duration'] = path_results
        metro_parser.df_parse(metros_info)

        return metros_info
        # metros_info.to_csv('{0}_metro_{1}m.csv'.format(shop_name, distance))
        # print('{0} done'.format(shop_name))

    def collect_bus(self, shop_name, shop_location, distance):
        # 构造解析器
        output_map = config.content_output_map['bus']
        bus_parser = api.Parse(output_map)

        bus_results = self.map_handler.circle_search('公交车站', '公交车站',
                                                     shop_location, distance)

        # 计数器
        counter = log.getCounter('%s 公交' % (shop_name), len(bus_results))
        # 获取房价信息
        results = []

        # 记录个数, 为0 直接返回
        logging.info('%s %s: %s个' % (shop_name, '公交', len(bus_results)))
        if len(bus_results) == 0:
            return pd.DataFrame(columns=['个数为0'])

        for result in bus_results:
            result['location'] = bus_parser.location_parse(result['location'])
            results.append(result)
            # print(result['name'] + ' done')
            counter.add()
            counter.show()
        counter.end()

        # 获取距离信息
        bus_info = pd.DataFrame(results)
        bus_location = bus_info['location']

        paths = self.map_handler.path_search('walking', shop_location,
                                             bus_location)
        path_results = []
        for path in paths:
            path_results.append(path['distance']['value'])

        bus_info['duration'] = path_results
        bus_parser.df_parse(bus_info)

        return bus_info
        # bus_info.to_csv('{0}_bus_{1}m.csv'.format(shop_name, distance))
        # print('{0} done'.format(shop_name))
