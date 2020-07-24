from django.urls import path

from .views import LoginView,ProfileView,LogoutView,SignupView,Verfication
urlpatterns=[
path('login/',LoginView.as_view(),name='Login'),
path('profile/',ProfileView.as_view(),name='profile'),
path('logout/',LogoutView.as_view()),
path('signup/',SignupView.as_view()),
path('activate/<uidb64>/<token>',Verfication.as_view(),name="verify"),
]
