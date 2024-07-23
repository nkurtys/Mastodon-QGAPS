from mastodon import Mastodon
#Mastodon ID - timestamp conversion
from datetime import datetime, timedelta
#html conversion
from bs4 import BeautifulSoup
#sort list
from operator import itemgetter
#for reading auth files
import os.path
#sqlite import
import sqlite3

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
    if os.path.isfile('Q-GAPS-WebApp/app/pytooter_clientcred.secret') == False:
        print('Initializing App')
        Mastodon.create_app(
        "APP_NAME",
        api_base_url = instance,
        to_file = 'Q-GAPS-WebApp/app/pytooter_clientcred.secret'
        )
        print("App created")

#Start up App
    App = Mastodon(
    client_id = 'Q-GAPS-WebApp/app/pytooter_clientcred.secret',
    api_base_url = instance
    )
#Case 1 - no auth code given but file with access token availble - Log in via access token
    if auth_code == False and os.path.isfile('Q-GAPS-WebApp/app/pytooter_usercred.secret') == True:
    #Acces Mastodon via acces token
        App = Mastodon(access_token='Q-GAPS-WebApp/app/pytooter_usercred.secret')
        print("logged in")        
        return App
#Case 2 - auth code given - log in via access token and create/overwrite file
    if auth_code:
        App.log_in(
            code = auth_code,
            to_file = 'Q-GAPS-WebApp/app/pytooter_usercred.secret',
            scopes=['read', 'write', 'follow']
        )    
        return App
#Case 3 - No authentication code and no file - Request authentication URL 
    if auth_code == False and os.path.isfile('Q-GAPS-WebApp/app/pytooter_usercred.secret') == False:
        url = App.auth_request_url(scopes=['read', 'write', 'follow'])
        print(url)
        return False
    

def searchInstance(instance = 'mastodon.social', query = None, start_date = None, end_date = None):
    #Log into App
    App = makeApp(instance)
    # Define initial parameters
    limit = 40
    min_id = None
    max_id = None
    now = datetime.now()

    #Date Error cases
    if start_date == '' or end_date == '':
        print("Given None Datetypes")
        raise AttributeError
    elif datetime.fromisoformat(end_date) <= now:
        print("Transforming Dates...")
        min_id = ( int( (datetime.fromisoformat(start_date)).timestamp() ) << 16 ) * 1000
        max_id = ( int( (datetime.fromisoformat(end_date)).timestamp() ) << 16 ) * 1000
        print("Dates succesfully transformed.")
    else:
        print("Different Date Error...")
        raise AttributeError

    start_time = now.strftime("%H:%M:%S")
    current_time = now.strftime("%H:%M:%S")
    print("Started fetching and waiting for ratelimit to reset...", start_time)

# Fetch first 60 statuses
    if query ==  None:
        #Fetch a page of statuses from public timeline
        statuses = App.timeline_public(limit=limit, max_id=max_id, min_id=min_id)

    else:
        #search user timeline and public hashtags for query
        results = App.search(query, max_id=max_id, min_id=min_id)
        statuses = results["statuses"] + App.timeline_hashtag(query, limit=limit, max_id=max_id, min_id=min_id)
        statuses = sorted(statuses, key=itemgetter("created_at"))

#turn content from html code to normal text
    for status in statuses:
        html = status['content']
        soup = BeautifulSoup(html, features="html.parser")
        status['content'] = soup.get_text()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Finished fetching - " + current_time)
    
    return statuses
    

def test():
    print("Hello World")
    return "Hello World"

def saveDatabase(table=None, query=None):
#Log into App
    App = makeApp("mastodon.social")

    #Access Database
    connection = sqlite3.connect("Q-GAPS-WebApp/app/test.db")
    cursor = connection.cursor()
    #cursor.execute("DROP TABLE IF EXISTS " + table)
    cursor.execute("CREATE TABLE IF NOT EXISTS " + table + " (id int NOT NULL UNIQUE, created_at, language, uri, url, content)")
    print("Connected to table") 

    # Define initial parameters
    limit = 40
    min_id = None
    max_id = None
    now = datetime.now()
    print("Transforming Dates...")
    #min_id = ( int( (datetime.fromisoformat(start_date)).timestamp() ) << 16 ) * 1000
    max_id = ( int( (now).timestamp() ) << 16 ) * 1000
    #max_id = ( int( (datetime.fromisoformat(end_date)).timestamp() ) << 16 ) * 1000
    print("Dates succesfully transformed.")

    # cursor.execute("SELECT COUNT(*) FROM " + table + " WHERE id > min_id AND id < max_id")
    # c = cursor.fetchone()[0]
    # if (c != 0):
    #     #return warning that some datapoints are already inserted and to maybe select a time period after the last id
    #     print ("Warning: Dublicates in databse! " + str(c))
    #     print(c)

    start_time = now.strftime("%H:%M:%S")
    current_time = now.strftime("%H:%M:%S")
    print("Started fetching and waiting for ratelimit to reset...", start_time)


    # Fetch a page of statuses
    if query ==  None:
        return "No query submitted"
        #Fetch a page of statuses
    else:
        #search user timeline and public hashtags for query
        results_query = App.search(query, max_id=max_id)
        statuses = results_query["statuses"] + App.timeline_hashtag(query, limit=limit, max_id=max_id)
        #statuses = sorted(statuses, key=itemgetter("id"), reverse=True)
        print(len(statuses))

    # Load Statuses into Database
    for status in statuses:
        #turn content from html code to normal text
        html = status['content']
        soup = BeautifulSoup(html, features="html.parser")
        status['content'] = soup.get_text()

        #insert found posts into database
        try:
            cursor.execute("INSERT INTO " + table + " VALUES (:id, :created_at, :language, :uri, :url, :content)", (status))
            connection.commit() 
        except sqlite3.IntegrityError as err:
            continue
        except DeprecationWarning as deperr:
            print("dumb warning")

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("ST: " + start_time + ". Still fetching and waiting fo ratelimit to reset..." + current_time)
    #cursor.execute("SELECT * FROM " + table + " ORDER BY created_at")
    connection.commit()
    connection.close()
    print("Finished loading into the Database.") 
    return False
       
def deleteTable(tablename):
    connection = sqlite3.connect("Q-GAPS-WebApp/app/test.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS " + tablename)
    print("Delted Table")
    connection.commit()
    connection.close()

def checkforNew(instance = "mastodon.social", tablename=None, last_id=None):
    #Log into App
    App = makeApp(instance)
    #check if there are new ids between now and last recorded id
    new_ids_online_dic =  App.search(tablename, min_id=last_id)
    new_ids_online = new_ids_online_dic["statuses"]
    if len(new_ids_online) > 1:
        for id in new_ids_online:
            print(str(id['id']) + " new posts found")
        return True
    else:
        return False

def updateTable(tablename, last_id): #TODO
#Log into App
    App = makeApp("mastodon.social")
#Access Database
    connection = sqlite3.connect("Q-GAPS-WebApp/app/test.db")
    cursor = connection.cursor()
# Define initial parameters
    now = datetime.now()
# Fetch statuses fitting the query page by page
    while True:
        new_ids_dict = App.search(tablename, min_id=last_id)
        new_ids = new_ids_dict["statuses"]
        for id in new_ids:
            #turn content from html code to normal text
            html = id['content']
            soup = BeautifulSoup(html, features="html.parser")
            id['content'] = soup.get_text()

            #insert found posts into database
            try:
                print("added Post" + str(id["id"]))
                cursor.execute("INSERT INTO " + tablename + " VALUES (:id, :created_at, :language, :uri, :url, :content)", (id))
                print(len(new_ids))
                connection.commit() 
                
            except sqlite3.IntegrityError as err:
                continue
            except DeprecationWarning as deperr:
                print("dumb warning")

        # Check if there are more pages
        if len(new_ids) <= 1:
            print(len(new_ids))
            print("No more statuses found...saving to database.")
            break  # No more pages

        #go to next page
        last_id = new_ids[0]['id']
    connection.close()
    return True
    


def workDatabase(instance, table = "qfever", query = None, start_date = None, end_date = None, first = False):
    #Log into App
    App = makeApp(instance)

    #Access Database
    connection = sqlite3.connect("Q-GAPS-WebApp/app/test.db")
    cursor = connection.cursor()
    if first == True:
        cursor.execute("DROP TABLE IF EXISTS " + table)
    cursor.execute("CREATE TABLE IF NOT EXISTS " + table + " (id int NOT NULL UNIQUE, created_at, language, uri, url, content)")
    print("Connected to table")
    
    # Define initial parameters
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
            #search user timeline and public hashtags for query
            results_query = App.search(query, max_id=max_id, min_id=min_id)
            results_more = App.search("Coxiella", max_id=max_id, min_id=min_id)
            statuses = results_query["statuses"] + results_more["statuses"] + App.timeline_hashtag(query, limit=limit, max_id=max_id, min_id=min_id)
            # if more==True:
            #     statuses = App.search(max_id=max_id, min_id=min_id)
            statuses = sorted(statuses, key=itemgetter("id"), reverse=True)
            print(len(statuses))

        # Load Statuses into Database
        for status in statuses:
            #turn content from html code to normal text
            html = status['content']
            soup = BeautifulSoup(html, features="html.parser")
            status['content'] = soup.get_text()

            #insert found posts into database
            try:
                cursor.execute("INSERT INTO " + table + " VALUES (:id, :created_at, :language, :uri, :url, :content)", (status))
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
    #cursor.execute("SELECT * FROM " + table + " ORDER BY created_at")
    connection.commit()
    connection.close()
    print("Finished loading into the Database.")