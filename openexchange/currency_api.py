import csv
import datetime
import os.path
import time
from environs import Env
from openexchangerate import OpenExchangeRates


env = Env()
env.read_env()

client = OpenExchangeRates(api_key=env.str('API_KEY'))


def now_currency():
    all_currency = client.latest()
    current_currency = all_currency[0]
    date_name_file = "currency/" + str(datetime.date.today()) + ".csv"
    print("GET-VALUE" + " " + str(datetime.datetime.now()))
    with open(date_name_file, "w", newline="") as csv_file:
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


def start_server():
    while True:
        date_name = "currency/" + str(datetime.date.today()) + ".csv"
        if not os.path.exists(date_name):
            now_currency()
        else:
            print("EXIST" + " " + str(datetime.datetime.now()))
            time.sleep(3600)


if __name__ == "__main__":
    start_server()