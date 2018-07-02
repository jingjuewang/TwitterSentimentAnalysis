import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    consumer_key, consumer_secret, \
    access_token, access_token_secret \
        = loadkeys(twitter_auth_filename)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def fetch_tweets(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary

    For efficiency, create a single Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.
    """

    ret = {'user': name, 'tweets': []}
    counts = 0
    sid = SentimentIntensityAnalyzer()
    try:
        for status in tweepy.Cursor(api.user_timeline, id=name).items(100):
            counts += 1
            tweet = {'id': status.id, 'created': status.created_at,
                     'retweeteds': status.retweet_count,
                     'text': status.text,
                     'hashtags': [item['text'] for item in status.entities['hashtags']],
                     'urls': [item['url'] for item in status.entities['urls']],
                     'mentions': [item['screen_name'] for item in status.entities['user_mentions']]}
            tweet['score'] = sid.polarity_scores(tweet['text'])['compound']
            ret['tweets'].append(tweet)
    except tweepy.TweepError as e:
        print e
        print "The number of tweets is less than 100."

    ret['count'] = counts
    return ret


def fetch_following(api, name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get a list of "friends IDs" then get
    the list of users for each of those.
    """
    followed_by = []
    for user in api.friends_ids(name):
        follow_user = {'name': api.get_user(user).name, 'screen_name': api.get_user(user).screen_name,
                       'followers': api.get_user(user).followers_count, 'created': api.get_user(user).created_at,
                       'image': api.get_user(user).profile_image_url}
        followed_by.append(follow_user)
    followed_by = sorted(followed_by, key=lambda k: k['followers'], reverse=True)

    return followed_by
