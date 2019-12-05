import os
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from apscheduler.scheduler import Scheduler
import json, requests
import modelPredict as mp
import util

import pickle 
from bson.binary import Binary

app = Flask(__name__)

mongo = MongoClient("mongodb+srv://admin:admin@facterrcluster-v12sw.mongodb.net/test?retryWrites=true&w=majority")
db = mongo['news']
collection = db['newsData']

schedule = Scheduler() # Scheduler object
schedule.start()


def fetch_real_news():
	url = ('https://newsapi.org/v2/top-headlines?'
			'country=ca&'
			'language=en&'
			'category=general&'
			'pageSize=1&'
			'page=1&'
			'apiKey=944fd308bb7a49798093550409b3c2b9')
	response = requests.get(url)
	response_dict =response.json()
	
	data_dict = {}
	article_dict = response_dict['articles'][0]
	data_dict['title'] = article_dict['title']
	data_dict['description'] = article_dict['description']
	data_dict['url'] = article_dict['url']
	data_dict['publishedAt'] = article_dict['publishedAt']

	title = data_dict['title']
	body = data_dict['description']
	result = mp.classify(title, body)

	value = result[1].item()

	data_dict['label'] = result[0]
	data_dict['score'] = value
	collection.update_one(data_dict, {'$set': data_dict }, upsert=True);
	
schedule.add_interval_job(fetch_real_news, minutes=30)

@app.route("/")
@app.route("/dashboard")
def index():
	# online_users = mongo.db.users.find({"online": True})
	fake_count = collection.find( { "label": "Fake" } ).count()
	real_count = collection.find( { "label": "Real" } ).count()

	return render_template("index.html", message="Dashboard", timeseries = util.read(), fake_count = fake_count, real_count = real_count);   

@app.route("/news")
def news():
	results = collection.find({})
	return render_template("news.html", message="News Feed", news_list = results);  

@app.route("/search")
def search():
	return render_template("search.html", message="Custom Search");   

@app.route('/classify', methods=['POST'])
def classify():
	# get the input text email
	news_text = request.form['message']
	return jsonify(mp.classify_single(news_text))

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html', title='Page not found'), 404


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)