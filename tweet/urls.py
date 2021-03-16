from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.showTweet, name='showTweet'),
    path('api/', views.api_root),
    path('api/v1/tweet/', views.TweetList.as_view(), name='tweet-list'),
    path('api/v1/tweet/<int:pk>/', views.TweetDetail.as_view(), name='tweet-detail'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('settings/password/', views.password, name='password'),
]
urlpatterns = format_suffix_patterns(urlpatterns)