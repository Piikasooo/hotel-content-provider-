'''
import csv
from openexchangerate import OpenExchangeRates
import os.path
from datetime import datetime


file_path = "D:\info.csv"
client = OpenExchangeRates(api_key="6ff8323a7eed443693dd7d6bfbe2490b")
FILENAME = "users.csv"
FILE = "user.csv"


my_dir = 'C:\\'
file_name = 'test.txt'
fname = os.path.join(my_dir, file_name)
file_example = open(fname,'w')

users = [
    ["Tom", 28],
    ["Alice", 23],
    ["Bob", 34]
]

with open(FILENAME, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(users)

with open(FILENAME, "a", newline="") as file:
    user = ["Sam", 31]
    writer = csv.writer(file)
    writer.writerow(user)

with open(FILE, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(users)

with open(file_path, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(users)


if os.path.exists('user.csv'):
    print("EXIST")
    print(datetime.today().date())

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
sched = BackgroundScheduler()
'''

from openexchangerate import OpenExchangeRates
import csv
import os.path
import datetime
import time


client = OpenExchangeRates(api_key="6ff8323a7eed443693dd7d6bfbe2490b")


def now_currency():
    all_currency = client.latest()
    current_currency = all_currency[0]
    date_name_file = "openexchange/currency/" + str(datetime.date.today()) + ".csv"
    print("GET-VALUE")
    with open(date_name_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in current_currency.items():
            writer.writerow(row)


def get_currency(date_today, currency_name):
    date_name_need = "openexchange/currency/" + str(date_today) + ".csv"
    with open(date_name_need, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == currency_name:
                return float(row[1])
        return "None currency_name"

'''
def start_shred():
    print('HELPPPPPPPPPPPPPPPPPPPPPPPP')
    date_name = str(datetime.date.today()) + ".csv"
    if not os.path.exists(date_name):
        sched.add_job(now_currency, "date", run_date=datetime.date.today() + datetime.timedelta(days=1))
        sched.start()


sched_block = BackgroundScheduler()
sched_block.add_job(now_currency, 'interval', seconds=8)
'''


def start_server():
    while True:
        date_name = "openexchange/currency/" + str(datetime.date.today()) + ".csv"
        if not os.path.exists(date_name):
            now_currency()
        else:
            print("EXIST")
            time.sleep(3600)



'''
# Here, you can generate your needed days
dates = ["2017-09-08 13:30:20", "2017-09-08 13:31:20", "2017-09-08 13:32:20"]
sched = BackgroundScheduler()

for date in dates:
    sched.add_job(job_function, "date", next_run_time=date)

sched.start()


def currency():
    print('HELLOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')
'''