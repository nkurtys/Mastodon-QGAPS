from unittest import result
from flask import Flask
from flask import request
from MastodonScrape import searchPeriod, datetime

app = Flask(__name__)

#instance, query = None, start_date = None, end_date = None, first = False

@app.route("/")
def index():
    instance = request.args.get("instance", "")
    query = request.args.get("query", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    
    if query:
        res = searchWrap(query, start_date, end_date)
        result = str(res[1]) + " -> " + str(res[0])
    else:
        result = "Add a query."
    return (

        #TODO change that only mastodon.social - dropdown menue open for dding more instnaces
        """ 
        <html>
        <head>
            <h1> Add Mastodon Posts to Database </h1>
        </head>
        <form action="" method="get">
                Mastodon Instance: <input type="text" value = "mastodon.social" name="instance"> <br>
                Search query: <input type="text" name="query"> <br>
                Time from: <input type="date" name="start_date">
                to: <input type="date" name="end_date">
                <input type="submit" value="Add">
            </form>"""
        + "Results (Posts in the database): "
        + result
    )

#TODO divide saving to data base and pure search algorithm thru database (qfever)
#mayve search allowed only for the past week
#TODO - and return recent x posts from mastodon api without saving to database
#TODO - how which weeks got aleady added to database
#TODO - to safe time check if posts already in database/ selected timeframe/ids
#TODO - estimated time and cancle button

def searchWrap(query, start_date, end_date):
    """Wrapper for searchPeriod function"""
    #TODO - check dates for dates that are in the future
    try:
        return searchPeriod("mastodon.social", query, start_date, end_date)
    except TypeError:
        return "invalid Instance"
    except AttributeError:
        return "invalid Date"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)