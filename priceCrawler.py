from bs4 import BeautifulSoup
import requests
import re
import json

def getPriceAmazon(itemName):
    query = itemName
    url = "https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Dinstant-video&field-keywords=" + query
    resp = requests.get(url)
    html_data = resp.text
    soup = BeautifulSoup(html_data, 'html.parser')
    numScrape = 3
    tags = soup.find_all(attrs={'class':'sx-price sx-price-large'}, limit=numScrape)
    if not tags:
        price = 'Click to See Prices'
        return price
    # print("tag is", tags)


    priceTag = str(tags[0])
    # print("priceTag is :", priceTag)
    # print(type(priceTag))

    priceWithoutDecimal = re.findall('([0-9]+)', priceTag)
    price = priceWithoutDecimal[0] + "." + priceWithoutDecimal[1]
    # print(priceWithoutDecimal)
    # print(price)

    if not price:
        price = 'Click to See Prices'
        return price
    else:
        price = "Watch From $" + str(price)
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

    if not priceTag:
        price = 'Click to See Prices'
        return price
    else:
        priceTag = (priceTag[0])
    # print(priceTag)

    # priceTag='$16.99</span></span></button>, <button aria-expanded="false" aria-haspopup="true" '

    price = re.findall('\$([0-9]+\.[0-9]+)', priceTag)
    price = price[0]


    if not price:
        price = 'Click to See Prices'
        return price
    else:
        price = "Watch From $" + str(price)
    print(price)

    return price

def getURLYouTube(itemName):
    query = itemName
    url = "https://www.youtube.com/results?search_query=" + query + " full movie"
    return url


def getPriceITunes(itemName):
    price = "Click to See Prices" # as backup

    queryList = re.findall('(.*)[1][9][0-9][0-9]|(.*)[2][0][0-9][0-9]', itemName) # remove year and just use name
    if queryList:
        print(queryList)

        for element in queryList[0]:
            if element:
                name = element
                break
    else:
        name = itemName
    # print(name)
    nameWords = name.split()
    # print(nameWords)
    query = nameWords[0]
    # print(type(query))
    for word in nameWords[1:]:
        query = query + "+" + word
    # print(query)

    url = "https://itunes.apple.com/search?term=" + query + "&country=us&media=movie"
    resp = requests.get(url)
    # print(resp)
    JSON = resp.text

    parsedJSON = json.loads(JSON)

    print(parsedJSON)
    # print(type(parsedJSON))

    if not parsedJSON['results']:
        price = "Click to See Prices"
        return price, "www.google.com"



    print(parsedJSON['results'][0])
    # print("number of elements in list:", len(parsedJSON['results']))

    if 'trackPrice' in parsedJSON['results'][0]:
        price = parsedJSON['results'][0]['trackPrice']

    elif 'trackHdPrice' in parsedJSON['results'][0]:
        price = parsedJSON['results'][0]['trackHdPrice']

    else:
        price = "Click to See Prices"
        return price, "www.google.com"

    price = "Watch From $" + str(price)
    # print(price)

    if 'trackViewUrl' in parsedJSON['results'][0]:
        urlITunes = parsedJSON['results'][0]['trackViewUrl']
    else:
        urlITunes = "https://www.google.com"

    return price, urlITunes

def getURLITunes(itemName, itemIdITunes): # NOT USED be cause getPriceITunes can get url!!
    url = "https://itunes.apple.com/us/movie/" + itemName + "/id" + str(itemIdITunes)
    return url




if __name__=="__main__":
    # getPriceAmazon("return of the jedi 1983")
    # getPriceYouTube("return of the jedi 1983")
    # getPriceITunes("the godfarther (1972)")
    getPriceITunes("the last jedi")

    #976965981 for testing itemId_iTunes
