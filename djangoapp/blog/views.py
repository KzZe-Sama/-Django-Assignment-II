from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
from django.views import generic
from django.views.generic import CreateView,UpdateView,DeleteView
from .models import Post
from .forms import PostForm
@method_decorator(login_required, name='dispatch')
class PostList(generic.ListView):

    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/index.html'
    paginate_by = 3

@method_decorator(login_required, name='dispatch')
class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

@method_decorator(login_required, name='dispatch')
class BLogPostView(CreateView):
    form_class = PostForm
    template_name = 'blog/post.html'
    success_url = "/blog/"

    # only logged user creates this
    def form_valid(self, form):
        self.object=form.save(commit=False)
        self.object.author=self.request.user
        self.object.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class DeletePostView(DeleteView):
    model=PostForm
    success_url = "/blog/myblog/"

    # only logged user creates this
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    def get(self,request,*args,**kwargs):
        return self.post(request,*args,**kwargs)


@login_required()
def my_blog(request):
    from .models import Post
    blogs=Post.objects.filter(author=request.user)
    return render(request,'blog/myblogs.html',{'posts':blogs})
