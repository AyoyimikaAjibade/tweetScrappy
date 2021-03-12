from django.db import models

class Tweet(models.Model):
    id = models.IntegerField(primary_key=True,unique=True)
    tip = models.TextField(max_length=245)
    timeStamps = models.DateTimeField()
    author = models.CharField(max_length=10)
    mediaUrl = models.URLField(max_length=2545,blank=True,null=True)
    totalLike = models.IntegerField()
    totalRetweet = models.IntegerField()
