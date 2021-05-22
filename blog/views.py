from django.shortcuts import render
from django.http import HttpResponse
from .models import Post,Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
ListView,
DetailView,
CreateView,
UpdateView,
DeleteView,
)



# Create your views here.
def index(request):
    data = {
        'posts': Post.objects.all()
        }
    return render(request, 'home.html', data)


class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 2

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html' #<app>/<model>_<viewtype>.html

class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content'] 

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)     


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'login'
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)    

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False    

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin , DeleteView):
    login_url = '/login/' 
    redirect_field_name = 'login'

    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False    

def about(request):
    return render(request,'about.html') 


def post_detail(request, year, month, day, post):
    post =get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish_year=year, 
                                   publish_month=month,
                                   publish_day=day)

    # List of active comments for this post 
    comments = post.comments.filter(active=True)


    new_comment = None
    
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database 
            new_comment.save()
            
    else:
        comment_form = CommentForm()
    return render(request,
                 'blog/post/detail.html',
                 {'post': post,
                 'comments': comments,
                 'new_comment': new_comment, 
                 'comment_form': comment_form})






    