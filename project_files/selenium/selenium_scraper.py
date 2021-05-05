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
    """
    Selenium scraper is triggering from the main function by setting up webdriver, gecko path and url.
    :param watchlist:
    :param email:
    :param passwd:
    :return:
    """
    gecko_path = 'C:\\Program Files\\Mozilla Firefox\\geckodriver.exe'
    url = 'https://finance.yahoo.com/'
    options = webdriver.firefox.options.Options()
    options.headless = False
    driver = webdriver.Firefox(options=options, executable_path=gecko_path)

    start_scrape(driver, url)
    watchlist_scrape(driver, email, passwd) if watchlist else most_active_scrape(driver)


def start_scrape(driver, url):
    """
    This function is used to start selenium bot.
    :param driver:
    :param url:
    :return:
    """
    driver.get(url)
    time.sleep(2)

    cookie_handler(driver)
    time.sleep(2)


def cookie_handler(driver):
    """
    While selenium bot is trying to reach the website, a popup message appears to give consent for cookies in the website.
    This function used to handle this cookie message by clicking on the “accept all cookies in this page” button.
    :param driver:
    :return:
    """
    cookie = driver.find_element_by_xpath('//button[@class="btn primary"]')
    cookie.click()


def most_active_scrape(driver):
    """
    :if --watchlist is False
    This function is triggering the Stocks: Most Actives mechanism to scrape data in this most active page by:
    - Click on the “Markets” button,
    - Click on the “Stocks: Most Actives” button.
    :param driver:
    :return:
    """
    markets_button = driver.find_element_by_xpath('//a[@title="Markets"]')
    markets_button.click()
    time.sleep(10)

    most_active_button = driver.find_element_by_xpath('//a[@title="Stocks: Most Actives"]')
    most_active_button.click()
    time.sleep(20)

    new_window_scraper(driver, 'most_active')


def watchlist_scrape(driver, email, passwd):
    """
    :if --watchlist is True
    This function is triggering the watchlist scraper mechanism by:
    - Click on the “sign in” button,
    - Input “email address”,
    - Input “password”,
    - Click on the “My Watchlist” button.
    :param driver:
    :param email:
    :param passwd:
    :return:
    """
    # Sign in button
    sign_in_button = driver.find_element_by_xpath('//a[@id="header-signin-link"]')
    sign_in_button.click()
    time.sleep(2)

    # Input email address
    email_input = driver.find_element_by_xpath('//input[@id="login-username"]')
    my_email = email if email else input('Please provide your e-mail address:')
    email_input.send_keys(my_email)
    next_button = driver.find_element_by_xpath('//input[@id="login-signin"]')
    next_button.click()
    time.sleep(2)

    # Input password
    password = driver.find_element_by_xpath('//input[@id="login-passwd"]')
    my_pass = passwd if passwd else getpass.getpass('Please provide your password:')
    password.send_keys(my_pass)
    next_button = driver.find_element_by_xpath('//button[@id="login-signin"]')
    next_button.click()
    time.sleep(2)

    # Click on "My Watchlist" button
    watch_list = driver.find_element_by_xpath('//a[@title="My Watchlist"]')
    watch_list.click()
    time.sleep(20)

    new_window_scraper(driver, 'watchlist')


def new_window_scraper(driver, option):
    """
    This function is used to scrape data for every single company page by:
    - Open company pages in the list into the new tab,
    - Scrape data inside the table,
    - Save scraped data into dictionary of lists
    - Close the new tab,
    - Scrape all data in a loop like described above,
    - After all data is scraped into the dictionary, convert this to pandas dataframe and save data into a csv file
    (name of csv file created based on the users’ prefer, if --watchlist is True, name of the file is
    selenium_scrape_watchlist.csv, else: selenium_scrape_most_active.csv).
    - Terminate the selenium session.
    :param driver:
    :param option:
    :return:
    """
    links = driver.find_elements_by_xpath('//a[@class="Fw(600) C($linkColor)"]')
    keys = list()
    data_index = list()
    table = defaultdict(list)

    # For loop to scrape all data for companies in the list
    for index, link in enumerate(links):
        values = list()
        # New window process
        temp = link.get_attribute('href')
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(temp)
        time.sleep(5)

        # Regex to get name and shortcut of the company
        regex = re.compile('(.*)\s\((.*)\)')
        company_all = driver.find_element_by_xpath("//h1[@class='D(ib) Fz(18px)']")
        company_name, company_short = re.findall(regex, company_all.text)[0]
        # Add company data to the list
        data_index.append(company_name)

        # Get all company short cut information just a single time when index == 0
        if index == 0:
            keys.append(str('Company Short'))
            keys_find = driver.find_elements_by_xpath("//td[@class='C($primaryColor) W(51%)']")
            keys = keys + [f.text for f in keys_find]

        # Append company shortcut value into the list
        values.append(company_short)
        # Scrap values into the table
        value_find = driver.find_elements_by_xpath("//td[@class='Ta(end) Fw(600) Lh(14px)']")
        values = values + [v.text for v in value_find]

        # Configure dictionary
        for k, v in zip(keys, values):
            try:
                table[k].append(v)
            except Exception as e:
                print(e)
                table[k].append(None)

        driver.close()
        # Close the new window
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(5)

    # Import data inside the dictionary to the pandas dataframe
    data = pd.DataFrame(table, index=data_index)
    print(data)
    # Save csv file based on the user preferences.
    # If users select to scrape date from the "My Watchlist" option -> watchlist
    # If users select to scrape date from the "Most Active Page" option -> most_active
    data.to_csv(f"selenium_scrape_{option}.csv", index=True, index_label="Company Name")

    # Quit driver, end selenium bot
    time.sleep(5)
    driver.quit()


if __name__ == '__main__':
    """
    You can find detailed description about the command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--watchlist', type=bool, required=False)
    parser.add_argument('--email', type=str, required=False)
    parser.add_argument('--passwd', type=str, required=False)
    args = parser.parse_args()
    main(watchlist=args.watchlist, email=args.email, passwd=args.passwd)
