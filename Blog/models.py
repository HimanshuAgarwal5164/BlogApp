##Models is used to create our database


from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class DraftManager(models.Manager):
    def get_queryset(self):
        return super(DraftManager, self).get_queryset().filter(status='draft')


class Post(models.Model):    #Creating a table in our database
    STATUS_CHOICES = (
    ('draft', 'Draft'),      #Shows if a blog has been saved as a draft
    ('published', 'Published'),   #Shows if a blog has been published
    )
    title = models.CharField(max_length = 500)
    slug = models.SlugField(max_length = 500, unique_for_date = 'publish')
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
            return self.title

    objects = models.Manager()    #Default PublishedManager
    published = PublishedManager()    #Custom Manager
    draft = DraftManager()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,self.publish.month, self.publish.day, self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
