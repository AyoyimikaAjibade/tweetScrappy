from rest_framework import serializers
from tweet.models import Tweet


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['id', 'tip', 'timeStamps', 'author', 'mediaUrl', 'totalLike', 'totalRetweet']