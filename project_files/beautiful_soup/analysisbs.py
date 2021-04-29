
import matplotlib.pyplot as plt
import pandas as pd

# load the data from the csv file. 
data = pd.read_csv("~/Desktop/Stock_Price_Scraping/output_fixtures/beautiful_soup/stocks_bs.csv") 

# select numeric variables for plotting
data = data.iloc[0:5,] # select the top 5 rows for readability. 
data1 = data["Previous Close"].to_list() # change the dataframe columns to lists
data2 = data["Open"].to_list()
data3 = data["PE Ratio (TTM)"].to_list()
data4 = data["EPS (TTM)"].to_list()
plt.close("all")

year=data["Symbols"].to_list()

fig,ax=plt.subplots(4,1,figsize=(10,8)) # the title on top
fig.suptitle('Stock market analysis', fontsize=16)
ax[0].bar(year,data1,color="red")
ax[0].legend(["Previous Close"])
ax[1].bar(year,data2,color="yellow")
ax[1].legend(["Open"])
ax[2].bar(year,data3,color="green")
ax[2].legend(["PE Ratio (TTM)"])
ax[3].bar(year,data4,color="green")
ax[3].legend(["EPS (TTM)"])
plt.show()
