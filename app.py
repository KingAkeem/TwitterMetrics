from flask import json, render_template, Flask, request 
from flask_assets import Environment, Bundle
from markupsafe import escape


from lib.file import make_csv_response
from lib.twitter import scrape_tweets, scrape_user

app = Flask(__name__)
assets = Environment(app) 
js = Bundle('js/main.js', output='gen/entry.js')
assets.register('js_all', js)

@app.route("/")
def main():
	return render_template('main.html')

@app.route("/tweets")
def tweets():
	return render_template('tweets.html')

@app.route("/user")
def followers():
	return render_template('user.html')

@app.route("/export/<file_type>", methods=['post'])
def export(file_type):
	username = escape(request.args.get('username', '', type=str))
	rows = json.loads(request.form.get('rows'))

	fields = rows[0].keys()
	if file_type == 'csv':
		return make_csv_response(username, rows, fields)

@app.route("/search/tweets")
def get_tweets():
	username = escape(request.args.get('username', '', type=str))
	limit = escape(request.args.get('limit', '', type=str))
	filter = escape(request.args.get('filter', '', type=str))
	tweets = scrape_tweets(username=username, limit=limit, filter_text=filter)
	return json.jsonify(tweets)

@app.route("/search/user")
def get_user():
	username = escape(request.args.get('username', '', type=str))
	users = scrape_user(username=username)
	return json.jsonify(users)