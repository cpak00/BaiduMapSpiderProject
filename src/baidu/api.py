# -*-coding:utf-8-*-
from urllib.parse import urlencode
import requests
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from util import log
import platform


logging = log.getLogger('api')


# 百度地图api
class Handler:
    # 单次最大信息数
    page_size = 20

    # 单次最大出错次数
    error_max = 10

    # 构造函数 传入秘钥
    def __init__(self, p_key):
        self.key = p_key
        self.raw_map = {
            'ak': p_key,
            'output': 'json',
            'scope': '2',
            'page_size': self.page_size
        }
        return

    # 地域检索api
    def region_search(self, query, tag, region, get_all=True):
        url = Url('https://api.map.baidu.com/place/v2/search')
        url.set_map(self.raw_map)

        params = {
            'query': query,
            'tag': tag,
            'region': region,
        }
        url.set_map(params)

        if get_all:
            return self._get_list(url)
        else:
            return self._get_result(url)

    # 圆形区域检索api
    # 查找请求, 经纬度(逗号分隔), 查找半径(米)
    def circle_search(self, query, tag, location, radius, filter=None):
        url = Url('https://api.map.baidu.com/place/v2/search')
        url.set_map(self.raw_map)

        params = {
            'query': query,
            'tag': tag,
            'location': location,
            'radius': radius,
        }
        url.set_map(params)

        results = self._get_list(url)

        if filter is not None:
            filtered_results = []
            for result in results:
                if result['detail'] == 1:
                    if 'tag' not in result['detail_info']:
                        filtered_results.append(result)
                    elif filter in result['detail_info']['tag']:
                        filtered_results.append(result)
                else:
                    filtered_results.append(result)
            results = filtered_results.copy()

        logging.info('共{0}个结果'.format(str(len(results))))
        return results

    # 批量算路
    def path_search(self, way, org_location, dst_locations):
        url = Url('https://api.map.baidu.com/routematrix/v2/{0}'.format(way))
        url.set_map(self.raw_map)

        paths = []
        index = 0
        num = 30
        while True:
            time.sleep(0.5)
            dsts = []
            if index >= len(dst_locations):
                break
            else:
                start = index
                end = min(index + num, len(dst_locations))
                dsts = dst_locations[start:end].copy()
                index += num
            params = {'origins': org_location, 'destinations': '|'.join(dsts)}
            url.set_map(params)
            logging.info(url)
            paths += self._get_result(url)
        return paths

    # 获取请求信息
    def _get_result(self, url):
        error_flag = 0
        json = {}
        while True:
            time.sleep(0.5)
            if (error_flag > self.error_max):
                logging.error('错误次数超过{0}'.format(self.error_max))
                self.on_error(json)
                break
            try:
                r = requests.get(url)
                json = r.json()
                status = json['status']
                if status == 0:
                    # 请求成功
                    result = json['result']
                    return result
                else:
                    # 请求失败
                    error_flag += 1
                    logging.warning(json['message'])
                    continue
            except requests.exceptions.RequestException:
                logging.error('网络连接异常')
                return None

    # 获取请求列表
    def _get_list(self, url):
        page_num = 0
        error_flag = 0

        total_results = []
        json = {}
        while True:
            time.sleep(0.5)
            if (error_flag > self.error_max):
                logging.error('错误次数超过{0}'.format(self.error_max))
                self.on_error(json)
                break
            try:
                url.set_param('page_num', page_num)
                r = requests.get(url)
                json = r.json()
                status = json['status']
                if status == 0:
                    # 请求成功
                    results = json['results']
                    # print(results)
                    logging.info(url)
                    # print(len(results))
                    if len(results) == 0:
                        # 结束迭代
                        # print('结束')
                        break
                    else:
                        # 继续迭代
                        total_results += results
                        page_num += 1
                        continue
                else:
                    # 请求失败
                    error_flag += 1
                    logging.warning(str(json['message']) + str(url))
                    continue
            except requests.exceptions.RequestException:
                logging.error('网络连接异常')
                return None
        return total_results

    def on_error(self, json):
        # print('错误超过{0}次, 已暂停'.format(self.error_max))
        raise ApiError(json)
    pass


# Url管理
class Url:
    # 构造函数 传入唯一资源定位地址
    def __init__(self, p_url):
        self.url = p_url
        self.param_map = {}
        return

    # 传出Url字符串
    def __str__(self):
        query_param = urlencode(self.param_map)
        return self.url + '?' + query_param

    # 设置参数
    def set_param(self, key, value):
        self.param_map[key] = value
        return

    # 批量设置参数
    def set_map(self, map):
        self.param_map.update(map)
        return

    # 清空参数
    def clear_map(self):
        self.param_map = {}
        return

    pass


# 解析对象
class Parse:
    # 构造函数 字典映射 键为json中的键 值为存储的列名
    def __init__(self, map):
        # 查找当前环境
        executable_path = '../bin/chromedriver'
        environment = ','.join(platform.architecture())
        if 'Windows' in environment:
            executable_path += '.exe'

        # 配置服务器
        # headless Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            executable_path=executable_path,
            chrome_options=chrome_options)

        # PhantomJS
        # self.driver = webdriver.PhantomJS()

        self.jsonMap = map
        self.raw = {}
        values = map.values()
        for value in values:
            self.raw[value] = ''

    def json_parse(self, json):
        result = self.raw.copy()
        for key in self.jsonMap.keys():
            store_key = self.jsonMap[key]
            if key in json:
                result[store_key] = json[key]

        return result

    def df_parse(self, df):
        df.rename(columns=self.jsonMap, inplace=True)

    def house_parse(self, url):
        try:
            r = requests.get(url)
            r.encoding = 'utf-8'
            price_pattern = re.search(r'history: \[{"price":"(\d+.\d+)"',
                                      r.text)
            time_pattern = re.search(r'"building_time":"(\d+)"', r.text)

            price = ''
            time = ''
            if price_pattern is not None:
                price = price_pattern.group(1)
            if time_pattern is not None:
                time = time_pattern.group(1)

            return {"house_time": time, "house_price": price}
        except:
            return {"house_time": '', "house_price": ''}

    def hotel_parse(self, url):
        try:
            self.driver.get(url)
            id_pattern = re.search(r'dt-(\d+)', self.driver.page_source)
            id_ = id_pattern.group(1)
            detail_url = 'https://hotel.qunar.com/city/shanghai_city/dt-{0}'

            r = requests.get(detail_url.format(id_))
            r.encoding = 'utf-8'

            price_pattern = re.search(r'<span class="price f24">(\d+)</span>',
                                      self.driver.page_source)
            num_pattern = re.search(r'(\d+)间客房', r.text)

            price = ''
            num = ''
            if price_pattern is not None:
                price = price_pattern.group(1)
            if num_pattern is not None:
                num = num_pattern.group(1)

            return {"hotel_num": num, "hotel_price": price}
        except Exception as e:
            logging.error(repr(e))
            return {"hotel_num": '', "hotel_price": ''}

    def location_parse(self, location):
        lat = location['lat']
        lng = location['lng']
        return str(lat) + ',' + str(lng)

    pass


# api 错误句柄
class ApiError(BaseException):
    def __init__(self, json):
        self.json = json
        return

    def get_json(self):
        return self.json

    def get_message(self):
        return self.json['message']

    pass
