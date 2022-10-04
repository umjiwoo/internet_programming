from django.shortcuts import render
from django.views.generic import ListView, DetailView
from myBlog.models import Post
# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#     return render(request, 'blog/index.html', {'posts': posts})
#
#
# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(request, 'blog/single_post_page.html', {'post': post})


# class view 이용하는 경우 템플릿 이름 자동 설정됨 ; 모델명_list.html, 모델명_detail.html
# templates 하위 디렉토리 이름을 앱 이름과 동일하게 해줘야 파일 찾기 가능
class PostList(ListView):
    model = Post
    ordering = '-pk'
    # 매개변수 => post_list


class PostDetail(DetailView):
    model = Post
    # 매개변수 => post
