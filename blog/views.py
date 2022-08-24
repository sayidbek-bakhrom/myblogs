from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
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
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
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
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        messages.success(request, f'{post.title} is updated successfully!')
        return redirect('home')

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'blog/post_update.html', context)


def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, 'Successfully deleted, ')
    return redirect('home')



