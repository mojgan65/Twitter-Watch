from django.db import models


class Account(models.Model):
    user_id = models.TextField()
    username = models.CharField(max_length=255)


class Tweet(models.Model):
    id = models.TextField(primary_key=True)
    conversation_id = models.TextField()
    date = models.DateTimeField(null=True)
    text = models.TextField()
    language = models.TextField(null=True)
    user_id = models.TextField(null=True)
    username = models.CharField(max_length=255)
    nlikes = models.IntegerField(null=True)
    nreplies = models.IntegerField(null=True)
    nretweet = models.IntegerField(null=True)
    lastupdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class TweetThreads(models.Model):
    id = models.TextField(primary_key=True)
    conversation_id = models.TextField()
    date = models.DateTimeField(null=True)
    text = models.TextField()
    user_id = models.TextField(null=True)
    username = models.CharField(max_length=255)
    replies = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='replied_to')

    def __str__(self):
        return self.text


class TweetSentimentReply(models.Model):
    id = models.TextField(primary_key=True)
    conversation_id = models.TextField()
    text = models.TextField()
    sentiment = models.TextField()
    username = models.CharField(max_length=255)
    replies = models.TextField()

    def __str__(self):
        return self.text


class TweetSentiment(models.Model):
    id = models.TextField(primary_key=True)
    conversation_id = models.TextField()
    text = models.TextField()
    sentiment = models.TextField()
    username = models.CharField(max_length=255)
    replies = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='replied_to')

    def __str__(self):
        return self.text



