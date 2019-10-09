
import requests,json
from pandas_datareader import data
from datetime import datetime, timedelta

def get_ticker(arr):
    us={'symbol':''}
    bol=True
    for i in arr:
        if i['exchDisp']=='NSE' or i['exchDisp']=='Bombay':
            return i
        if (i['exchDisp']=='NASDAQ' and bol==True) or (i['exchDisp']=='NYSE' and bol==True):
            us=i
            bol=False
    if len(us['symbol'])>0:
        return us
    return arr[0]

lol=input("Enter name of stock you want to get info of:")
lol=lol.replace('&',' and ')
URL='http://d.yimg.com/aq/autoc?query='+lol+'&region=IN&lang=en-UK&callback=YAHOO.Finance.SymbolSuggest.ssCallback'
    
page = requests.post(URL)
cop=page.text[39:-2]
k=json.loads(cop)
if (k['ResultSet']['Result']==[]):
    print("Sorry, unable to fetch results")
else:
    love=get_ticker(k['ResultSet']['Result'])
    sym=love['symbol']
    name=love['name']
    today=datetime.now()
    i=1
    start_date=datetime.strftime(today-timedelta(i),'%Y-%m-%d')
    end_date=today.strftime('%Y-%m-%d')
    panel_data = data.DataReader('^NSEI', 'yahoo', start_date, end_date)
    while panel_data.shape[0]!=3:
        i+=1
        start_date=datetime.strftime(today-timedelta(i),'%Y-%m-%d')
        panel_data = data.DataReader(sym, 'yahoo', start_date, end_date)
        
    a,b,c=panel_data['Close'].to_list()
    a,b=b,c
    print(" ")
    print(name+' ('+sym+')')
    print(love['exchDisp'])
    vat=str(round((b-a)*100/a,2))+'%'
    print(round(b,2),end=' (')
    print(vat,end=')\n')
    print(' ')