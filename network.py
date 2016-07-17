import time
from selenium import webdriver
from pprint import pprint

driver = webdriver.Chrome()
driver.get('https://www.google.com');
time.sleep(5)
timings = driver.execute_script("return window.performance.getEntries();")
pprint(timings)
driver.close()