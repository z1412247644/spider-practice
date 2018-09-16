'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
try:
    browser.get('https://www.baidu.com')
    input = browser.find_element_by_id('kw')
    input.send_keys('美女')
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)    
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    print(browser.current_url)
    print(browser.get_cookies())
    #print(browser.page_source)
except:
    pass
#finally:
    #browser.close()
'''

from selenium import webdriver
from selenium.webdriver import ActionChains
import time
browser = webdriver.Chrome()
'''
url = 'http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable'
browser.get(url)
browser.switch_to.frame('iframeResult')
time.sleep(1)
source = browser.find_element_by_css_selector('.ui-draggable')
target = browser.find_element_by_css_selector('.ui-droppable')
id = source.get_attribute('id')
actions = ActionChains(browser)
actions.()
print(id)
'''

browser.get('https://m.weibo.com')
time.sleep(2)
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(5)
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("NICE")')