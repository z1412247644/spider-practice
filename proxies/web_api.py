'''
基于flask的web，用以提供代理接口
'''
from flask import Flask, g
from db import RedisClient

__all__ = ['app']
app = Flask(__name__)

def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    return '<h2>Welcome to Proxy Pool System</h2>'

@app.route('/random')   #从数据库随机调取高质量代理
def get_proxy():
    conn = get_conn()
    return conn.random()

@app.route('/count')    #计算代理数
def get_counts():
    conn = get_conn()
    return str(conn.count())

if __name__ == '__main__':
    app.run()
