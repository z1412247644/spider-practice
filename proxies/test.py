import time
import requests


headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}

proxy_url = 'http://47.101.136.128:8888/random'
aim_url = 'http://47.101.136.128/'

def get_proxy():
    try:
        res = requests.get(proxy_url)
        if res.status_code == 200:
            return res.text
    except:
        return None
def main():
    proxy = get_proxy()
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    try:
        res =  requests.get(aim_url, proxies=proxies, timeout = 3)
        print(res.status_code)
    except Exception as e:
        print(e)
while(True):
    main()
    time.sleep(1)
