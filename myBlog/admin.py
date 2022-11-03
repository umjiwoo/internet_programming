from django.contrib import admin
from .models import Post, Category

admin.site.register(Post)


# prepopulated_fields 옵션을 통해 slug 필드값 자동 지정
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)
