from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Follow, Post, Group, User
from .forms import PostForm, CommentForm
from django.conf import settings
from django.views.decorators.cache import cache_page


@cache_page(20, key_prefix="index_page")
def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    page_size = settings.DEFFAULT_PAGE_SIZE
    paginator = Paginator(posts, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'page_obj': page_obj
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_size = settings.DEFFAULT_PAGE_SIZE
    paginator = Paginator(posts, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'group': group,
        'posts': posts,
        'title': f'записи сообщества {group}',
        'description': group.description,
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    page_size = settings.DEFFAULT_PAGE_SIZE
    paginator = Paginator(posts, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    following = False
    if request.user.is_authenticated:
        following = Follow.objects.filter(
            user=request.user.id, author=author.id).exists()
    context = {
        'page_obj': page_obj,
        'count_posts': author.posts.count(),
        'author': author,
        'following': following
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post_detail = get_object_or_404(
        Post.objects.select_related(
            'author').select_related('group'), id=post_id)
    amount = post_detail.author.posts.count()
    username = post_detail.author
    comments = post_detail.comments.all()
    form = CommentForm()
    context = {
        'post_detail': post_detail,
        'amount': amount,
        'username': username,
        'form': form,
        'comments': comments
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        create_post = form.save(commit=False)
        create_post.author = request.user
        create_post.save()
        return redirect('posts:profile', create_post.author)
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/create_post.html'
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)
    context = {
        'form': form,
        'post': post,
        'is_edit': True,
        'help_text': 'текст нового поста',
        'help_group': 'группа, к которой будет относиться пост'
    }
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    template = 'posts/follow.html'
    posts = Post.objects.filter(author__following__user=request.user)
    page_size = settings.DEFFAULT_PAGE_SIZE
    paginator = Paginator(posts, page_size)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': posts,
        'page_obj': page_obj
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', author)


@login_required
def profile_unfollow(request, username):
    follower = get_object_or_404(
        Follow,
        user=request.user,
        author__username=username
    )
    follower.delete()
    return redirect('posts:profile', username)
