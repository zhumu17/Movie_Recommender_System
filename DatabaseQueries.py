import sqlite3
import pandas as pd


def createTables():
    df_inventory = pd.read_csv('./DATA/inventory.csv')
    df_itemFeature = pd.read_csv('./DATA/itemFeature.csv')
    df_userFeature = pd.read_csv('./DATA/userFeature.csv')
    df_ratings = pd.read_csv('./DATA/ratings.csv')
    conn = sqlite3.connect('database.sqlite')
    conn.text_factory = str
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS inventory")
    cur.execute("DROP TABLE IF EXISTS itemFeature")
    cur.execute("DROP TABLE IF EXISTS userFeature")
    cur.execute("DROP TABLE IF EXISTS ratings")


    cur.execute("CREATE TABLE inventory (itemId INTEGER PRIMARY KEY NOT NULL, itemName TEXT, itemImageURL TEXT)")

    cur.execute('''CREATE TABLE itemFeature (itemId INTEGER PRIMARY KEY NOT NULL, itemName TEXT,
    Year INTEGER, Action INTEGER, Adventure INTEGER, Animation INTEGER, Children INTEGER,
    Comedy INTEGER, Crime INTEGER, Documentary INTEGER, Drama INTEGER, Fantasy INTEGER, FilmNoir INTEGER, Horror INTEGER, IMAX INTEGER,
    Musical INTEGER, Mystery INTEGER, Romance INTEGER, SciFi INTEGER, Thriller INTEGER, War INTEGER, Western INTEGER)
    ''')

    cur.execute('''CREATE TABLE userFeature (userId INTEGER PRIMARY KEY NOT NULL, Year INTEGER, Action INTEGER, Adventure INTEGER, Animation INTEGER, Children INTEGER,
    Comedy INTEGER, Crime INTEGER, Documentary INTEGER, Drama INTEGER, Fantasy INTEGER, FilmNoir INTEGER, Horror INTEGER, IMAX INTEGER,
    Musical INTEGER, Mystery INTEGER, Romance INTEGER, SciFi INTEGER, Thriller INTEGER, War INTEGER, Western INTEGER)
    ''')

    cur.execute('''CREATE TABLE ratings (userId INTEGER, itemId INTEGER, rating INTEGER,
    FOREIGN KEY(userId) REFERENCES userFeature(userId), FOREIGN KEY(itemId) REFERENCES itemFeature(itemId),
    FOREIGN KEY(itemId) REFERENCES inventory(itemId))
    ''')

    df_inventory.to_sql("inventory", conn, if_exists = 'append', index=False)
    df_itemFeature.to_sql("itemFeature", conn, if_exists='append', index=False)
    df_userFeature.to_sql("userFeature", conn, if_exists='append', index=False)
    df_ratings.to_sql("ratings", conn, if_exists='append', index=False)

    conn.commit()
    conn.close()

# def cleanExcessiveRatings():
#     conn = sqlite3.connect('database.sqlite')
#     df_numItems = pd.read_sql_query(''' SELECT MAX(itemId) FROM itemFeature;''', conn)
#     print(df_numItems.iloc[0,0])
#     numItems = df_numItems.iloc[0,0]
#     print(numItems)
#     cur = conn.cursor()
#     cur.execute(''' DELETE FROM ratings
#                     WHERE itemId > ?''', numItems)



def getInventory():
    conn = sqlite3.connect('database.sqlite')
    df_inventory = pd.read_sql_query(''' SELECT * FROM inventory;''', conn)
    return df_inventory

def getItemFeature():
    conn = sqlite3.connect('database.sqlite')
    df_itemFeature = pd.read_sql_query(''' SELECT * FROM itemFeature;''', conn)
    # results = cur.fetchall()
    conn.commit()
    conn.close()
    return df_itemFeature

def getUserFeature():
    conn = sqlite3.connect('database.sqlite')
    df_userFeature = pd.read_sql_query(''' SELECT * FROM userFeature;''', conn)
    conn.commit()
    conn.close()
    return df_userFeature

def getRatings():
    conn = sqlite3.connect('database.sqlite')
    df_ratings = pd.read_sql_query(''' SELECT * FROM ratings;''', conn)
    conn.commit()
    conn.close()
    return df_ratings

def getNumRatingsPerUser():
    conn = sqlite3.connect('database.sqlite')
    df_numRatingsPerUser = pd.read_sql_query('''
    SELECT userId, count(itemId) AS numOfRatings
    FROM ratings
    GROUP BY userId; ''', conn)
    conn.commit()
    conn.close()
    return df_numRatingsPerUser


# def putNewUser(userId, age, gender, occupation):
#     conn = sqlite3.connect('database.sqlite')
#     if gender == 'female':
#         genderCol = 'gender_F'
#     elif gender == 'male':
#         genderCol = 'gender_M'
#     occupationCol = "occupation_" + str(occupation)
#
#     cur = conn.cursor()
#     cur.execute('''INSERT INTO userFeature VALUES(?, ?, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)''', (userId, age))
#     if gender == 'female':
#         cur.execute('''
#             UPDATE userFeature
#             SET gender_F = 1
#             WHERE userId = ?''', (userId,))
#     elif gender == 'male':
#         cur.execute('''
#             UPDATE userFeature
#             SET gender_M = 1
#             WHERE userId = ?''', (userId,))
#     cur.execute('''
#     UPDATE userFeature
#     SET ''' + occupationCol + ''' = 1
#     WHERE userId= ?''', (userId,))
#     conn.commit()
#     conn.close()

def putNewUser(userId, preferences):
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    cur.execute('''INSERT INTO userFeature VALUES(?,0,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (userId,
                preferences[0], preferences[1], preferences[2], preferences[3], preferences[4], preferences[5], preferences[6],
                preferences[7], preferences[8], preferences[9], preferences[10], preferences[11], preferences[12], preferences[13],
                preferences[14], preferences[15], preferences[16], preferences[17], preferences[18], ))

    conn.commit()
    conn.close()


def getRecentPopularItem():
    conn = sqlite3.connect('database.sqlite')
    df_recentPopular = pd.read_sql_query('''
        SELECT I.itemId, I.itemName, I.Year, R.avgRating, R.numRating
        FROM (
        SELECT *
        FROM itemFeature
        WHERE Year >2008
        )  AS I JOIN  (
        SELECT itemId, AVG(rating) AS avgRating, COUNT(rating) AS numRating
        FROM ratings
        GROUP BY itemId
        HAVING numRating>15
        ORDER BY avgRating DESC
         ) AS R
        ON I.itemId = R.itemId
        ORDER BY R.avgRating DESC
        ;
    ''', conn)


    conn.commit()
    conn.close()
    return df_recentPopular



def putNewRating(userId, itemId, ratingScore):
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT COUNT(rating) FROM ratings''')
    numRatings=cur.fetchone()[0]+1
    cur.execute('''INSERT INTO ratings VALUES(?,?,?)''', (userId, itemId, ratingScore))
    conn.commit()
    conn.close()



def replaceTable():
    conn = sqlite3.connect('database.sqlite')
    conn.text_factory = str
    cur = conn.cursor()
    conn.executescript('''
        PRAGMA foreign_keys=off;
        BEGIN TRANSACTION;
        ALTER TABLE itemFeature RENAME TO old_table;
        /*create a new table with the same column names and types while
        defining a primary key for the desired column*/
        CREATE TABLE new_table (col_1 TEXT PRIMARY KEY NOT NULL, col_2 TEXT);
        INSERT INTO new_table SELECT * FROM old_table;
        DROP TABLE old_table;
        COMMIT TRANSACTION;
        PRAGMA foreign_keys=on;''')
    conn.commit()
    conn.close()




if __name__ == "__main__":
  createTables()
  # cleanExcessiveRatings()
  # putNewUser(945, 15, 'female', 'artist')
  # putNewRating(1,2,5)