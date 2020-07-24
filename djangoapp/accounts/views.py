from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .forms import LoginForm, SignUpForm, Verify
from django.contrib.auth import authenticate, login, logout
from .email_backend import EmailBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from .models import Profile
import random
from django.contrib.auth.models import User

from django.views.generic import TemplateView
from django.utils.encoding import  force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import  urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
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
class ProfileView(TemplateView):

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(user=request.user)
        if len(profile) != 0:
            return render(request, 'accounts/profile.html', {'image': profile[0]})
        else:
            return render(request, 'accounts/profile.html')

    def post(self, request, *args, **kwargs):
        if request.FILES:

            file_obj = request.FILES['photo']
            file_name = file_obj.name
            split_ext = file_name.split('.')
            ext = split_ext[1]
            ext = ext.lower()
            if ext == 'jpg' or ext == 'png' or ext == 'jpeg':
                if len(Profile.objects.filter(user=request.user)) == 0:
                    profile = Profile(user=str(request.user), image=file_obj)
                    profile.save()
                    return redirect('/accounts/profile/')
                else:
                    obj = Profile.objects.get(user=request.user)
                    obj.image = file_obj
                    obj.save()
                    return redirect('/accounts/profile/')
            else:
                messages.error(request, 'Upload PNG,JPEG/JPG extensions only.')
            return render(request, 'accounts/profile.html')
        else:
            messages.error(request, 'Please Upload Your Photo First.')
            return redirect('/accounts/profile/')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/accounts/login/')


class SignupView(View):
    user = object
    v_code = ""

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = USER(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],

            )

            # # Email Verification Mail




            user.save()
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            uidb64=urlsafe_base64_encode(force_bytes(user.pk))

            domain=get_current_site(request).domain
            link=reverse('verify',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
            subject = "Verify Yourself"
            activate_url='http://'+domain+link
            message = f"Hi {user.username}, Please use this link to verify your account"+'\n'+activate_url
            recp = [form.cleaned_data['email'], ]
            email = EmailMessage(
                subject,
                message,
                'admin@gmail.com',
                recp,
            )
            email.send(fail_silently=False)

            # user.save()
            Profile(user=form.cleaned_data['username']).save()
            messages.success(request,'We Have Sent You A Verification Email.')
            return redirect('/accounts/login/')
        return render(request, 'accounts/register.html', {'form': form})


class Verfication(View):

    def get(self,request,uidb64,token):
        try:
            id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)
            if not token_generator.check_token(user,token):
                return redirect('Login'+'?message='+'User is Already Verified.')
            if user.is_active:
                return redirect('Login')
            user.is_active=True
            user.save()
            messages.success(request,'Account Activated Successfully')
            return redirect('Login')
        except Exception as e:
            pass

        return redirect('Login')