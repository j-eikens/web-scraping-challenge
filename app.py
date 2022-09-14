from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

@app.route("/")
def index():
    
    mars = mongo.db.collections.find_one()
    
    return render_template("index.html", mars=mars)


@app.route('/scrape')
def scraper():

    #mars = mongo.db.mars

    mars_data = scrape_mars.scrape()

    mongo.db.collection.update_one({}, {"$set": mars_data}, upsert=True)

    #mars.update_one({}, {"$set": mars_data}, upsert=True)


    return redirect("/", code=302)  







if __name__ == "__main__":
    app.run(debug=True)
