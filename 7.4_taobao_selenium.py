from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By     #用来传递选择器
from selenium.webdriver.support import expected_conditions as EC    #等待条件
from selenium.webdriver.support.wait import WebDriverWait   
from urllib.parse import quote

from pyquery import PyQuery as pq
from re import sub
import json
import time
import pymongo

MONGO_URL = '127.0.0.1'     #数据库配置
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products_otg'

#无界面模式
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
wait = WebDriverWait(browser, 10)   #显式等待
KEYWORD = 'OTG转接头'

client = pymongo.MongoClient(MONGO_URL)     #数据库初始化
db = client[MONGO_DB]

def get_html(index):    #selenium模拟访问，返回网页源jiedian
    print('loading page ' + str(index))
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)     #url构造
        browser.get(url)
        if index > 1:
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager .form input')))     #等待页码输入框加载
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager .form span.btn.J_Submit')))    #等待页面跳转按钮加载
            #print(input, submit)
            input.clear()
            input.send_keys(str(index))
            submit.click()  #页面跳转
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager .items li.item.active'), str(index)))     #确认页面跳转成功
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))   #等待商品加载完毕
        return browser.page_source
    except TimeoutException:
        get_html(index)

def get_products(html):     #商品信息解析
    product = []
    doc = pq(html)  #pq对象实例化
    items = doc('#mainsrp-itemlist .m-itemlist .items .item.J_MouserOnverReq').items()      #选择商品节点
    for it in items:
        info = {
            'title': it.find('.pic .img').attr('alt'),
            'img': sub('//', 'http://', it.find('.pic .img').attr('data-src')),
            'price': sub('\n', '', it.find('.price').text()),
            'deal-cnt': it.find('.deal-cnt').text(),
            'detail': sub('//', 'http://', it.find('.ctx-box .title .J_ClickStat').attr('href')),
            'shop': it.find('.shop').text(),
            'location': it.find('.location').text()
        }
        product.append(info)
    return product

def save_mongo(data):
    try:
        if db[MONGO_COLLECTION].insert_many(it for it in data):
            print('save ok')
    except Exception:
        print('save fail')

def main():

    for page in range(1,51):
        html = get_html(page)
        result = get_products(html)
        #with open('taobao.json', 'w', encoding='utf-8') as file:
        #    file.write(json.dumps(result, indent=2, ensure_ascii=False))
        save_mongo(result)
        #time.sleep(3)

    browser.close()

if __name__ == '__main__':
    main()