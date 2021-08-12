from flask import json, render_template, Flask, request 
from markupsafe import escape
from twint import run, Config


from lib.file import make_csv_response

def marshal_tweet(tweet):
	return vars(tweet);

def marshal_user(user):
	return vars(user);

batch_size = 20 # twint uses increments of 20
default_limit = 1 * batch_size 
def grab_tweets(username, filter, limit = default_limit):
	tweets = []
	run.Search(Config(
		Limit=int(limit),
		Search=filter,
		Username=username,
		Hide_output=True,
		Store_object=True,
		Store_object_tweets_list=tweets,
	))
	return [marshal_tweet(tweet) for tweet in tweets]

def grab_user(username):
	users = []
	run.Lookup(Config(
		Username=username,
		Store_object=True,
		Store_object_users_list=users
	))
	return marshal_user(user=users.pop())

app = Flask(__name__)

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
	print('fields are ', fields)
	print('rows are', rows)
	if file_type == 'csv':
		return make_csv_response(username, rows, fields)

@app.route("/search/tweets")
def get_tweets():
	username = escape(request.args.get('username', '', type=str))
	limit = escape(request.args.get('limit', '', type=str))
	filter = escape(request.args.get('filter', '', type=str))
	tweets = grab_tweets(username=username, limit=limit, filter=filter)
	return json.jsonify(tweets)

@app.route("/search/user")
def get_user():
	username = escape(request.args.get('username', '', type=str))
	users = grab_user(username=username)
	return json.jsonify(users)