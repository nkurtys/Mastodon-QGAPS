import mastodon
from mastodon import Mastodon
from datetime import datetime, timedelta
import sqlite3
from bs4 import BeautifulSoup

import os.path


'''
instance: mastodon server, default=mastodon.social
auth_code: Default is False, only needed for first authentication from the device

'''

#HOW TO: 1. create app only once 2. request authentication url 
#3. log into mastodon acc via link 4. log in using access token

# # url = App.auth_request_url(scopes=['read', 'write', 'follow'])
# # print(url)

# App.log_in(
#     code = "SZ5EbCMh5hNhNgWBF8vBGfi3MYmb__rEH_5Otv0vIVw",
#     to_file = 'pytooter_usercred.secret',
#     scopes=['read', 'write', 'follow']
# )
# print("logged in")

# App = Mastodon(access_token='pytooter_usercred.secret')
# App.toot("Test post via API using OAuth")

def makeApp(instance='mastodon.social', auth_code=False):
#Initialize Application if no client_file given
    if os.path.isfile('pytooter_clientcred.secret') == False:
        Mastodon.create_app(
        "APP_NAME",
        api_base_url = instance,
        to_file = 'pytooter_clientcred.secret'
        )
        print("App created")

#Start up App
    App = Mastodon(
    client_id = 'pytooter_clientcred.secret',
    api_base_url = instance
    )
#Case 1 - no auth code given but file with access token availble - Log in via access token
    if auth_code == False and os.path.isfile('pytooter_usercred.secret') == True:
    #Acces Mastodon via acces token
        App = Mastodon(access_token='pytooter_usercred.secret')
        print("logged in")        
        return App
#Case 2 - auth code given - log in via access token and create/overwrite file
    if auth_code:
        App.log_in(
            code = auth_code,
            to_file = 'pytooter_usercred.secret',
            scopes=['read', 'write', 'follow']
        )    
        return App
#Case 3 - No authentication code and no file - Request authentication URL 
    if auth_code == False and os.path.isfile('pytooter_usercred.secret') == False:
        url = App.auth_request_url(scopes=['read', 'write', 'follow'])
        print(url)
        return False

def searchPeriod(instance, query = None, start_date = None, end_date = None, first = False):
    #Log into App
    App = makeApp(instance)

    #Access Database
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    if first == True:
        cursor.execute("DROP TABLE IF EXISTS example")
    cursor.execute("CREATE TABLE IF NOT EXISTS example (id int NOT NULL, created_at, language, uri, url, content)")
    print("Connected to table")
    

    # Define initial parameters
    cursor.execute("SELECT COUNT(*) FROM example")
    count_old = cursor.fetchone()[0]
    limit = 40
    min_id = None
    max_id = None
    now = datetime.now()
    if start_date == '' or end_date == '':
        print("Given None Datetypes")
        raise AttributeError
    elif datetime.fromisoformat(end_date) <= now:
        print("Transforming Dates...")
        min_id = ( int( (datetime.fromisoformat(start_date)).timestamp() ) << 16 ) * 1000
        max_id = ( int( (datetime.fromisoformat(end_date)).timestamp() ) << 16 ) * 1000
        print("Dates succesfully transformed.")

        cursor.execute("SELECT COUNT(*) FROM example WHERE id > 'min_id' AND id < 'max_id'")
        c = cursor.fetchone()[0]
        if (c != 0):
            #return warning that some datapoints are already inserted and to maybe select a time period after the last id
            print ("Warning: Dublicates in databse! " + str(c))
            print(c)
        
    else:
        print("Different Date Error...")
        raise AttributeError

    
    start_time = now.strftime("%H:%M:%S")
    current_time = now.strftime("%H:%M:%S")
    print("Started fetching and waiting for ratelimit to reset...", start_time)

# Fetch statuses fitting the query page by page
    while True:
        # Fetch a page of statuses
        if query ==  None:
            #Fetch a page of statuses
            statuses = App.timeline_public(limit=limit, max_id=max_id, min_id=min_id)
    
        else:
            results = App.search(query, max_id=max_id, min_id=min_id)
            statuses = results["statuses"] + App.timeline_hashtag(query, limit=limit, max_id=max_id, min_id=min_id)
            

        # Load Statuses into Database
        for status in statuses:
            
            html = status['content']
            soup = BeautifulSoup(html, features="html.parser")
            status['content'] = soup.get_text()
            try:
                cursor.execute("INSERT INTO example VALUES (:id, :created_at, :language, :uri, :url, :content)", (status))
                connection.commit() 
            except sqlite3.IntegrityError as err:
                continue
            except DeprecationWarning as deperr:
                print("dumb warning")

        # Check if there are more pages
        if len(statuses) <= 1:
            print("No more statuses found...saving to database.")
            break  # No more pages

        # Set max_id for the next page
        #max_id = statuses[-1]['id']
        min_id = statuses[0]['id']

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("ST: " + start_time + ". Still fetching and waiting fo ratelimit to reset..." + current_time)
    cursor.execute("SELECT COUNT(*) FROM example")
    count = cursor.fetchone()[0]
    connection.close()
    print("Finished loading into the Database.")
    return [count,count_old]
    
        
def activityPERweek(start_date = "2016-02-02", end_date = False):
    App = makeApp('mastodon.social')
    limit = 40  # Number of statuses per page
    week = timedelta(days = 7)
    lent = 0

#prep paameters
    pre_min_id = start_date
    pre_max_id = start_date + week
    last_max_id = end_date
    
    #print("prep done")

#calculate how many weeks between start and end date
    id = last_max_id
    small_id = pre_min_id
    
    weeks = 0
    while id > small_id:
        id = id-week
        # if id < small_id:
        #     #was mit leftover tagen
        #     continue
        weeks = weeks + 1
    print("Collecting toots of " + str(weeks) + " weeks containing the term 'covid'...")

#Connect to sql database
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS example")
    cursor.execute("CREATE TABLE IF NOT EXISTS example (id int NOT NULL UNIQUE, created_at, language, uri, url, content)")


#Fetch per week
    for period in range(weeks):

        min_id = ( int( ( pre_min_id + (timedelta(days = period*7)) ).timestamp()  ) << 16 ) * 1000
        max_id = ( int( ( pre_max_id + (timedelta(days = period*7)) ).timestamp()  ) << 16 ) * 1000

        week_lent = 0
        # Fetch timeline statuses page by page 
        while True:
            result = App.search("coxiella", max_id= max_id, min_id=min_id)
        
            statuses = result["statuses"]
            hashtags = result["hashtags"]
            
            #print(len(statuses))
             #Check if there are more pages
            if len(statuses) <= 1:
                break  # No more pages
            else:
                lent = lent + len(statuses) - 1
                week_lent = week_lent + len(statuses) -1

            #Set max_id for the next page
            if max_id > min_id:
                max_id = statuses[-1]['id']
            else:
                break
            
            #Insert status into sql database
            if len(statuses) > 0:
                try:
                    cursor.executemany("INSERT INTO example VALUES (:id, :created_at, :language, :uri, :url, :content)", (statuses[0],))
                    connection.commit() 
                except sqlite3.IntegrityError as err:
                    continue

        print("Collected " + str(week_lent) + " toots in week " + str(period+1) + ".")
    print("Collected a total of " + str(lent) + " toots mentioning 'covid'.")
            

#makeApp('mastodon.social')
#activityPERweek(datetime(2021,1,1,00,1), datetime(2021,6,30,23,59))
#searchPeriod("mastodon.social", query= "qfever", start_date="2016-03-15", end_date="2024-05-03", first=True)

connection = sqlite3.connect("test.db")
cursor = connection.cursor()
cursor.execute("SELECT content FROM example")
rows = cursor.fetchall()
# for row in rows:
#     # html = row[0]
#     # soup = BeautifulSoup(html, features="html.parser")
#     # print(soup.get_text())
#     #print(html)
#     print(row)
print(len(rows))

# connection.commit()


#Functions

    # qfever = App.search("covid")
    # print(type(qfever))
    # print(len(qfever))
    # print(qfever["statuses"][0]["content"])
    # for toot in range(len(qfever["statuses"])-1):
    #         print('\n')
    #         html = qfever["statuses"][toot]["uri"]
    #         #soup = BeautifulSoup(html, features="html.parser")
    #         #print(soup.get_text())
    #         print(html)