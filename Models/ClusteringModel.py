# Kmeans model, item-item collaborative filtering
import numpy as np
from sklearn.cluster import KMeans
import DatabaseQueries

# clustering model is to group items with similar features, this is a content based model
# it is used for online recommendation

class ClusteringModel(object):
    def __init__(self, n_cluster=40):
        self.model = KMeans(n_cluster, random_state=12345)  # set random state for reproducible
        self.groups = {}  # keyed by cluster index and values are itemId's

    def train(self, itemFeatures):
        # self.indices = itemFeatures.index  # the index of item, not necessary the itemIds
        self.model.fit(itemFeatures)
        self.labels = self.model.labels_  # the "label of cluster" every data point belongs to

        # set up groups of items using dictionary  e.g. {label 1:[item 1,item 2], label 2:[item 3, item 4, item 5]}
        for k, v in zip(self.labels, itemFeatures.index.tolist()):
            self.groups.setdefault(k, []).append(v)

    def predict(self, itemFeature):
        label = self.model.predict(itemFeature.reshape(1,-1))
        # print(label)
        similarItemIndex = self.groups[int(label)]  # find similar item list in the group (with cluster label) where the rated item belongs to
        # print(similarItemIndex)
        df_Inventory = DatabaseQueries.getInventory()

        result = []
        for i in similarItemIndex:
            # print(i)
            # print(df_Inventory[df_Inventory.index == i])
            result.append(df_Inventory[df_Inventory.index == i].itemId.item())
        # df_Inventory[]
        # print(result)
        return result

    def recommend(self, itemId = None, itemFeature = None):
        if itemFeature == None:
            df_Inventory = DatabaseQueries.getInventory()
            itemIndex = df_Inventory[df_Inventory['itemId']==itemId].index # itemId is not necessarily the same as index
            itemFeature = DatabaseQueries.getItemFeature().loc[itemIndex, "Action":].values
        else:
            itemFeature = np.array(itemFeature) # itemFeature as a list of preferences passed in
        # print(itemIndex)
        # print(df_Inventory[df_Inventory['itemId']==itemId].itemName)
        return self.predict(itemFeature) # directly use predicted similarity items to recommend

if __name__ == "__main__":
    import DatabaseQueries
    itemFeatureTable = DatabaseQueries.getItemFeature().loc[:, "Action":]
    model = ClusteringModel()
    model.train(itemFeatureTable)
    print(model.recommend(1196))
    # print(model.predict(itemFeatureTable.loc[954].values.reshape(1, -1)))
    print(itemFeatureTable.loc[[954]])
    # print(model.labels[:20])
