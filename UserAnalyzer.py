# User Type Analyzer
# Determine different type of user, send different user to different recommendation module

class UserAnalyzer(object):
    def __init__(self):
        pass

    def analyze(self, userId, numRatingsPerUser):
        # categorize users into unregistered, new and old

        # print(numRatingsPerUser)
        if userId == -1:
            userType = 'unregistered'
        elif userId in numRatingsPerUser.loc[:,'userId']:
            # print(userId)
            # print(numRatingsPerUser.loc[userId,'numOfRatings'])
            if numRatingsPerUser.loc[userId,'numOfRatings'] >= 10: # if the user has already rated more than certain number of items, that's an old user
                userType = 'old'
            else:
                userType = 'new'
        else:
            userType = 'new'

        return userType


