
MAX_FAILED_TIME = 3
OK_CODE = [200, 304, 301]

from requests import Session
from Request import wechatRequest, RedisQueue
from Proxy import get_proxy
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from db_mysql import MySQL
from urllib import request
import random


class Spider():
    base_url = 'http://weixin.sogou.com/weixin'
    keyword = '杭电'
    mysql = MySQL()
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'pt2gguin=o1412247644; RK=Y8BxU0rwQf; ptcz=d578b38bcd52bed2c43086d26214629964a3bebbc1516120b7dbc05e8dc74ac9; pgv_pvi=761763840; rewardsn=; wxtokenkey=777'
    }
    session = Session()
    queue = RedisQueue()

    def start(self):
        # self.session.headers.update(self.headers)  #更新全局headers
        start_url = self.base_url + '?' + \
            urlencode({'query': self.keyword, 'type': 2})  # 请求构造
        weixin_req = wechatRequest(
            url=start_url, callback=self.parse_index, need_proxy=True)  # 特制request实例化
        self.queue.add(weixin_req)  # 请求入队列

    def request(self, weixin_req):  # 源码请求
        try:
            if weixin_req.need_proxy:
                proxy = get_proxy()
                if proxy:
                    proxies = {
                        'http': 'http://' + proxy,
                        'https': 'https://' + proxy
                    }
                    return self.session.send(weixin_req.prepare(), timeout=weixin_req.timeout, allow_redirects=False, proxies=proxies)
                print('proxy error:', proxy)
            return self.session.send(weixin_req.prepare(), timeout=weixin_req.timeout, allow_redirects=False)
        except Exception as e:
            print(e.args)
            return False

    def request_urlib(self, weixin_req):
        try:
            if weixin_req.need_proxy:
                proxy = get_proxy()
                if proxy:
                    proxy = request.ProxyHandler({'http': proxy})
                    opener = request.build_opener(proxy, request.HTTPHandler)
                    request.install_opener(opener)
                    data = request.urlopen(weixin_req.url, timeout=5).read()
                    return data
                print('proxy error:', proxy)
            req = request.Request(weixin_req.url)
            f = request.urlopen(req)
            return f.read()
        except Exception as e:
            print(e.args)
            return False

    def parse_index(self, response):  # 索引页解析，返回新的wechatRequest类的实例
        #doc = pq(response.text)
        doc = pq(response)
        # 解析出所有文章链接
        items = doc('.news-box .news-list li .txt-box h3 a').items()
        for it in items:
            url = it.attr('href')
            # 返回一个wechatRequest对象，url为文章链接，callback采用parse_detail
            weixin_req = wechatRequest(
                url=url, callback=self.parse_detail, need_proxy=True)
            yield weixin_req

        next = doc('#sogou_next').attr('href')  # 获取下一页的链接
        if next:
            url = self.base_url + str(next)
            # 返回一个wechatRequest对象，url为下一页链接，callback采用parse_index
            weixin_req = wechatRequest(
                url=url, callback=self.parse_index, need_proxy=True)
            yield weixin_req

    def parse_detail(self, response):  # 详情页解析,返回包含页面信息的字典
        #doc = pq(response.text)
        doc = pq(response)
        data = {
            'id': random.randint(1, 1000),
            'title': doc('head title').text(),
            'content': doc('.rich_media_content').text(),
            'date': doc('#post-date').text(),
        }

        yield data

    def error(self, wexin_req):
        wexin_req.fail_time += 1
        print('Requst Failed', wexin_req.fail_time, wexin_req.url)
        if wexin_req.fail_time < MAX_FAILED_TIME:
            self.queue.add(wexin_req)

    def schedule(self):  # 调度模块
        while not self.queue.empty():
            try:
                weixin_req = self.queue.pop()  # 从队列中拿出一个请求
                callback = weixin_req.callback  # 导出回调函数
                print('Schedule',  weixin_req.url)
                response = self.request_urlib(weixin_req)  # 调用request方法，执行请求
                if response:  # and response.status_code in OK_CODE:
                    results = list(callback(response))
                    if results:
                        for res in results:
                            print('New Result:', res)
                            if isinstance(res, wechatRequest):
                                self.queue.add(res)
                            if isinstance(res, dict):
                                self.mysql.insert('articles', res)
                    else:
                        self.error(weixin_req)
                else:
                    self.error(weixin_req)
            except Exception as e:
                print(e.args)
                self.start()

    def run(self):
        self.start()
        self.schedule()


if __name__ == '__main__':
    spider = Spider()
    spider.run()
