from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User


# 테스트 명령어 실행 -> python manage.py test
# 명령어 실행 시 각각의 앱 경로 하위의 test.py 파일을 찾아 실행
# beautifulsoup4 -> 브라우저에 구현한 내용이 제대로 표현됐는지 확인하는 라이브러리

# Create your tests here.
class TestView(TestCase):
    # 테스트 실행 전 공통적으로 수행할 작업에 대한 내용 설정
    def setUp(self):
        self.client = Client()
        # Client()->실제 경로의 뷰
        self.jiwoo = User.objects.create(username="jiwoo", password="jiwoo1234")
        self.test_jiwoo = User.objects.create(username="test_jiwoo", password="jiwoo1234")

        self.category_com = Category.objects.create(name="computer", slug="computer")
        self.category_edu = Category.objects.create(name="education", slug="education")

        self.post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.", author=self.jiwoo,
                                            category=self.category_com)
        self.post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다.", author=self.test_jiwoo,
                                            category=self.category_edu)
        self.post_003 = Post.objects.create(title="세번째 포스트", content="세번째 포스트입니다.", author=self.jiwoo)

    def nav_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About_Me', navbar.text)

        home_btn = navbar.find('a', text="Home")
        self.assertEqual(home_btn.attrs['href'], '/')
        blog_btn = navbar.find('a', text="Blog")
        self.assertEqual(blog_btn.attrs['href'], '/blog/')
        about_btn = navbar.find('a', text="About_Me")
        self.assertEqual(about_btn.attrs['href'], '/about_me/')

    def category_test(self, soup):
        category_card = soup.find('div', id='category_card')
        self.assertIn('Categories', category_card.text)
        self.assertIn(f'{self.category_com.name} ({self.category_com.post_set.count()})', category_card.text)
        self.assertIn(f'{self.category_edu.name} ({self.category_edu.post_set.count()})', category_card.text)
        self.assertIn('미분류 (1)', category_card.text)

        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id="main-area")
        self.assertIn(self.post_001.title, main_area.text)
        self.assertIn(self.post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        self.assertIn(self.post_001.author.username.upper(), main_area.text)
        self.assertIn(self.post_002.author.username.upper(), main_area.text)

        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

    def test_post_list(self):
        self.assertEqual(3, 3)  # 괄호 안에 있는 것들끼리 같은지 확인

        # client.get()을 이용해 특정 uri 값을 웹에서 접속했을 때의 내용을 가져옴
        response = self.client.get('/blog/')
        # response 결과가 정상적으로 보이는 지 확인
        self.assertEqual(response.status_code, 200)

        # html 파일을 가져와 분석 -> 태그별 분석 가능
        soup = BeautifulSoup(response.content, 'html.parser')

        # title 이 정상적으로 보이는 지 확인
        # soup.title 하면 태그 포함된 내용 리턴 : <title>Blog</title>
        self.assertEqual(soup.title.text, 'BLOG')

        # navbar 가 정상적으로 보이는 지 확인 -> 함수 모듈화 하여 여러 곳에서 사용
        # navbar = soup.nav
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About_Me', navbar.text)
        self.nav_test(soup)
        self.category_test(soup)

        # post 가 정상적으로 보이는 지 확인
        # 처음엔 Post 모델 없음
        # self.assertEqual(Post.objects.count(), 3)

        # div 태그 중 id 가 main-area 인 부분 찾아옴
        # main_area = soup.find('div', id="main-area")
        # self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # Post 가 추가된 경우
        # post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.", author=self.jiwoo)
        # post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다.", author=self.test_jiwoo)


    def test_post_detail(self):
        post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.", author=self.jiwoo)
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        # navbar = soup.nav
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About_Me', navbar.text)
        self.nav_test(soup)
        self.category_test(soup)

        self.assertIn(post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)
        self.assertIn(post_001.content, post_area.text)
        self.assertIn(post_001.author.username.upper(), post_area.text)
