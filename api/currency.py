from openexchangerate import OpenExchangeRates


client = OpenExchangeRates(api_key="6ff8323a7eed443693dd7d6bfbe2490b")


def currency(price_uah, request):
    if not request.data.get("currency"):
        uah = price_uah
        return uah
    elif request.data.get("currency") == "USD":
        all_currency = client.latest()
        uah = float(all_currency[0]['UAH'])
        price_in_usd = float(price_uah) / uah
        return price_in_usd
    elif request.data.get("currency") == "EUR":
        pass
    else:
        return price_uah