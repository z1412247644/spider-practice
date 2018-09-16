import redis
from random import choice


MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):  #增加元素
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)
    def random(self):   #按分数随机选取
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE) #获取满score的元素集
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                return None
    def decrease(self, proxy):  #将元素的值减少1
        score = self.db.zscore(REDIS_KEY, proxy)
        if score > MIN_SCORE:
            print('proxy_',proxy, 'score:', score, '-1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print('proxy_',proxy, 'score:', score, ' DEL')
            return self.db.zrem(REDIS_KEY, proxy)
    def exists(self, proxy):    #判断是否元素存在
        return not self.db.zscore(REDIS_KEY, proxy) == None
    def set_max(self, proxy):   #将某元素的值设为最大
        print('proxy', proxy, ' is usable, set as', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)
    def count(self):    #计算总元素数
        return self.db.zcard(REDIS_KEY)     
    def all(self):      #返回所有元素
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
