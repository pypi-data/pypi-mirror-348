import requests as rq 
from bs4 import BeautifulSoup as bs 


def USD():
    url = 'https://www.tgju.org/profile/price_dollar_rl'
    response = rq.get(url)
    soup = bs(response.text, 'html.parser')
    price = soup.find('span', {'data-col': 'info.last_trade.PDrCotVal'}).text
    if price:
        gh = str(price).replace(',', '')
        rial = int(gh) // 10
        return rial
    else:
        return 'Dollar price not found.'
    
    