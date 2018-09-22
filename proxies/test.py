import json
import requests
from lxml import etree

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}
def get_html(url):  #简单获取网页源码
    req = requests.get(url, headers=headers)
    return req.text


def Proxy_get_daili66(page_num):
        base_url = 'http://www.66ip.cn/areaindex_{}/1.html'
        urls = [base_url.format(page) for page in range (1,page_num)]
        print(urls)
        for url in urls:
            print('get proxy from ', url)
            doc = etree.HTML(get_html(url))
            ip = doc.xpath('//div[@id="main"]//div//tr/td[1]/text()')
            port = doc.xpath('//div[@id="main"]//div//tr/td[2]/text()')
            for index in range(1,len(ip)):
                 print(':'.join([ip[index], port[index]]))
Proxy_get_daili66(2)