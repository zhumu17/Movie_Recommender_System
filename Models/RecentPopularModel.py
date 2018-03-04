# most popular model
# here it is a simple design: find the one with highest score with most of the users
import DatabaseQueries
import pandas as pd
import numpy as np
import logging
class RecentPopularModel(object):
    # the year and number of rating thresholds can be modified inside DatabaseQueries SQL query
    def __init__(self):
        pass

    def train(self):
        df_ratings = DatabaseQueries.getRatings()
        df_itemYear = DatabaseQueries.getItemFeature().loc[:,['itemId','Year']]
        df_ratingsYear = pd.merge(df_ratings,df_itemYear, on='itemId')
        df_ratingsYear = df_ratingsYear[df_ratingsYear.Year>2008]
        # print(df_ratingsYear)

        itemID = list(df_ratingsYear)[1]
        ratings = list(df_ratingsYear)[2]
        ratingsGrouped = df_ratingsYear.groupby(itemID)
        ratingsGroupedCount = ratingsGrouped[ratings].count()
        # print(ratingsGroupedCount)

        itemRatingGroupedSorted = ratingsGrouped[ratings].mean()[ratingsGroupedCount > 15].sort_values(ascending=False)
        # print(itemRatingGroupedSorted)
        self.recentPopularList = itemRatingGroupedSorted.index.tolist()
        # print(self.recentPopularList)


    # unlike other models, most popular model doesn't need to predict, just directly recommend
    def predict(self):
        pass

    # directly recommend with the item_id index, based on corresponding rating from high to low
    def recommend(self):
        return self.recentPopularList



