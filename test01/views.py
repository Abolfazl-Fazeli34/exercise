from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from .models import *


# Create your views here.


def post_list(request):
    posts = Post.published.all()
    context = {
        'posts': posts,
    }
    return render(request, 'project/post_list.html', context)

def post_detail(request, pk):
    try:
        post = Post.published.get(pk=pk)
    except:
        raise Http404("page not found")
    context = {
        'post': post,
    }
    return render(request, 'project/post_details.html', context)