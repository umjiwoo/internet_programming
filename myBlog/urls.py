from django.urls import path

from myBlog import views

urlpatterns = [
    # FunctionBasedView
    # path('', views.index),
    # path('<int:pk>/', views.single_post_page),

    # ClssBasedView
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('category/<str:slug>/', views.category_page),
    path('tag/<str:slug>/', views.tag_page),
]
