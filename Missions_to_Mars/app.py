from flask import Flask
from flask_pymongo import PyMongo
import scrape_mars.py

app = Flask(__name__)
app.config("MONGO_URI") = conn
mongo = PyMongo(app)

@app.route("/")

@app.route("/scrape")

    