from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


LOGGED_IN = False
headless = True
use_chrome = False

def login_by_fb() : 
    attr_element = '"navbar__link navbar__link--account navbar__link--tappable navbar__link--hoverable navbar__link-text navbar__link-text--medium"'
    while not(driver.find_elements_by_css_selector("li[class={}]".format(attr_element))) :
        time.sleep(2)
    element = driver.find_elements_by_css_selector("li[class={}]".format(attr_element))[0]
    element.click()
    global LOGGED_IN
    LOGGED_IN = True

with open('login_info.txt') as f :
    email_addr , password = f.read().split('\n')

options = Options()

if headless :
    if use_chrome :
        options.add_argument('--headless')
    else :
	    options.headless = True

if use_chrome :
    driver = webdriver.Chrome(options=options)
else :
    driver = webdriver.Firefox(options=options)

try :

    driver.get("http://facebook.com")

    if headless :
        print('Trying to login facebook')

    time.sleep(3)

    email = driver.find_element_by_css_selector('input[class="inputtext"][name="email"]')
    email.send_keys(email_addr)
    passw = driver.find_element_by_css_selector('input[class="inputtext"][name="pass"]')
    passw.send_keys(password)
    passw.send_keys(Keys.ENTER)

    time.sleep(10)

    driver.get('http://shopee.sg')
    time.sleep(5)

    while not(LOGGED_IN) :
        try : 
            login_by_fb()
        except :
            element = driver.find_element_by_css_selector('div[class*= "close-btn"]')
            element.click()
            login_by_fb()
			
    print('Logged in!')
		
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class="shopee-authen-modal__tab"]')))

    element = driver.find_elements_by_css_selector('button[class="shopee-authen-modal__tab"]')[0]
    element.click()
    time.sleep(1)

    while driver.find_elements_by_css_selector('div[class="_32sqWs"]') :
        driver.execute_script('document.querySelectorAll("div._32sqWs")[1].click()')
        time.sleep(2)

    time.sleep(4)
    driver.get('https://shopee.sg/shopee-coins/')
    time.sleep(3)

    if headless :
        print('Trying to fetch coins.')

    new_path = driver.find_elements_by_tag_name('iframe')[0].get_attribute('src')
    driver.get(new_path)
    time.sleep(3)

    if "Come back tomorrow" in driver.find_element_by_css_selector('div[class*="top-btn"]').text :
        time.sleep(2)
        print('Coins already claimed!!')
        driver.quit()
    else :
        time.sleep(2)
        driver.find_elements_by_css_selector('div[class*="top-btn"]')[0].click()
        print('Collection Success!!')
    driver.quit()
except :
    driver.quit()