import datetime

from openexchange.currency_api import get_currency


def convert_currency(price_uah, request):
    if not request.data.get("currency"):
        uah = price_uah
        return uah
    else:
        currency_uah = "UAH"
        date_need = datetime.date.today()
        currency_usd_uah = get_currency(date_need, currency_uah)
        price_in_usd = float(price_uah) / currency_usd_uah
        if request.data.get("currency") == "USD":
            return price_in_usd
        else:
            currency_name = request.data.get("currency")
            currency_name_usd = get_currency(date_need, currency_name)
            price_in_name_currency = price_in_usd * currency_name_usd
            return price_in_name_currency
