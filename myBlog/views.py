from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from myBlog.models import Post, Category, Tag


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

    # get_context_data() => 페이지에 원하는 내용 띄우기 위해 생성한 함수
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


class PostCreate(CreateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    # CreateView 호출 뷰 ->  모델명_form.html
    # 뷰에 form 이름으로 전달됨

    # ModelFormMixin 클래스 상속 함수 -> 입력받은 내용이 모델에 적합한지 확인

    def test_func(self):
        return self.reqeust.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and current_user.is_superuser or current_user.is_staff:  # 요청 보낸 유저가 인가된 유저라면
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')

    def get_context_data(self, **kwargs):
        context = super(PostCreate, self).get_context_data()  # 템플릿으로 전달할 내용을 담음
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


def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(request, 'myBlog/post_list.html', {
        'tag': tag,
        'post_list': post_list,
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count
    })
