import numpy as np
import pandas as pd
import re
import os

def cleanMovies():
    df_movie = pd.read_csv('./ml-latest-small/movies_org.csv')
    print(df_movie.head())
    print("any null values?", df_movie.isnull().values.any())
    df_movie = pd.read_csv('./ml-latest-small/movies_org.csv')
    for i in df_movie.index:
        movieTitle = str(df_movie.title.values)
        try:
            movieTitle.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            pass
            # print(False)
        else:
            print(True) # non-utf-8 encoding!!!


    features = ['Year', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
                  'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    # print(len(df_movie))
    # print(np.zeros((len(df_movie), len(features))))
    df_features = pd.DataFrame(np.zeros((len(df_movie), len(features))), columns = features)
    df_movie = pd.concat([df_movie, df_features], axis = 1)
    # print(df_movie.head())
    for i in df_movie.loc[:,:].index:
        if i % 10 == 0:
            print(i)

        movieTitle = df_movie.loc[i,'title']
        if re.findall(',(\s)The', movieTitle):
            # print("-----")
            # print(movieTitle)
            movieTitle = re.sub(',(\s)The', '', movieTitle)
            movieTitle = "The " + movieTitle
            # print(movieTitle)
            # print("-----")
            df_movie.loc[i, "title"] = movieTitle

        df_movie.loc[i,'Year'] = re.findall('\(([1-2][0-9][0-9][0-9])', movieTitle)[0]
        genreList = str(df_movie.loc[i,'genres']).split(sep='|')
        # print(genreList)
        for word in genreList:
            # print(word)
            if word in features:
                # print(word)
                df_movie.loc[i, word] = 1

    df_movie = df_movie.drop(columns = 'genres')

    df_movie.to_csv('./ml-latest-small/itemFeature.csv', index=False)
    print(df_movie.head())









    # df_movie = pd.get_dummies(df_movie)


    df_ratings = pd.read_csv('./ml-latest-small/ratings.csv')
    df_ratings = df_ratings.loc[:,['userId','movieId','rating']]
    # print(df_ratings.head())

    # MANUALLY CHANGED HEADER NAMES: movieId into itemId, title to itemName!!!!!!!



def cleanRatings():
    df_ratings = pd.read_csv('./ml-latest-small/ratings_org.csv')
    df_ratings = df_ratings.loc[:,['userId','movieId','rating']]
    df_ratings.to_csv('./ml-latest-small/ratings.csv', index = False)
    # MANUALLY CHANGED HEADER NAMES: movieId into itemId !!!!!!!

def createInventory():
    df_inventory = pd.read_csv('./ml-latest-small/itemFeature.csv').loc[:,['itemId','itemName']]

    df_imageURL = pd.DataFrame({'itemImageURL': np.zeros(len(df_inventory))})
    df_inventory = pd.concat([df_inventory, df_imageURL], axis = 1)
    print(df_inventory.head())
    df_inventory.to_csv('./ml-latest-small/inventory.csv', index=False)

def createUserFeature():
    df_ratings = pd.read_csv('./ml-latest-small/ratings.csv')
    userId_max = df_ratings.userId.values.max()
    print(userId_max)

    userIdList = np.arange(1, userId_max+1)
    # print(userIdList)
    df_users = pd.DataFrame({'userId': userIdList})
    # print(df_users)
    features = ['Year', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama',
                'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
    df_features = pd.DataFrame(np.zeros((len(df_users), len(features))), columns=features)
    df_users = pd.concat([df_users, df_features], axis=1)
    print(df_users)
    df_users.to_csv('./ml-latest-small/userFeature.csv', index=False)



def cleanFrenchChar():
    df_inventory = pd.read_csv('./DATA/inventory.csv')

    for i in df_inventory.index:
        if i % 100:
            print(i)
        name = df_inventory.loc[i, 'itemName']


        # print(name)
        name = re.sub('(à|á|â|ä|æ|ã|å|ā)', 'a', name)
        name = re.sub('(À|Á|Â|Ä|Æ|Ã|Å|Ā)', 'A', name)
        name = re.sub('(è|é|ê|ë|ē|ė|ę)', 'e', name)
        name = re.sub('(È|É|Ê|Ë|Ē|Ė|Ę)', 'E', name)
        name = re.sub('(î|ï|í|ī|į|ì)', 'i', name)
        name = re.sub('(Î|Ï|Í|Ī|Į|Ì)', 'I', name)
        name = re.sub('(ô|ö|ò|ó|œ|ø|ō|õ)', 'o', name)
        name = re.sub('(Ô|Ö|Ò|Ó|Œ|Ø|Ō|Õ)', 'O', name)
        name = re.sub('(û|ü|ù|ú|ū)', 'u', name)
        name = re.sub('(Û|Ü|Ù|Ú|Ū)', 'U', name)
        # print(name)

        df_inventory.loc[i,'itemName'] = name
    df_inventory.to_csv('./DATA/inventory.csv', index=False)




def cleanColumnSign():
    df_itemFeature = pd.read_csv('./DATA/itemFeature.csv')
    df_inventory = pd.read_csv('./DATA/inventory.csv')
    for i in df_inventory.index:
        name = df_inventory.loc[i,'itemName']
        if re.findall('\:', name):
            print("-------")
            print(name)
            nameClean = re.sub('\:', ' -', name)
            df_inventory.loc[i, 'itemName'] = nameClean
            print(nameClean)
    # df_inventory.to_csv('./DATA/inventory.csv', index=False)


def cleanPictureNameColumnSign():
    os.chdir('./Pictures')
    count=0
    for name in os.listdir("."):
        if re.findall('\:', name):
            if count == 1:
                stop
            print("-------")
            print(name)
            # nameClean = re.sub('\:', ' -', name)
            # os.rename("./Pictures/"+name, "./Pictures/"+nameClean)
            # print(nameClean)
            count += 1
            print(count)
        # print(name)
        # if re.findall('\/', name):
            # if count == 1:
            #     stop
            # print(name)
            # print("-------")
            # print(name)
            # nameClean = re.sub('\:', ' -', name)
            # os.rename("./Pictures/"+name, "./Pictures/"+nameClean)
            # print(nameClean)
            # count += 1
            # print(count)


def unifyItemNames():
    df_inventory = pd.read_csv('./DATA/inventory.csv')
    df_itemFeature = pd.read_csv('./DATA/itemFeature.csv')
    for i in df_itemFeature.index:
        print(i)
        df_itemFeature.loc[i, 'itemName'] = df_inventory.loc[i, 'itemName']

    df_itemFeature.to_csv('./DATA/itemFeatureNew.csv', index=False)

def unifyItemNumbers():
    df_inventory = pd.read_csv('./DATA/inventoryNew.csv')
    df_itemFeature = pd.read_csv('./DATA/itemFeature.csv')
    for i in df_itemFeature.index:
        if i % 10 == 0:
            print(i)
        df_itemFeature.loc[i, 'itemId'] = df_inventory.loc[i, 'itemId']

    df_itemFeature.to_csv('./DATA/itemFeatureNew.csv', index=False)
    print("new itemFeature is saved as ./DATA/itemFeatureNew.csv")

def cleanItemNumber():
    df_inventory = pd.read_csv("./DATA/inventory.csv")
    df_inventory.index = df_inventory.index + 1
    # df_ratings = pd.read_csv("./DATA/ratings.csv")

    # print(df_inventory)
    # for i in df_ratings.index:
    #     itemIdOld = df_ratings.loc[i,'itemId']
    #     itemIdNew = int(df_inventory[df_inventory.itemId == itemIdOld].index.values)
    #     df_ratings.loc[i,'itemId'] = itemIdNew
    #     # print("===========================")
    #     if i % 100 == 0:
    #         print(i)
    #     # print(itemIdOld)
    #     # print(itemIdNew)
    # print(df_ratings.head())
    # print(df_ratings.tail())


    # reindex inventory
    for i in df_inventory.index:
        df_inventory.loc[i,'itemId'] = i


    print(df_inventory.head())
    print(df_inventory.tail())

    # df_ratings.to_csv("./DATA/ratingsNEW.csv", index = False)
    # print("new ratings is saved as ./DATA/ratingsNew.csv")

    df_inventory.to_csv("./DATA/inventoryNew.csv", index = False)
    print("new inventory is saved as ./DATA/inventoryNew.csv")




if __name__ =="__main__":
    # cleanMovies()
    # cleanRatings()
    # createInventory()
    # createUserFeature()
    # cleanFrenchChar()
    ###### cleanColumnSign()  # no need!
    ###### cleanPictureNameColumnSign()
    # cleanItemNumber()
    unifyItemNumbers()
