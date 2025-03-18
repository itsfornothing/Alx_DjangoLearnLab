from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .form import UserForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DeleteView
from .models import Post, Comment
from django.urls import reverse_lazy


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Please provide both email and password!")
            return render(request, 'login.html')
        
        try:
            user_instance = User.objects.get(email=email)

        except User.DoesNotExist:
            messages.error(request, "Please register! You don't have an account.")
            return render(request, 'blog/login.html')

        user = authenticate(request, username=user_instance.username, password=password)
        if user:
            login(request, user)
            return redirect('home_page')
        
        messages.error(request, 'Invalid Credential!')

    return render(request, 'blog/login.html')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            if User.objects.filter(username__iexact=username).exists():
                messages.error(request, "Username is already taken, please enter another.")

            elif User.objects.filter(email__iexact=email).exists():
                messages.error(request, "You already have an account, please login instead!")

            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                login(request, user)
                return redirect('home_page')
    else:
        form = UserForm()

    return render(request, 'blog/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'blog/profile.html')


class BlogListView(ListView):
    model = Post
    template_name = 'blog/home_page.html'
    context_object_name = 'posts'

class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'posts'

    def get_object(self):
        try:
            post = Post.objects.get(author=self.request.user, pk=self.kwargs['pk'])
        except Post.DoesNotExist:
            raise Http404('Book does not exist')


class BlogCreate(CreateView):
    model = Post
    template_name = 'blog/add_blog.html'
    form_class = PostForm


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html' 
    success_url = reverse_lazy('home_page')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('home_page') 


def comment_view(request):
    all_posts = Post.objects.all()
    comments = []

    for post in all_posts:
        post_comments = Comment.objects.filter(post=post)
        comments.append(post_comments)

    if comments:
        return render(request, 'blog/home_page.html', {'comments': comments})
    else:
        return render(request, 'blog/home_page.html', {'comments': "No Comment"})
        
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)
        
    
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    success_url = reverse_lazy('home_page')

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    success_url = reverse_lazy('home_page')

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

   
