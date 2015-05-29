from django.db import models
from django.contrib.auth.models import User
from sorl import thumbnail



class Article(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=250, unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    body = models.TextField()
    pub_date = models.DateTimeField('date published')
    category=models.ForeignKey('Category')
    cover=thumbnail.ImageField(upload_to='news_covers/%Y/%m/%d')


    def __str__(self):
        return self.title

class PopularArticle(models.Model):
    article=models.ForeignKey(Article)
    priority= models.IntegerField()

class SliderArticle(models.Model):
    article=models.ForeignKey(Article)
    priority= models.IntegerField()



class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username