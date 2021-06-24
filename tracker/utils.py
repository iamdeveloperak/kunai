from bs4 import BeautifulSoup
import requests
# from urllib.request import urlopen
from django.conf import settings
# Windows 10 with Google Chrome
user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '\
'Safari/537.36'

headers = { 'User-Agent': user_agent_desktop}

def getproduct(url):
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, 'lxml')
    print(soup)
    price = 0
    deal_price = 0
    title = soup.find('span',attrs={'id':'productTitle'}).text.strip()
    availability = ''
    if type(soup.find('div',attrs={'id':'availability'})) != type(None):
        availability = soup.find('div',attrs={'id':'availability'}).text.strip()
        if availability.find('Currently unavailable') != -1:
            availability = 'unavailable'
            price = 0
        elif availability.find('Available from these sellers.') != -1:
            availability = 'unavailable'
            price = 0
        elif availability == '':
            availability = 'unavailable'
            price = 0
        else:
            availability = availability.rstrip('.')
            # print('---price type: ', type(soup.find('span',attrs={'id':'priceblock_saleprice'})))
            if type(soup.find('span',attrs={'id':'priceblock_saleprice'})) != type(None):
                price = float(soup.find('span',attrs={'id':'priceblock_saleprice'}).text.strip().replace(',','')[2:])
            else:
                if type(soup.find('span',attrs={'id':'priceblock_ourprice'})) != type(None):
                    price = float(soup.find('span',attrs={'id':'priceblock_ourprice'}).text.strip().replace(',','')[2:])
                else:
                    price = 0

            if  type(soup.find('span',attrs={'id':'priceblock_dealprice'})) != type(None):
                deal_price = float(soup.find('span',attrs={'id':'priceblock_dealprice'}).text.strip().replace(',','')[2:])
            else:
                deal_price = 0
    else:
        availability = 'In Stock'
        price = float(soup.find('span',attrs={'id':'priceblock_ourprice'}).text.strip().replace(' ','').replace(',','').split('-')[1][2:])

    print('----availability: ',availability)
    print('----price: ',price)

    image_url = soup.find('img',attrs={'id':'landingImage'})['data-old-hires']
    if image_url == '':
        image_url = soup.find('img',attrs={'id':'landingImage'})['src']

    image_name = image_url.split('/')[-1]
    product = {
        'url' : url,
        'title' : title,
        'availability': availability,
        'price' : price,
        'deal_price' : deal_price,
        'image_url' : image_url,
        'image_name' : image_name,
    }
    return product
