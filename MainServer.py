# main.py
# Written in Python 2.7, NOT working in Python 3.5
# simulate different request coming into the system

#######################################################################################################################


from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import DatabaseQueries
from SearchInventory import searchItem
# from wtforms import validators

app = Flask(__name__)

app.config.from_object('config')
app.secret_key = 'temp'


from Process import Process

configMap = {"numberToServe": 12, "data_dir": "DATA"} # basic configuration
numberToServe = configMap["numberToServe"]
process = Process(configMap)
process.start() # initialize all the modules/classes, load all the data in the database, start the first model training



###############################
# Backend API
###############################

@app.route('/', methods = ['GET','POST'])
def index():
    # show recommendations
    # session.pop('username', None) # for debug purpose
    # session.pop('itemToRate', None)
    # session.pop('itemIdToRate', None)
    # session.pop('ratingScore', None)
    if request.method == 'POST':
        itemNameInput = request.form['itemName']  # get the form of searching itemName from index.html
        df_searched = searchItem(itemNameInput)
        if len(df_searched) != 0:
            itemIdToRate = df_searched.iloc[0,0]
            df_searched = df_searched.reset_index()
            itemToRate = df_searched.loc[0, 'itemName']
            session['itemToRate'] = itemToRate
            session['itemIdToRate'] = itemIdToRate
            return redirect(url_for('rateItem'))
        else:
            return redirect(url_for('rateItemNotFound'))

    if 'ratingScore' in session:
        itemIdToRate = session['itemIdToRate']
        ratingScore = session['ratingScore']
        ratingScore = int(ratingScore) # it was a string type by default
        itemsRecommended = process.renderRecommendation(numberToServe=numberToServe, itemId=itemIdToRate, ratingScore=ratingScore)
        itemsRecommended = list(itemsRecommended.iloc[:, -1].values)
        # no matter user is registered or not, once item rated, recommend similar item
        if 'username' in session:
            userId = session['username']
            DatabaseQueries.putNewRating(userId, itemIdToRate, ratingScore)
            session.pop('itemToRate', None)
            session.pop('itemIdToRate', None)
            session.pop('ratingScore', None)
            return render_template('index.html', user=userId, itemsRecommended=itemsRecommended)
        else:
            session.pop('itemToRate', None)
            session.pop('itemIdToRate', None)
            session.pop('ratingScore', None)
            return render_template('index.html', itemsRecommended=itemsRecommended)

    else:
        if 'username' in session: # a registered user
            userId = session['username'] # get userId from cookie
            userId = int(userId) # convert unicode type from user's input to python integer

            itemsRecommended = process.renderRecommendation(userId, numberToServe)
            itemsRecommended = itemsRecommended.iloc[:,-1].values.flatten()
            return render_template('index.html', user = userId, itemsRecommended = itemsRecommended)
        else:
            userId = -1 # -1 represent an unregistered user
            itemsRecommended = process.renderRecommendation(userId, numberToServe)  # output recommendations for unregistered user
            itemsRecommended = itemsRecommended.iloc[:, -1].values.flatten() # flatten() converts 2D array into 1D, works as well as list()



    return render_template('index.html', itemsRecommended=itemsRecommended)

@app.route('/login', methods = ['GET','POST'])
def login():
    numUsers = len(DatabaseQueries.getUserFeature())
    if request.method == 'POST':
        userId = request.form['LoginUsername']
        session['username'] = userId # save cookie
        return redirect(url_for('index'))

    return render_template('login.html', numUsers = numUsers)


@app.route('/logout')
def logout():
    session.pop('username', None) # clear cookie
    return redirect(url_for('index'))


# from wtforms import Form, validators
# class SignupForm(Form):
#     userId =

@app.route('/signup', methods = ['GET','POST'])
def signup():
    # form = SignupForm(request.form)
    numUsers = len(DatabaseQueries.getUserFeature())
    if request.method == 'POST' : # add form validation later: and form.validate()
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



@app.route('/rateItem', methods=['GET','POST'])
def rateItem():
    itemToRate = session['itemToRate']
    if request.method == 'POST':
        ratingScore = str(request.form['rating'])
        session['ratingScore'] = ratingScore
        return redirect(url_for('index'))  # redirect back to main page

    return render_template('rateItem.html', itemToRate = itemToRate)


@app.route('/rateItemNotFound', methods=['GET','POST'])
def rateItemNotFound():
    if request.method == 'POST':
        itemNameInput = request.form['itemName']  # get the form of searching itemName from index.html
        df_searched = searchItem(itemNameInput)
        if len(df_searched) != 0:
            itemIdToRate = df_searched.iloc[0,0]
            df_searched = df_searched.reset_index()
            itemToRate = df_searched.loc[0, 'itemName']
            session['itemToRate'] = itemToRate
            session['itemIdToRate'] = itemIdToRate
            return redirect(url_for('rateItem'))
        else:
            return redirect(url_for('rateItemNotFound'))
    return render_template('rateItemNotFound.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.errorhandler(500)
def value_error(error):
    return render_template('505.html')


if __name__ == '__main__':
    app.run(debug = True)