
from urllib import request
import requests 
from bs4 import BeautifulSoup 
import csv 
import pandas as pd
from lxml import etree
import lxml.html


symbols=[]
names=[]
prices=[]
changes=[]
percentChanges=[]
averageVolume=[]
volume=[]
marketCaps=[]

CryptoCurrenciesUrl = "https://in.finance.yahoo.com/most-active?offset"
r= requests.get(CryptoCurrenciesUrl)
data=r.text
soup=BeautifulSoup(data, 'html.parser')
# print(soup)

for listing in soup.find_all('tr', attrs={'class':'simpTblRow'}):
	# print(listing)
	for symbol in listing.find_all('td', attrs={'aria-label':'Symbol'}):
		symbols.append(symbol.text)
	for name in listing.find_all('td', attrs={'aria-label':'Name'}):
		names.append(name.text)
	for price in listing.find_all('td', attrs={'aria-label':'Price (intraday)'}):
		prices.append(price.find('span').text)
	for change in listing.find_all('td', attrs={'aria-label':'Change'}):
		changes.append(change.text)
	for percentChange in listing.find_all('td', attrs={'aria-label':'% change'}):
		percentChanges.append(percentChange.text)
	for marketCap in listing.find_all('td', attrs={'aria-label':'Market cap'}):
		marketCaps.append(marketCap.text)
	for avVolume in listing.find_all('td', attrs={'aria-label':'Avg vol (3-month)'}):
		averageVolume.append(avVolume.text)
	for toVolume in listing.find_all('td', attrs={'aria-label':'Volume'}):
		volume.append(toVolume.text)



ddf = pd.DataFrame({"Symbols": symbols, "Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges, "Average Volume": averageVolume,"Volume":volume, "Market Cap": marketCaps})
# def convert_to_numeric(column):
# 	first_col = [i.replace(',','') for i in column]
# 	second_col = [i.replace('-','') for i in first_col]
# 	final_col = pd.to_numeric(second_col)
# 	return final_col

# for index in range(2,5):
# 	# df[column] = convert_to_numeric(df[column])
# 	ddf.iloc[index] = pd.to_numeric(ddf.iloc[index])
	# final_df = df.fillna('-') 

ddf.to_csv('stocks.csv', mode = 'a', header = False)
