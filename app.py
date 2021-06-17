from flask import json
from flask.json import jsonify
from markupsafe import escape
from flask import render_template, Flask, request, Response
from twint import run, Config 

def marshal_tweet(tweet):
	return {
		'id': tweet.id,
		'user_id': tweet.user_id,
		'username': tweet.username,
		'content': tweet.tweet
	}

def marshal_user(user):
	return {
		'id': user.id,
		'username': user.username,
		'icon': user.avatar
	}

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

@app.route("/export/pdf", methods=['post'])
def export_pdf():
	rows = json.loads(request.form.get('rows'))
	for row in rows:
		print(row)
	return Response(status=200)

@app.route("/search/tweets")
def get_tweets():
	username = escape(request.args.get('username', '', type=str))
	limit = escape(request.args.get('limit', '', type=str))
	filter = escape(request.args.get('filter', '', type=str))
	tweets = grab_tweets(username=username, limit=limit, filter=filter)
	return jsonify(tweets)

@app.route("/search/user")
def get_user():
	username = escape(request.args.get('username', '', type=str))
	users = grab_user(username=username)
	return jsonify(users)