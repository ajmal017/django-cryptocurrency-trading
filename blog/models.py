from django.db import models
from wallet.models import User

from taggit.managers import TaggableManager
from tinymce.models import HTMLField
from stop_words import get_stop_words

import time
import random
import re
import itertools


class BlogPost(models.Model):
    """
    Class used for defining blog posts
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    contents = HTMLField()
    abstract = HTMLField()
    image = models.ImageField(
        upload_to='blog_images',
        null=True,
        blank=True
    )
    show_image = models.BooleanField(default=True)
    show_creator = models.BooleanField(default=True)
    show_comments = models.BooleanField(default=True)
    creation_date = models.DateField(default=time.strftime("%Y-%m-%d"))
    last_updated = models.DateField(default=time.strftime("%Y-%m-%d"))
    pin_to_top = models.BooleanField(default=False)
    tags = TaggableManager()

    def get_similar_by_tags(self):
        posts = self.tags.similar_objects()
        return posts

    def get_similar_by_title(self):
        stop_words = get_stop_words('english')
        title_words = re.findall(r"\w+", self.title)
        posts = []
        for word in title_words:
            if word not in stop_words:
                post_list = BlogPost.objects.filter(title__contains=word).exclude(pk=self.pk).all()
                for post in post_list:
                    if post not in post_list:
                        posts.append(post)
            return posts

    def get_random_posts(self):
        all_posts = BlogPost.objects.exclude(pk=self.pk).all()
        return [post for post in all_posts]

    @property
    def get_similar(self):
        number = 3
        similar = self.get_similar_by_tags()
        if len(similar) >= number:
            return similar[:number]
        similar = self.get_similar_by_title()
        if len(similar) >= number:
            return similar[:number]
        return self.get_random_posts()[:number]

    def __str__(self):
        return self.title + ', created at: '+self.creation_date.isoformat()
