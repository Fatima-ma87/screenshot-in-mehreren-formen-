import configparser
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

config = configparser.ConfigParser()		
config.read("config.ini")
path = config['path']
size = config['size']
suche = config['suche']
login = config['login']



user_agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36 /1.1"
options = webdriver.ChromeOptions()  
driver = webdriver.Chrome(path["driver_location"], chrome_options=options)
 
 
def open_url(url, prefix):  
    options = Options()
    options.add_argument("user-agent=" + user_agent)
 
    options.headless = False
    driver = webdriver.Chrome(path["driver_location"],options=options)
    driver.maximize_window()
    driver.get(url)
    site_login(url,driver)
    driver.set_window_position(-1900,-1000)
    driver.implicitly_wait(3)
    driver.set_window_size(width=size["res_x"], height=size["res_y"])
    
    save_screenshot(driver, prefix)
 
def save_screenshot(driver, prefix):
    height, width = scroll_down(driver, prefix)
    driver.set_window_size(width, height)
    img_binary = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(img_binary))
    file_path = path["ordner"] + prefix +  ".png"
    img.save(file_path)
   
    print(" screenshot saved ")
 
def save_part(driver, count, prefix):
    img_binary = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(img_binary))
    fname =  path["ordner"] + prefix   # hier muss die richtige folderName und navigieren 
    file_path = fname + "." + "{0:03d}".format(count) + ".png"
    img.save(file_path)
    print(" screenshot "+str(count)+" saved ")


def site_login(url, driver ):
    #driver.get(url)
    driver.find_element(By.XPATH, 'xxxxxxxxxxxx').click() 
    # https://selenium-python.readthedocs.io/locating-elements.html
    driver.find_element(By.XPATH, 'xxxxxxxxxx').send_keys(login['username'], Keys.TAB)
    driver.find_element(By.XPATH, 'xxxxxxxxxxx').send_keys(login['password'])
    driver.find_element(By.XPATH, 'xxxxxxxxxxx').submit()
    driver.find_element(By.XPATH, 'xxxxxxxxxxxxx').send_keys(suche["muster"], Keys.ENTER) 
    print("login")
 
 
def scroll_down(driver, prefix):
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
 
    rectangles = []
 
    i = 0
    c = 0
 
    while i < total_height:
        c = c + 1
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
            print(c)
 
            ii = ii + viewport_width
 
        i = i + viewport_height
 
    previous = None
    part = 0
 
    c = 0
    for rectangle in rectangles:
        c = c + 1
        if not previous is None:
            driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
            time.sleep(0.5)
 
        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])
 
        previous = rectangle
        save_part(driver,c,prefix)
 
    return (total_height, total_width)
 
open_url('https://www.xxxxxxxxxx ', suche["muster"] + '-' + time.strftime('.%Y%m%d-%H%M-%S')) 

