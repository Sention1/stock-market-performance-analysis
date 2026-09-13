import schedule
import time
from pipeline import run_pipeline

schedule.every().monday.at("23:30").do(run_pipeline, "IBM")
schedule.every().monday.at("23:31").do(run_pipeline, "MSFT")
schedule.every().monday.at("23:32").do(run_pipeline, "SPY")

schedule.every().tuesday.at("23:30").do(run_pipeline, "IBM")
schedule.every().tuesday.at("23:31").do(run_pipeline, "MSFT")
schedule.every().tuesday.at("23:32").do(run_pipeline, "SPY")

schedule.every().wednesday.at("23:30").do(run_pipeline, "IBM")
schedule.every().wednesday.at("23:31").do(run_pipeline, "MSFT")
schedule.every().wednesday.at("23:32").do(run_pipeline, "SPY")

schedule.every().thursday.at("23:30").do(run_pipeline, "IBM")
schedule.every().thursday.at("23:31").do(run_pipeline, "MSFT")
schedule.every().thursday.at("23:32").do(run_pipeline, "SPY")

schedule.every().friday.at("23:30").do(run_pipeline, "IBM")
schedule.every().friday.at("23:31").do(run_pipeline, "MSFT")
schedule.every().friday.at("23:32").do(run_pipeline, "SPY")

while True:
    schedule.run_pending()
    time.sleep(60)