# 百度地图数据采集爬虫

<!-- TOC -->

- [百度地图数据采集爬虫](#百度地图数据采集爬虫)
    - [项目简介](#项目简介)
        - [开发语言](#开发语言)
        - [项目功能](#项目功能)
        - [开发库及版本](#开发库及版本)
        - [第三方依赖](#第三方依赖)
        - [开发者](#开发者)
    - [快速开始](#快速开始)
        - [初始配置](#初始配置)
        - [安装第三方库](#安装第三方库)
        - [执行主进程](#执行主进程)
    - [爬虫流程](#爬虫流程)
    - [配置说明](#配置说明)
    - [格式说明](#格式说明)
    - [模块说明](#模块说明)
        - [baidu](#baidu)
            - [baidu.api](#baiduapi)
        - [spider](#spider)
            - [spider.collector](#spidercollector)
            - [spider.controllor](#spidercontrollor)
            - [spider.storage](#spiderstorage)
    - [项目备注](#项目备注)

<!-- /TOC -->

## 项目简介

### 开发语言
python3.5

### 项目功能
使用百度地图的WebApi进行地图数据的采集

使用selenium自动化运维工具控制~~phantomJS~~Chrome(Headless模式)爬取去哪儿网上的酒店床位以及最低价信息


### 开发库及版本
第三方库 | 开发时版本 | 功能
---------|------------|----------
requests | 2.18.4     | 进行api调用
pandas   | 0.20.3     | 数据集处理
openpyxl | 2.5.5      | excel表格处理
selenium | 3.12.0     | 自动化网页运行

### 第三方依赖

* ~~phantomJS~~

* ChromeDriver

### 开发者

github@cpak00

baidu@cpak00

## 快速开始

### 初始配置
1.修改src/config/config.py中的配置(尤其注意文件的位置)
2.创建src/baidu.key文件, 并在其第一行填上可用的百度地图api的ak_key
3.在src/util/data/目录中, 放置符合[规定格式](#格式说明)的初始爬虫信息
4.在bin/目录中, 放置符合版本要求的[chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)和Chrome

### 安装第三方库

linux
```bash
pip3 install numpy
pip3 install pandas
pip3 install requests
pip3 install selenium
pip3 install openpyxl
pip3 install xlrd
```

windows
```bash
pip install numpy
pip install pandas
pip install requests
pip install selenium
pip install selenium
pip install xlrd
```

### 执行主进程
```bash
>$BaiduMapSpider: cd src
>$BaiduMapSpider/src: python deamon.py
```

## 爬虫流程

    1.启动守护deamon, 准备执行爬虫
    2.deamon读取sqlite数据库, 查找当前应该爬取的店的基础信息
    3.deamon将待爬基础信息传递给爬虫spider, 由spider爬取所需信息
    4.在spider爬取所需信息的时候, deamon执行告警功能, spider崩溃时发信(不选择重启
    爬虫, api额度宝贵, 避免浪费)
    5.spider爬取完成后,deamon读取下一条待爬信息, 发送给spider, 完成循环

## 配置说明
百度api需要申请ak_key, key配置文件位src/baidu.key文件中, 可以写多行, 在deamon的
__init__构造函数中, 通过readkey.get_key调用, 可以传入行号(从0开始, 默认为0)调用
不同行的ak_key.

爬虫配置文件位于src/config/config.py中, 注释说明

配置文件直接使用了py文件导入, 直接在项目文件中进行调用
```python
from config import config

config.content
```

运行开始前, 需保证配置项配置正确, 以及配置中的文件/文件夹已经按[规定格式](#格式说明)存在
    
## 格式说明

    以下名称均为config.py中的键, 创建文件(夹)的时候, 需使用对应键的值

    shop_filename:
        该目录对应一个excel文件, 记录商店的基础信息, 格式如下
        
|  |查找|实际|坐标
--|--|--|--
0|初始名称|地图名称|地图坐标
1|...|...|...

    complete_filename:
        该目录对应一个没有内容的excel文件, 记录已经爬取的内容, 格式如下

|  |实际|已完成
--|--|--
||

    output:
        该目录对应一个文件夹, 用于存储最终爬取出来的数据

## 模块说明

### baidu

百度地图包

#### baidu.api

百度地图api

示例
```python
from baidu import api

map_handler = api.Handler(ak_key)

# 地域范围搜索
map_handler.region_search('小区', '房地产', '上海', get_all=True):
# 圆形区域搜索
map_handler.circle_search('小区', '房地产', shop_location, distance)
# 批量算路
map_handler.path_search('walk', org_location, dst_locations)
```

### spider

爬虫主体包

#### spider.collector

数据收集器

```python
from spider import collector

collector = collector.Collector(ak_key)
collector.run('hotel', shop_name, shop_location, distance)

```

#### spider.controllor

爬虫控制器

```python
from spider import controllor

successful = []
main_controller = controllor.Controller(self.ak_key)
successful = self.main_controller.run(shop_name, real_name, 
location, save_successful, successful)
```

save_successful为存储已完成结果的句柄, 该方法用来存储已完成的结果, 避免爬虫中断
导致的重复爬取浪费api调用额度
successful为已经成功的结果, 传入控制器用来过滤, 即不会执行爬取过程

#### spider.storage

数据存储器

```
from spider import storage

storage = storage.Storage(shop_name)
storage.store(data, collect_name, distance)
```

特化的存储器, 用来将同一个地点的不同地缘信息存储到同一个excel表的不
同sheet中, sheet名称为distance加collect_name的中文(在config中配置)

## 项目备注

    1.建议备份complete_file, 在存储complete_file的过程中发生中断将导致complete_file无法挽回性的损坏
