from datetime import datetime
from flask import render_template, request
import sqlite3
from app.scripts import functions
from app import app

@app.route("/")

@app.route('/home', methods=['GET', 'POST'])
def index():
    user = {'username': 'Natalie'}
    return render_template('index.html', title='Home', user=user)


@app.route('/database') #collection
def database():
#Access Database of fav tables
    connection = sqlite3.connect("WIP/app/test.db")
    cursor = connection.cursor()
#Update datatable in active tab TODO
    # update_table = request.args.get("update", "")
    # print(update_table)
    # if update_table:
    #     last_id = cursor.execute('SELECT id FROM ' + update_table).fetchone()
    #     print(update_table)
    #     new_ids = functions.checkforNew(tablename=update_table, last_id = last_id[0])
    #     if (new_ids):
    #         functions.updateTable(tablename=update_table, last_id = last_id[0])

    #Delete Datatable
    to_delete_tablename = request.args.get("button-id", "")
    if to_delete_tablename:
        functions.deleteTable(to_delete_tablename)

#Display all Datatables in tab
    names = cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name").fetchall()
    
    listOfTables = []
    for tablename in names:
        #Disable deleting qfever database without admin rights
        # if tablename[0] == "qfever":
        #     continue
        listOfLists = []
        listOfLists.append(tablename[0])
        listOfLists.append(cursor.execute("SELECT * FROM " + tablename[0]).fetchall())
        listOfTables.append(listOfLists)
    cursor.close()
    connection.close()
    return render_template('database.html', title='Database',tablenames=names, 
                            listOfTables=listOfTables)

@app.route('/search')
def search():
    #change sdave to save 60 toots 
    query = request.args.get("query", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    tablename = request.args.get("tablename", "")
    
    if query:
        #search toots for query and display it on the website
        result = functions.searchInstance(instance="mastodon.social", query=query, start_date=start_date, end_date=end_date)
    elif tablename:
        #setup new table in database
        result = functions.saveDatabase(table=tablename, query=tablename)
    else:
        result = False
        print("No query")

    return render_template('search.html', title='Search', posts=result, query=query)
        

@app.route('/admin')
def admin():

    now = datetime.now()
    redo = request.args.get("redo", "")
    update = request.args.get("update", "")


    if redo == "Loading... Don't cancel.":
        #setup database
        print("Redoing")
        functions.workDatabase(instance="mastodon.social", query = "qfever", start_date = "2020-03-16", end_date = str(now), first = True)  
    elif update == "Updating... Don't cancel.":
        #Access Database for last entry date
        connection = sqlite3.connect("WIP/app/test.db")
        cursor = connection.cursor()
        last_date = cursor.execute('SELECT created_at FROM qfever').fetchone()
        cursor.close()
        print("Updating")

        #update Database
        functions.workDatabase(instance="mastodon.social", query = "qfever", start_date = last_date[0], end_date = str(now), first = False)

    user = {'username': 'Natalie'}
    return render_template('admin.html', title='Admin', user=user)