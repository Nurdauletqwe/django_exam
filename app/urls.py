from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(template_name="app/logout.html",next_page="app:login"), name='logout'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/read/<int:notification_id>/', views.notification_read, name='notification_read'),
]
