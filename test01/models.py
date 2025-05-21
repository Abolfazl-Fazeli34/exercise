from cgitb import strong
from datetime import date
from time import sleep

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_jalali.db import models as jmodels
from django_resized import ResizedImageField


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
    slug = models.SlugField(max_length=255, verbose_name='اسلاگ', blank=False, null=False)
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name='زمان ایجاد')
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    reading_time = models.PositiveIntegerField(verbose_name='زمان مطالعه')

    objects = models.Manager()
    published = PublishedManager()

    def pop_slug(self):
        if not self.slug:
            self.slug = slugify(self.title)

    def save(self, *args, **kwargs):
        self.pop_slug()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        storage, path = self.img_file.storage, self.img_file.path
        storage.delete(path)
        super().delete(*args, *kwargs)

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def get_absolute_url(self):
        return reverse('test01:post_detail', kwargs={'pk': self.id})

    def __str__(self):
        return f'title post : {self.title}'

class Ticket(models.Model):
    full_name = models.CharField(max_length=255, verbose_name='نام و نام خانوادگی')
    subject = models.CharField(max_length=255, verbose_name='نوع تیکت')
    message = models.TextField(verbose_name='پیغام')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11, verbose_name='شماره همراه')

    class Meta:
        ordering = ['-subject']
        indexes = [models.Index(fields=['-subject'])]
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    def __str__(self):
        return f'full name : {self.full_name}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255, verbose_name='اسم')
    letter = models.TextField(verbose_name='متن کامنت')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True, verbose_name='وضعیت')

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'

    def __str__(self):
        return f'name: {self.name} letter: {self.letter}'

def date_directory_path(instance, filename):
    today = date.today().strftime('%B %d %Y')
    return 'exercise/{}/{}'.format(today, filename)

def user_directory_path(instance, filename):
    user = instance.post.author.username
    return 'exercise/{}/{}'.format(user, filename)

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images')
    # img_file = ResizedImageField(upload_to='images',size=[120,120], scale=1, crop=['center', 'middle'], verbose_name='عکس')
    # img_file = ResizedImageField(upload_to=date_directory_path,size=[120,120], scale=1, crop=['center', 'middle'], verbose_name='عکس')
    img_file = ResizedImageField(upload_to=user_directory_path, verbose_name='عکس', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات عکس')
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]
        verbose_name = 'عکس'
        verbose_name_plural = 'عکس ها'
    def __str__(self):
        return '{}'.format(self.title) if self.title else '{}'.format(self.img_file)
