MAX_FAILED_TIME = 3
OK_CODE = [200, 304]

from requests import Session
from Request import wechatRequest,RedisQueue
from Proxy import get_proxy
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from db_mysql import MySQL

class Spider():
    base_url = 'http://weixin.sougou.com/weixin'
    keyword = '杭电'
    mysql = MySQL()
    headsers = {
        'Host': 'weixin.sogou.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://weixin.sogou.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'SUV=00B717907BBC19375B754DE5DDD1C135; CXID=40C55C98489DD144249E942682A3E077; SUID=1C17BC7B3965860A5B7B778500073D9C; ad=Oyllllllll2bIKJ8lllllVmODXcllllltl$juZlllltlllllVklll5@@@@@@@@@@; ABTEST=7|1537766358|v1; IPLOC=CN3301; weixinIndexVisited=1; SNUID=CE93D6304B493DDC6DE85E0A4C40C414; sct=3; JSESSIONID=aaalRzNa7jxDyeIwoMHvw'
    }
    session = Session()
    queue = RedisQueue()

    def start(self):
        self.session.headers.update(self.headsers)  #更新全局headers
        start_url = self.base_url + '?' + urlencode({'query':self.keyword, 'type':2})  #请求构造
        weixin_req = wechatRequest(url=start_url, callback=self.parse_index, need_proxy=True)  #特制request实例化
        self.queue.add(weixin_req)  #请求入队列

    def request(self, weixin_req):  #源码请求
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
        except(ConnectionError) as e:
            print(e.args)
            return False

    def parse_index(self, response):  #索引页解析，返回新的wechatRequest类的实例
        doc = pq(response.text)
        items = doc('.new-box .new-list li .txt-box h3 a').items()  #解析出所有文章链接
        for it in items:
            url = it.attr('href')
            weixin_req = wechatRequest(url=url, callback=self.parse_detail, need_proxy=True)    #返回一个wechatRequest对象，url为文章链接，callback采用parse_detail
            yield weixin_req
        next = doc('#sogou_next').attr('href')  #获取下一页的链接
        if next:
            url = self.base_url + str(next)
            weixin_req = wechatRequest(url=url, callback=self.parse_index, need_proxy=True) #返回一个wechatRequest对象，url为下一页链接，callback采用parse_index
            yield weixin_req
    
    def parse_detail(self, response):   #详情页解析,返回包含页面信息的字典
        doc = pq(response.text)
        data = {
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

    def schedule(self):     #调度模块
        while not self.queue.empty():
            weixin_req = self.queue.pop()   #从队列中拿出一个请求
            callback = weixin_req.callback  #导出回调函数
            print('Schedule',  weixin_req.url) 
            response = self.request(weixin_req)  #调用request方法，执行请求
            if response and response.status_code == 200:
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

    def run(self):
        self.start()
        self.schedule()

if __name__ == '__main__':
    spider = Spider()
    spider.run()

