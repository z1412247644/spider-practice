
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
    keyword = 'AI'
    mysql = MySQL()
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'SUV=00B717907BBC19375B754DE5DDD1C135; CXID=40C55C98489DD144249E942682A3E077; SUID=1C17BC7B3965860A5B7B778500073D9C; ad=Oyllllllll2bIKJ8lllllVmODXcllllltl$juZlllltlllllVklll5@@@@@@@@@@; ABTEST=7|1537766358|v1; IPLOC=CN3301; weixinIndexVisited=1; SNUID=0BF51597484C3FA58EB98F094941C6D8; ppinf=5|1538299679|1539509279|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToxMzpoZWxsbyUyMHdvcmxkfGNydDoxMDoxNTM4Mjk5Njc5fHJlZm5pY2s6MTM6aGVsbG8lMjB3b3JsZHx1c2VyaWQ6NDQ6bzl0Mmx1STdHeHd2ZDhsNDVUMHVFQ3RUSzNmQUB3ZWl4aW4uc29odS5jb218; pprdig=FLnPNNnfIQ3McE6JNfSq6VNE2Uomnfr5JvZyUbwGRjn1gx3rPX7hDeDFhjr8MiTjE5Bpu1TbvIZYQjrujiMMIoibkIUtoTR5HyWcS7kihLVcn6Re2yy5SpNavN__1T_bAJsD5j_56nunIAuR4rBW1V0kjGsjADhiAc8512WlcVM; sgid=08-37325885-AVuwlx9FeuVbNPIFOoCPzW4; ppmdig=1538299679000000b706e0fce1bd92b5f8fa8aef411841c7; sct=4; JSESSIONID=aaakz_uVUUW6NcYg1bJvw',
        'Referer': 'https://weixin.sogou.com/weixin?query=AI&_sug_type_=&sut=19182&lkt=1%2C1538299670346%2C1538299670346&s_from=input&_sug_=y&type=2&sst0=1538299670449&page=1&ie=utf8&w=01019900&dr=1'
    }
    session = Session()
    queue = RedisQueue()

    def start(self):
        self.session.headers.update(self.headers)  #更新全局headers
        start_url = self.base_url + '?' + \
            urlencode({'query': self.keyword, 'type': 2, 'page': 4, 'ie': 'utf8'})  # 请求构造
        weixin_req = wechatRequest(url=start_url, callback=self.parse_index, need_proxy=True, req_func=0)  # 特制request实例化
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
        doc = pq(response.text)
        # 解析出所有文章链接
        items = doc('.news-box .news-list li .txt-box h3 a').items()
        for it in items:
            url = it.attr('href')
            # 返回一个wechatRequest对象，url为文章链接，callback采用parse_detail
            weixin_req = wechatRequest(
                url=url, callback=self.parse_detail, need_proxy=True, req_func = 1)
            yield weixin_req

        next = doc('#sogou_next').attr('href')  # 获取下一页的链接
        if next:
            url = self.base_url + str(next)
            # 返回一个wechatRequest对象，url为下一页链接，callback采用parse_index
            weixin_req = wechatRequest(
                url=url, callback=self.parse_index, need_proxy=True, req_func = 0)
            yield weixin_req

    def parse_detail(self, response):  # 详情页解析,返回包含页面信息的字典
        #doc = pq(response.text)
        doc = pq(response)
        data = {
            'id': random.randint(1, 1000),
            'title': doc('head title').text(),
            'content': doc('.rich_media_content').text(),
            #'date': doc('#post-date').text(),
            'date': doc('#js_author_name').text()
        }

        yield data

    def error(self, wexin_req):
        wexin_req.fail_time += 1
        print('Requst Failed', wexin_req.fail_time, wexin_req.url)
        if wexin_req.fail_time < MAX_FAILED_TIME or wexin_req.req_func == 0:
            self.queue.add(wexin_req)

    def schedule(self):  # 调度模块
        while not self.queue.empty():
            try:
                weixin_req = self.queue.pop()  # 从队列中拿出一个请求
                callback = weixin_req.callback  # 导出回调函数
                print('Schedule',  weixin_req.url)
                if weixin_req.req_func == 0:    #判断调用哪个request方法,这里解析索引用requests库，解析内容用urllib库
                    response = self.request(weixin_req)
                else:
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
