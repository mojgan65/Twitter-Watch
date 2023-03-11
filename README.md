# Twitter-Watch
This is a Django rest API, which contains a twitter app. In this project tweets and replies of the following accounts from February 1st, 2023  until February 25st, 2023  are tracked. Unfortunately, tweets cannot be updated at this time.  <br />
    {
        "user_id": "44196397",
        "username": "elonmusk"
    },
    <br />
    {
        "user_id": "813286",
        "username": "BarackObama"
    },
    <br />
    {
        "user_id": "2361631088",
        "username": "CathieDWood"
    }
    <br />

five URLs are available as follows: <br />
<t /><br />1)  Accounts/:
<t />This api returns all three accounts
<t /><br />2)  Tweets/<int:id>: 
<t />This API gets a user id and returns all conversations for each tweet of the user
<t /><br />3)  Audience/<int:id>: 
<t />This API gets a user id and returns all conversations and replies for each tweet of the user
<t /><br />4)  Sentiment/<int:id>: 
<t />This API gets a user id and returns the sentiment of all conversations and replies for each tweet of the user
<t /><br />5)  Sentiment-account/<str:username>: 
This API takes the username and calculates the sentiment of the account. For each tweet it receives, it calculates the sentiment of an account according to the following formula: <br/> [the weighted sentiment of the tweet + [the weighted sentiment of the tweet replies]/(the total weight of replies)]/(the total weight of user tweets) <br/>
the weight of a tweet is sum of the number of likes, retweets, and replies, and the weight of the follower tweet is sum of the number of likes, retweets, and replies of the reply of the follower.
<t /><br />6)  Summary/<str:username>: The API receives the username of the account and returns a summary of the account containing 200 words. The API uses the XLNet language model to obtain an abstract summary of the text.
