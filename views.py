import csv
import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView, status
from rest_framework.response import Response
from twint.tweet import tweet

from .models import Tweet, Account, TweetSentiment, TweetSentimentReply
from .serializer import TweetSerializer, TweetRepliesSerializer, AccountSerializer, TweetSentimentSerializer
import twint
import pandas as pd

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from summarizer import TransformerSummarizer


# Configure
usernames = ["elonmusk", "BarackObama", "cathiedwood"]
dataframes = []


@api_view(['POST','GET'])
@permission_classes((AllowAny, ))
def create_tweet_list(request):

    tweets_data = []

    with open('twitter/concatenated_file.csv', encoding='utf-8') as csvfile:
    # with open('twitter/tweets.csv', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            tweet_data = {
                'id': row['id'],
                'conversation_id': row['conversation_id'],
                'date': row['date'],
                'text': row['tweet'],
                'language': row['language'],
                'user_id': row['user_id'],
                'username': row['username'],
                'nlikes': row['nlikes'],
                'nreplies': row['nreplies'],
                'nretweet': row['nretweets'],
            }
            tweets_data.append(tweet_data)

    # Serialize the tweets_data list and return it as a response
    ser = TweetSerializer(data=tweets_data, many=True)
    if ser.is_valid():
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)



def UpdateTweets():
    lastupdate = Tweet.objects.latest('lastupdate')

    for username in usernames:
        config = twint.Config()
        config.Since = lastupdate.strftime('%Y-%m-%d')
        config.Until = datetime.date.today().strftime('%Y-%m-%d')
        config.Pandas = True
        config.Store_csv = True
        config.Lang = 'en'
        config.To = username
        # config.Username = username
        # Run
        twint.run.Search(config)

        df = twint.storage.panda.Tweets_df

        # Add the DataFrame to the list
        dataframes.append(df)

    # Concatenate the DataFrames for each account into a single DataFrame
    all_tweets_df = pd.concat(dataframes, ignore_index=True)

    if all_tweets_df.isnull:
        return Response({'message': 'No more tweets to process.'}, status=400)

    for row in all_tweets_df:
        tweet = Tweet.objects.update_or_create(
            id=row['id'],
            conversation_id=row['conversation_id'],
            date=row['date'],
            text=row['text'],
            language=row['language'],
            user_id=row['user_id'],
            username=row['username'],
            nlikes=row['nlikes'],
            nreplies=row['nreplies'],
            nretweet=row['nretweet'],
        )


@api_view(['POST','GET'])
@permission_classes((AllowAny, ))
def create_account(request):
    usernames = ["elonmusk", "BarackObama", "CathieDWood"]
    accounts = []
    for username in usernames:
        tweet = Tweet.objects.filter(username=username).first()
        if tweet:
            account = {
                'user_id': tweet.user_id,
                'username': tweet.username
            }
            accounts.append(account)
    ser = AccountSerializer(data=accounts , many=True)
    if ser.is_valid():
        ser.save()
        return Response(ser.data, status=status.HTTP_201_CREATED)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_accounts(request):
    # UpdateTweets()
    accounts = Account.objects.all()
    if accounts:
        ser = AccountSerializer(accounts, many=True)
        return Response(ser.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_tweets(request,id):
    tweet_thread = []

    tweets = Tweet.objects.filter(user_id=id)
    if tweets:
        for tweet in tweets:
            conversation_id = tweet.conversation_id
            tweets_replies = Tweet.objects.filter(conversation_id=conversation_id, user_id=id)
            if tweets_replies:
                tweet_reply = {
                    'id': tweet.id,
                    'conversation_id': tweet.conversation_id,
                    'date': tweet.date,
                    'text': tweet.text,
                    'user_id': tweet.user_id,
                    'username': tweet.username,
                    'replies': tweets_replies
                }
                tweet_thread.append(tweet_reply)

        serializer = TweetRepliesSerializer(tweet_thread, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_audience(request, id):
    tweet_thread = []

    # Retrieve all tweets for the user
    tweets = Tweet.objects.filter(user_id=id)
    if tweets:
        for tweet in tweets:
            conversation_id = tweet.conversation_id
            tweets_replies = Tweet.objects.filter(conversation_id=conversation_id)
            if tweets_replies:
                tweet_reply = {
                    'id': tweet.id,
                    'conversation_id' : tweet.conversation_id,
                    'date' : tweet.date,
                    'text': tweet.text,
                    'user_id': tweet.user_id,
                    'username': tweet.username,
                    'replies': tweets_replies
                }
                tweet_thread.append(tweet_reply)

        serializer = TweetRepliesSerializer(tweet_thread, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_sentiment(request, id):
    tweet_thread = []

    # create a SentimentIntensityAnalyzer object
    sia = SentimentIntensityAnalyzer()

    # Retrieve all tweets for the user
    tweets = Tweet.objects.filter(user_id=id)
    #
    if tweets:
        for tweet in tweets:
            conversation_id = tweet.conversation_id
            tweets_replies = Tweet.objects.filter(conversation_id=conversation_id)

            replies_sentiment= []
            if tweets_replies:
                for tweets_reply in tweets_replies:
                    sentiment = "positive" if sia.polarity_scores(tweets_reply.text)['compound'] > 0.5 else "negative"
                    tweet_reply = TweetSentimentReply(
                        id=tweets_reply.id,
                        conversation_id=tweets_reply.conversation_id,
                        text=tweets_reply.text,
                        sentiment=sentiment,
                        username=tweets_reply.username,
                    )
                    replies_sentiment.append(tweet_reply)

            sentiment = "positive" if sia.polarity_scores(tweet.text)['compound'] > 0.5 else "negative"

            tweet_sentiment = {
                'id': tweet.id,
                'conversation_id': tweet.conversation_id,
                'text': tweet.text,
                'username': tweet.username,
                'sentiment': sentiment,
                'replies': replies_sentiment
            }
            tweet_thread.append(tweet_sentiment)

        serializer = TweetSentimentSerializer(tweet_thread, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_account_sentiment(request, username):
    sia = SentimentIntensityAnalyzer()

    sum_account_weighs = 0
    # Retrieve all tweets for the user
    tweets = Tweet.objects.filter(username=username)

    if tweets:
        total_tweet_sentiment = 0
        for tweet in tweets:
            conversation_id = tweet.conversation_id
            tweets_replies = Tweet.objects.filter(conversation_id=conversation_id)
            tweet_sentiment = sia.polarity_scores(tweet.text)['compound'] * (tweet.nretweet + tweet.nreplies + tweet.nlikes + 1)
            total_tweet_sentiment = tweet_sentiment + total_tweet_sentiment
            sum_account_weighs = sum_account_weighs + (tweet.nretweet + tweet.nreplies + tweet.nlikes)

            total_follower_sentiments = 0
            sum_followe_weighs = 0
            for tweet_reply in tweets_replies:
                follower_sentiments = sia.polarity_scores(tweet_reply.text)['compound'] * (tweet_reply.nretweet + tweet_reply.nreplies + tweet_reply.nlikes + 1)
                total_follower_sentiments = total_follower_sentiments + follower_sentiments
                sum_followe_weighs = sum_followe_weighs + (tweet_reply.nretweet + tweet_reply.nreplies + tweet_reply.nlikes)
            total_follower_sentiments = total_follower_sentiments / sum_followe_weighs
            total_tweet_sentiment = total_tweet_sentiment + total_follower_sentiments

        total_tweet_sentiment = total_tweet_sentiment / sum_account_weighs

        response = {
            'username': username,
            'account-sentiment': total_tweet_sentiment
        }

        return Response(data=response, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_account_summary(request, username):
    model = TransformerSummarizer(transformer_type="XLNet", transformer_model_key="xlnet-base-cased")

    tweets = Tweet.objects.filter(username=username)
    total_tweet = ''
    if tweets:
        for tweet in tweets:
            total_tweet = total_tweet + ' ' + tweet.text
        summary = ''.join(model(total_tweet, min_length=10, max_length=200))

        response = {
            'account': username,
            'summary': summary
        }

        return Response(response, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)








