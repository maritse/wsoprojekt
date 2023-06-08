import schedule
import time
from logic import run_turn

# run function every 24h at 1 am
schedule.every().day.at("01:00").do(run_turn, "The job is starting")

while True:
    schedule.run_pending()
    time.sleep(60)
