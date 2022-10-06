from django.db import models


class Post(models.Model):  # 클래스 이름이 곧 모델 이름
    title = models.CharField(max_length=30)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)

    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO author 필드 추가

    def __str__(self):
        return f'[{self.pk}] {self.title} {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
