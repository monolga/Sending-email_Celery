from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, ProfileUserUpdate, IndexView
from .views import upgrade_me


urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
    path('profile/<int:pk>/edit/', ProfileUserUpdate.as_view(template_name='profile_edit.html'), name = 'profile_user_edit'),
    path('', IndexView.as_view()),
    path('upgrade/', upgrade_me, name='upgrade'),
]
