# TwitterSentimentAnalysis

This project is used to perform a simple sentiment analysis for Tweets by using tweepy (an API wrapper around the twitter API) and vaderSentiment library. The result is a web application running at AWS to display a list of users that are followed by the given user and the most recent 100 tweets posted by the given user. The tweets are color-coded by sentiment using a red to green gradient (red: negative; green: positive).       


### Files     
- IP.txt: indicates the IP address of the AWS server (currently terminated). If run it locally, it will be `localhost:5000`;    
- server.py: implements methods: tweets(), add_color(), and following();  
- tweetie.py: implements methods: authenticate(), fetch_tweets(), fetch_following().      

### Results  
![alt text](https://github.com/jingjuewang/TwitterSentimentAnalysis/blob/master/screenshots/trump_followers.jpg){height: 100px;}
![alt text](https://github.com/jingjuewang/TwitterSentimentAnalysis/blob/master/screenshots/trump_tweets.jpg)


