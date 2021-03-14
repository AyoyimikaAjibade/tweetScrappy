from django.db import models
from django.utils import timezone
class Tweet(models.Model):
    id = models.IntegerField(primary_key=True)
    tip = models.TextField(max_length=245)
    timeStamps = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=10)
    mediaUrl = models.URLField(max_length=2545,blank=True,null=True)
    totalLike = models.IntegerField()
    totalRetweet = models.IntegerField()
