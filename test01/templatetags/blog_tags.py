from itertools import count

from django import template
from django.db.models import Count

from ..models import *


register = template.Library()

@register.simple_tag()
def total_post():
    return Post.objects.count()

@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()

@register.simple_tag()
def last_post_date():
    return Post.published.last().publish

@register.inclusion_tag(filename='partials/latest.html')
def latest_post(count=5):
    l_post = Post.published.order_by('-publish')[:count]
    return l_post

@register.simple_tag()
def most_popular_posts(count=5):
    return Post.published.annotate(comment_count=Count('comments')).order_by('-comment_count')[:count]