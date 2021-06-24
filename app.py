import csv

from flask import json
from flask.json import jsonify
from markupsafe import escape
from flask import render_template, Flask, request, Response, make_response
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


def create_csv(name, rows):
	filename = f'{name}.csv'
	with open(filename, 'w+') as csvfile:
		csvwriter = csv.DictWriter(csvfile, fieldnames=['ID', 'Tweets'])
		csvwriter.writeheader()
		for row in rows:
			try:
				csvwriter.writerow({
					'ID': row['id'],
					'Tweets': row['content']
				})
			except KeyError as e:
				print(f'Found invalid row. {e}')
		return filename 



@app.route("/export/<file_type>", methods=['post'])
def export(file_type):
	username = escape(request.args.get('username', '', type=str))
	rows = json.loads(request.form.get('rows'))

	if file_type == 'csv':
		filename = create_csv(username, rows)
		with open(filename, 'rb') as csv_file:
			response = make_response(csv_file.read())
			response.status = 200
			response.headers["Content-Disposition"] = f"attachment; filename={filename}"
			response.headers["Content-type"] = "text/csv"
			return response

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