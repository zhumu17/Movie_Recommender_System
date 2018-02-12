from bs4 import BeautifulSoup
import requests
import re
import urllib2
import os
import cookielib
import json



import pandas as pd
import numpy as np
df_inventory = pd.read_csv("./DATA/inventory.csv")

print(df_inventory.head(10))
inventory = df_inventory.iloc[:,1].values
# for item in inventory:
#     print(item)
#     print(type(item))
#     print("----")


def get_soup(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')


for i in range(len(inventory)):
    query = inventory[i]# you can change the query for the image  here
    name = inventory[i]
    print(name)
    image_type="ActiOn"
    query= query.split()
    query='+'.join(query)
    url="https://www.google.com/search?q="+query+"&source=lnms&tbm=isch"
    print url







    #add the directory for your image here
    DIR="Pictures"
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }
    soup = get_soup(url,header)


    ActualImages=[]# contains the link for Large original images, type of  image
    count = 0;
    for a in soup.find_all("div",{"class":"rg_meta"}):
        if count == 1:
            break
        link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        ActualImages.append((link,Type))
        count = count+1


    print  "there are total" , len(ActualImages),"images"

    if not os.path.exists(DIR):
                os.mkdir(DIR)
    # DIR = os.path.join(DIR, query.split()[0])

    # if not os.path.exists(DIR):
    #             os.mkdir(DIR)

    ###print images
    for i , (img , Type) in enumerate( ActualImages[:1]):
        try:
            req = urllib2.Request(img, headers={'User-Agent' : header})
            raw_img = urllib2.urlopen(req).read()

            cntr = len([i for i in os.listdir(DIR) if image_type in i]) + 1
            print cntr
            if len(Type)==0:
                f = open(os.path.join(DIR , name+".jpg"), 'wb')
            else :
                f = open(os.path.join(DIR ,  name+".jpg"), 'wb')


            f.write(raw_img)
            f.close()
        except Exception as e:
            print "could not load : "+img
            print e