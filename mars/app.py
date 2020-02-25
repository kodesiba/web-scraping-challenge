from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import PyMongo

# initialize app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

#routes
@app.route("/scrape")
def scrapeit():
    
    scrapedmars = mongo.db.scrapedmars
    scrapedmars_data = scrape_mars.scrape()
    scrapedmars.update({}, scrapedmars_data, upsert=True)
    return redirect("/", code=302)


@app.route("/")
def main():
    marsdata = mongo.db.scrapedmars.find_one()
    return render_template("index.html", listings=marsdata)


# finish
if __name__ == "__main__":
    app.run()