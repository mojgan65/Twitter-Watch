from rest_framework import serializers
from .models import Tweet, TweetThreads, Account, TweetSentiment, TweetSentimentReply


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = '__all__'
        read_only_fields = ['lastupdate']


class TweetRepliesSerializer(serializers.ModelSerializer):
    replies = TweetSerializer(many=True)

    class Meta:
        model = TweetThreads
        fields = '__all__'


class SentimentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetSentimentReply
        fields = '__all__'


class TweetSentimentSerializer(serializers.ModelSerializer):
    replies = SentimentReplySerializer(many=True)

    class Meta:
        model = TweetSentiment
        fields = '__all__'


