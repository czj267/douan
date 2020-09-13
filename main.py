import re
import time

import requests
from pymysql import connect


class DouBan:
    def __init__(self):
        exclude_kw = [
            '5号线', '7号线', '桃源', '珠光', '茶光', '宝体',
            '灵芝', '大学城', '大新', '西丽', '前海', '西乡', '荔湾''白石龙', '单房', '皇岗', '蛇口', '宝安', '水湾',
            '大新', '星海名城', '固戍', '龙岗', '翻身', '桃源村', '登良', '万科云城', '东角头', '留仙', '福永',
            '泊寓', '公寓', '复式', 'loft', '单间', '一房一厅', '1房1厅', '两室一厅', '一室一厅',
            '求合租', '求租', '纯女生', '全女生', '限女', '女生合租',
        ]
        re_re = r''
        for kw in exclude_kw:
            re_re += r'(?:%s)|' % kw

        self.re_re = re_re[:-1]
        self.group_ids = [
            # 深圳南山租房团
            'https://frodo.douban.com/api/v2/group/498004/topics?start={'
            'start}&count=20&sortby=new&os_rom=android&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel'
            '=Yingyongbao_Market&udid=867a65cd33ed85b31b22cc7cee1e920286518bc0&_sig=pa1Wr7hNlxw2ri9Ythe4vYCP5LE%3D'
            '&_ts=1599281465',
            # 深圳租房|南山租房
            'https://frodo.douban.com/api/v2/group/512841/topics?start={'
            'start}&count=20&sortby=new&os_rom=android&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel'
            '=Yingyongbao_Market&udid=867a65cd33ed85b31b22cc7cee1e920286518bc0&_sig=4MYX%2BFtF82X9bP2E12ifykiCjjo%3D'
            '&_ts=1599287439',
            # 深圳南山租房
            'https://frodo.douban.com/api/v2/group/598241/topics?start={'
            'start}&count=20&sortby=new&os_rom=android&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel'
            '=Yingyongbao_Market&udid=867a65cd33ed85b31b22cc7cee1e920286518bc0&_sig=shVmagVzVdRBqh6CD6qPCyyf5WY%3D'
            '&_ts=1599287661',
        ]
        self.max_page = 5

        db_conf = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "root",
            "db": "douban",
            "charset": "utf8mb4",
            "autocommit": True,
        }
        self.db = connect(**db_conf)

    def run(self):
        for group_id in self.group_ids:
            for page in range(1, self.max_page + 2):
                topics = self.get_data(group_id, page)['topics']
                for item in topics:
                    insert_data = {
                        'title': item['title'],
                        'a_id': item['id'],
                        'a_created_at': item['create_time'],
                        'a_updated_at': item['update_time']
                    }
                    if not self.filter_title(item['title']):
                        continue
                    self.insert_or_update_one(insert_data)

                time.sleep(5)

    def filter_title(self, title):
        price = re.findall(r'\d{4}', title)
        if price and int(price[0]) > 2300:
            return False

        if re.findall(self.re_re, title):
            return False
        return True

    def insert_or_update_one(self, data):
        sql = """
            INSERT INTO rent(title,a_id,a_created_at,a_updated_at) 
                            VALUE (%(title)s,%(a_id)s,%(a_created_at)s,%(a_updated_at)s)
                            ON DUPLICATE KEY UPDATE a_updated_at=values(a_updated_at)
        """

        self.db.cursor().execute(sql, data)
        aff_rows = self.db.affected_rows()
        self.__log(aff_rows, data)

    def get_data(self, group_url, page):
        start = (page - 1) * 20
        url = group_url.format(**{"start": start})
        headers = {
            "User-Agent": "api-client/1 com.douban.frodo/6.0.0(137) Android/22 product/R11 Plus vendor/OPPO "
                          "model/OPPO R11 Plus  rom/android  network/wifi "
        }
        res = requests.get(url, headers=headers, verify=False)

        return res.json()

    def __log(self, *args, **kwargs):
        print(time.strftime("%Y-%m-%d %H:%M:%S"), *args, **kwargs)


if __name__ == '__main__':
    DouBan().run()
