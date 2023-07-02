from django.shortcuts import render, get_object_or_404
from .models import Post
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator
# Create your views here.



def board_main_view(request):
    postlist= Post.objects.all()
    paginator = Paginator(postlist, 8)

    page = request.GET.get('page')
    postlist = paginator.get_page(page)
    return render(request, 'board/board.html', {"postlist":postlist})


def posting_view(request,pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'board/posting.html', {'post':post})

def new_post_view(request):
    if request.method == 'POST':
        postname = request.POST['postname']
        content = request.POST['content']
        post = Post(postname=postname, content=content, created_by=request.user.username)
        post.save()
        return redirect(reverse('board:board'))



    return render(request, 'board/new_post.html')

def update_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        postname = request.POST['postname']
        content = request.POST['content']
        post.postname = postname
        post.content = content
        post.save()
        return redirect(reverse('board:board'))

    return render(request, 'board/update_post.html', {'post': post})


def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user.username == post.created_by:
        post.delete()

    return redirect(reverse('board:board'))