from itertools import count
from django.utils import timezone
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown

from ..models import *


register = template.Library()

@register.simple_tag()
def total_post() -> list:
    return Post.objects.count()

@register.simple_tag()
def total_comments() -> list:
    return Comment.objects.filter(active=True).count()

@register.simple_tag()
def last_post_date() -> timezone.datetime:
    return Post.published.last().publish

# ------- نکته مهم اینجاست که در استفاده از inclusion_tag() یک رشته را بر میگرداند و با اون باید به صورت یک رشته رفتار کرد

@register.inclusion_tag(filename='partials/latest.html')
def latest_post(count:int=5) -> dict:
    l_post = Post.published.order_by('-publish')[:count]
    l_post = {'l_post': l_post}
    return l_post

@register.simple_tag()
def most_popular_posts(count:int=5) -> list:
    return Post.published.annotate(comment_count=Count('comments')).order_by('-comment_count')[:count]

@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))
# نمایش بشترین زمان های پست هایی ک وجود داره
@register.simple_tag()
def max_reading_time_post() -> list:
    return Post.published.order_by("-reading_time")[:5].first()

@register.simple_tag()
def min_reading_time_post() -> list:
    return Post.published.order_by("-reading_time")[:5].last()

@register.simple_tag()
def most_total_user() -> list:
    return User.objects.annotate(total_post=Count('user_posts')).order_by('-total_post').first()

@register.simple_tag()
def text_censor(text) -> str:
    censor = ['A','B','C','D','E','F','G']
    for c in censor:
        if c in text:
            text.replace(c,'...')
    return text

# @register.simple_tag()
# def count_post_img(id_post):
#     return Post.published.filter(id=id_post)