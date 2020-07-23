from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('create/', views.BLogPostView.as_view(), name='createBlog'),
    path('myblog/', views.my_blog, name='MyBlogs'),
    path('myblog/delete/<int:pk>/', views.DeletePostView.as_view(), name='delete'),
    path('myblog/update/<int:pk>/', views.BLogUpdateView.as_view(), name='update'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]