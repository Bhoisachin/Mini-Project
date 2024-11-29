import streamlit as st
import os
import re
from sklearn.linear_model import LinearRegression
from datetime import date
import yfinance as yf
import pandas as pd
import time as t
import google.generativeai as genai
genai.configure(api_key="Enter your API KEY")
st.header('MARKET.AI')
def AI(que='Hello MARKET.AI'):
    st.success('listning....')
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(que)
    return response.text

def question_recognizer(qur=st.text_input('enter the prompe')):
    
    process_question(qur)

with st.spinner('in progress...'):
 t.sleep(5)

def process_question( DF_que=''):
    convert = re.sub('[^a-zA-Z]', ' ', DF_que).lower().split() 
    os.makedirs('csvfile', exist_ok=True)   
    for stock_name, stock_symbol in stock_name_list:
        if re.sub('[^a-zA-Z]', ' ', stock_name).lower() in convert:
            if 'close' in convert:
                return handle_close_operation(stock_name=stock_name,stock_symbol=stock_symbol)
            elif 'high' in convert:
                return handle_high_operation( stock_name=stock_name, stock_symbol=stock_symbol)
            elif 'low' in convert:
                return handle_low_operation(stock_name=stock_name,stock_symbol= stock_symbol)
            else:
                return st.warning(' opration is not found')
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
            st.warning('please update the data')
            return handle_close_operation(stock_name=stock_name,stock_symbol=stock_symbol)
    else:
        high=st.number_input('enter the high value')
        low=st.number_input('enter the low value')
        open=st.number_input('enter the open value')
        volume=st.number_input('enter the volume of the stock')
        if st.button('Enter','enter'):
             value_crater(stock_name,operation='close',df=data_close(high=high,low=low,open=open,volume=volume))  
             question_recognizer(qur=f'{stock_name} {stock_symbol}')
             return 0
        
def handle_high_operation(stock_name,stock_symbol):
    file_path = f'csvfile/{stock_name}NS_high.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if df['Date'].iloc[-1] == str(date.today()):
            print('present sir...')
            hight(df=train_data(stock_symbol),hight='high',stock_name=stock_name)
            pass
        else:
            os.remove(file_path)
            st.warning('please update the data')
            return handle_high_operation(stock_name=stock_name,stock_symbol=stock_symbol)
    else:
         close=st.number_input('enter the close value')
         low=st.number_input('enter the low value')
         open=st.number_input('enter the open')
         vol=st.number_input('enter the volume ')
         if st.button('Enter','enter'):
             value_crater(stock_name,operation='high',df=data_high(close=close,low=low,open=open,volume=vol))  
             question_recognizer(qur=f'{stock_name} {stock_symbol}')
             return 0        
  
def handle_low_operation(stock_name,stock_symbol):
    file_path = f'csvfile/{stock_name}NS_low.csv'
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if df['Date'].iloc[-1] == str(date.today()):
            print('present sir...')
            low(df=train_data(stock_symbol),low='low',stock_name=stock_name)    
        else:
            os.remove(file_path)
            st.warning('please update the data')
            return handle_low_operation(stock_name=stock_name,stock_symbol=stock_symbol)
    else:
         close=st.number_input('enter the close value')
         high=st.number_input('enter the high value')
         open=st.number_input('enter the open')
         vol=st.number_input('enter the volume ')
         if st.button('Enter','enter'):
            #  close, high, open, volume
             value_crater(stock_name,operation='low',df=data_low(close=close,high=high,open=open,volume=vol))  
             question_recognizer(qur=f'{stock_name} {stock_symbol}')
             return 0

stock_name_list = [
    # Add your stock names and symbols here
    # Example: ('Tata', 'TATASTEEL'), 
    ('reliance', 'RELIANCE'),
    ('tata', 'TATASTEEL.NS'),
    ('tataconsultancy', 'TCS.NS'),
    ('state bank of india', 'SBI'),
    ('ITC', 'ITC.NS'),
]
def train_data(stock_name='GOOG'):
    start = '2012-01-01'
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
    df1=pd.read_csv(f'csvfile/{stock_name}NS_{close}.csv')
    # Drop the 'Date' column from df1
    df1.drop(columns=['Date'],axis=1, inplace=True)  
    # Convert 'Price' column to numeric, handling errors by coercing to NaN
    df1['Price'] = pd.to_numeric(df1['Price'], errors='coerce')
    df1 = df1.set_index('Price')
    s=df['Close'].tail(1)
    s=s.to_numpy()
    actual_price=s.tolist()

    x=df.drop( columns=['Close','Adj Close'],axis=1)
    y=df['Close']
    lr=LinearRegression()
    lr.fit(x,y)
    # Ensure df1 is a DataFrame with numeric values
    y_pred=lr.predict(df1)
    predected_price=  y_pred.tolist()

    
    
    return st.success(f"{AI(f'hallow ai it my actual price:{actual_price} and it my predected price :{predected_price} can you sumraized the stock can i bye or sale stock nema is {stock_name}')}  predected price:{predected_price}")

def hight(df, hight,stock_name):
   df1=pd.read_csv(f'csvfile/{stock_name}NS_{hight}.csv')

   df1.drop(columns=['Date'],axis=1, inplace=True)  
    # Convert 'Price' column to numeric, handling errors by coercing to NaN
   df1['Price'] = pd.to_numeric(df1['Price'], errors='coerce')
   df1 = df1.set_index('Price')
   s=df['High'].tail(1)
   s=s.to_numpy()
   actual_price=s.tolist()
   x=df.drop( columns=['High','Adj Close'],axis=1)
   y=df['High']
   lr=LinearRegression()
   lr.fit(x,y)
   y_pred=lr.predict(df1)
   predected_price=  y_pred.tolist()
   return st.success(f"{AI(f'hallow ai it my actual price:{actual_price} and it my predected price :{predected_price} can you sumraized the stock can i bye or sale stock nema is {stock_name}')}  predected price:{predected_price}")

def low(df,low,stock_name):
   df1=pd.read_csv(f'csvfile/{stock_name}NS_{low}.csv')
   df1.drop(columns=['Date'],axis=1, inplace=True)  
    # Convert 'Price' column to numeric, handling errors by coercing to NaN
   df1['Price'] = pd.to_numeric(df1['Price'], errors='coerce')
   df1 = df1.set_index('Price')
   s=df['Low'].tail(1)
   s=s.to_numpy()
   actual_price=s.tolist()
   x=df.drop( columns=['Low','Adj Close'],axis=1)
   y=df['Low']
   lr=LinearRegression()
   lr.fit(x,y)
   y_pred=lr.predict(df1)
   predected_price=  y_pred.tolist()
   return st.success(f"{AI(f'hallow ai it my actual price:{actual_price} and it my predected price :{predected_price} can you sumraized the stock can i bye or sale stock nema is {stock_name}')}  predected price:{predected_price}")


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
