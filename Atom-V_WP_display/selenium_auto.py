from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
# chrome_path = r'C:\Users\vilvakannan.velusamy\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'
# service = Service(executable_path=chrome_path)
driver = webdriver.Chrome()
driver.get('https://www.youtube.com/')
title = driver.title # returns page title
print(title)
# print(driver.page_source) # returns HTML page

''' 
Navigation commands 

driver.back() backward button
driver.forward() forward button

Conditional commands
is_enabled() returns True/False
is_displayed() returns True/False
is_selected() returns True/False
 '''
ele = driver.find_element(By.ID,'search')

print(ele.is_displayed())
print(ele.is_enabled())


time.sleep(3000)


driver.close() # close current window
# driver.quit() # close all tab in window