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
    #setup database
    user = {'username': 'Natalie'}
    return render_template('admin.html', title='Admin', user=user)