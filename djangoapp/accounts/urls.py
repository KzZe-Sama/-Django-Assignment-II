from django.urls import path

from .views import LoginView,ProfileView,LogoutView,SignupView
urlpatterns=[
path('login/',LoginView.as_view()),
path('profile/',ProfileView.as_view(),name='profile'),
path('logout/',LogoutView.as_view()),
path('signup/',SignupView.as_view()),
]
