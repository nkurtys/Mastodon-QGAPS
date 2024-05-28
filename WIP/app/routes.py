from flask import render_template
import sqlite3
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
    return render_template('database.html', title='Database Lookup', posts=posts)
@app.route('/search')
def search():
    return render_template('search.html', title='Search-Tool')
@app.route('/admin')
def admin():
    user = {'username': 'Natalie'}
    return render_template('admin.html', title='Admin', user=user)