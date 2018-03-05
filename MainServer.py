# main.py
# Written in Python 2.7, NOT working in Python 3.5
# simulate different request coming into the system

#######################################################################################################################


from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import numpy as np
import DatabaseQueries
from SearchInventory import searchItem
import videoCrawler, priceCrawler
import math
import UserAnalyzer
# from wtforms import validators

app = Flask(__name__)

app.config.from_object('config')
app.secret_key = 'temp'


from FlowControl import FlowControl

configMap = {"numberToServe": 12, "data_dir": "DATA"} # basic configuration
numberToServe = configMap["numberToServe"]
flowControl = FlowControl(configMap)
flowControl.start() # initialize all the modules/classes, load all the data in the database, start the first model training



###############################
# Backend API
###############################

@app.route('/', methods = ['GET','POST']) # Home page shows recommendations
def index():
    # session.pop('username', None) # for debug purpose
    # session.pop('itemToRate', None)
    # session.pop('itemIdRated', None)
    # session.pop('clipURL', None)
    # session.pop('ratingScore', None)
    # session.pop('itemToBuy', None)
    # session.pop('priceList', None)
    # session.pop('priceURLList', None)
    print(request.method)
    if 'username' in session:
        username = session['username']
    else:
        username = []
    print(username)
    if 'userId' in session:
        userId = session['userId']
    else:
        userId = -1
    print('userId in session:', userId)
    if 'itemToRate' in session:
        itemToRate = session['itemToRate']
    else:
        itemToRate = []
    print('itemToRate in session:',itemToRate)
    if 'clipURL' in session:
        clipURL = session['clipURL']
    else:
        clipURL = []
    print('clipURL in session:', clipURL)
    if 'ratingScore' in session:
        ratingScore = session['ratingScore']
    else:
        ratingScore = []
    print('ratingScore in session:', ratingScore)
    if 'userPreferences' in session:
        userPreference = session['userPreferences']
    else:
        userPreference = []
    print('userPreferences in session:', userPreference)
    if 'itemIdRated' in session:
        itemIdRated = session['itemIdRated']
    else:
        itemIdRated = []
    print('itemIdRated in session:',itemIdRated)
    if 'watchFullMovie' in session:
        watchFullMovie = session['watchFullMovie']
    else:
        watchFullMovie = []
    print('watchFullMovie in session:', watchFullMovie)
    if 'itemToBuy' in session:
        itemToBuy = session['itemToBuy']
    else:
        itemToBuy = []
    print('itemToBuy in session:', itemToBuy)
    if 'priceList' in session:
        priceList = session['priceList']
    else:
        priceList = []
    print('priceList in session:', priceList)
    if 'priceURLList' in session:
        priceURLList = session['priceURLList']
    else:
        priceURLList = []
    print('priceURLList in session', priceURLList)






    # itemsRecommended = {}
    itemsRecommended = {'classical': [], 'recentPopular':[], 'itemBased': [], 'userBased': [] }
    itemsImageURL = {'classical': [], 'itemBased': [], 'userBased': [] }
    # Other the recommendation cases will be covered specifically later
    itemsRecommended['classical'], itemsImageURL['classical'] = flowControl.renderRecommendation(userId = -1, numberToServe = numberToServe, classical=1)  # output recommendations for unregistered user
    itemsRecommended['recentPopular'], itemsImageURL['recentPopular'] = flowControl.renderRecommendation(userId = -1, numberToServe = numberToServe)  # output recommendations for unregistered user


    print(request.method)


    ############################
    #   REQUEST POST METHOD    #
    ############################
    if request.method == 'POST' and request.form['submit'] == 'searchClip':
        clipNameInput = request.form['clipName']
        clipId = videoCrawler.getVideoId(clipNameInput)
        clipURL = videoCrawler.getVideoURL(clipId)
        session['itemToRate'] = clipNameInput
        session['clipURL'] = clipURL
        session.pop('ratingScore', None)
        session.pop('watchFullMovie', None)
        return redirect(url_for('index', _anchor='trailerPlayer'))

    if request.method =='POST' and request.form['submit'] == 'selectClip':
        clipNameInput = request.form['clipName']
        print("clipName Input is : " , clipNameInput)
        clipId = videoCrawler.getVideoId(clipNameInput)
        clipURL = videoCrawler.getVideoURL(clipId)
        print("clip Name Input URL is : ", clipURL)
        session['itemToRate'] = clipNameInput
        session['clipURL'] = clipURL
        session.pop('ratingScore', None)
        session.pop('watchFullMovie', None)

        return redirect(url_for('index', _anchor='trailerPlayer'))

    if request.method == 'POST' and request.form['submit']=='rateScore':

        itemToRate = session['itemToRate']
        if request.form.get('rating', None) == None:
            ratingScore = 1
        else:
            ratingScore = int(request.form['rating'])
        # if ratingScore >=4:
        #     if session['ratingScore']:
        #         session['ratingScoreHighest'] = np.maximum(ratingScore, session['ratingScore'])
        #     else:
        #         session['ratingScoreHighest'] = ratingScore
        session['ratingScore'] = ratingScore

        df_searched = searchItem(itemToRate)
        # print(df_searched)
        # print(len(df_searched))
        # print("--------------")

        if len(df_searched) != 0:
            itemIdRated = df_searched.loc[df_searched.index[0],'itemId']

            session['itemIdRated'] = int(itemIdRated) # dataframe.iloc returns a numpy array, even just one element, must convert to int!
        else:
            session['itemIdRated'] = [] # not in inventory, not for item based recommendation
        if ratingScore <= 3:
            session.pop('clipURL',None)
            session.pop('ratingScore', None)
        return redirect(url_for('index', _anchor = 'trailerPlayer'))

    if request.method == 'POST' and request.form['submit'] == 'watchFullMovie': # better to use anchor tag scroll down without refreshing
        session['watchFullMovie'] = True
        return redirect(url_for('index', _anchor='purchaseMovie'))


    if request.method == 'POST' and request.form['submit']=='findPrice':
        itemToBuy = request.form['itemToBuy']
        priceAmazon = priceCrawler.getPriceAmazon(itemToBuy)
        priceURLAmazon = priceCrawler.getURLAmazon(itemToBuy)
        priceYouTube = priceCrawler.getPriceYouTube(itemToBuy)
        priceURLYouTube = priceCrawler.getURLYouTube(itemToBuy)
        priceITunes, priceURLITunes = priceCrawler.getPriceITunes(itemToBuy)
        session['itemToBuy'] = itemToBuy
        session['priceList'] = [priceAmazon, priceYouTube, priceITunes]
        session['priceURLList']=[priceURLAmazon, priceURLYouTube, priceURLITunes]
        return redirect(url_for('index',_anchor='purchaseMovie'))


    ############################
    #   REQUEST GET METHOD     #
    ############################
    #  if there is a movie rated
    if 'ratingScore' in session :
        # -------------------------------------------
        # first check if the item is selected from inventory or searched from outside
        if session['itemIdRated']: # rated item is IN inventory
            itemIdRated = session['itemIdRated']
            ratingScore = session['ratingScore']
            ratingScore = int(ratingScore) # it was a string type by default
            # classical category was treated in the beginning
            itemsRecommended['itemBased'], itemsImageURL['itemBased'] = flowControl.renderRecommendation(numberToServe=numberToServe, itemId=itemIdRated, ratingScore=ratingScore)
            if 'username' in session:  # a registered user
                userId = session['username']  # get userId from cookie
                userId = int(userId)  # convert unicode type from user's input to python integer
                userPreference = session['userPreference']
            itemsRecommended['userBased'], itemsImageURL['userBased'] = flowControl.renderRecommendation(userId,numberToServe, userPreference=userPreference)  # output recommendations for unregistered user
        else: # rated item is NOT in the inventory
            if 'username' in session:  # a registered user
                userId = session['username']  # get userId from cookie
                userId = int(userId)  # convert unicode type from user's input to python integer
                userPreference = session['userPreference']
                itemsRecommended['userBased'], itemsImageURL['userBased'] = flowControl.renderRecommendation(userId,numberToServe,userPreference=userPreference)  # output recommendations for unregistered user
            else: # treated in the beginning
                userId = -1  # -1 represent an unregistered user
                itemsRecommended['classical'], itemsImageURL['classical'] = flowControl.renderRecommendation(userId=-1, numberToServe=numberToServe, classical=1)  # output recommendations for unregistered user
                itemsRecommended['recentPopular'], itemsImageURL['recentPopular'] = flowControl.renderRecommendation(userId=-1, numberToServe=numberToServe)  # output recommendations for unregistered user

        # check if user signed in, if so then record the rating
        if 'username' in session: # user signed in
            userId = session['username']
            DatabaseQueries.putNewRating(userId, itemIdRated, ratingScore)
        else:
            userId = []
        if 'watchFullMovie' in session and 'priceList' not in session:
            watchFullMovie = session['watchFullMovie'] # depend on wether user want to watch full movie, show compare price session in html
            return render_template('index.html', itemsRecommended=itemsRecommended, itemsImageURL=itemsImageURL, clipURL=clipURL, itemToRate=itemToRate,
                                   ratingScore=ratingScore, watchFullMovie=watchFullMovie)
        if 'priceList' in session: # user have gone through the end of routine
            # session.pop('itemToRate', None)
            # session.pop('clipURL', None)
            # session.pop('ratingScore', None)
            # session.pop('itemIdRated', None)
            # session.pop('watchFullMovie', None)
            session.pop('itemToBuy', None)
            session.pop('priceList', None)
            session.pop('priceURLList', None)

        return render_template('index.html', userId=userId, itemsRecommended=itemsRecommended, itemsImageURL=itemsImageURL, clipURL=clipURL, itemToRate=itemToRate,
                               ratingScore=ratingScore, watchFullMovie=watchFullMovie, priceList=priceList, priceURLList=priceURLList)

    # if NO movie was rated or rated movie is NOT in inventory,  no rating score then no purchase session
    else:
        if 'username' in session: # a registered user
            userId = session['username'] # get userId from cookie
            userId = int(userId) # convert unicode type from user's input to python integer

            if 'userPreference' in session:
                userPreference = session['userPreference']
            else:
                df_userFeatures = DatabaseQueries.getUserFeature()
                df_userFeatures.index = df_userFeatures.index + 1
                userPreference = list(df_userFeatures.loc[userId,'Action':])
            itemsRecommended['userBased'], itemsImageURL['userBased'] = flowControl.renderRecommendation(userId, numberToServe, userPreference=userPreference)  # output recommendations for unregistered user
            return render_template('index.html', userId = userId, itemsRecommended = itemsRecommended, itemsImageURL=itemsImageURL, clipURL=clipURL)
        else:
            userId = -1 # -1 represent an unregistered user
            itemsRecommended['classical'], itemsImageURL['classical'] = flowControl.renderRecommendation(userId=-1, numberToServe=numberToServe, classical=1)  # output recommendations for unregistered user
            itemsRecommended['recentPopular'], itemsImageURL['recentPopular'] = flowControl.renderRecommendation(userId=-1, numberToServe=numberToServe)  # output recommendations for unregistered user

    return render_template('index.html', itemsRecommended=itemsRecommended, itemsImageURL=itemsImageURL, clipURL=clipURL)




@app.route('/login', methods = ['GET','POST'])
def login():
    session.pop('clipURL', None)
    session.pop('ratingScore', None)
    session.pop('itemIdRated', None)
    session.pop('watchFullMovie', None)
    session.pop('itemToBuy', None)
    session.pop('priceList', None)
    session.pop('priceURLList', None)
    numUsers = len(DatabaseQueries.getUserFeature())
    if request.method == 'POST':
        userId = request.form['LoginUsername']
        userId = int(userId)

        session['username'] = userId # save cookie
        return redirect(url_for('index'))

    return render_template('login.html', numUsers = numUsers)


@app.route('/logout')
def logout():
    session.pop('clipURL', None)
    session.pop('ratingScore', None)
    session.pop('itemIdRated', None)
    session.pop('watchFullMovie', None)
    session.pop('itemToBuy', None)
    session.pop('priceList', None)
    session.pop('priceURLList', None)
    session.pop('username', None) # clear cookie
    return redirect(url_for('index'))


# from wtforms import Form, validators


@app.route('/signup', methods = ['GET','POST'])
def signup():
    session.pop('clipURL', None)
    session.pop('ratingScore', None)
    session.pop('itemIdRated', None)
    session.pop('watchFullMovie', None)
    session.pop('itemToBuy', None)
    session.pop('priceList', None)
    session.pop('priceURLList', None)
    # form = SignupForm(request.form)
    numUsers = len(DatabaseQueries.getUserFeature())
    if request.method == 'POST': #
        # get new user from input
        userId = numUsers + 1 # new user Id is assigned
        # age = request.form['age'] # get user's input from form with input name 'age'
        # age = int(age)
        # gender = str(request.form['gender'])
        # occupation = str(request.form['occupation'])
        # # add new user to user database
        # DatabaseQueries.putNewUser(userId, age, gender, occupation)
        preferences = np.zeros((19, 1))
        preferences[0] = request.form.get('Action')
        preferences[1] = request.form.get('Adventure')
        preferences[2] = request.form.get('Animation')
        preferences[3] = request.form.get('Children')
        preferences[4] = request.form.get('Comedy')
        preferences[5] = request.form.get('Crime')
        preferences[6] = request.form.get('Documentary')
        preferences[7] = request.form.get('Drama')
        preferences[8] = request.form.get('Fantasy')
        preferences[9] = request.form.get('FilmNoir')
        preferences[10] = request.form.get('Horror')
        preferences[11] = request.form.get('IMAX')
        preferences[12] = request.form.get('Musical')
        preferences[13] = request.form.get('Mystery')
        preferences[14] = request.form.get('Romance')
        preferences[15] = request.form.get('SciFi')
        preferences[16] = request.form.get('Thriller')
        preferences[17] = request.form.get('War')
        preferences[18] = request.form.get('Western')
        for i, value in enumerate(preferences):
            if math.isnan(value):
                preferences[i] = 0
        preferences = list(preferences.flatten())
        # print(preferences)

        DatabaseQueries.putNewUser(userId, preferences)
        session['username'] = userId # create session dict for cookie, cuz REST is stateless i.e. memorize NOTHING
        session['userPreference'] = preferences
        return redirect(url_for('index')) # redirect back to main page

    return render_template('signup.html', numUsers = numUsers)


@app.route('/rateMenu', methods=['GET', 'POST'])
def rateMenu():
    df_inventory = DatabaseQueries.getInventory()
    itemsMenu= df_inventory.loc[:, 'itemName'].values.flatten()
    itemsMenu = list(itemsMenu) # list is to separate the array with comma
    itemsMenu = np.random.choice(itemsMenu,16)
    print(itemsMenu)
    print(type(itemsMenu))

    if request.method == 'POST' :
        if request.form['submit'] == 'search':
            itemNameInput = request.form['itemName']  # get the form of searching itemName from index.html
        elif request.form['submit'] == 'select':
            itemNameInput = request.form['itemSelect']

        # print(itemNameInput)
        df_searched = searchItem(itemNameInput)
        # print(df_searched)
        if len(df_searched) != 0:
            itemIdRated = df_searched.iloc[0,0]
            df_searched = df_searched.reset_index()
            itemToRate = df_searched.loc[0, 'itemName']
            session['itemToRate'] = itemToRate
            session['itemIdRated'] = itemIdRated
            return redirect(url_for('rateItem'))
        else:
            return redirect(url_for('rateItemNotFound'))



    return render_template('rateMenu.html', itemsMenu = itemsMenu)


@app.route('/rateItem', methods=['GET','POST'])
def rateItem():
    itemToRate = session['itemToRate']
    if request.method == 'POST':
        ratingScore = int(request.form['rating'])
        session['ratingScore'] = ratingScore
        # return redirect(url_for('index'))  # redirect back to main page
        return redirect(url_for('thanksForRating'))

    return render_template('rateItem.html', itemToRate = itemToRate)


@app.route('/rateItemNotFound', methods=['GET','POST'])
def rateItemNotFound():
    if request.method == 'POST':
        itemNameInput = request.form['itemName']  # get the form of searching itemName from index.html
        df_searched = searchItem(itemNameInput)
        if len(df_searched) != 0:
            itemIdRated = df_searched.iloc[0,0]
            df_searched = df_searched.reset_index()
            itemToRate = df_searched.loc[0, 'itemName']
            session['itemToRate'] = itemToRate
            session['itemIdRated'] = itemIdRated
            return redirect(url_for('rateItem'))
        else:
            return redirect(url_for('rateItemNotFound'))
    return render_template('rateItemNotFound.html')


@app.route('/thanksForRating')
def thanksForRating():
    ratingScore = session['ratingScore']
    return render_template('thanksForRating.html', ratingScore = ratingScore)


@app.errorhandler(400)
def value_error(error):
    return render_template('400.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html')


if __name__ == '__main__':
    app.run(debug = False)