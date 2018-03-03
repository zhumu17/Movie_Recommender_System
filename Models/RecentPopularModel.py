# most popular model
# here it is a simple design: find the one with highest score with most of the users
import DatabaseQueries
import logging
class RecentPopularModel(object):
    # the year and number of rating thresholds can be modified inside DatabaseQueries SQL query
    def __init__(self):
        pass

    def train(self):
        df_recentPopular = DatabaseQueries.getRecentPopularItem()
        print(df_recentPopular.head())
        log = logging.getLogger(__name__)
        log.info("responding to request: %s" % df_recentPopular.head())
        self.recentPopularList = df_recentPopular.itemId.tolist()

    # unlike other models, most popular model doesn't need to predict, just directly recommend
    def predict(self):
        pass

    # directly recommend with the item_id index, based on corresponding rating from high to low
    def recommend(self):
        return self.recentPopularList



