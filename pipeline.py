import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
db_password = os.getenv("DB_PASSWORD")
engine = create_engine(f"postgresql://postgres:{db_password}@localhost:5432/postgres")



def run_pipeline(symbol):
    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    response = requests.get(url)
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    print(response.status_code)

    data = response.json()

    if 'Time Series (Daily)' not in data:
        print(f"{symbol}: API response error")
        print(data)
        return

    daily_data = data['Time Series (Daily)']

    df = pd.DataFrame.from_dict(daily_data, orient='index')
    df.index = pd.to_datetime(df.index, errors='coerce')
    df.columns = ['open', 'high', 'low', 'close', 'volume']

    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['symbol'] = symbol
    df['daily_change'] = (df['close'] - df['open']) / df['open']
    df = df.sort_index(ascending=True)
    df['moving_avg'] = df['close'].rolling(window=5).mean()


    existing = pd.read_sql(f"SELECT date FROM stock_prices WHERE symbol = '{symbol}'", engine)
    existing_dates = pd.to_datetime(existing['date'])

    new_rows = df[~df.index.isin(existing_dates)]
    new_rows.to_sql('stock_prices', engine, if_exists='append', index=True, index_label='date')

    print(f"{symbol}: Added {len(new_rows)} new rows")
