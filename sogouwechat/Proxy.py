PROXY_SERVER = 'http://47.101.136.128:8888/random'

import requests

def get_proxy():
    try:
        res =requests.get(PROXY_SERVER)
        if res.status_code == 200:
            return res.text
    except Exception as e:
        print('GET PROXY ERROR:',e)
        return None

