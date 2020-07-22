from django.urls import path

from .views import LoginView,profile_view,LogoutView,SignupView
urlpatterns=[
path('login/',LoginView.as_view()),
path('profile/',profile_view),
path('logout/',LogoutView.as_view()),
path('signup/',SignupView.as_view()),
]
