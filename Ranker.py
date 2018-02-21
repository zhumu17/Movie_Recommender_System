# Ranker - just rank the recommended items

import logging
import numpy as np
import DatabaseQueries

# rank the items from each recommendation module
# highly influenced by business strategy and varies from system to system


class Ranker(object):
    logging.basicConfig(level=logging.INFO)

    def __init__(self):
        self.ratings = DatabaseQueries.getRatings()
        self.log = logging.getLogger(__name__)

    def rank(self, recommendations, userId, numberToServe):
        # recommendations is a dictionary of lists {RecType: Items}, RecType can be "online", "offline", "popular"
        # if the userId is -1, it is an unregistered user.
        # else remove the already watched item
        self.log.info("Recommendations received in Ranker: %s" % recommendations)
        self.log.info("Recommendation types received in Ranker: %s" % recommendations.keys())

        results = []
        # rankings have priorities: itemBased -> userBased -> collaborativeFiltering -> popular
        if "itemBased" in recommendations:  # online exists as long as user has been active
            results.extend(recommendations["itemBased"])  # remove the one just got rated

        if "collaborativeFiltering" in recommendations:  # offline exist only if user are registered, the recs could be from CF or LR
            results.extend(recommendations["collaborativeFiltering"])

        if "userBased" in recommendations:  # online exists as long as user has been active
            results.extend(recommendations["userBased"])  # should only has one

        if "popular" in recommendations:  # most popular should always exist
            # if there is no personalized recs, the remaining should be filled by most popular
            results.extend(recommendations["popular"][:numberToServe*2])
        else:
            self.log.error("recommendations do not contain popular items")


        # remove the already visited items from
        if userId == -1:
            ratedItems = set([]) # unregistered user doesn't have any rating history
        else:
            ratedItems = set(self.ratings[self.ratings.loc[:, "userId"] == userId].loc[:, "itemId"])


        # try:
        # results = list(set(results) - ratedItems)[:numberToServe]
        # except ValueError:
        #     results = np.random.choice(results, numberToServe, replace=False)
        results = list(set(results[:numberToServe*2])) # remove duplcates among different recommendation cases
        results = np.random.choice(results, numberToServe, replace=False)
        return list(results)



