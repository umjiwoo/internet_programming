from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),  # IP 주소/admin/
    path('blog/', include('myBlog.urls')),  # IP 주소/blog/
    path('', include('single_pages.urls')),  # IP 주소/
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
