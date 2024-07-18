from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import os
from time import time
from time import sleep # amount of seconds it sleeps before running again
import seaborn as sns
import matplotlib.pyplot as plt

# df = pd.DataFrame()

def run_api():
    global df # declares it as global variable
    global df3
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'20', # can change this limit to see data easier
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '4ae4cf29-a671-4408-89cb-d7ca1a4d4835',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    
    df = pd.json_normalize(data['data']) 
    df['timestamp'] = pd.to_datetime('now') # shows exactly when it was last run to check if automation has worked
    df3 = df.groupby('name', sort=False)[[
                'quote.USD.percent_change_1h', 
                'quote.USD.percent_change_24h', 
                'quote.USD.percent_change_7d', 
                'quote.USD.percent_change_30d', 
                'quote.USD.percent_change_60d', 
                'quote.USD.percent_change_90d']].mean()
    df3 = df3.stack() # converts cols to rows for better visualisation
    
    # print(type(df2)) # checking type for series
    
    df3 = df3.to_frame(name= 'averages') # converts to df with the name averages
    
    # print(type(df2)) # checking type for df
    
    df3 = df3.reset_index(drop=False) # adds unique index for each row
    
    # print("Index added")
    
    # print(df2.columns.tolist())     to find column names to check if need to rename 
    
    df3 = df3.rename(columns={'level_1': 'percentage change'})
    
    # print(df2.columns.tolist()) 
    
    df3['percentage change'] = df3['percentage change'].replace(['quote.USD.percent_change_1h',
                                                                 'quote.USD.percent_change_24h',
                                                                  'quote.USD.percent_change_7d',
                                                                  'quote.USD.percent_change_30d',
                                                                  'quote.USD.percent_change_60d',
                                                                  'quote.USD.percent_change_90d'],
                                                                ['1h', '24h', '7d', '30d', '60d', '90d'])
    
    if not os.path.isfile('coinmarketapi2.csv'):
        df.to_csv('coinmarketapi2.csv', header='column_names')
    else:
        df.to_csv('coinmarketapi2.csv', mode='a', header=False) # appending new data every minute to csv file

    # if not os.path.isfile('coinmarketapi2_agg.csv'):
    #     df2.to_csv('coinmarketapi2_agg.csv', header='column_names')
    # else:
    #     df2.to_csv('coinmarketapi2_agg.csv', mode='a', header=False) # appending new data every minute to csv file 
        
    if not os.path.isfile('coinmarketapi3_agg.csv'):
        df3.to_csv('coinmarketapi3_agg.csv', header='column_names')
    else:
        df3.to_csv('coinmarketapi3_agg.csv', mode='a', header=False) # appending new data every minute to csv file     
         

for i in range(2): # testing, up to 333 data retrievals per day
    run_api()
    print('API ran successfully')
    sleep(5)
#exit() 

sns.catplot(x='percentage change', y='averages', data=df3, hue='name', kind='point')
plt.show() 
print("Graph plotted successfully")

exit()