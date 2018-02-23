# Recommendation Engine

from ModelStore import ModelStore
import logging


class RecEngine(object):
    logging.basicConfig(level=logging.INFO)

    def __init__(self, userAnalyzer, modelStore, numRatingsPerUser):
        self.userAnalyzer = userAnalyzer
        self.modelStore = modelStore
        self.numRatingsPerUser = numRatingsPerUser
        # to pre-compute the most popular items, because this recommendation is independent from users
        self._cacheMostPopular()  # most popular only computed once when initializing RecEngine and be reused for a day
        self.log = logging.getLogger(__name__)

    # general reset & cache
    def resetCache(self):
        self._cacheMostPopular()

    def _cacheMostPopular(self):
        # for unregistered users, compute once the recommendation of most popular items
        model = self.modelStore.getModel(ModelStore.MP_MODEL_KEY)
        self.mostPopularList = model.recommend()

    # CORE function: provide recommendations
    def provideRecommendation(self, userId = None, itemId = None, ratingScore = None):
        # recommendations stored as dictionary with type as key, itemId list as value, in order for the ranker to finalize
        recommendations = {}

        # for unregistered users, popular item are always computed and ready to display
        recommendations["popular"] = self.mostPopularList
        self.log.info("Recommending using Most Popular items")

        # for registered users, based on new or old user provide recommendation
        userType = self.userAnalyzer.analyze(userId, self.numRatingsPerUser)
        self.log.info("user type: %s" % userType)
        if ratingScore == None: # no item is rated
            if userType == "new":
                # for new user, use KNN model based on similar users
                model = self.modelStore.getModel(ModelStore.KNN_MODEL_KEY) # use key to get model in model dictionary
                recommendations["userBased"] = model.recommend(userId)
                self.log.info("Recommending using KNN algorithm")
            elif userType== "old":
                # for old user, use CF model
                model = self.modelStore.getModel(ModelStore.CF_MODEL_KEY) # use key to get model in model dictionary
                recommendations["collaborativeFiltering"] = model.recommend(userId)
                self.log.info("Recommending using Collaborative Filtering algorithm")
        else:

            # if get a rated one item, provide recommendation of similar item if rated score is high, otherwise pass
            if ratingScore >= 4:
                model = self.modelStore.getModel(ModelStore.CL_MODEL_KEY)
                recommendations["itemBased"] = model.recommend(itemId)
                self.log.info("Recommending using KMeans algorithm")

        # print(recommendations.keys())
        return recommendations