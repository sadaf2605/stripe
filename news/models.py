from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=250, unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    body = models.TextField()
    pub_date = models.DateTimeField('date published')
    category=models.ForeignKey('Category')
    cover=models.ImageField()

class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)



class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username