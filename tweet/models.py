from django.db import models

class Tweet(models.Model):
    id = models.IntegerField(primary_key=True,unique=True)
    tip = models.TextField(max_length=245)
    timeStamps = models.DateTimeField()
    author = models.CharField(max_length=10)
    mediaUrl = models.URLField(max_length=2545,blank=True,null=True)
    totalLike = models.IntegerField()
    totalRetweet = models.IntegerField()

    # @classmethod
    # def create(cls, **kwargs):
    #     tweet = cls(
    #         id=kwargs['id'],
    #         tip=kwargs['text'],
    #         timeStamps=kwargs['createdAt'],
    #         author=kwargs['author'],
    #         mediaUrl=kwargs['mediaUrl'],
    #         totalLike=kwargs['totalLike'],
    #         totalRetweet=kwargs['totalRetweet']
    #     )
    #     return tweet

    # @classmethod
    # def create(cls, title):
    #     book = cls(title=title)
    #     # do something with the book
    #     return book
    @classmethod
    def create(cls, **kwargs):
        tweet = cls.objects.get_or_create(
            id=kwargs['id'],
            tip=kwargs['text'],
            timeStamps=kwargs['createdAt'],
            author=kwargs['author'],
            mediaUrl=kwargs['mediaUrl'],
            totalLike=kwargs['totalLike'],
            totalRetweet=kwargs['totalRetweet']
        )
        return tweet
