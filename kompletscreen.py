import configparser
import time
from io import BytesIO
from re import U

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36 /1.1"

config = configparser.ConfigParser()		
config.read("config.ini")
path = config['path']
size = config['size']
suche = config['suche']
 


 
 
def open_url(url, prefix):
    options = Options()
    options.add_argument("user-agent=" + user_agent)
 
    options.headless = True
    driver = webdriver.Chrome(path["driver_location"],options=options)
    driver.maximize_window()
    driver.get(url)
    site_suchen(url,driver)
    driver.set_window_position(-1900,-1000)
    driver.implicitly_wait(3)
    driver.set_window_size(width=size["res_x"], height=size["res_y"])
    save_screenshot(driver, prefix)
 
def save_screenshot(driver, prefix):
    height, width = scroll_down(driver)
    driver.set_window_size(width, height)
    img_binary = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(img_binary))
    file_path = path["ordner"] + prefix +  ".png"
    img.save(file_path)
    print(" screenshot saved ")
 
 
def site_suchen(url, driver):
    driver.get(url)
    driver.find_element(By.XPATH, 'xxxxxx').click()
    driver.find_element(By.XPATH, 'xxxxxxx').send_keys(suche["muster"], Keys.ENTER)  #suchmuster 
    time.sleep(1)
    print(" eingabe ")
 
def scroll_down(driver):
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
 
    rectangles = []
 
    i = 0
 
    while i < total_height:
        ii = 0
        top_height = i + viewport_height
 
        if top_height > total_height:
            top_height = total_height
 
        while ii < total_width:
            top_width = ii + viewport_width
 
            if top_width > total_width:
                top_width = total_width
 
            rectangles.append((ii, i, top_width, top_height))
            print(rectangles)
 
            ii = ii + viewport_width
 
        i = i + viewport_height
 
    previous = None
    part = 0
 
    for rectangle in rectangles:
        if not previous is None:
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
            time.sleep(0.5)
 
        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])
 
        previous = rectangle
 
    return (total_height, total_width)
 

 
open_url('https://www.xxxxxxxxxx', suche["muster"] + time.strftime('%Y%m%d-%H%M-%S'))
