import requests as rq 
from bs4 import BeautifulSoup as bs 


def USD(toman=True):
    url = 'https://www.tgju.org/profile/price_dollar_rl'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if toman:
            toman = int(gh) // 10
            return toman
        else:
            return int(gh)

    else:
        return 'Dollar price not found.'

def GBP(toman=True):
    url = 'https://www.tgju.org/profile/price_gbp'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        if toman:
            toman = int(gh) // 10
            return toman
        else:
            return int(gh)
    else:
        return 'Pound price not found.'    
    