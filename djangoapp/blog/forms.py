from django.forms import ModelForm
from .models import Post
from django import forms

class PostForm(ModelForm):
    class Meta:
        model=Post
        fields=['title','content','status']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control'}),
        }

class UpdateForm(ModelForm):
    class Meta:
        model=Post
        fields=['title','content','status']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'content':forms.Textarea(attrs={'class':'form-control'}),
        }