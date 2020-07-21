from django.shortcuts import render,redirect
from .forms import LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
# Create your views here.

def login_view(request):
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            user=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user:
                    #user found
                login(request,user)
                return redirect('/accounts/profile/')
            else:
                return dec
    elif request.method == "GET":
        form=LoginForm()
    return render(request,'accounts/login.html',{'form':form})

@login_required()
def profile_view(request):
    return render(request,'accounts/profile.html')