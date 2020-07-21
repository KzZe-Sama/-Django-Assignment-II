from django.shortcuts import render
from .forms import LoginForm
# Create your views here.

def login_view(request):
    form=LoginForm()
    return render(request,'accounts/login.html',{'form':form})

def profile_view(request):
    return render(request,'accounts/profile.html')