from django.shortcuts import render
from django.views.generic import ListView, DetailView
from myBlog.models import Post, Category
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context


class PostDetail(DetailView):
    model = Post
    # 매개변수 => post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()  # 템플릿으로 전달할 내용을 담음
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context


def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(request, 'myBlog/post_list.html', {
        'category': category,
        'post_list': post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count
    })
