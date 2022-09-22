from django.db import models


class Post(models.Model):  # 클래스 이름이 곧 모델 이름
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO author 필드 추가

    def __str__(self):
        return f'[{self.pk}] {self.title}'
