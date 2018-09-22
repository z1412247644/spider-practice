import json
import requests
from pyquery import PyQuery as pq
from lxml import etree
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}
def get_html(url):  #简单获取网页源码
    req = requests.get(url, headers=headers)
    return req.text()

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__Func__'] = []
        for k,v in attrs.items():
            if 'Proxy_get_' in k:
                attrs['__Func__'].append(k)
                count+=1
        attrs['__FuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class Proxy_get(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('Successfully get proxy:', proxy)
            proxies.append(proxy)
        return proxies

    def Proxy_get_daili66(self, page_num):
        base_url = 'http://www.66ip.cn/areaindex_{}/1.html'
        urls = [base_url.format(page) for page in range (1,page_num)]
        for url in urls:
            print('get proxy from ', url)
            print('get proxy from ', url)
            doc = etree.HTML(get_html(url))
            ip = doc.xpath('//div[@id="main"]//div//tr/td[1]/text()')
            port = doc.xpath('//div[@id="main"]//div//tr/td[2]/text()')
            for index in range(1,len(ip)):
                yield ':'.join([ip[index], port[index]])

 #   def Proxy_get_
    
