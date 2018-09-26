'''
采用多进程同时运行调度个模块
'''
TESTER_CYCLE = 20
GETTER_CYCLE = 300
TESTER_ENABLE = True
GETTER_ENABLE = True
API_ENABLE = True
API_HOST = '127.0.0.1'
API_PORT = 8888

from multiprocessing import Process
from web_api import app
from Proxy_add import Getter
from detect import Tester
import time 
class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        tester = Tester()
        while(True):
            print('start TESTER')
            tester.run()
            time.sleep(cycle)
    
    def schedule_getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while(True):
            print('start GETTER')
            getter.run()
            time.sleep(cycle)
    
    def schedule_api(self):
        app.run(API_HOST, API_PORT)

    def run(self):
        print('PROXY SYSTEM START')
        if TESTER_ENABLE :
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()
        if GETTER_ENABLE :
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()
        if API_ENABLE :
            api_process = Process(target=self.schedule_api)
            api_process.start()

if __name__ == '__main__':
    main = Scheduler()
    main.run()