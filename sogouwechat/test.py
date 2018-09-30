# coding=utf-8
from urllib import request
from pyquery import PyQuery as pq
import re
PROXY_SERVER = 'http://47.101.136.128:8888/random'
headers = {
        'Cookie': 'rewardsn=; wxtokenkey=777'
    }
url = 'http://mp.weixin.qq.com/s?src=11&timestamp=1538296201&ver=1153&signature=5fVoIM8Ja7okYnmq*tmWLtv4IYjK3tlYdpmroNqAF7bOBa6VM6GcACA*XtG021utsjxhbmdkyT*98mMeWL9kAemAfxFap9bN6VcA9NjLQZQ7v-fpIqD11Qt*hdLWteRt&new=1'
'''
def get_proxy():
    try:
        res =requests.get(PROXY_SERVER)
        if res.status_code == 200:
            proxy = res.text
    except Exception as e:
        print('GET PROXY ERROR:',e)
        return None
    if proxy:
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        return proxies
'''
def parse_detail(response):   #详情页解析,返回包含页面信息的字典
    doc = pq(response)
    data = {
        'title': doc('head title').text(),
        'content': doc('.rich_media_content').text(),
       'date': re.findall('^var\spublish_time\s=\s\"(.*?)\"', response.decode('utf-8')),
       'id': doc('#js_author_name').text()
    }
    #print(data)
    print(response.decode('utf-8'))
def main():
    #req = requests.get(url=url, headers=headers, proxies=get_proxy())
    #req = requests.get(url=url, headers=headers)
    req = request.Request(url)

    with request.urlopen(req) as f:
        data = f.read()
        parse_detail(data)
        #print(res)

main()