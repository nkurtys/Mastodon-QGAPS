from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    return render_template('index.html', title='Home', user=user)
@app.route('/search')
def search():
    return render_template('search.html', title='Search-Tool')