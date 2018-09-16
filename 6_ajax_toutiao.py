from urllib.parse import urlencode
import requests, os
from  pyquery import PyQuery as pq
from pymongo import MongoClient
from hashlib import md5
from multiprocessing import Pool
baseurl = 'https://www.toutiao.com/search_content/?'

headers = {     #请求头必要参数
    'content-type': 'application/x-www-form-urlencoded',
    'Referer': 'https://www.toutiao.com/search/?keyword=%%E8%A1%%97%%E6%8B%8D',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

def get_source_code(offset):   #html获取
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '美女',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1'
    }
    url = baseurl + urlencode(params)   #url构造拼接(将参数字典通过urlencode()方法转化为GET参数)
    print(url)
    try:
        req = requests.get(url, headers= headers)
        if req.status_code == 200:
            return req.json()
        return None
    except requests.ConnectionError as e:
        print('Error', e.args)
        return None

def parse_page(json):
    if json:
        items = json.get('data')
        for it in items:
            pic = {}
            try:
                pic['title'] = it.get('title')
                pic['url'] = it.get('large_image_url')
            except:
                pass
            finally:
                yield pic

def img_save(res):
    try:
        #if not os.path.exists(res.get('title')):
            #os.mkdir(res.get('title'))
        response = requests.get(res.get('url'))
        if response.status_code == 200:
            file_path = '{0}.{1}'.format(res.get('title'), 'jpg')
            #if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(response.content)

    except:
        print('Failed to Save')

def main(num):
    for offset in range(num):
        json = get_source_code(offset*20)
        results = parse_page(json)
        for res in results:
            print(res)
            if res != {'title': None, 'url': None}:
                img_save(res)

GROP_START = 0
GROP_END = 20

if __name__ == '__main__':
   pool = Pool()
   groups = ([x for x in range(GROP_START, GROP_END+1)])
   print(groups)
   pool.map(main, groups)
   pool.close()
   pool.join()
