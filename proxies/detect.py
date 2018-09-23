'''
代理检测类，检测数据库中代理是否可用，采用异步方式
'''
from db import RedisClient
import aiohttp
import asyncio
import time

VALID_STATUS_CODES = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100   #一次检测代理数

class Tester(object):
    def __init__(self):
        self.redis = RedisClient()
    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('Test ',proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
                    if response.status in VALID_STATUS_CODES:
                        self.redis.set_max(proxy)
                        print('ok', proxy)
                    else:
                        self.redis.decrease(proxy)
                        print('response code illegal', proxy)
            except:
                self.redis.decrease(proxy)
                print('requre fail ',proxy)

    def run(self):
        print('detect running')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()

            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i:i+BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(2)
        except Exception as e:
            print('Tester error', e.args)
    

    