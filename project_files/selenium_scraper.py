#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 20.04.2021 - 22:09

@author: ALPARSLAN
"""
from selenium import webdriver
import time
import re
import pandas as pd
from collections import defaultdict
import getpass


gecko_path = 'C:\\Program Files\\Mozilla Firefox\\geckodriver.exe'
url = 'https://finance.yahoo.com/'


options = webdriver.firefox.options.Options()
options.headless = False

driver = webdriver.Firefox(options=options, executable_path=gecko_path)

driver.get(url)
# print(driver.page_source)

time.sleep(1)

cookie = driver.find_element_by_xpath('//button[@class="btn primary"]')
cookie.click()

time.sleep(1)

sign_in_button = driver.find_element_by_xpath('//a[@id="header-signin-link"]')
sign_in_button.click()

time.sleep(2)

email = driver.find_element_by_xpath('//input[@id="login-username"]')
my_email = input('Please provide your e-mail address:')
email.send_keys(my_email)
next_button = driver.find_element_by_xpath('//input[@id="login-signin"]')
next_button.click()

time.sleep(1)

password = driver.find_element_by_xpath('//input[@id="login-passwd"]')
my_pass = getpass.getpass('Please provide your password:')
password.send_keys(my_pass)
next_button = driver.find_element_by_xpath('//button[@id="login-signin"]')
next_button.click()

time.sleep(1)

watch_list = driver.find_element_by_xpath('//a[@title="My Watchlist"]')
watch_list.click()

time.sleep(5)
# print(driver.page_source)

links = driver.find_elements_by_xpath('//a[@class="Fw(600) C($linkColor)"]')

keys = list()
data_index = list()
table = defaultdict(list)

for index, link in enumerate(links):
    values = list()
    temp = link.get_attribute('href')
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(temp)
    time.sleep(5)

    regex = re.compile('(.*)\s\((.*)\)')
    company_all = driver.find_element_by_xpath("//h1[@class='D(ib) Fz(18px)']")
    company_name, company_short = re.findall(regex, company_all.text)[0]

    data_index.append(company_name)

    if index == 0:
        keys.append(str('Company Short'))
        keys_find = driver.find_elements_by_xpath("//td[@class='C($primaryColor) W(51%)']")
        keys = keys + [f.text for f in keys_find]

    values.append(company_short)
    value_find = driver.find_elements_by_xpath("//td[@class='Ta(end) Fw(600) Lh(14px)']")
    values = values + [v.text for v in value_find]

    for k, v in zip(keys, values):
        try:
            table[k].append(v)
        except Exception as e:
            print(e)
            table[k].append(None)

    time.sleep(5)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

data = pd.DataFrame(table, index=data_index)
print(data)

time.sleep(5)
driver.quit()
