from db import RedisClient
from get_proxy import Proxy_get

POLL_UPPER_THRESHOLD = 10000    #数据库容纳最大代理数

class Getter():
    def __init__(self):
        self.redis = RedisClient()  #实例化数据库操作类
        self.get = Proxy_get()  #实例化代理爬取类
    def is_over_threshold(self):
        if self.redis.count() >= POLL_UPPER_THRESHOLD:
            return True
        else:
            return False
    def run(self):
        print('Getter start')
        if not self.is_over_threshold():
            for callback_label in range(self.get.__FuncCount__):    #遍历代理爬取方法
                callback = self.get.__Func__[callback_label]
                proxies = self.get.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)   #添加到数据库