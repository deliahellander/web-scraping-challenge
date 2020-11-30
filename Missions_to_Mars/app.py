from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars 

# Create an instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route('/')
def index():
	
	mars = mongo.db.mars.find_one()
	return render_template("index.html", mars=mars)

@app.route('/scrape')
def scrape():
	mars = mongo.db.mars
	mars_data = scrape_mars.scrape()
	mars.update({}, mars_data, upsert=True)
	
	return redirect("/", code=302)

if __name__ == "__main__":
	app.run(debug=True)
