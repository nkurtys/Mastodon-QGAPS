from flask import render_template
import sqlite3
from MastodonScrape import makeApp, searchPeriod
from app import app

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
    # try: 
    #     statuses = searchPeriod("mastodon.social", )
        return render_template('search.html', title='Search-Tool'
                               #, statuses=statuses
                               )

    #except:
        

@app.route('/admin')
def admin():
    user = {'username': 'Natalie'}
    return render_template('admin.html', title='Admin', user=user)