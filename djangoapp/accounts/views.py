from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm,Verify
from django.contrib.auth import authenticate, login, logout
from .email_backend import EmailBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.core.mail import send_mail
import random
from django.views.generic import TemplateView

# Create your views here.


USER = get_user_model()


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/blog')
        form = LoginForm()
        return render(request,
                      'accounts/login.html',
                      {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            back = EmailBackend()

            user = back.authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user:
                print(" a user is found", user)
                print(user)
                login(request, user)
                return redirect("/blog")
            else:
                messages.error(request, "Login Invalid")
                return redirect('/accounts/login/')


# Soon to be implememnted on class views
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    template_name = '/accounts/login.html'



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/accounts/login/')


class SignupView(View):
    user=object
    v_code=""
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            from django.contrib.auth.models import User
            user = USER(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],

            )
            v_code=str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))

            # Email Verification Mail
            # subject="Verify Yourself"
            # message=f"Your Code is :{v_code}"
            # recp=[form.cleaned_data['email'],]
            # send_mail(
            #     subject,
            #     message,
            #     'noreply@admin.com',
            #     recp,
            #     fail_silently=False,
            # )

            # if request.method == "POST":
            #     form=Verify(request.POST)
            #     if form.is_valid():
            #         print(form.cleaned_data['code'])
            #         return render(request,'accounts/verify.html',{'form':form})


            user.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/accounts/login/')
        return render(request, 'accounts/register.html', {'form': form})











