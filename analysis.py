import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
db_password = os.getenv("DB_PASSWORD")
engine = create_engine(f"postgresql://postgres:{db_password}@localhost:5432/postgres")



#What date range does this dataset cover, from earliest to most recent trading day?
query1= ("""
    SELECT MIN("date") AS first_date, MAX("date") AS latest_date
    FROM stock_prices
""")
result = pd.read_sql(query1, engine)
print(result)



#What was each symbol's average closing price per week?
query2= ("""
    SELECT symbol,AVG(close) AS avg_closing_price, DATE_TRUNC('week', date) AS weekly
    FROM stock_prices
    GROUP BY symbol,DATE_TRUNC('week', date)
    ORDER BY weekly, symbol
""")
result = pd.read_sql(query2, engine)
print(result)







#What is each symbol's 5-day rolling average closing price, calculated separately per symbol?
query3= ("""
    SELECT symbol, date, close,
        AVG(close) OVER (PARTITION BY symbol ORDER BY date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS rolling_avg_5
    FROM stock_prices
""")
result = pd.read_sql(query3, engine)
print(result)




#What was each symbol's total percentage return, comparing its first closing price to its last?
query4= ("""
WITH symbol_prices AS (
    SELECT DISTINCT symbol,
        FIRST_VALUE(close) OVER (PARTITION BY symbol ORDER BY date) AS first_close,
        LAST_VALUE(close) OVER (
            PARTITION BY symbol ORDER BY date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS last_close
    FROM stock_prices
)

SELECT symbol, first_close, last_close,
    ROUND(((last_close - first_close) / first_close * 100)::numeric, 2) AS total_return_pct
FROM symbol_prices
ORDER BY total_return_pct DESC
""")
result = pd.read_sql(query4, engine)
print(result)



#Which symbol had the single best one-day percentage gain, and on what date?
query5= ("""
    SELECT symbol, date,
        ROUND(((close - open) / open * 100)::numeric, 2) AS best_percentage
    FROM stock_prices
    ORDER BY best_percentage DESC
    LIMIT 1
""")
result = pd.read_sql(query5, engine)
print(result)



#What percentage of days did each symbol's closing price finish above its own 5-day moving average?
query6= ("""
    SELECT symbol,
        ROUND(
            100.0 * SUM(CASE WHEN close > moving_avg THEN 1 ELSE 0 END) / COUNT(moving_avg),2) AS pct_days_up
    FROM stock_prices
    WHERE moving_avg IS NOT NULL
    GROUP BY symbol
    ORDER BY pct_days_up DESC
""")
result = pd.read_sql(query6, engine)
print(result)





#What was each symbol's average daily volatility (high-low range as a percentage of the opening price)?
query7= ("""
    WITH daily_average_volatility AS(
        SELECT symbol,
            ROUND(((high - low) / open * 100)::numeric, 2) AS daily_percentage
        FROM stock_prices
    )
        SELECT symbol,
            AVG(daily_percentage) AS avg_daily_percentage
        FROM daily_average_volatility
        GROUP BY symbol
        ORDER BY avg_daily_percentage DESC
""")
result = pd.read_sql(query7, engine)
print(result)





query9 = """
SELECT
    symbol,
    date,
    open,
    close,
    daily_change
FROM stock_prices
ORDER BY date DESC
LIMIT 10;
"""

result = pd.read_sql(query9, engine)
print(result)


query10 = """
SELECT
    symbol,
    date,
    close,
    moving_avg
FROM stock_prices
WHERE symbol = 'IBM'
ORDER BY date DESC
LIMIT 10;
"""

result = pd.read_sql(query10, engine)
print(result)


