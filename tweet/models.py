from django.db import models
from django.utils import timezone

class Tweet(models.Model):
    id = models.CharField(primary_key=True,max_length=245)
    tip = models.TextField(max_length=245)
    timeStamps = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=10)
    mediaUrl = models.URLField(max_length=2545, blank=True, null=True)
    totalLike = models.IntegerField()
    totalRetweet = models.IntegerField()

    class Meta:
        ordering = ['-totalLike']
