
from ModelStore import ModelStore
import DatabaseQueries
import numpy as np
import logging

class TrainingCenter():
    def __init__(self, modelStore):
        self.modelStore = modelStore
        self.log = logging.getLogger(__name__)

    def trainModel(self):
        # first get useful data from database
        self.log.info("Get training data from database...")

        ratings = DatabaseQueries.getRatings().loc[:, "userId":]
        ratings.index = ratings.index + 1  # make dataframe index start from 1 instead of 0 by default
        itemFeatureTable = DatabaseQueries.getItemFeature().loc[:, "unknown":]
        itemFeatureTable.index = itemFeatureTable.index + 1
        userFeatureTable = DatabaseQueries.getUserFeature().loc[:, "age":]
        userFeatureTable.index = userFeatureTable.index + 1
        ratingsMatrix = self.transformToMat(ratings)

        # start to train each model
        self.log.info("Start training...")

        model = self.modelStore.getModel(ModelStore.MP_MODEL_KEY)
        model.train(ratings)
        self.pushModel(model, ModelStore.MP_MODEL_KEY)
        self.log.info("Most Popular Model training finished")

        model = self.modelStore.getModel(ModelStore.KNN_MODEL_KEY)
        model.train(userFeatureTable, ratingsMatrix)
        self.pushModel(model, ModelStore.KNN_MODEL_KEY)
        self.log.info("K-Nearest Neighborhood Model training finished")

        model = self.modelStore.getModel(ModelStore.CF_MODEL_KEY)
        model.train(ratingsMatrix, itemFeatureTable)
        self.pushModel(model, ModelStore.CF_MODEL_KEY)
        self.log.info("Collaborative Filtering Model training finished")

        model = self.modelStore.getModel(ModelStore.CL_MODEL_KEY)
        model.train(itemFeatureTable)
        self.pushModel(model, ModelStore.CL_MODEL_KEY)
        self.log.info("Clustering Model training finished")

    def pushModel(self, model, key):
        self.modelStore.setModel(model, key)

    @staticmethod
    def transformToMat(ratings):
        ratingsMatrix = np.zeros([ratings.userId.max(), ratings.itemId.max()])
        for row in ratings.itertuples():
            ratingsMatrix[row[1]-1, row[2]-1] = row[3]
        return ratingsMatrix
