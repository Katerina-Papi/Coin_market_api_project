from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import os
from time import time
from time import sleep # amount of seconds it sleeps before running again

df = pd.DataFrame()

def run_api():
    global df # declares it as global variable
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
    df = df.map(lambda x: '{:.5f}'.format(x) if isinstance(x, (float)) else x)
    df['timestamp'] = pd.to_datetime('now') # shows exactly when it was last run to check if automation has worked
    
    
    if not os.path.isfile('coinmarketapi2.csv'):
        df.to_csv('coinmarketapi2.csv', header='column_names')
    else:
        df.to_csv('coinmarketapi2.csv', mode='a', header=False) # appending new data every minute to csv file
           

for i in range(3): # testing with 3 api retrievals over 3 minutes
    run_api()
    print('API ran successfully')
    sleep(60)
exit() 
