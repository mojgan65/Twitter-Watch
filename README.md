# Twitter-Watch
This is a Django rest API, which contains a twitter app. In this project tweets and replies of the following accounts from February 1st, 2023  until February 25st, 2023  are tracked. Unfortunately, tweets cannot be updated at this time.  
    {
        "user_id": "44196397",
        "username": "elonmusk"
    },
    {
        "user_id": "813286",
        "username": "BarackObama"
    },
    {
        "user_id": "2361631088",
        "username": "CathieDWood"
    }

five URLs are available as follows:
	Accounts/
This api returns all three accounts
	Tweets/<int:id>
This API gets a user id and returns all conversations for each tweet of the user
	Audience/<int:id>
This API gets a user id and returns all conversations and replies for each tweet of the user
	Sentiment/<int:id>
This API gets a user id and returns the sentiment of all conversations and replies for each tweet of the user
	Sentiment-account/<str:username>
This API gets a user id and calculate of the sentiment of the account.
for each tweet it calculate [the weighted sentiment of the tweet + [the weighted sentiment of the tweet replies]/(the total weight of replies)]/(the total weight of user tweets)
the weight of a tweet is sum of the number of likes, retweets, and replies, and the weight of the follower tweet is sum of the number of likes, retweets, and replies of the reply of the follower.
