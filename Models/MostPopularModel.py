# most popular model
# here it is a simple design: find the one with highest score with most of the users

class MostPopularModel(object):
    # set a threshold to avoid item rated high but very vew number of ratings
    N_Freq_limit = 0.0022  # at least 0.2% of users have rated it can be qualified to be considered if it is most popular

    def __init__(self):
        pass

    def train(self, ratingHistory):
        # list() method convert an dataframe to a list
        itemID = list(ratingHistory)[1]
        ratings = list(ratingHistory)[2]

        nLimit = int(ratingHistory.shape[0] * self.N_Freq_limit)
        itemRatingGrouped = ratingHistory.groupby(itemID) # dataframe.groupby() method
        itemRatingGroupedCount = itemRatingGrouped[ratings].count()
        # print("itemRatingGroupedCount:")
        # print(itemRatingGroupedCount)

        itemRatingGroupedSorted = itemRatingGrouped[ratings].mean()[itemRatingGroupedCount > nLimit].sort_values(ascending=False)
        # print(itemRatingGroupedSorted)
        self.mostPopularList = itemRatingGroupedSorted.index.tolist()

    # unlike other models, most popular model doesn't need to predict, just directly recommend
    def predict(self):
        pass

    # directly recommend with the item_id index, based on corresponding rating from high to low
    def recommend(self):
        return self.mostPopularList



