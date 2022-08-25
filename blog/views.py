from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, User
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator

def home(request):
    p = Paginator(Post.objects.all(), 10)
    page = request.GET.get('page')
    # posts = Post.objects.all().order_by('updated_at')

    posts = p.get_page(page)
    nums = 'a' * posts.paginator.num_pages
    context = {
        'posts': posts,
        # 'nums': nums,
    }

    return render(request, 'blog/index.html', context)


def all_posts(request):
    posts = Post.objects.all().order_by('title')
    context = {'posts': posts}
    return render(request, 'blog/all_posts.html', context)


def post_create(request):
    submitted = False
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect('/post-create?submitted=True')
    else:
        form = PostForm()

    if 'submitted' in request.GET:
        submitted = True
    context = {
        'form': form,
        'submitted': submitted
    }
    return render(request, 'blog/post_create.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {'post': post}
    return render(request, 'blog/post_read.html', context)


def post_update(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        if request.user == post.author:
            form.save()
            messages.success(request, f'{post.title[:30]} is updated successfully!')
        return redirect('home')

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/post_update.html', context)


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author or request.user.is_superuser:
        post.delete()
        messages.success(request, 'Successfully deleted.')
    else:
        messages.warning(request, 'You cannot delete other\'s form')
    return redirect('home')


def search_post(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        posts = Post.objects.filter(content__contains=searched)
        context = {
            'searched': searched,
            'posts': posts,
        }
        return render(request, 'blog/search_post.html', context)
    else:
        return render(request, 'blog/search_post.html')


def admin_page(request):
    posts_count = Post.objects.all().count()
    users_count = User.objects.all().count()
    posts_list = Post.objects.all().order_by('title')
    context = {
        'posts_count': posts_count,
        'users_count': users_count,
        'posts': posts_list
    }
    if request.user.is_superuser:
        if request.method == 'POST':
            id_list = request.POST.getlist('boxes')
            # undelete all posts
            posts_list.update(deleted=False)
            for x in id_list:
                Post.objects.filter(pk=int(x)).update(deleted=True)

            messages.success(request, 'Have been deleted')
            return redirect('admin-page')
        else:
            return render(request, 'blog/admin_page.html', context)

    else:
        messages.warning(request, 'You are not authorized to view this page')
        return redirect('home')


def user_posts(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user).order_by('updated_at')
        return render(request, 'blog/user_posts.html', {'posts': posts})
    else:
        return render(request, 'blog/user_posts.html')


# def add_comment(request, pk):
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             form.save()
#     else:
#         form = CommentForm()
#     return render(request, 'blog/add_comments.html', {'form': form})
