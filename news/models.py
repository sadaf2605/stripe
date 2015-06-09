from django.db import models
from django.contrib.auth.models import User
from sorl import thumbnail
from django.template.defaultfilters import slugify


class Article(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=250, unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    body = models.TextField()
    pub_date = models.DateTimeField('date published',auto_now=True)
    categories=models.ManyToManyField('Category',blank=True,null=True)
    cover=thumbnail.ImageField(upload_to='news_covers/%Y/%m/%d',blank=True,null=True)
    draft=models.BooleanField(default=True)
    public=models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username