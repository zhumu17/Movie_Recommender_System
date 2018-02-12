# User Type Analyzer
# Determine different type of user, send different user to different recommendation module

class UserAnalyzer(object):
    def __init__(self):
        pass

    def analyze(self, userId, numRatingsPerUser):
        # categorize users into unregistered, new and old
        if userId == -1:
            userType = 'unregistered'
        elif userId in numRatingsPerUser.loc[:,'userId']:
            if numRatingsPerUser.loc[userId,list(numRatingsPerUser)[1]] >= 5: # if the user has already rated more than certain number of items, that's an old user
                userType = 'old'
            else:
                userType = 'new'
        else:
            userType = 'new'

        return userType

    def analyzeAction(self, action):
        if isinstance(action.userId, str):
            return "unregistered"
        else:
            return "registered"
