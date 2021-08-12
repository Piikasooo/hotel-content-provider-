from openexchangerate import OpenExchangeRates
import csv
import os.path
import datetime
import time


client = OpenExchangeRates(api_key="6ff8323a7eed443693dd7d6bfbe2490b")


def now_currency():
    all_currency = client.latest()
    current_currency = all_currency[0]
    date_name_file = "currency/" + str(datetime.date.today()) + ".csv"
    print("GET-VALUE" + " " + str(datetime.datetime.now()))
    with open(date_name_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in current_currency.items():
            writer.writerow(row)


def get_currency(date_today, currency_name):
    date_name_need = "currency/" + str(date_today) + ".csv"
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


if __name__ == '__main__':
        start_server()
