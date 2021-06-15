from flask import Flask, render_template
import pymongo
import scrape_mars
from pprint import pprint

app = Flask(__name__)

conn = 'mongodb://localhost:27017/'
client= pymongo.MongoClient(conn)
scrape_collection = client.mission_to_mars.scrape
nasamars_collection = client.mission_to_mars.nasamars
jplimages_collection = client.mission_to_mars.jplimages
spacefacts_collection = client.mission_to_mars.spacefacts
usgsimages_collection = client.mission_to_mars.usgsimages

@app.route("/")
def index():
    return render_template("index.html",
                            nasanews = nasamars_collection.find(),
                            usgsimages = usgsimages_collection.find(),
                            spacefacts = spacefacts_collection.find() )

@app.route("/scrape")
def scrape():
    scrape_mars.scrape(scrape_collection)
    return([x for x in scrape_collection.find('Nasa_Mars_Exploration_Aticles')])


if __name__ == "__main__":
    app.run(debug=True)