TIMEOUT = 10

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'sogouwechat'

from requests import Request
from pickle import dumps, loads
from redis import StrictRedis

class wechatRequest(Request):
    def __init__(self, url, callback, method='GET', headers=None, need_proxy=False, fail_time=0, timeout=TIMEOUT):
        Request.__init__(self, method, url,headers)
        self.callback = callback
        self.need_proxy = need_proxy
        self.fail_time = fail_time
        self.timeout = timeout

class RedisQueue():
    def __init__(self):
        self.db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
    def add(self, req):
        if isinstance(req, wechatRequest):
            return self.db.rpush(REDIS_KEY, dumps(req))
        return False
    def pop(self):
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        return False
    def empty(self):
        return self.db.llen == 0

