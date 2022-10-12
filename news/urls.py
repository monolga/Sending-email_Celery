from django.contrib import admin
from django.urls import path
from .views import (
    PostList, PostDetail, PostCreate, PostSearch, PostUpdate, PostDelete,
    ArticlesPostCreate, ArticlesPostUpdate, ArticlesPostDelete, CategoryListView, subscribe, upgrade_me,
)

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('news_create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='new_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view()),
    path('articles_create/', ArticlesPostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', ArticlesPostUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', ArticlesPostDelete.as_view(), name = 'articles_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]

