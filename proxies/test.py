import json
import requests
from lxml import etree

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}
def get_html(url):  #简单获取网页源码
    req = requests.get(url, headers=headers)
    return req.text


def Proxy_get_xici():
    url = 'http://www.xicidaili.com/nn'
    print('get proxy from ', url)
    doc = etree.HTML(get_html(url))
    ip = doc.xpath('//tr//td[2]/text()')
    port = doc.xpath('//tr//td[3]/text()')
    for index in range(len(ip)):
        print(':'.join([ip[index], port[index]]))

Proxy_get_xici()
