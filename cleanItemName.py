import re
import os
import pandas as pd

def cleanItemNameInventory():
    df_inventory = pd.read_csv('./DATA/inventory.csv')
    print(df_inventory)
    count = 0
    for row in df_inventory.itertuples():

        name = row.itemName
        if re.findall(',(\s)The', name):
            # print("--------")
            # print name
            name = re.sub(',(\s)The', '', name)
            name = "The "+ name
            count += 1
            # print name
            # print("--------")
            df_inventory.loc[row.itemId-1,"itemName"] = name
    print(count)
    print(df_inventory)
    df_inventory.to_csv('./DATA/inventory2.csv', sep=',', encoding='utf-8', index = False)


def cleanItemNameItemFeature():
    df_itemFeature = pd.read_csv('./DATA/itemFeature.csv')
    # print(df_itemFeature)
    count = 0

    for row in df_itemFeature.itertuples():
        name = row.itemName
        if re.findall(',(\s)The', name):
            print("-----")
            print(name)
            name = re.sub(',(\s)The', '', name)
            name = "The "+name
            count+=1
            print(name)
            print("-----")
            df_itemFeature.loc[row.itemId-1,"itemName"] = name
    print(count)
    print(df_itemFeature)
    df_itemFeature.to_csv('./DATA/itemFeature2.csv', sep = ',', encoding='utf-8', index = False)


def cleanitemNamePoster():
    directory = "./static/images/moviePosters/"
    for filename in os.listdir(directory):
        if re.findall(',(\s)The', filename):
            print("-----")
            print(filename)
            newname =filename
            newname = re.sub(',(\s)The', '', newname)
            newname = "The " + newname
            print(newname)
            print("-----")

            os.rename(directory+filename, directory+newname)


if __name__ =="__main__":
    cleanItemNameInventory()
    cleanItemNameItemFeature()
    cleanitemNamePoster()