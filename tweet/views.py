from django.shortcuts import render, redirect
from django.db.utils import OperationalError, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Tweet
import os
import time
import tweepy
from dotenv import load_dotenv
load_dotenv()

from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

#Api
from tweet.serializers import TweetSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


def setApi():
    '''
    :return: the api object with all necessary token and keys verified
    '''
    consumerKey = str(os.getenv('apiKey'))
    consumerSecret = str(os.getenv('apiSecretKey'))
    accessToken = str(os.getenv('accessToken'))
    accessTokenSecret = str(os.getenv('accessTokenSecret'))

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def getData():
    '''
    using the cursor method get all tweets from '@pythpn_tip' and convert to
    dictionary on each iterations created the tweet and save to the database
    :return: successful or throwing an exception
    '''
    api = setApi()
    searchWord = '@python_tip'
    tweets = []
    # make the code run every 24 hours to update based on new tweets
    time.sleep(24*3600)
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


@login_required
def showTweet(request):
    '''
    :param request: the request object is firstly defined
    :return: the rendered html page populated with data as a
    response to the request
    '''
    tweets = Tweet.objects.all().order_by('-totalLike')
    context = {'tweets': tweets}
    return render(request, 'tweet/showTweet.html', context)

@api_view(['GET'])
def api_root(request, format=None):
    '''
    :param request: the request object
    :param format: make the api url flexible to request and respond to data in any format(json, text, html e.t.c)
    :return: response where this function is the entry point for all api endpoint
    '''
    return Response({
        'tweets': reverse('tweet-list', request=request, format=format),
    })


class TweetList(generics.ListCreateAPIView):
    '''
    Using the django built in class based view having read and create method on all tweet
    '''
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TweetDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Using the django built in class based view having update, read, and delete method on a particular tweet
    '''
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SettingsView(LoginRequiredMixin, TemplateView):
    '''
    Creating a settings page and function if user wants to disconnect from the twitter login authentications
    '''
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            twitter_login = user.social_auth.get(provider='twitter')
        except ObjectDoesNotExist:
            twitter_login = None

        can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

        return render(request, 'tweet/setting.html', {
            'twitter_login': twitter_login,
            'can_disconnect': can_disconnect
        })


@login_required
def password(request):
    '''
    :param request: the request object having properties like user
    :return: the change password page so user can change password before log in out of twitter
    '''
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'tweet/password.html', {'form': form})







