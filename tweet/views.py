from django.shortcuts import render
from .models import Tweet
import os
from dotenv import load_dotenv
load_dotenv()
import tweepy


def getTweet(searchWord):
    consumerKey = str(os.getenv('apiKey'))
    consumerSecret = str(os.getenv('apiSecretKey'))
    accessToken = str(os.getenv('accessToken'))
    accessTokenSecret = str(os.getenv('accessTokenSecret'))

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    tweets = []
    count = 1
    sinceDate = '2017-02-01'

    for tweet in tweepy.Cursor(api.user_timeline, count=100, screen_name=searchWord, since=sinceDate,
                               exclude_replies=True, include_rts=False).items(12):
        count += 1
        try:
            if 'media' in tweet.entities:
                # print(dir(tweet))
                for image in tweet.entities['media']:
                    head = ['id', 'text', 'createdAt', 'author', 'mediaUrl', 'totalLike', 'totalRetweet']
                    data = [tweet.id_str, tweet.text, tweet.created_at, tweet.author.screen_name,
                            image['media_url'], tweet.favorite_count, tweet.retweet_count]

            else:
                head = ['id', 'text', 'createdAt', 'author', 'totalLike', 'totalRetweet']
                data = [tweet.id_str, tweet.text, tweet.created_at, tweet.author.screen_name,
                       tweet.favorite_count, tweet.retweet_count]

            tweets.append(data)
            tweetDict = {head[i]: data[i] for i in range(len(head))}
            tweet = Tweet.objects.get_or_create(
                id=tweetDict.get('id'),
                tip=tweetDict.get('text'),
                timeStamps=str(tweetDict.get('createdAt')),
                author=tweetDict.get('author'),
                mediaUrl=tweetDict.get('mediaUrl'),
                totalLike=tweetDict.get('totalLike'),
                totalRetweet=tweetDict.get('totalRetweet')
            )
            if tweet:
                print('imported...')

            else:
                print('ERROR...')
        except tweepy.TweepError as e:
            print('ERROR', e.reason)
            continue
        return tweet

# word= '@python_tip'
# context = getTweet(word)


def showTweet(request):
    tweets = Tweet.objects.all().order_by('totalLike')
    context = {'tweets': tweets}
    return render(request, 'tweet/showTweet.html', context)





