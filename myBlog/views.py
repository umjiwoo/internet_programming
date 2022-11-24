from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from myBlog.models import Post, Category, Tag, Comment
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404


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
    paginate_by = 5

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
        context['comment_form'] = CommentForm  # 컨텍스트에 CommentForm 객체 함께 보내 화면에서 해당 폼 사용
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
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()
                tags_str = tags_str.replace(',', ';')
                tag_list = tags_str.split(';')

            for t in tag_list:
                t = t.strip()
                tag, created = Tag.objects.get_or_create(name=t)
                if created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)  # 생성된 객체에 생성한 tag 추가
            return response
        else:
            return redirect('/blog/')

    def get_context_data(self, **kwargs):
        context = super(PostCreate, self).get_context_data()  # 템플릿으로 전달할 내용을 담음
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context


class PostUpdate(UpdateView, LoginRequiredMixin):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    template_name = 'myBlog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):  #dispatch 가 request 시 어떤 http 메소드를 사용해 들어오는 지 파악하고 POST면 form_valid 실행
        response = super(PostUpdate, self).form_valid(form)

        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tag_list = tags_str.split(';')

        for t in tag_list:
            t = t.strip()
            tag, created = Tag.objects.get_or_create(name=t)
            if created:
                tag.slug = slugify(t, allow_unicode=True)
                tag.save()
            self.object.tags.add(tag)  # 생성된 객체에 생성한 tag 추가

        return response

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()  # 템플릿으로 전달할 내용을 담음

        if self.object.tags.exists:
            tag_str_list = list()
            for t in self.object.tags.all():
                tag_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tag_str_list)
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context


def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user  # 댓글 작성 요청자는 로그인한 유저
                comment.save()
                return redirect(comment.get_absolute_url())

        else:  # 요청 메소드가 POST가 아닌 경우
            return redirect(post.get_absolute_url())
    else:  # 요청자가 로근이 유저 아닌 경우
        raise PermissionDenied


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    # 템플릿 매개변수 -> comment_form.html

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


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
