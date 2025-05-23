from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from django.db.models.expressions import result
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST, require_GET
from .forms import TicketForm, CommentForm, CreatePostForm, PostSearchForm
from .models import *


# Create your views here.


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 6)
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
    count_img = post.post_images.count()
    context = {
        'post': post,
        'comment': comment,
        'count_img': count_img,
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
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            c_post = form.save(commit=False)
            c_post.author = request.user
            c_post.save()

            all_image = ['image1', 'image2']
            for img in all_image:
                img_file = form.cleaned_data.get(img)
                if img:
                    Image.objects.create(img_file=img_file, post=c_post)

            return redirect('test01:post_list')
    else:
        form = CreatePostForm()
    context = {
        'form': form,
    }
    return render(request, 'form/create_post.html', context)

def post_search(request):
    query = None
    result = []
    if 'query' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            # query = form.cleaned_data['query']
            # # result1 = Post.published.filter(description__icontains=query)
            # # result2 = Post.published.filter(title__icontains=query)
            # search_query = SearchQuery(query)
            # search_vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
            # result = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(rank__gte=.5).order_by('-rank')
            # # result = result1 ^ result2
            query = form.cleaned_data['query']
            result = Post.published.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
    context = {
        'query': query,
        'result': result,
    }
    return render(request, 'form/post_search.html', context)

def profile(request):
    user = request.user
    pub_posts = Post.published.filter(author=user)
    all_posts = Post.objects.filter(author=user)
    context = {
        'pub_posts': pub_posts,
        'all_posts': all_posts,
        'user': user,
    }
    return render(request, 'project/profile.html', context)


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            c_post = form.save(commit=False)
            c_post.author = request.user
            c_post.save()

            all_image = ['image1', 'image2']
            for img in all_image:
                img_file = form.cleaned_data.get(img)
                if img:
                    Image.objects.create(img_file=img_file, post=c_post)

            return redirect('test01:post_list')
    else:
        form = CreatePostForm()
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'form/edit_post.html', context)

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('test01:post_list')
    return render(request, 'project/profile.html', {'post': post})