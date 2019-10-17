# Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
# import scrape_mars.py script to get mars_data
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")


# Create root route 
@app.route('/')
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template('index.html', mars_data=mars_data)


@app.route('/scrape')
def scrape():
	mars_data = mongo.db.mars_data
	data = scrape_mars.scrape()
	mars_data.update(
		{},
		data,
		upsert=True
	)
	
	return redirect("http://localhost:5000/", code=302)

if __name__ == '__main__':
	app.run(debug=True)