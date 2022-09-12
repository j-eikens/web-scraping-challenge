from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app.config["MONGO_URI"] = "mongodb://localhost:27017/phone_app"
mongo = PyMongo(app)

@app.route('/scrape')
def scraper():

    mars = mongo.db.mars

    mars_data = scrape_mars.scrape()

    







if __name__ == "__main__":
    app.run(debug=True)
