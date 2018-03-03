# This module contains 3 classes: WebServer, Request, Action
import logging
import os
import DatabaseQueries
from RecEngine import RecEngine
from Ranker import Ranker
from TrainingCenter import TrainingCenter
from UserAnalyzer import UserAnalyzer
from ModelStore import ModelStore


class FlowControl(object):
    logging.basicConfig(level=logging.INFO)  # Output information for log use

    def __init__(self, configMap):
        # numberToServe: the number of items finally served to the users
        self.numberToServe = configMap['numberToServe']
        self.log = logging.getLogger(__name__)

    # instantiate all together the classes that will be used, and start with training offline models
    def start(self):
        # DatabaseQueries.createTables()
        self.modelStore = ModelStore()  # "database" of models
        self.userAnalyzer = UserAnalyzer()  # classify user type: anonymous? registered new? or registered old?
        self.trainingCenter = TrainingCenter(self.modelStore)
        self.ranker = Ranker()  # just rank the recommended items
        # once start should firstly train the models and immediately have recommendations on home page
        self.trainingCenter.trainModel() # NOTE: need to firstly train models once for a welcome page
        self.recEngine = RecEngine(self.userAnalyzer, self.modelStore, DatabaseQueries.getNumRatingsPerUser())

    # Use models - Output recommendations results directly to user
    def renderRecommendation(self, userId = None, numberToServe = None, itemId = None, ratingScore = None, classical = None, userPreference = None):
        self.log.info("responding to request: %s" % userId)
        recommendations = self.recEngine.provideRecommendation(userId, itemId, ratingScore, classical, userPreference) # returns a dict
        rankings = self.ranker.rank(recommendations, userId, numberToServe) # a list of item ids
        # output is the detail content of item, not just item id, but sorted (ranked) by the id value
        # print("results from recEngine:", recommendations)
        # print(rankings)
        df_inventory = DatabaseQueries.getInventory()
        df_inventory.index = df_inventory.index + 1
        itemsRecommended=[]
        itemsImageURL = []
        # for i in rankings:
        #     itemsRecommended.append(df_inventory[ df_inventory['itemId'] == i].itemName.item())
        #     itemsImageURL.append(df_inventory[df_inventory['itemId']== i].itemImageURL.item())
        # print(itemsRecommended)
        # print(itemsImageURL)
        for i in rankings:
            itemName = df_inventory[ df_inventory['itemId'] == i].itemName.item()
            itemsRecommended.append(itemName)

            if os.path.exists("./static/images/moviePosters/" + itemName + ".jpg"):
                url = "./static/images/moviePosters/" + itemName + ".jpg"
            else:
                url = df_inventory[df_inventory['itemId']== i].itemImageURL.item()
            itemsImageURL.append(url)

        return itemsRecommended, itemsImageURL

    # Set up and update models - increment system - update offline models and clear online model at the end of day
    def increment(self):
        self.log.info("incrementing the system, update the models")
        # increment the whole system by one day, trigger offline training
        self.trainingCenter.trainModel()
        self.recEngine.resetCache() # reset most popular
