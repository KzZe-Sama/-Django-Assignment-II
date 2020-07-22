from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
from django.views import generic
from .models import Post

@method_decorator(login_required, name='dispatch')
class PostList(generic.ListView):

    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'
    paginate_by = 3

@method_decorator(login_required, name='dispatch')
class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

