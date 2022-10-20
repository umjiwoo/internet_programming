import os

from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):  # 클래스 이름이 곧 모델 이름
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)  # 미리 보기
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)

    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Post의 외래키로 지정된 User 객체가 삭제되어도 해당 User가 게시한 Post 객체는 없어지지 않도록 함
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}] {self.title} - {self.author}     {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)  # os.path.basename()으로 경로 빼고 이름만 추출해줌

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
