from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # IP주소/admin/
    path('blog/', include('myBlog.urls')),

]
