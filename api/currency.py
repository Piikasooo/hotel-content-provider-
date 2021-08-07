import requests
from bs4 import BeautifulSoup

UAH_USD = 'https://www.google.com/search?q=%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0+%D0%BA+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D1%83&sxsrf=ALeKk01HqsqbrdcNX0hqL3aDk-_zMJEV3w%3A1628240964618&ei=RPwMYf34JJ6A9u8PnKqD8AI&oq=%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0+%D0%BA+&gs_lcp=Cgdnd3Mtd2l6EAMYADILCAAQgAQQsQMQgwEyBQgAEMsBMgUIABCABDIFCAAQywEyBQgAEIAEMgUIABDLATIFCAAQgAQyBQgAEMsBMgUIABDLATIFCAAQywE6BwgjEOoCECc6BAgjECc6BAgAEEM6CwguEIAEEMcBEK8BOggIABCxAxCDAToKCAAQsQMQgwEQQzoICAAQgAQQsQM6BwgAELEDEENKBAhBGABQ_6QCWMq4AmC4yAJoAXACeACAAfEBiAHfC5IBBTAuOS4xmAEAoAEBsAEKwAEB&sclient=gws-wiz'
UAH_EUR = 'https://www.google.com/search?q=%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0+%D0%BA+%D0%B5%D0%B2%D1%80%D0%BE&sxsrf=ALeKk00MXmbE8WaKg4mGRS5tu31qePM0BQ%3A1628243198340&ei=_gQNYdmGFI397_UPtLOk6AE&oq=%D0%B3%D1%80%D0%B8%D0%B2%D0%BD%D0%B0+%D0%BA+%D0%B5&gs_lcp=Cgdnd3Mtd2l6EAMYADIFCAAQgAQyBQgAEMsBMgUIABDLATIFCAAQywEyBQgAEMsBMgcIABAKEMsBMgUIABDLATIFCAAQywEyCAgAEMkDEMsBMgUIABCABDoECAAQRzoECCMQJzoLCAAQgAQQsQMQgwE6EQguEIAEELEDEIMBEMcBENEDOgkIIxAnEEYQggI6BAgAEEM6CwguEIAEELEDEIMBOggILhCxAxCDAToICAAQsQMQgwE6CAguEIAEELEDSgQIQRgAUOIYWIU3YNVCaAFwA3gBgAGmAogBgg-SAQYwLjEwLjKYAQCgAQGwAQfIAQfAAQE&sclient=gws-wiz'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}


def convert_to(currency):

    if currency == "USD":
        UAH_USD_page = requests.get(UAH_USD, headers=headers)
        soup_usd = BeautifulSoup(UAH_USD_page.content, 'html.parser')
        convert = soup_usd.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 3})
        usd = convert[0].text
        return usd

    if currency == "EUR":
        UAH_EUR_page = requests.get(UAH_EUR, headers=headers)
        soup_eur = BeautifulSoup(UAH_EUR_page.content, 'html.parser')
        convert = soup_eur.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 3})
        eur = float(convert[0].text)
        return eur
