#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 3.05.2021 - 18:33

@author: Tesfahun Tegene Boshe
"""
"""
- import the necessary libraries
- matplotlib for plotting and 
- pandas for handling the dataframe
"""
import matplotlib.pyplot as plt
import pandas as pd

# load the data from the csv file. 
# This is the output file after running bs.py

# put the correct url
data = pd.read_csv("stocks_bs.csv") 

"""
- The aim here is to demonestrate that the data scraped can be useful for further steps
- select the top 5 rows for readability of the graphs.
- selecting numeric variables for plotting
- convert each column to a list
"""

data = data.iloc[0:5, ]

data1 = data["Previous Close"].to_list()
data2 = data["Open"].to_list()
data3 = data["PE Ratio (TTM)"].to_list()
data4 = data["EPS (TTM)"].to_list()

# close all plots currently open
plt.close("all")

# symbols will be on the x-axis. 
symbol = data["Symbols"].to_list()

# 4 subplots with size 10X8
fig, ax = plt.subplots(4, 1, figsize=(10, 8))

# the title on top
fig.suptitle('Stock market analysis', fontsize=16)

# bar graph 1
ax[0].bar(symbol, data1, color="red")
ax[0].legend(["Previous Close"])

# bar graph 2
ax[1].bar(symbol, data2, color="yellow")
ax[1].legend(["Open"])

# bar graph 3
ax[2].bar(symbol, data3, color="green")
ax[2].legend(["PE Ratio (TTM)"])

# bar graph 4
ax[3].bar(symbol, data4, color="green")
ax[3].legend(["EPS (TTM)"])

# show the plot
plt.show()

data.info()

#Calculating sample statistics of all columns including float values
data.describe()

#Plotting box plots
df = pd.DataFrame(data,columns=['Previous Close', 'Open', '1y Target Est'])
df.plot.box()

df = pd.DataFrame(data,columns=['Beta (5Y Monthly)'])
df.boxplot()

df = pd.DataFrame(data,columns=['Beta (5Y Monthly)'])
df.boxplot()
