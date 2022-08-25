from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login-user'),
    path('logout/', views.logout_user, name='logout-user'),
    path('signup/', views.signup_user, name='signup-user'),
    path('profile/', views.profile, name='profile'),
]
