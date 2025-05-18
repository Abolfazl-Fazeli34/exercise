from django.shortcuts import render
# from django.shortcuts import redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *


# Create your views here.


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    context = {
        'posts': posts,
        'page_obj': page_obj,
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