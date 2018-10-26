# -*-coding:utf-8-*-
# 配置文件

# 待爬取列表位置
shop_filename = "E:/GuoDaProject/src/util/data/shop.xlsx"
# 已爬取列表位置
complete_filename = "E:/GuoDaProject/src/util/data/complete.xlsx"

# 数据存储文件夹绝对位置
output = "E:/GuoDaProject/out"

# 爬取内容及对应距离(m)
content = {"house": 1000, "hotel": 1000, "bus": 1000, "metro": 3000}

# 爬取内容中文映射
content_zh_CN = {"house": "小区", "hotel": "酒店", "bus": "公交车站", "metro": "地铁站"}

# 输出内容映射
content_output_map = {
    "house": {
        'name': '小区名',
        'location': '小区坐标',
        'uid': '小区标识符',
        'address': '小区地址',
        'house_price': '小区房价(￥/m^2)',
        'house_time': '小区建造年份',
        'duration': '小区距离(m)'
    },
    "hotel": {
        'name': '酒店名',
        'tag': '标签',
        'location': '酒店坐标',
        'uid': '酒店标识符',
        'address': '酒店地址',
        'duration': '酒店距离(m)',
        'hotel_price': '酒店最低价',
        'hotel_num': '酒店房间数'
    },
    "bus": {
        'name': '地铁站名',
        'location': '地铁站坐标',
        'uid': '地铁站标识符',
        'address': '地铁站地址',
        'duration': '地铁站距离(m)'
    },
    "metro": {
        'name': '公交车站名',
        'location': '公交车站坐标',
        'uid': '公交车站标识符',
        'address': '公交车站地址',
        'duration': '公交车站距离(m)'
    }
}
