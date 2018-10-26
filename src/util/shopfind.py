# -*-coding:utf-8-*-
from baidu import api
import pandas as pd
import time
from os import path
from config import config
from util import readkey

ak_key = readkey.get_key()
map_handler = api.Handler(ak_key)


def location_parse(location):
    lat = location['lat']
    lng = location['lng']
    return str(lat) + ',' + str(lng)


def find_location(shop_name, address):
    infos = map_handler.region_search(shop_name, '', '上海')
    if len(infos) > 0:
        location = location_parse(infos[0]['location'])
        real_name = infos[0]['name']
        print('查找:%s 实际:%s 位置:%s' % (shop_name, real_name, location))
        return real_name, location
    else:
        '''
        # 已有数据, 节约额度
        print('没找到 %s' % (shop_name))
        return '', ''
        '''
        # 常规
        infos = map_handler.region_search(address, '', '上海', get_all=False)
        if infos and len(infos) > 0:
            location = location_parse(infos[0]['location'])
            real_name = infos[0]['name']
            print('查找:%s 实际:%s 位置:%s' % (shop_name, real_name, location))
            return real_name, location
        else:
            print('没找到 %s' % (shop_name))
            return '', ''


def find_all():
    filename = "./util/data/国大上海门店表.xlsx"
    df = pd.read_excel(filename)

    save = ''
    save_filename = config.shop_filename
    
    if not path.exists(save_filename):
        save = pd.DataFrame(columns=['查找', '实际', '坐标'])
    else:
        save = pd.read_excel(save_filename)

    # complete = pd.DataFrame(columns=['实际', '已完成'])
    for i, row in df.iterrows():
        time.sleep(0.1)
        shop_name = df['门店名称'][i]

        result = save.loc[save['查找'] == shop_name]
        if (len(result)
                and str(result.loc[result.index[0], '坐标']).strip() != ''
                and str(result.loc[result.index[0], '坐标']).strip() != 'nan'):
            print('%s 已找到 %s' %
                  (shop_name, str(result.loc[result.index[0], '坐标']).strip()))
            save.to_excel("./util/data/shop.xlsx")
            continue

        address = df['地址'][i]
        real_name, location = find_location(shop_name, address)
        row = pd.Series({'查找': shop_name, '实际': real_name, '坐标': location})
        if (len(result)):
            save.loc[result.index[0], '实际'] = real_name
            save.loc[result.index[0], '坐标'] = location
        else:
            save = save.append(row, ignore_index=True)
        save.to_excel(save_filename)
    save.to_excel(savesave_filename)
    # complete.to_excel("./util/data/complete.xlsx")
