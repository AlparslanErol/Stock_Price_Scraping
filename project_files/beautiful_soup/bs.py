
# import the necessary libraries
from urllib import request
import requests 
from bs4 import BeautifulSoup
import pandas as pd

# find symbols and names of 24 most active stocks
symbols=[]
names=[]

url = "https://in.finance.yahoo.com/most-active?offset"
data= requests.get(url).text
soup=BeautifulSoup(data, 'html.parser')

for listing in soup.find_all('tr', attrs={'class':'simpTblRow'}):
	for symbol in listing.find_all('td', attrs={'aria-label':'Symbol'}):
		symbols.append(symbol.text)
	for name in listing.find_all('td', attrs={'aria-label':'Name'}):
		names.append(name.text)

# empty lists to store data for each stock
Previous_Close=[]
Open=[]
Bid=[]
Ask=[]
percentChanges=[]
Day_Range=[]
_52_Week_Range=[]
Volume=[]
Avg_Volume=[]
Market_Cap=[]
Beta_5Y_Monthly=[]
PE_Ratio_TTM=[]
EPS_TTM=[]
Earnings_Date = []
Forward_Dividend_Yield = []
Ex_Dividend_Date = []
_1y_target_Est = []


#all urls to individual yahoo finance pages of the most active stocks have similar format
# url = "https://finance.yahoo.com/quote/"+symbol+"?p="+symbol
links = []
for symbol in symbols:
	links.append("https://finance.yahoo.com/quote/"+symbol+"?p="+symbol)

# get html of each page by url, find the first and the second tables
# find the respective variable by its data-test attribute
# [0].text) returns only the text part of the first element of the list 
for link in links:
	r= requests.get(link)
	html=r.text
	parsed=BeautifulSoup(html, 'html.parser')
	# the first table
	soup = parsed.find_all('table',)[0]

	Previous_Close.append(soup.find_all('td', attrs={'data-test':'PREV_CLOSE-value'})[0].text)
	Open.append(soup.find_all('td', attrs={'data-test':'OPEN-value'})[0].text)
	Bid.append(soup.find_all('td', attrs={'data-test':'BID-value'})[0].text)
	Ask.append(soup.find_all('td', attrs={'data-test':'ASK-value'})[0].text)
	Day_Range.append(soup.find_all('td', attrs={'data-test':'DAYS_RANGE-value'})[0].text)
	_52_Week_Range.append(soup.find_all('td', attrs={'data-test':'FIFTY_TWO_WK_RANGE-value'})[0].text)
	Volume.append(soup.find_all('td', attrs={'data-test':'TD_VOLUME-value'})[0].text)
	Avg_Volume.append(soup.find_all('td', attrs={'data-test':'AVERAGE_VOLUME_3MONTH-value'})[0].text)
	# the second table
	soup = parsed.find_all('table',)[1]

	Market_Cap.append(soup.find_all('td', attrs={'data-test':'MARKET_CAP-value'})[0].text)
	Beta_5Y_Monthly.append(soup.find_all('td', attrs={'data-test':'BETA_5Y-value'})[0].text)
	PE_Ratio_TTM.append(soup.find_all('td', attrs={'data-test':'PE_RATIO-value'})[0].text)
	EPS_TTM.append(soup.find_all('td', attrs={'data-test':'EPS_RATIO-value'})[0].text)
	Earnings_Date.append(soup.find_all('td', attrs={'data-test':'EARNINGS_DATE-value'})[0].text)
	Forward_Dividend_Yield.append(soup.find_all('td', attrs={'data-test':'DIVIDEND_AND_YIELD-value'})[0].text)
	Ex_Dividend_Date.append(soup.find_all('td', attrs={'data-test':'EX_DIVIDEND_DATE-value'})[0].text)
	_1y_target_Est.append(soup.find_all('td', attrs={'data-test':'ONE_YEAR_TARGET_PRICE-value'})[0].text)

# create dataframe with column names as in the web page
data_frame = pd.DataFrame({"Symbols": symbols, "Names": names, "Previous Close": Previous_Close, "Open": Open, "Bid": Bid, "Ask": Ask, "Day's Range": Day_Range,
 			"52 Week Range": _52_Week_Range,"Volume":Volume, "Avg. Volume": Avg_Volume, "Market Cap": Market_Cap, "Beta (5Y Monthly)": Beta_5Y_Monthly,
 			"PE Ratio (TTM)": PE_Ratio_TTM, "EPS (TTM)": EPS_TTM, "Earnings Date": Earnings_Date, "Forward Dividend & Yield": Forward_Dividend_Yield,
 			"Ex-Dividend Date": Ex_Dividend_Date, "1y Target Est": _1y_target_Est})

# save the data in data_frame into a csv file named "stocks_new.csv"
data_frame.to_csv('stocks_bs.csv', mode = 'a', header = True)