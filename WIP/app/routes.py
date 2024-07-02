from datetime import datetime
from flask import render_template, request
import sqlite3
from app.scripts import functions
from app import app


@app.route('/')
    
@app.route('/index')
def index():
    user = {'username': 'Natalie'}
    #Access Database of fav tables
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    names = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name").fetchall()

    listOfTables = []
    for tablename in names:
        listOfLists = []
        listOfLists.append(tablename[0])
        listOfLists.append(cursor.execute("SELECT * FROM " + tablename[0]).fetchall())
        listOfTables.append(listOfLists)
    cursor.close()
    
    return render_template('index.html', title='Home', tablenames=names, 
                            listOfTables=listOfTables, user=user)

@app.route('/database')
def database():
# TODO exchang example for qfever keyword
    #TODO make function call example for normal database even if user doesnt select a table name
    #Access Database
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    posts = cursor.execute('SELECT * FROM example').fetchall()
    cursor.close()

    return render_template('database.html', title='Database Lookup', posts=posts)

@app.route('/search')
def search():
    #change sdave to save 60 toots 
    query = request.args.get("query", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    tablename = request.args.get("tablename", "")
    save = request.args.get("save", "")
    
    if query:
        #search toots for query and display it on the website
        result = functions.searchInstance(instance="mastodon.social", query=query, start_date=start_date, end_date=end_date)
    elif tablename:
        #setup new table in database
        result = functions.saveDatabase(table=tablename, query=tablename)
    else:
        result = False
        print("No query")

    return render_template('search.html', title='Search Tool', posts=result, query=query)
        

@app.route('/admin')
def admin():

    now = datetime.now()
    redo = request.args.get("redo", "")
    update = request.args.get("update", "")


    if redo == "Loading... Don't cancel.":
        #setup database
        result = functions.workDatabase(instance="mastodon.social", query = "qfever", start_date = "2020-03-16", end_date = str(now), first = True)  
    elif update == "Updating... Don't cancel.":
        #Access Database for last entry date
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        last_date = cursor.execute('SELECT created_at FROM example').fetchone()
        cursor.close()
        print(last_date)

        #update Database
        functions.workDatabase(instance="mastodon.social", query = "qfever", start_date = last_date[0], end_date = str(now), first = False)

    user = {'username': 'Natalie'}
    return render_template('admin.html', title='Admin', user=user)