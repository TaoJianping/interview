import json
import os
import os.path
import time

import pymongo
import requests
from jinja2 import Environment, FileSystemLoader
from pymongo import MongoClient

client = MongoClient()

db = client["kLine"]

path = '{}/templates/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)
template = env.get_template('k线图-高清.html')

collection_name = "MU"

class K_Line(object):
    def __init__(self, name):
        self.name = name
        self.k_line_data = self.get_xhr_data()

    def get_xhr_data(self):
        file_name = self.name
        dir_name = "cache"
        if os.path.exists(dir_name) is not True:
            os.mkdir(dir_name)
        path = os.path.join(dir_name, file_name)
        if os.path.exists(path) is not True:
            header = {
                "Accept":"application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding":"gzip, deflate, br",
                "Accept-Language":"en,zh-CN;q=0.9,zh;q=0.8",
                "Connection":"keep-alive",
                "Host":"hk.investing.com",
                "Referer":"https://hk.investing.com/equities/geely-auto-candlestick",
                "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
                "X-Requested-With":"XMLHttpRequest",
            }
            s = requests.Session()
            url = "https://www.investing.com/common/modules/js_instrument_chart/api/data.php?pair_id=8092&pair_id_for_news=8092&chart_type=candlestick&pair_interval=week&candle_count=70&events=patterns_only&volume_series=yes&period=1-year"
            s.get("https://www.investing.com/equities/micron-tech", headers=header)
            data = s.get(url,headers=header)
            ret = data.json()
            k_line_data = ret["candles"]
            print(k_line_data)
            s = json.dumps(k_line_data, indent=2, ensure_ascii=False)
            with open(path, 'w+', encoding='utf-8') as f:
                f.write(s)
            return k_line_data
        else:
            with open(path, 'r', encoding='utf-8') as f:
                s = f.read()
                return json.loads(s)

    def save(self):
        data = self.__dict__
        db[self.name].insert(data)

    def save_k_line_html(self):
        k_line_data = list(db[self.name].find())[0]['k_line_data']
        data = []
        for i in k_line_data:
            timestamps = i[0] / 1000
            show_time = time.strftime("%Y/%m/%d", time.localtime(timestamps))
            single_week_data = [show_time, [i[1], i[4], i[3], i[2]]]
            data.append(single_week_data)
        ans = template.render(data = data)
        html_name = ".".join((self.name, "html",))
        if os.path.exists(html_name):
            os.remove(html_name)
        with open(html_name, 'w+', encoding='utf-8') as f:
            f.write(ans)
    
mu = K_Line(collection_name)
mu.save()
mu.save_k_line_html()
