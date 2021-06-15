from flask import Flask, render_template
import pymongo
import scrape_mars
from pprint import pprint

app = Flask(__name__)

conn = 'mongodb://localhost:27017/'
client= pymongo.MongoClient(conn)
scrape_collection = client.mission_to_mars.scrape

@app.route("/")
def index():
    scrape_collection = client.mission_to_mars.scrape
    return render_template("index.html", list = scrape_collection.find())

@app.route("/scrape")
def scrape():
    scrape_mars.scrape(scrape_collection)
    return([x for x in scrape_collection.find()])


if __name__ == "__main__":
    app.run(debug=True)