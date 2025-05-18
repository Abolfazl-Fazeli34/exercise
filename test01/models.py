from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISH)

class Post(models.Model):

    class Status(models.TextChoices):
        PUBLISH = 'PB' ,'Publish'
        DRAFT = 'DF' ,'Draft'
        REJECTED = 'RJ' ,'Rejected'

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    title = models.CharField(max_length=255, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='اسلاگ')
    published = models.DateTimeField(default=timezone.now, verbose_name='زمان ایجاد')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published']
        indexes = [models.Index(fields=['published'], name='published_index')]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return f'title post : {self.title}'