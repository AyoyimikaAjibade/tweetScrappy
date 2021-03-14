from django.shortcuts import render
from django.db.utils import OperationalError, IntegrityError
from .models import Tweet
import os
from dotenv import load_dotenv
load_dotenv()
import tweepy

def setApi():
    consumerKey = str(os.getenv('apiKey'))
    consumerSecret = str(os.getenv('apiSecretKey'))
    accessToken = str(os.getenv('accessToken'))
    accessTokenSecret = str(os.getenv('accessTokenSecret'))

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def getData():
    api = setApi()
    searchWord = '@python_tip'
    tweets = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=searchWord).items():

        try:
            if 'media' in tweet.entities:
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
            try:
                print('RETREIVING DATA FROM API...')
                tweet = Tweet.objects.create(
                    id=tweetDict.get('id'),
                    tip=tweetDict.get('text'),
                    timeStamps=tweetDict.get('createdAt'),
                    author=tweetDict.get('author'),
                    mediaUrl=tweetDict.get('mediaUrl'),
                    totalLike=tweetDict.get('totalLike'),
                    totalRetweet=tweetDict.get('totalRetweet')
                )
            except OperationalError as e:
                print('ERROR', e)
                continue
            except IntegrityError as e:
                print('ERROR', e)
                continue
        except tweepy.TweepError as e:
            print('ERROR', e.reason)
            continue
    print('DATA SUCCESSFULLY RETREIVED')

# Will schedule time to retrieve data at a certain time
# getData()

def showTweet(request):
    tweets = Tweet.objects.all().order_by('totalLike')
    context = {'tweets': tweets}
    return render(request, 'tweet/showTweet.html', context)





