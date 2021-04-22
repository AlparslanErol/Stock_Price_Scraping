
import matplotlib.pyplot as plt
import pandas as pd
# import numpy


data = pd.read_csv("~/Desktop/Stock_Price_Scraping/stocks_new.csv") 
# print(data.head())

# fig = plt.figure()
# ax = fig.add_axes([0,0,1,1])


# data.iloc[:,4].plot.bar(); 


# fig = plt.figure()
# ax = fig.add_axes([0,0,1,1])
# ax.bar(data[::1],data[::4])
# plt.show(block=True)


# data1 = data.sort_values("Price")
# # f = plt.figure(1)
# data1.plot(x ='Symbols', y=['Price'], kind = 'bar')
# plt.show(block=True) 


# data2 = data.sort_values("Change")
# # g = plt.figure(2)
# data2.plot(x ='Symbols', y=['Change'], kind = 'bar')
# plt.show(block=True) 




# data3 = data.sort_values("Price")

# data3.plot(x ='Symbols', y=['Price','Change'], kind = 'bar')
# plt.show(block=True) 
# data1 = data.sort_values("Price")
# data2 = data.sort_values("Change")
# fig, axs = plt.subplots(2)
# fig.suptitle('Stock Exchange Analysis')
# axs[0].plot(x ='Symbols', y=['Price'], kind = 'bar')
# axs[1].plot(x ='Symbols', y=['Change'], kind = 'bar')
# plt.show(block=True) 


# fig, (ax1, ax2) = plt.subplots(2, sharex=True)
# fig.suptitle('Aligning x-axis using sharex')
# ax1.plot(data1.iloc[:,1], data1.iloc[:,3], kind = 'bar')
# ax2.plot(data2.iloc[:,1], data1.iloc[:,4], kind = 'bar')
# plt.show(block=True) 

# dat = data[['Price','Change']]
# axes = dat.plot(kind='bar',rot=0,lw=2,colormap='jet',
#              title='Stock Exchange Analysis', subplots=True, layout=(2,1))

# plt.show() 


data1 = data.sort_values("Previous Close")
data2 = data.sort_values("Open")

ax1 = plt.subplot(311)
data1.plot(x ='Symbols', y=['Previous Close'], kind = 'bar')
plt.show(block=True)
data2.plot(x ='Symbols', y=['Open'], kind = 'bar')
plt.show(block=True)