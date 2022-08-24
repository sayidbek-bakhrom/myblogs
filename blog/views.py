from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, User
from .forms import PostForm
from django.http import HttpResponseRedirect
from django.contrib import messages


def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/index.html', context)


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
    if request.user.is_superuser:
        messages.success(request, 'Successfully deleted.')
        post.delete()
    if request.user == post.author:
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
