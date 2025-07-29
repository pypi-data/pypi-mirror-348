import requests as rq 
from bs4 import BeautifulSoup as bs 
from .currency import USD


def BTC(toman=True):
    """
    if toman is False, then BTC Price is in $
    """
    url = 'https://www.tgju.org/profile/crypto-bitcoin'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if toman:
            dollar_price = USD(toman=True)
            final_price = int(float(gh) * dollar_price)
            return int(final_price) // 10
        else:
            return int(gh)

    else:
        return 'BTC price not found.'