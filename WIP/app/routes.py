from datetime import datetime
from flask import render_template, request
import sqlite3
from app import app, functions

@app.route('/')
    
@app.route('/index')
def index():
    user = {'username': 'Natalie'}
    return render_template('index.html', title='Home', user=user)

@app.route('/database')
def database():
    #Access Database
    connection = sqlite3.connect("test.db")
    cursor = connection.cursor()
    posts = cursor.execute('SELECT * FROM example').fetchall()
    cursor.close()

    #Detect Qfever in Content for highlighting

    return render_template('database.html', title='Database Lookup', posts=posts)

@app.route('/search')
def search():
    ## imprt funtion from main.py

    query = request.args.get("query", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    
    if query:
        result = functions.searchInstance(instance="mastodon.social", query=query, start_date=start_date, end_date=end_date)
    else:
        result = False
    # try: 
    #     statuses = searchPeriod("mastodon.social", )
    return render_template('search.html', title='Search-Tool', posts=result)

    #except:
        

@app.route('/admin')
def admin():

    now = datetime.now()
    redo = request.args.get("redo", "")
    update = request.args.get("update", "")


    if redo == "Loading... Don't cancel.":
        #setup database
        result = functions.workDatabase(instance="mastodon.social", query = "qfever", start_date = "2016-03-16", end_date = str(now), first = True)  
    elif update == "Updating":
        #Access Database for last entry date
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        last_date = cursor.execute('SELECT created_at FROM example').fetchone()
        cursor.close()
        #update Database
        result = functions.workDatabase(instance="mastodon.social", query = "qfever", start_date = last_date, end_date = str(now), first = False)
    user = {'username': 'Natalie'}
    return render_template('admin.html', title='Admin', user=user)