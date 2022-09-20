from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")

@app.route("/")
def index():
    
    mars = mongo.db.scrape_data.find_one()
    
    return render_template("index.html", mars=mars)


@app.route('/scrape')
def scraper():

    mars = mongo.db.mars

    mars_scrape_data = scrape_mars.scrape()

    mars.update_one({}, {"$set": mars_scrape_data}, upsert=True)
    #mars.insert_many({'i': i} for i in range(len(mars_scrape_data)))

    return redirect("/", code=302)  

if __name__ == "__main__":
    app.run(debug=True)
