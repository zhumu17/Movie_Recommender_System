from bs4 import BeautifulSoup
import requests
import re

def getPriceAmazon(itemName):
    query = itemName
    url = "https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Dinstant-video&field-keywords=" + query
    resp = requests.get(url)
    html_data = resp.text
    soup = BeautifulSoup(html_data, 'html.parser')
    numScrape = 3
    tags = soup.find_all(attrs={'class':'a-offscreen'}, limit=numScrape)
    if not tags:
        price = 'Not Found'
        return price
    print(tags)
    priceTag = str(tags[0])
    # print(priceTag)
    # print(type(priceTag))
    price = re.findall('\$(.+)</span>', priceTag)
    price = price[0]
    if not price:
        price = 'Not Found'
    else:
        price = float(price)
    print(price)

    return price

def getURLAmazon(itemName):
    query = itemName
    url = "https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Dinstant-video&field-keywords=" + query
    return url

def getPriceYouTube(itemName):
    query = itemName
    url = "https://www.youtube.com/results?search_query=" + query + "full movie"
    resp = requests.get(url)
    html_data = resp.text
    soup = BeautifulSoup(html_data, 'html.parser')
    numScrape = 10
    # tags = soup.find_all('button', limit=numScrape)
    tags = soup.find_all(attrs={'class': 'yt-uix-button-content'}, limit=numScrape)
    # print(tags)
    tags = str(tags)
    # print(priceTag)
    # print(type(priceTag))
    priceTag = re.findall('(\$.+)</span>?', tags)
    # print(priceTag)
    # print(len(priceTag))
    priceTag = (priceTag[0])
    # print(priceTag)

    # priceTag='$16.99</span></span></button>, <button aria-expanded="false" aria-haspopup="true" '

    price = re.findall('\$([0-9]+\.[0-9]+)', priceTag)
    price = price[0]


    if not price:
        price = 'Not Found'
    else:
        price = float(price)
    print(price)

    return price

def getURLYouTube(itemName):
    query = itemName
    url = "https://www.youtube.com/results?search_query=" + query + " full movie"
    return url








if __name__=="__main__":
    # getPriceAmazon("return of the jedi 1983")
    getPriceYoutube("return of the jedi 1983")