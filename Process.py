# This module contains 3 classes: WebServer, Request, Action
import logging

import DatabaseQueries
from RecEngine import RecEngine
from Ranker import Ranker
# from Learners.OfflineLearner import OfflineLearner
# from Learners.OnlineLearner import OnlineLearner
from TrainingCenter import TrainingCenter
from UserAnalyzer import UserAnalyzer
from ModelStore import ModelStore


class Process(object):
    logging.basicConfig(level=logging.INFO)  # Output information for log use

    def __init__(self, configMap):
        # numberToServe: the number of items finally served to the users
        self.numberToServe = configMap['numberToServe']
        self.log = logging.getLogger(__name__)

    # instantiate all together the classes that will be used, and start with training offline models
    def start(self):
        DatabaseQueries.createTables()
        self.modelStore = ModelStore()  # "database" of models
        self.userAnalyzer = UserAnalyzer()  # classify user type: anonymous? registered new? or registered old?
        self.trainingCenter = TrainingCenter(self.modelStore)
        self.ranker = Ranker()  # just rank the recommended items

        # once start should firstly train the models and immediately have recommendations on home page
        self.trainingCenter.trainModel() # NOTE: need to firstly train models once for a welcome page
        self.recEngine = RecEngine(self.userAnalyzer, self.modelStore, DatabaseQueries.getNumRatingsPerUser())

    # Use models - Output recommendations results directly to user
    def renderRecommendation(self, userId = None, numberToServe = None, itemId = None, ratingScore = None):
        self.log.info("responding to request: %s" % userId)
        recommendations = self.recEngine.provideRecommendation(userId, itemId, ratingScore) # returns a dict
        rankings = self.ranker.rank(recommendations, userId, numberToServe) # a list of item ids
        # for the purpose of testing, we sort the index, output item names
        # output is the detail content of item, not just item id, but sorted (ranked) by the id value
        # print(recommendations)
        print(rankings)
        inventory = DatabaseQueries.getInventory()
        inventory.index = inventory.index + 1
        return inventory.loc[rankings,:]

    # Set up and update models - increment system - update offline models and clear online model at the end of day
    def increment(self):
        self.log.info("incrementing the system, update the models")
        # increment the whole system by one day, trigger offline training
        self.trainingCenter.trainModel()
        self.recEngine.resetCache() # reset most popular
