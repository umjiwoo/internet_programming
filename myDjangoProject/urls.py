from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # IP 주소/admin/
    path('blog/', include('myBlog.urls')),  # IP 주소/blog/
    path('', include('single_pages.urls')),  # IP 주소/
    # path(''),
]
