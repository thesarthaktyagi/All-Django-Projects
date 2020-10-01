from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    # This is the field for post title
    title = models.CharField(max_length=250)

    # This is the field that will be used in the urls
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')

    # This field defines many to one relationship meaning that each post is written by a user , and a user can write any
    # number of posts
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length = 10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager() # The default manager
    published = PublishedManager() # Our custom manager

    # creating canonical url
    def get_absolute_url(self):
        return reverse('blog_app:post_detail',
                        args=[self.publish.year,
                            self.publish.month,
                            self.publish.day, self.slug])



    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title