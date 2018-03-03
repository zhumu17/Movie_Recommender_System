from bs4 import BeautifulSoup
import requests
import re
# import urllib2 # urllib2 is replaced as urllib.request
import urllib.request
import os
# import cookielib
import json
import time
import pandas as pd
import numpy as np


def combine():
    df_inventory = pd.read_csv("./DATA/inventory.csv")
    df_inventory1 = pd.read_csv("./DATA/inventory_URL0-960.csv")
    df_inventory2 = pd.read_csv("./DATA/inventory_URL960-1000.csv")
    df_inventory3 = pd.read_csv("./DATA/inventory_URL8500-9000.csv")
    df_inventory4 = pd.read_csv("./DATA/inventory_URL9000-9123.csv")
    for i in df_inventory.index:
        if df_inventory.loc[i, 'itemImageURL'] == '0.0':
            if df_inventory1.loc[i,'itemImageURL'] != '0.0':
                df_inventory.loc[i,'itemImageURL'] = df_inventory1.loc[i,'itemImageURL']
            if df_inventory2.loc[i,'itemImageURL'] != '0.0':
                df_inventory.loc[i,'itemImageURL'] = df_inventory2.loc[i,'itemImageURL']
            if df_inventory3.loc[i,'itemImageURL'] != '0.0':
                df_inventory.loc[i,'itemImageURL'] = df_inventory3.loc[i,'itemImageURL']
            if df_inventory4.loc[i,'itemImageURL'] != '0.0':
                df_inventory.loc[i,'itemImageURL'] = df_inventory4.loc[i,'itemImageURL']
    df_inventory.to_csv('./DATA/inventory2.csv', index = False)




def get_soup(url,header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url,headers=header)),'html.parser')


def imageCrawl():
    # df_inventory = pd.read_csv("./DATA/inventory.csv")
    df_inventory_old = pd.read_csv("./DATA/inventory_old.csv")
    df_inventory_URL = pd.read_csv("./DATA/inventory_URL.csv")
    count = 0
    total = 0
    for i in df_inventory_URL.iloc[:,:].index:
        query = df_inventory_URL.loc[i,'itemName']

        # print(True in df_inventory_old.itemName.str.contains(query, case=False, regex=False))
        print(i)

        # (not (True in df_inventory_old.itemName.str.contains(query, case=False, regex=False))) and
        # print(df_inventory_URL.loc[i,'itemImageURL'] == '0.0')
        if df_inventory_URL.loc[i,'itemImageURL'] != '0.0' :
            # df_inventory.loc[i,'itemImageURL'] = df_inventory_URL.loc[i,'itemImageURL']
            print("link was there")
        elif "True" in str(df_inventory_old.itemName.str.contains(query, case=False, regex=False)):
            # print("True" in str(df_inventory_old.itemName.str.contains(query, case=False, regex=False)))
            print("image was downloaded before")
        else:
            count += 1
            total += 1
            print(query)
            # image_type="ActiOn"
            query= query.split()
            query='+'.join(query)+'+poster'
            url="https://www.google.com/search?num=1&q="+query+"&source=lnms&tbm=isch"
            # print (url)

            if total % 100 <= 60:
                header = {'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"}
            # elif total % 100 >20 and total % 100 <= 40:
            #     header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"}
            # elif total % 100 >40 and total % 100 <= 60:
            #     header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0 "}
            elif total % 100 >60 and total % 100 <= 80:
                header = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
            elif total % 100 >80 and total <= 90:
                header = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41 "}
            elif total % 100 > 90:
                header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}


            print("there are total number of ", total, " of movies crawled this time")
            print(header)
            soup = get_soup(url,header)
            # print(soup)


            # ActualImages=[]# contains the link for Large original images, type of  image
            for a in soup.find_all("div",{"class":"rg_meta"}, limit=1):
                link =json.loads(a.text)["ou"]
                # Type = json.loads(a.text)["ity"]
                # ActualImages.append((link,Type))
                df_inventory_URL.loc[i,'itemImageURL'] = link
                print("image link is :" , link)
                # print ("there are total" , len(ActualImages),"images")
                print ("link of " , query ," is saved")

            print("Now breath for 2 seconds..")
            time.sleep(2)

            print("------- Updating inventory_CRL.csv -------")
            df_inventory_URL.to_csv('./DATA/inventory_URL.csv', index=False)

            # if count % 2 == 0:
            nap = np.random.rand()*3
            print("Now nap randomly for", nap , " seconds...")
            time.sleep(nap)

            # if count == 3:
            #     print("Now nap for 3 seconds...")
            #     time.sleep(3)
            #
            # if count == 5:
            #     print("Now sleep for 5 seconds......")
            #     time.sleep(5)
            #
            if count == 7:
                print("Now sleep for 7 seconds......")
                time.sleep(7)
            #
            # if count == 10:
            #     count = 0
            #     print("Now deep sleep for 10 seconds..........")
            #     time.sleep(10)
            #
            if total % 30 == 0:
                print("Pause for 30 seconds............")
                time.sleep(30)

            # if total % 50 == 0:
            #     print("Take a break for 50 seconds...............")
            #     time.sleep(50)

            if total == 401:
                stop


def imageDownload():
    df_inventory_URL = pd.read_csv("./DATA/inventory_URL.csv")
    count = 0
    for i in df_inventory_URL.index:
        if 'impawards' in df_inventory_URL.loc[i,'itemImageURL']:
            url = df_inventory_URL.loc[i, 'itemImageURL']
            name = df_inventory_URL.loc[i,'itemName']
            print(name)
            count += 1

            # if count == 2:
            #     stop
            #
            DIR = "Pictures"

            # #print images
            if count >= 400:
                if 'xlg' not in url:
                    print("downloading image...")
                    urllib.request.urlretrieve(url, os.path.join(DIR, name + ".jpg"))
                    print("sleep for 2.5 seconds...")
                    time.sleep(2.5)
                    nap = np.random.rand() * 2
                    print("and ", nap, " seconds...")


            if count % 50 ==0 and count >=410:
                print("sleep for 30 seconds......")
                time.sleep(30)


            print(count)






if __name__ == "__main__":
    imageCrawl()
    # combine()
    # imageDownload()