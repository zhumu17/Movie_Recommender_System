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


    cur.execute("CREATE TABLE inventory (itemId INTEGER PRIMARY KEY NOT NULL, itemName TEXT)")

    cur.execute('''CREATE TABLE itemFeature (itemId INTEGER PRIMARY KEY NOT NULL, itemName TEXT,
    Date TEXT, URL TEXT, unknown INTEGER, Action INTEGER, Adventure INTEGER, Animation INTEGER, Children INTEGER,
    Comedy INTEGER, Crime INTEGER, Documentary INTEGER, Drama INTEGER, Fantasy INTEGER, FilmNoir INTEGER, Horror INTEGER,
    Musical INTEGER, Mystery INTEGER, Romance INTEGER, SciFi INTEGER, Thriller INTEGER, War INTEGER, Western INTEGER)
    ''')

    cur.execute('''CREATE TABLE userFeature (userId INTEGER PRIMARY KEY NOT NULL, age INTEGER, gender_F INTEGER, gender_M INTEGER,
    occupation_administrator INTEGER, occupation_artist INTEGER, occupation_doctor INTEGER, occupation_educator INTEGER,
    occupation_engineer INTEGER, occupation_entertainment INTEGER, occupation_executive INTEGER, occupation_healthcare INTEGER,
    occupation_homemaker INTEGER, occupation_lawyer INTEGER, occupation_librarian INTEGER, occupation_marketing INTEGER,
    occupation_none INTEGER, occupation_other INTEGER, occupation_programmer INTEGER, occupation_retired INTEGER,
    occupation_salesman INTEGER, occupation_scientist INTEGER, occupation_student INTEGER, occupation_technician INTEGER,
    occupation_writer INTEGER)
    ''')

    cur.execute('''CREATE TABLE ratings (ratingIndex INTEGER PRIMARY KEY NOT NULL, userId INTEGER, itemId INTEGER, rating INTEGER,
    FOREIGN KEY(userId) REFERENCES userFeature(userId), FOREIGN KEY(itemId) REFERENCES itemFeature(itemId),
    FOREIGN KEY(itemId) REFERENCES inventory(itemId))
    ''')

    df_inventory.to_sql("inventory", conn, if_exists = 'append', index=False)
    df_itemFeature.to_sql("itemFeature", conn, if_exists='append', index=False)
    df_userFeature.to_sql("userFeature", conn, if_exists='append', index=False)
    df_ratings.to_sql("ratings", conn, if_exists='append', index=False)

    conn.commit()
    conn.close()

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
    GROUP BY userId, ratingIndex, rating; ''', conn)
    conn.commit()
    conn.close()
    return df_numRatingsPerUser


def putNewUser(userId, age, gender, occupation):
    conn = sqlite3.connect('database.sqlite')
    if gender == 'female':
        genderCol = 'gender_F'
    elif gender == 'male':
        genderCol = 'gender_M'
    occupationCol = "occupation_" + str(occupation)

    cur = conn.cursor()
    cur.execute('''INSERT INTO userFeature VALUES(?, ?, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)''', (userId, age))
    if gender == 'female':
        cur.execute('''
            UPDATE userFeature
            SET gender_F = 1
            WHERE userId = ?''', (userId,))
    elif gender == 'male':
        cur.execute('''
            UPDATE userFeature
            SET gender_M = 1
            WHERE userId = ?''', (userId,))
    cur.execute('''
    UPDATE userFeature
    SET ''' + occupationCol + ''' = 1
    WHERE userId= ?''', (userId,))
    conn.commit()
    conn.close()



def putNewRating(userId, itemId, ratingScore):
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    cur.execute('''SELECT COUNT(ratingIndex) FROM ratings''')
    numRatings=cur.fetchone()[0]+1
    cur.execute('''INSERT INTO ratings VALUES(?,?,?,?)''', (numRatings, userId, itemId, ratingScore))
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
  # createTables()
  # putNewUser(945, 15, 'female', 'artist')
  putNewRating(1,2,5)