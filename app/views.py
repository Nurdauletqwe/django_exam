from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Post, Comment, Notification
from .forms import UserRegistrationForm, PostForm, CommentForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('app:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('app:index')
        else:
            return render(request, 'app/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'app/index.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('app:index')
    else:
        form = PostForm()
    return render(request, 'app/create_post.html', {'form': form})

@login_required
def my_posts(request):
    posts = request.user.posts.all()
    return render(request, 'app/my_posts.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent=None)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            if comment.post.author != request.user:
                Notification.objects.create(user=comment.post.author, comment=comment)
            return redirect('app:post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'app/post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def profile(request):
    return render(request, 'app/profile.html', {'user': request.user})

@login_required
def notifications(request):
    notifications = request.user.notifications.filter(is_read=False)
    return render(request, 'app/notifications.html', {'notifications': notifications})

@login_required
def notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('app:notifications')
