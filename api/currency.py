from openexchange.currency_api import get_currency
import datetime


def convert_currency(price_uah, request):
    if not request.data.get("currency"):
        uah = price_uah
        return uah
    elif request.data.get("currency") == "USD":
        currency_name = "UAH"
        date_need = datetime.date.today()
        currency_usd_uah = get_currency(date_need, currency_name)
        price_in_usd = float(price_uah) / currency_usd_uah
        return price_in_usd
    elif request.data.get("currency") == "EUR":
        pass
    else:
        return price_uah