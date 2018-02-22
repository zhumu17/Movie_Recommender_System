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
    # print(tags)
    priceTag = str(tags[0])
    # print(priceTag)
    # print(type(priceTag))
    price = re.findall('\$(.+)</span>', priceTag)
    price = float(price[0])
    if not price:
        price = -1
    print(price)

    return price

def getURLAmazon(itemName):
    query = itemName
    url = "https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Dinstant-video&field-keywords=" + query
    return url

def getPriceYoutube(itemName):
    query = itemName
    url = "https://www.youtube.com/results?search_query=" + query + "full movie"
    resp = requests.get(url)
    html_data = resp.text
    soup = BeautifulSoup(html_data, 'html.parser')
    numScrape = 3
    tags = soup.find_all(attrs={'class':'ytd-item-section-renderer'}, limit=numScrape)
    print(tags)
    priceTag = str(tags[0])
    print(priceTag)
    print(type(priceTag))
    price = re.findall('\$(.+)</span>', priceTag)
    price = float(price[0])
    if not price:
        price = -1
    print(price)

    return price

def getURLYoutube(itemName):
    query = itemName
    url = "https://www.youtube.com/results?search_query=" + query + "full movie"
    return url








if __name__=="__main__":
    # getPriceAmazon("return of the jedi 1983")
    getPriceYoutube("return of the jedi 1983")