from django.urls import path
from twitter import views as v

urlpatterns = [
    # path('create-tweets/', v.create_tweet_list),
    # path('create-accounts/', v.create_account),
    path('accounts/', v.get_accounts),
    path('tweets/<int:id>/', v.get_tweets),
    path('audience/<int:id>/', v.get_audience),
    path('sentiment/<int:id>/', v.get_sentiment),
    path('sentiment-account/<str:username>/', v.get_account_sentiment),
    path('summary/<str:username>/', v.get_account_summary)

]