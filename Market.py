import streamlit as st
import os
import re
from sklearn.linear_model import LinearRegression
from datetime import date
import yfinance as yf
import pandas as pd
import time as t
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
def AI(que='Hello MARKET.AI'):
    genai.configure(api_key=GOOGLE_API_KEY)
    st.success('listning....')
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(que)
    # print(f'{que}:>>> {response.text}') 
    return response.text
    
st.header('MARKET.AI')
st.sidebar.header('MARKET.AI')
st.sidebar.title("Avalible stock")


def question_recognizer(que=''):
   
    qur=st.text_input('Enter the prompt :')
    
    process_question(qur)
    

with st.spinner('in progress...'):
 t.sleep(5)

def process_question( DF_que=''):
    convert = re.sub('[^a-zA-Z]', ' ', DF_que).lower().split() 
    os.makedirs('csvfile', exist_ok=True) 
    i=1 
    for stock_name,stock_symbol in stock_name_list: 
        
        st. sidebar.write(f'{i}--{stock_name}')
        i+=1
    for stock_name in stock_name_dict:
        if  re.sub('[^a-zA-Z]', ' ', stock_name).lower() in convert:
            stock_symbol = stock_name_dict[stock_name]
            if 'close' in convert:
                return handle_close_operation(stock_name, stock_symbol)
            elif 'high' in convert:
                return handle_high_operation(stock_name, stock_symbol)
            elif 'low' in convert:
                return handle_low_operation(stock_name, stock_symbol)
            else:
                return st.success(AI(DF_que))
        
    else:
        if not DF_que:
          return st.success(AI())
        else:
            return st.success(AI(DF_que))
       
def  handle_close_operation(stock_name,stock_symbol):
    file_path = f'csvfile/{stock_name}NS_close.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if df['Date'].iloc[-1] == str(date.today()):
           
            close(df=train_data(stock_symbol),close='close',stock_name=stock_name)
            pass
        else:
            os.remove(file_path)
            st.warning('please update the data, try again')
            return handle_close_operation(stock_name=stock_name,stock_symbol=stock_symbol)
    else:
        st.warning('I dont have any data please insert..')
        high=st.number_input('Enter the high value:')
        low=st.number_input('Enter the low value:')
        open=st.number_input('Enter the open value:')
        volume=st.number_input('Enter the volume of the stock:')
        if st.button('Enter','enter'):
             value_crater(stock_name,operation='close',df=data_close(high=high,low=low,open=open,volume=volume))  
             process_question(f'{stock_name} close')
             return 0
        
def handle_high_operation(stock_name,stock_symbol):
    file_path = f'csvfile/{stock_name}NS_high.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if df['Date'].iloc[-1] == str(date.today()):
            
            hight(df=train_data(stock_symbol),hight='high',stock_name=stock_name)
            pass
        else:
            os.remove(file_path)
            st.warning('please update the data, try again')
            return handle_high_operation(stock_name=stock_name,stock_symbol=stock_symbol)
    else:
         st.warning('I dont have any data please insert..')
         close=st.number_input('Enter the close value:')
         low=st.number_input('Enter the low value:')
         open=st.number_input('Enter the open:')
         vol=st.number_input('Enter the volume: ')
         if st.button('Enter','enter'):
             value_crater(stock_name,operation='high',df=data_high(close=close,low=low,open=open,volume=vol))  
             process_question(f'{stock_name} high')
             return 0        
  
def handle_low_operation(stock_name,stock_symbol):
    file_path = f'csvfile/{stock_name}NS_low.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if df['Date'].iloc[-1] == str(date.today()):
            
            low(df=train_data(stock_symbol),low='low',stock_name=stock_name)    
        else:
            os.remove(file_path)
            st.warning('please update the data, try again')
            return handle_low_operation(stock_name=stock_name,stock_symbol=stock_symbol)
    else:
         st.warning('I dont have any data please insert..')
         close=st.number_input('Enter the close value:')
         high=st.number_input('Enter the high value:')
         open=st.number_input('Enter the open:')
         vol=st.number_input('Enter the volume: ')
         if st.button('Enter','enter'):
            #  close, high, open, volume
             value_crater(stock_name,operation='low',df=data_low(close=close,high=high,open=open,volume=vol))  
             process_question(f'{stock_name} low')
             return 0

stock_name_list  =[
    ('reliance', 'RELIANCE.NS'),
    ('TATASTEEL', 'TATASTEEL.NS'),
    ('TCS', 'TCS.NS'),
    ('SBI', 'SBI'),
    ('ITC', 'ITC.NS'),
    ('RivianAutomotive', 'RIVN'),
    ('HersHealth', 'HIMS'),
    ('NVIDIACorporation', 'NVDA'),
    ('HDFCBank ', 'HDFCBANK.NS'),
    ('CassavaSciences', 'SAVA'),
    ('TATAMOTORS', 'TATAMOTORS.NS'),
    ('TATAINVEST', 'TATAINVEST.BO'),
    ('TataAIA ', '0P0000NQJX.BO'),
    ('Lockheed', 'LMT'),
    ('AmericanBeacon', 'ADNIX'),
    ('GameStop', 'GME'),
    ('ICICIBank', 'IBN'),
    ('BandhanBanking', '0P000125VF.BO'),
    ('TheFederalBank', 'FEDERALBNK.NS'),
    ('KotakMahindraBank', 'KOTAKBANK.BO'),
    ('OLA', 'OLAELEC.NS'),
    ('JPP', 'JPPOWER.BO'),
    ('NCL ', 'NCLRESE.BO'),
    ('MTNL', 'MTNL.NS'),
    ('TataTeleservices', 'TTML.BO'),
    ('AngelOne', 'ANGELONE.NS'),
    ('Zomato', 'ZOMATO.NS'),
    ('Microsoft', 'MSFT'),
    ('google', 'GOOG'),
    ('SWIGGY', 'SWIGGY.NS'),
    ('Wipro', 'WIPRO.NS'),
    ('AdaniPower', 'ADANIPOWER.NS'),
    ('AdaniEnterprises', 'ADANIENT.NS'),
    ('LifeInsurance', 'LICI.NS'),
    ('HindustanUni', 'HINDUNILVR.NS'),
    ('LarsenToubro', 'LT.NS'),
    ('HCL', 'HCLTECH.NS'),
    ('Mahindra', 'M&M.NS'),
    ('NTPC', 'NTPC.NS'),
    ('MarutiSuzuki', 'MARUTI.BO'),
    ('UltraTechCement', 'UCLQF'),
    ('OilNaturalGas', 'ONGC.BO'),
    ('Siemens', 'SIEMENS.BO'),
    ('PricingCulture', 'CLTBWOWOM'),
    ('CoalIndia', 'COALINDIA.NS'),
    ('BajajAuto', 'BAJAJ-AUTO.BO'),
    ('Trent', 'TRENT.NS'),
    ('BharatElec', 'BEL.NS'),
    ('Hindustan', 'HINDZINC.BO'),
    ('Hindustan', 'HINDZINC.BO'),
    ('DLF', 'DLF.BO'),
    ('IndianRailway', 'IRFC.BO'),
    ('IndianOil', 'IOC.BO'),
    ('AdaniGreenEnergy', 'ADANIGREEN.NS'),
    ('GrasimIndustries', 'GRASIM.NS'),
    ('TechMahindra', 'TECHM.BO'),
    ('PowerFinanceCorporation', 'PFC.BO'),
    ('InterGlobeAviation', 'INDIGO.NS'),
    ('DivisLaboratories', 'DIVISLAB.BO'),
    ('Abbott', 'ABBOTINDIA.BO'),
    ('PidiliteIndustries', 'PIDILITIND.BO'),
    ('HindalcoIndustries', 'HINDALCO.NS'),
    ('EcoRecycling', 'ECORECO.BO'),
    ('HyundaiMotor', 'HYUNDAI.NS'),
    ('AmbujaCements', 'AMBUJACEM.BO'),
    ('GAIL(India)', 'GQI.F'),
    ('BankofBaroda.', 'BANKBARODA.NS'),
    ('MacrotecDevelopers', 'LODHA.NS'),
    ('EicherMotors', 'EICHERMOT.BO'),
    ('PunjabBank.', 'PNB.NS'),
    ('JSW', 'JSWHL.NS'),
    ('TataPower', 'TATAPOWER.NS'),
    ('IHCL', 'INDHOTEL.BO'),
    ('NTPC', 'NTPCGREEN.BO'),
    ('TVS ', 'TVSMOTOR.NS'),
    ('SHRIRAM ', 'SHRIRAMFIN.NS'),
    ('CGPower ', 'CGPOWER.NS'),
    ('Cipla ', 'CIPLA.NS'),
    ('Britannia ', 'BRITANNIA.BO'),
    ('Samvardhana  ', 'MOTHERSON.BO'),
    ('MaxHealth', 'MAXHEALTH.NS'),
    ('Godrej', 'GODREJCP.BO'),
    ('TorrentPharm', 'TORNTPHARM.BO'),
    ('POLYCAB', 'POLYCAB.NS'), 
    ('axisgold', 'AXISGOLD.NS'), 
]
stock_name_dict=dict(stock_name_list)
def train_data(stock_name='GOOG'):
    start = '2000-01-01'
    end = date.today()
    stock = stock_name
    data = yf.download(stock, start, end)
    # Check if 'Date' is in the columns, if not, assume it's the index
    if 'Date' not in data.columns:
        # If 'Date' is not a column, reset the index to make it a column
        data = data.reset_index() 
 
    # Now drop the 'Date' column
    data.drop('Date', axis=1,inplace=True)  
    return data

def close(df,close,stock_name):
     
    start_time = t.time() 
    df1=pd.read_csv(f'csvfile/{stock_name}NS_{close}.csv')
    # Drop the 'Date' column from df1
    df1.drop(columns=['Date'],axis=1, inplace=True)  
    # Convert 'Price' column to numeric, handling errors by coercing to NaN
    df1['Price'] = pd.to_numeric(df1['Price'], errors='coerce')
    df1 = df1.set_index('Price')
    s=df['Close'].tail(1)
    s=s.to_numpy()
    actual_price=s.tolist()

    x=df.drop( columns=['Close'],axis=1)
    print('hallow')
    y=df['Close']
    lr=LinearRegression()
    lr.fit(x,y)
    # Ensure df1 is a DataFrame with numeric values
    y_pred=lr.predict(df1)
    predected_price=  y_pred.tolist()
    end_time = t.time()
    processing_time = end_time - start_time
    st.success(f"Processing Time: {processing_time:.4f} seconds")


    return st.success(f"{AI(f'Hello AI its my actual price:{actual_price[0]} and its my predected price :{predected_price[0]} can you summerized the stock and can I bye or sale stock name is {stock_name}')}")

def hight(df, hight,stock_name):
   df1=pd.read_csv(f'csvfile/{stock_name}NS_{hight}.csv')

   df1.drop(columns=['Date'],axis=1, inplace=True)  
    # Convert 'Price' column to numeric, handling errors by coercing to NaN
   df1['Price'] = pd.to_numeric(df1['Price'], errors='coerce')
   df1 = df1.set_index('Price')
   s=df['High'].tail(1)
   s=s.to_numpy()
   actual_price=s.tolist()
   x=df.drop( columns=['High',],axis=1)
   y=df['High']
   lr=LinearRegression()
   lr.fit(x,y)
   y_pred=lr.predict(df1)
   predected_price=  y_pred.tolist()
   return st.success(f"{AI(f'Hello AI its my actual price:{actual_price[0]} and its my predected price :{predected_price[0]} can you summerized the stock and can I bye or sale stock name is {stock_name}')}")

def low(df,low,stock_name):
   df1=pd.read_csv(f'csvfile/{stock_name}NS_{low}.csv')
   df1.drop(columns=['Date'],axis=1, inplace=True)  
    # Convert 'Price' column to numeric, handling errors by coercing to NaN
   df1['Price'] = pd.to_numeric(df1['Price'], errors='coerce')
   df1 = df1.set_index('Price')
   s=df['Low'].tail(1)
   s=s.to_numpy()
   actual_price=s.tolist()
   x=df.drop( columns=['Low',],axis=1)
   y=df['Low']
   lr=LinearRegression()
   lr.fit(x,y)
   y_pred=lr.predict(df1)
   predected_price=  y_pred.tolist()
   return st.success(f"{AI(f'Hello AI its my actual price:{actual_price[0]} and its my predected price :{predected_price[0]} can you summerized the stock and can I bye or sale stock name is {stock_name}')}")


def data_close(high, low, open, volume):
    return pd.DataFrame({
        'Price': 0, 
        'High': high, 
        'Low': low, 
        'Open': open, 
        'Volume': volume, 
        'Date': date.today()
    },index=[0])

def data_high(close, low, open, volume):
    return pd.DataFrame({
        'Price': [0], 
        'Close': [close], 
        'Low': [low], 
        'Open': [open], 
        'Volume': [volume], 
        'Date': [date.today()]
    },index=[0])

def data_low(close, high, open, volume):
    return pd.DataFrame({
        'Price': [0], 
        'Close': [close], 
        'High': [high], 
        'Open': [open], 
        'Volume': [volume], 
        'Date': [date.today()]
    },index=[0])

def value_crater(stock_symbol, operation, df):
    # Save the data to CSV based on operation type
    file_path = f'csvfile/{stock_symbol}NS_{operation}.csv'
    df.to_csv(file_path, index=False)

question_recognizer()

