from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('all-posts/', views.all_posts, name='all-posts'),
    path('post/<slug>/', views.post_detail, name='post-detail'),
    path('post-create/', views.post_create, name='post-create'),
    path('post-update/<slug>/', views.post_update, name='post-update'),
    path('post-delete/<slug>/', views.delete_post, name='delete-post'),
    path('search-post/', views.search_post, name='search-post'),
    path('admin-page/', views.admin_page, name='admin-page'),
    path('user-posts/', views.user_posts, name='user-posts')
]
