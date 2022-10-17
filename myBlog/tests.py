from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post


# 테스트 명령어 실행 -> python manage.py test
# 명령어 실행 시 각각의 앱 경로 하위의 test.py 파일을 찾아 실행
# beautifulsoup4 -> 브라우저에 구현한 내용이 제대로 표현됐는지 확인하는 라이브러리

# Create your tests here.
class TestView(TestCase):
    # 테스트 실행 전 공통적으로 수행할 작업에 대한 내용 설정
    def setUp(self):
        self.client = Client()
        # Client()->실제 경로의 뷰

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
        self.assertEqual(soup.title.text, 'Blog')

        # navbar 가 정상적으로 보이는 지 확인
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About_Me', navbar.text)

        # post 가 정상적으로 보이는 지 확인
        # 처음엔 Post 모델 없음
        self.assertEqual(Post.objects.count(), 0)

        # div 태그 중 id 가 main-area 인 부분 찾아옴
        main_area = soup.find('div', id="main-area")
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # Post 가 추가된 경우
        post_001 = Post.objects.create(title="첫번째 포스트", content="첫번째 포스트입니다.")
        post_002 = Post.objects.create(title="두번째 포스트", content="두번째 포스트입니다.")
        self.assertEqual(Post.objects.count(), 2)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id="main-area")
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

