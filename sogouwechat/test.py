# coding=utf-8
from urllib import request
from pyquery import PyQuery as pq
PROXY_SERVER = 'http://47.101.136.128:8888/random'
headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'rewardsn=; wxtokenkey=777'
    }
url = 'http://mp.weixin.qq.com/s?src=11&timestamp=1538137801&ver=1150&signature=faU5tutIRMTMEdDFf2cF138S6qlo1VAVUw4j2R2pSvofIj2JwEmrwaTTSLOdNHoUXBO6Llv1x1wWwTGqwcIBLvizHK6B3*WuIjjv5Cnc20r0c38LzK*BEoOfhX*Qby3o&new=1'
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
       'date': doc('#post-date').text()            
    }
    print(data)
def main():
    #req = requests.get(url=url, headers=headers, proxies=get_proxy())
    #req = requests.get(url=url, headers=headers)
    req = request.Request(url)

    with request.urlopen(req) as f:
        data = f.read()
        parse_detail(data)
        #print(res)

main()