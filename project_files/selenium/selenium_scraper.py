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
import argparse


def main(watchlist=False, email=None, passwd=None):
    gecko_path = 'C:\\Program Files\\Mozilla Firefox\\geckodriver.exe'
    url = 'https://finance.yahoo.com/'
    options = webdriver.firefox.options.Options()
    options.headless = False
    driver = webdriver.Firefox(options=options, executable_path=gecko_path)

    start_scrape(driver, url)
    watchlist_scrape(driver, email, passwd) if watchlist else most_active_scrape(driver)


def start_scrape(driver, url):
    driver.get(url)
    time.sleep(2)

    cookie_handler(driver)
    time.sleep(2)


def cookie_handler(driver):
    cookie = driver.find_element_by_xpath('//button[@class="btn primary"]')
    cookie.click()


def most_active_scrape(driver):
    markets_button = driver.find_element_by_xpath('//a[@title="Markets"]')
    markets_button.click()
    time.sleep(10)

    most_active_button = driver.find_element_by_xpath('//a[@title="Stocks: Most Actives"]')
    most_active_button.click()
    time.sleep(20)

    new_window_scraper(driver, 'most_active')


def watchlist_scrape(driver, email, passwd):
    sign_in_button = driver.find_element_by_xpath('//a[@id="header-signin-link"]')
    sign_in_button.click()
    time.sleep(2)

    email_input = driver.find_element_by_xpath('//input[@id="login-username"]')
    my_email = email if email else input('Please provide your e-mail address:')
    email_input.send_keys(my_email)
    next_button = driver.find_element_by_xpath('//input[@id="login-signin"]')
    next_button.click()
    time.sleep(2)

    password = driver.find_element_by_xpath('//input[@id="login-passwd"]')
    my_pass = passwd if passwd else getpass.getpass('Please provide your password:')
    password.send_keys(my_pass)
    next_button = driver.find_element_by_xpath('//button[@id="login-signin"]')
    next_button.click()
    time.sleep(2)

    watch_list = driver.find_element_by_xpath('//a[@title="My Watchlist"]')
    watch_list.click()
    time.sleep(20)

    new_window_scraper(driver, 'watchlist')


def new_window_scraper(driver, option):
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

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)

    data = pd.DataFrame(table, index=data_index)
    print(data)
    data.to_csv(f"selenium_scrape_{option}.csv", index=True, index_label="Company Name")

    time.sleep(5)
    driver.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--watchlist', type=bool, required=False)
    parser.add_argument('--email', type=str, required=False)
    parser.add_argument('--passwd', type=str, required=False)
    args = parser.parse_args()
    main(watchlist=args.watchlist, email=args.email, passwd=args.passwd)
