from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST, require_GET
from .forms import TicketForm, CommentForm, CreatePostForm
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
        'page_obj': page_obj,
    }
    return render(request, 'project/post_list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISH)
    comment = post.comments.filter(active=True)
    context = {
        'post': post,
        'comment': comment,
    }
    return render(request, 'project/post_details.html', context)

def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(
                full_name=cd['full_name'],
                subject=cd['subject'],
                message=cd['message'],
                email=cd['email'],
                phone=cd['phone'],
            )
            redirect('test01:post_list')
    else:
        form = TicketForm()
    return render(request, 'form/ticket.html', context={'form': form})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISH)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }
    return render(request, 'form/comment.html', context)

# @require_POST
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Post.objects.create(
                author=request.user,
                title=cd['title'],
                description=cd['description'],
                reading_time=cd['reading_time'],
            )
            return redirect('test01:post_list')
    else:
        form = CreatePostForm()
    context = {
        'form': form,
    }
    return render(request, 'form/create_post.html', context)