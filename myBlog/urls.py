from django.urls import path

from myBlog import views

urlpatterns = [
    path('', views.index),
    path('<int:pk>/', views.single_post_page),
]