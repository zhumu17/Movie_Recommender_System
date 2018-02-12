# Collaborative filtering model
import numpy as np
from sklearn.neighbors import NearestNeighbors
import logging


class CFmodel():
    RARECASE_THRESHOLD = 5 # describe if an item is RARE or new item, if less than 5 item is rare
    logging.basicConfig(level=logging.INFO)

    def __init__(self):
        self.knnModel = NearestNeighbors(n_neighbors=15)
        self.log = logging.getLogger(__name__)

    def _CFSVD(self, ratingsMat): # can be replaced by SGD to get better performance
        user_ratings_mean = np.mean(ratingsMat, axis=1)  # mean over user ratings
        R_demeaned = ratingsMat - user_ratings_mean.reshape(-1, 1)
        from scipy.sparse.linalg import svds
        U, sigma, Vt = svds(R_demeaned, k=10)
        sigma = np.diag(sigma)
        self.all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)

    def train(self, ratingsMat, itemFeatureTable):
        # the logic: Need to fill some unknown ratings before using SVD
        # using content-based modeling for rare items, predict some ratings
        # using the ratings matrix filled with the predicted ratings from the content-based model to do matrix factorization
        # itemFeatureTable is used for content-based model, which will predict for those items with few ratings
        # SVD will be used for collaborative filtering after the rare items have enough ratings
        indices = itemFeatureTable.index
        self.knnModel.fit(itemFeatureTable) # firstly find similar item ratings to fill rating  matrix
        assert (ratingsMat.shape[1] == itemFeatureTable.index.max())

        rareCases = np.where((ratingsMat > 0).sum(axis=0) < self.RARECASE_THRESHOLD)[0]
        # if an item has less than 5 ratings, it is considered as a rare case
        # it is the 0-based matrix indices
        self.log.info("Number of rare cases: %s" % rareCases.shape[0])

        fillCount = 0
        ratingsMatFinal = ratingsMat.copy() # fill ratings of rarecases, but don't want to change the ratingsMat
        for case in rareCases:
            if case + 1 in itemFeatureTable.index: # dataframe index is pre-modified as starting from 1
                features = itemFeatureTable.loc[case + 1] # Content based item feature
                neighbors = self.knnModel.kneighbors(features.values.reshape(1, -1), return_distance=False)[0]
                neighborPos = indices[neighbors] - 1 # from pandas index to matrix so -1
                # compute the number of ratings got by the neighbors from each user
                target_count = (ratingsMat[:, neighborPos] > 0).sum(axis=1) # only count number of ratings that > 0
                # compute the predicted ratings generated from the content-based model
                target_ratings = ratingsMat[:, neighborPos].sum(axis=1).astype(float) / target_count # mean normalization
                # nonzero mean

                for i in range(ratingsMat.shape[0]):
                    if ratingsMat[i, case] == 0 and target_count[i] > 10:
                        # if the rating is missing and more than 10 ratings in its neighbors are available
                        # don't be confused with RARECASE_threshold, which is the item itself with less than 5 ratings
                        if target_ratings[i] != 0:
                            ratingsMatFinal[i, case] = target_ratings[i]
                            fillCount += 1

        # now we have the filled matrix for matrix factorization
        self.log.info("Number of ratings added by content-based model: %s" % fillCount)

        self._CFSVD(ratingsMatFinal) # Finally SVD, can be replaced by SGD, return ratings

    # predict method just predict ratings, no recommendations yet
    def predict(self, userId):
        return self.all_user_predicted_ratings[userId - 1]

    # using results of predictions to recommend
    def recommend(self, userId):
        # data is a tuple of (user feature, item feature)
        # compute the the average score, sorted from large to small, then report the item ids
        return self.all_user_predicted_ratings[userId - 1].argsort()[::-1] + 1 # argsort is sorting ratings but get positions


if __name__ == "__main__":
    from TrainingCenter import TrainingCenter
    import DatabaseQueries

    DatabaseQueries.createTables()
    history = DatabaseQueries.getRatings()
    itemFeatureTable = DatabaseQueries.getItemFeature().loc[:, "unknown":]
    ratingsMat = TrainingCenter.transformToMat(history)

    model = CFmodel()
    model.train(ratingsMat, itemFeatureTable)

    recs = model.recommend(1)
    print(recs)
    print(ratingsMat[0, recs - 1])
