# KNN model, not actually user-user collaborative filtering
# for new user, using (given) user feature, find the k nearest neighbor, using their ratings for the recommendation
# Note that the user feature is not user's preference vector on items, but user's age, gender and occupation information
import numpy as np
from sklearn.neighbors import NearestNeighbors
import DatabaseQueries

class KNNmodel(object):
    def __init__(self):
        self.knnModel = None

    def train(self, userFeatureTable, ratingsMat):
        # first do simple feature preprocessing, making age between 0 ~ 1, along with all other data in 0 ~ 1
        userFeatureTable.loc[:, "Action"] = userFeatureTable.loc[:, "Action"]
        # print(userFeatureTable.head())
        # train UNSUPERVISED Nearest Neighbor for clustering, just to get the neighbors users, so only fit(userFeatureTable)
        # don't be confused with Supervised K Nearest Neighbor, which directly predict labels and fit(feature, label)
        self.knnModel = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(userFeatureTable) # ball_tree, just run faster

        # ratingMat is the rating matrix
        self.ratingsMat = ratingsMat
        self.userFeatureTable = userFeatureTable
        self.userIds = self.userFeatureTable.index  # the actual order seen by the knnmodel

    # predict method just return neighbors of similar userIds, no recommendations yet
    def predict(self, userFeature):
        # code reference see http://scikit-learn.org/stable/modules/neighbors.html
        distances, indices = self.knnModel.kneighbors(userFeature)
        # indices are the nearest neighbors' index in the matrix, which is different from userId.
        print("userFeature", userFeature)
        return self.userIds[indices[0]]

    # using results of predictions to recommend
    def recommend(self, userId):
        print(userId)
        # data is a tuple of (user feature, item feature)
        self.userFeatureTable = DatabaseQueries.getUserFeature()
        self.userFeatureTable = self.userFeatureTable.loc[:, "age":]
        self.userFeatureTable.index = self.userFeatureTable.index + 1
        self.userFeatureTable.loc[:, "age"] = self.userFeatureTable.loc[:, "age"] / 10. # NEVER forget this!!

        userFeature = self.userFeatureTable.loc[userId].values.reshape(1,-1) # reshape 1D array into 2D array to feed KNN
        userIds = self.predict(userFeature) # userIds of neighbor users
        print("neighbor of similar userIds",userIds)

        # remove himself from nearest neighbor
        # userIds = np.array(list(set(userIds) - set([userId])))
        userIds = userIds[1:]
        print("neighbor of similar userIds", userIds)
        # for all nearest neighbors, compute the the average score, sorted from large to small
        # then report the item ids
        return self.ratingsMat[userIds - 1].mean(axis=0).argsort()[::-1] + 1


if __name__ == "__main__":
    from TrainingCenter import TrainingCenter
    import DatabaseQueries
    DatabaseQueries.createTables()
    rating_history = DatabaseQueries.getRatings()
    userFeatureTable = DatabaseQueries.getUserFeature()
    ratingsMat = TrainingCenter.transformToMat(rating_history)

    model = KNNmodel()
    model.train(userFeatureTable, ratingsMat)
    print(model.recommend(101))
