from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Category, Post
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CategoryForm, PostForm

# Create your views here.

class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'

def post_create(request):
    if not request.user.is_authenticated:
        messages.warning(request, "게시물을 생성 할 권한이 없습니다")
        return render(request, 'blog/post_list.html',{})
    else:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            form.instance.author_id = request.user.id
            if form.is_valid():
                post = form.save()
                return redirect(reverse("blog:index"))
        else:
            form = PostForm()

        return render(request, 'blog/post_create.html',{'form':form})

def post_update(request, post_id):
    if not request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "게시물을 수정 할 권한이 없습니다")
        return render(request, 'board/album_list.html',{})
    else:
        if request.method == "POST":
            post = Post.objects.get(pk=post_id)
            form = PostForm(request.POST, request.FILES, instance=post)

            if form.is_valid():
                    post = form.save()
                    return redirect(reverse("post:index"))
        else:
            post = Post.objects.get(pk=post_id)
            form = PostForm(instance=post)

        return render(request, 'blog/post_update.html',{'form':form})

def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author and not request.user.is_staff:
        messages.warning(request, "권한 없음")
        return redirect(post)

    if request.method == "POST":
        post.delete()
        return redirect(reverse("post:index"))
    else:
        return render(request, 'blog/post_delete.html', {'object': post})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'object':post})
