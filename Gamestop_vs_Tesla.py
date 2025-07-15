#!/usr/bin/env python
# coding: utf-8

# In[1]:


# INSTALL REQUIRED LIBRARIES
get_ipython().system('pip install yfinance')
get_ipython().system('pip install beautifulsoup4')
get_ipython().system('pip install lxml')
get_ipython().system('pip install plotly')


# In[3]:


# IMPORTS
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go


# In[5]:


tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
tesla_data.head()


# In[7]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
headers = {"User-Agent": "Mozilla/5.0"}
html_data = requests.get(url, headers=headers).text
soup = BeautifulSoup(html_data, "html.parser")
tables = soup.find_all("table")

for table in tables:
    if "Tesla Quarterly Revenue" in str(table):
        tesla_revenue = pd.read_html(str(table))[0]
        break

tesla_revenue.columns = ["Date", "Revenue"]
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].replace(r"[\$,]", "", regex=True)
tesla_revenue.dropna(inplace=True)
tesla_revenue.tail()


# In[9]:


gamestop = yf.Ticker("GME")
gme_data = gamestop.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.head()


# In[11]:


url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
headers = {"User-Agent": "Mozilla/5.0"}
html_data = requests.get(url, headers=headers).text
soup = BeautifulSoup(html_data, "html.parser")
tables = soup.find_all("table")

for table in tables:
    if "GameStop Quarterly Revenue" in str(table):
        gme_revenue = pd.read_html(str(table))[0]
        break

gme_revenue.columns = ["Date", "Revenue"]
gme_revenue["Revenue"] = gme_revenue["Revenue"].replace(r"[\$,]", "", regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue.tail()


# In[13]:


fig = go.Figure()
fig.add_trace(go.Scatter(x=tesla_data['Date'], y=tesla_data['Close'], name='Stock Price'))
fig.update_layout(title='Tesla Stock Price Over Time', xaxis_title='Date', yaxis_title='Price (USD)')
fig.show()


# In[17]:


fig = go.Figure()
fig.add_trace(go.Scatter(x=gme_data['Date'], y=gme_data['Close'], name='Stock Price'))
fig.update_layout(title='GameStop Stock Price Over Time', xaxis_title='Date', yaxis_title='Price (USD)')
fig.show()


# In[19]:


fig = go.Figure()
fig.add_trace(go.Scatter(x=tesla_data['Date'], y=tesla_data['Close'], name='Stock Price'))
fig.add_trace(go.Scatter(x=tesla_revenue['Date'], y=tesla_revenue['Revenue'].astype(float), name='Revenue'))
fig.update_layout(title='Tesla: Stock Price vs Revenue', xaxis_title='Date', yaxis_title='USD')
fig.show()


# In[ ]:




