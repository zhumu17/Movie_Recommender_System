# main.py
# Written in Python 2.7, NOT working in Python 3.5
# simulate different request coming into the system

#######################################################################################################################


from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import numpy as np
import DatabaseQueries
from SearchInventory import searchItem
import videoCrawler, priceCrawler
# from wtforms import validators

app = Flask(__name__)

app.config.from_object('config')
app.secret_key = 'temp'


from Process import Process

configMap = {"numberToServe": 18, "data_dir": "DATA"} # basic configuration
numberToServe = configMap["numberToServe"]
process = Process(configMap)
process.start() # initialize all the modules/classes, load all the data in the database, start the first model training



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
    if 'itemIdRated' in session:
        itemIdRated = session['itemIdRated']
    else:
        itemIdRated = []
    print('itemIdRated in session:',itemIdRated)
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


    itemsRecommended = process.renderRecommendation(userId,numberToServe)  # output recommendations for unregistered user
    itemsRecommended = itemsRecommended.iloc[:, -1].values.flatten()
    print(request.method)


    ############################
    #   REQUEST POST METHOD    #
    ############################
    if request.method == 'POST' and request.form['submit'] == 'searchClip':
        clipNameInput = request.form['clipName']
        clipId = videoCrawler.getVideoId(clipNameInput)
        clipURL = videoCrawler.getVideoURL(clipId)
        session['clipURL'] = clipURL
        return redirect(url_for('index', _anchor='trailerPlayer'))

    if request.method =='POST' and request.form['submit'] == 'selectClip':
        clipNameInput = request.form['clipName']
        clipId = videoCrawler.getVideoId(clipNameInput)
        clipURL = videoCrawler.getVideoURL(clipId)
        session['clipURL'] = clipURL
        session['itemToRate'] = clipNameInput
        return redirect(url_for('index', _anchor='trailerPlayer'))

    if request.method == 'POST' and request.form['submit']=='rateScore':

        itemToRate = session['itemToRate']
        ratingScore = int(request.form['rating'])
        session['ratingScore'] = ratingScore
        df_searched = searchItem(itemToRate)
        print(df_searched)
        if len(df_searched) != 0:
            itemIdRated = df_searched.iloc[0, 0]
            session['itemIdRated'] = int(itemIdRated) # dataframe.iloc returns a numpy array, even just one element, must convert to int!
        if ratingScore >= 4:
            return redirect(url_for('index', _anchor='purchaseMovie'))
        else:
            return redirect(url_for('index', _anchor='header-nav'))

    if request.method == 'POST' and request.form['submit']=='findPrice':
        itemToBuy = request.form['itemToBuy']
        priceAmazon = 1#priceCrawler.getPriceAmazon(itemToBuy)
        priceURLAmazon = 1#priceCrawler.getURLAmazon(itemToBuy)
        priceYouTube = priceCrawler.getPriceYouTube(itemToBuy)
        priceURLYouTube = priceCrawler.getURLYouTube(itemToBuy)
        session['itemToBuy'] = itemToBuy
        session['priceList'] = [priceAmazon, priceYouTube]
        session['priceURLList']=[priceURLAmazon, priceURLYouTube]
        return redirect(url_for('index',_anchor='purchaseMovie'))


    ############################
    #   REQUEST GET METHOD     #
    ############################
    #  if there is a movie rated
    if 'ratingScore' in session:
        itemIdRated = session['itemIdRated']
        ratingScore = session['ratingScore']
        ratingScore = int(ratingScore) # it was a string type by default
        itemsRecommended = process.renderRecommendation(numberToServe=numberToServe, itemId=itemIdRated, ratingScore=ratingScore)
        itemsRecommended = list(itemsRecommended.iloc[:, -1].values)
        # no matter user is registered or not, once item rated, recommend similar item
        if 'username' in session: # user signed in
            userId = session['username']
            DatabaseQueries.putNewRating(userId, itemIdRated, ratingScore)
            if 'priceList' in session and 'priceURLList' in session: # user have gone through the end of routine
                # session.pop('itemToRate', None)
                session.pop('clipURL', None)
                session.pop('ratingScore', None)
                session.pop('itemIdRated', None)
                session.pop('itemToBuy', None)
                session.pop('priceList', None)
                session.pop('priceURLList', None)
            return render_template('index.html', user=userId, itemsRecommended=itemsRecommended, clipURL=clipURL, itemToRate=itemToRate,
                                   ratingScore=ratingScore, priceList=priceList, priceURLList=priceURLList)
        else: # user not signed in
            if 'priceList' in session and 'priceURLList' in session:  # user have gone through the end of routine
                # session.pop('itemToRate', None)
                session.pop('clipURL', None)
                session.pop('ratingScore', None)
                session.pop('itemIdRated', None)
                session.pop('itemToBuy', None)
                session.pop('priceList', None)
                session.pop('priceURLList', None)

            return render_template('index.html', itemsRecommended=itemsRecommended,clipURL=clipURL, itemToRate=itemToRate,
                                   ratingScore=ratingScore, priceList=priceList, priceURLList=priceURLList)

    # if NO movie was rated
    else:
        if 'username' in session: # a registered user
            userId = session['username'] # get userId from cookie
            userId = int(userId) # convert unicode type from user's input to python integer

            itemsRecommended = process.renderRecommendation(userId, numberToServe)
            itemsRecommended = itemsRecommended.iloc[:,-1].values.flatten()
            return render_template('index.html', user = userId, itemsRecommended = itemsRecommended, clipURL=clipURL)
        else:
            userId = -1 # -1 represent an unregistered user
            itemsRecommended = process.renderRecommendation(userId, numberToServe)  # output recommendations for unregistered user
            itemsRecommended = itemsRecommended.iloc[:, -1].values.flatten() # flatten() converts 2D array into 1D, works as well as list()


    return render_template('index.html', itemsRecommended=itemsRecommended, clipURL=clipURL)




@app.route('/login', methods = ['GET','POST'])
def login():
    numUsers = len(DatabaseQueries.getUserFeature())
    if request.method == 'POST':
        userId = request.form['LoginUsername']
        userId = int(userId)

        session['username'] = userId # save cookie
        return redirect(url_for('index'))

    return render_template('login.html', numUsers = numUsers)


@app.route('/logout')
def logout():
    session.pop('username', None) # clear cookie
    return redirect(url_for('index'))


# from wtforms import Form, validators


@app.route('/signup', methods = ['GET','POST'])
def signup():
    # form = SignupForm(request.form)
    numUsers = len(DatabaseQueries.getUserFeature())
    if request.method == 'POST' and request.form['submit'] == 'search': # add form validation later: and form.validate()
        # get new user from input
        userId = numUsers + 1 # new user Id is assigned
        age = request.form['age'] # get user's input from form with input name 'age'
        age = int(age)
        gender = str(request.form['gender'])
        occupation = str(request.form['occupation'])
        # add new user to user database
        DatabaseQueries.putNewUser(userId, age, gender, occupation)

        session['username'] = userId # create session dict for cookie, cuz REST is stateless i.e. memorize NOTHING
        return redirect(url_for('index')) # redirect back to main page

    return render_template('signup.html', numUsers = numUsers)


@app.route('/rateMenu', methods=['GET', 'POST'])
def rateMenu():
    df_inventory = DatabaseQueries.getInventory()
    itemsMenu= df_inventory.iloc[:, -1].values.flatten()
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
    app.run(debug = True)