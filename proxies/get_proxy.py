'''
代理爬取工具库，包含简单requests请求源码，以及xpath解析，和一个基于元类可以方便添加爬取站点函数的类
'''

import requests
from pyquery import PyQuery as pq
from lxml import etree

headers = {     #伪造请求头
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}
def get_html(url):  #简单获取网页源码
    req = requests.get(url, headers=headers)
    return req.text

class ProxyMetaclass(type):     #元类构造
    def __new__(cls, name, bases, attrs):
        count = 0   #count用来计算符合条件的方法数
        attrs['__Func__'] = []      #attrs['__Func__']用以存储方法名
        for k, v in attrs.items():  #检测子类中符合条件的方法并存储计数
            if 'Proxy_get_' in k:
                attrs['__Func__'].append(k)
                count+=1
        attrs['__FuncCount__'] = count  #用attrs['__FuncCount__']带回方法数
        return type.__new__(cls, name, bases, attrs)

class Proxy_get(object, metaclass=ProxyMetaclass):  #代理获取类，使用元类构造
    def get_proxies(self, callback):    #callback为传入代理爬取函数名
        proxies = []
        for proxy in eval("self.{}()".format(callback)):    #将函数名转化为函数执行
            #print('Successfully get proxy:', proxy)
            proxies.append(proxy)
        return proxies

    def Proxy_get_daili66(self, page_num=4):
        base_url = 'http://www.66ip.cn/areaindex_{}/1.html'
        urls = [base_url.format(page) for page in range (1,page_num)]
        for url in urls:
            print('get proxy from ', url)
            doc = etree.HTML(get_html(url))
            ip = doc.xpath('//div[@id="main"]//div//tr/td[1]/text()')
            port = doc.xpath('//div[@id="main"]//div//tr/td[2]/text()')
            for index in range(1,len(ip)):
                yield ':'.join([ip[index], port[index]])

    def Proxy_get_kuaidaili(self):
        url = 'https://www.kuaidaili.com/free'
        print('get proxy from ', url)
        doc = etree.HTML(get_html(url))
        ip = doc.xpath('//div[@id="content"]//div[@id="list"]//tbody//td[@data-title="IP"]/text()')
        port = doc.xpath('//div[@id="content"]//div[@id="list"]//tbody//td[@data-title="PORT"]/text()')
        for index in range(len(ip)):
            yield ':'.join([ip[index], port[index]])

    def Proxy_get_daili5u(self):
        url = 'http://www.data5u.com/free/gngn/index.shtml'
        print('get proxy from ', url)
        doc = etree.HTML(get_html(url))
        res = doc.xpath('//div[@class="wlist"]/ul//ul[@class="l2"]//li/text()')
        for num in range(len(res)//4):
            ip = res[num*4]
            port = res[num*4+1]
            yield ':'.join([ip,port])
    
    def Proxy_get_xici(self):
        url = 'http://www.xicidaili.com/nn'
        print('get proxy from ', url)
        doc = etree.HTML(get_html(url))
        ip = doc.xpath('//tr//td[2]/text()')
        port = doc.xpath('//tr//td[3]/text()')
        for index in range(len(ip)):
            yield ':'.join([ip[index], port[index]])

