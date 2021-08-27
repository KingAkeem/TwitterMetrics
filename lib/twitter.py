import twint

def marshal_tweet(tweet):
	return vars(tweet)

def marshal_user(user):
	return vars(user)

def parse_filter(filter_text):
	filter = dict()
	for segment in filter_text.split(','):
		pieces = segment.split(':')
		if len(pieces) == 2:
			key, value = pieces
			filter[key] = value.strip() 	
	return filter

def add_filter(config, filter):
	for key, value in filter.items():
		if key == 'keyword':
			config.Search = value
		elif key == 'since':
			config.Since = value
		elif key == 'until':
			config.Until = value

batch_size = 20 # twint uses increments of 20
default_limit = 1 * batch_size 
def scrape_tweets(username, filter_text, limit = default_limit):
	tweets = []
	filter = parse_filter(filter_text)
	config = twint.Config(
		Limit=int(limit),
		Username=username,
		Store_object=True,
		Store_object_tweets_list=tweets,
	)
	add_filter(config, filter)
	twint.run.Search(config) # run config once filters have been added
	return [marshal_tweet(tweet) for tweet in tweets]

def scrape_user(username):
	users = []
	twint.run.Lookup(twint.Config(
		Username=username,
		Store_object=True,
		Store_object_users_list=users
	))
	return marshal_user(user=users.pop())