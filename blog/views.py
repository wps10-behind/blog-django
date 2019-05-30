from django.shortcuts import render
import math
from django.views.generic.list import ListView
from .models import Category, Post
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.db.models import Q

from .forms import CategoryForm, PostForm

# Create your views here.

class PostList(ListView):
    model = Post
    print(model.title)
    template_name = 'blog/post_list.html'

def post_list(request, category_id=0):
    page = int(request.GET.get('page', 1))
    paginated_by = 6

    search_type = request.GET.getlist('search_type', None)

    if not search_type:
        search_type = ['text']

    search_key = request.GET.get('search_key', None)
    search_q = None

    option_q = Q(post__category__id__contains=category_id)
    if search_key:
        if 'title' in search_type:
            temp_q = Q(title__icontains=search_key)
            search_q = search_q | temp_q & option_q if search_q else temp_q & option_q
        if 'text' in search_type:
            temp_q = Q(text__icontains=search_key)
            search_q = search_q | temp_q & option_q if search_q else temp_q & option_q
        if 'username' in search_type:
            temp_q = Q(author__username__icontains=search_key)
            search_q = search_q | temp_q & option_q if search_q else temp_q & option_q

        if category_id==0:
            posts = Post.objects.all()
        else:
            posts = get_list_or_404(Post, search_q)
    else:
        posts = Post.objects.all()

    if(category_id==0):
        posts = Post.objects.all()

    total_count = len(posts)
    total_page = math.ceil(total_count / paginated_by)
    page_range = range(1, total_page + 1)

    start_index = paginated_by * (page-1)
    end_index = paginated_by * page

    posts = posts[start_index:end_index]

    count = Post.objects.count()
    return render(request, 'blog/post_list.html', {'object_list': posts, 'total_page': total_page, 'page_range': page_range, 'count':count})

def post_create(request):
    if not request.user.is_authenticated:
        messages.warning(request, "게시물을 생성 할 권한이 없습니다")
        return render(request, 'blog/post_list.html',{'fuck':1})
    else:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            form.instance.author_id = request.user.id
            if form.is_valid():
                form.save()
                return redirect(reverse("blog:index"))
        else:
            form = PostForm()

        return render(request, 'blog/post_create.html',{'form':form})

def post_update(request, post_id):
    if not request.user.is_authenticated and not request.user.is_staff:
        messages.warning(request, "게시물을 수정 할 권한이 없습니다")
        return render(request, 'blog/post_list.html',{'fuck':1})
    else:
        if request.method == "POST":
            post = Post.objects.get(pk=post_id)
            form = PostForm(request.POST, request.FILES, instance=post)

            if form.is_valid():
                form.save()
                return redirect(reverse("post:index"))
        else:
            post = Post.objects.get(pk=post_id)
            form = PostForm(instance=post)

        return render(request, 'blog/post_update.html',{'form':form})

def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.created

    if request.user != post.author and not request.user.is_staff:
        messages.warning(request, "권한 없음")
        return render(request, 'blog/post_list.html',{'fuck':1})

    if request.method == "POST":
        post.delete()
        return redirect(reverse("blog:index"))
    else:
        return render(request, 'blog/post_delete.html', {'object': post})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'blog/post_detail.html', {'object':post})