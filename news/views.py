from django.urls import reverse_lazy
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    ListView, DetailView,  CreateView, UpdateView, DeleteView, TemplateView
)
from requests import request
from django.conf import settings
from .models import*
from .filters import PostFilter
from .forms import PostForm
from django.views import View
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.template.loader import render_to_string
from .tasks import notify_post


def news_home(request):
    news = Post.objects.all()
    return render(request, 'posts.html', {'news': news})


class PostList(ListView):
    model = Post
    ordering = 'title'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostSearch(ListView):
    model = Post
    ordering = ['title']
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
       queryset = super().get_queryset()
       self.filterset = PostFilter(self.request.GET, queryset)
       return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for category in self.get_object().postCategory.all():
            if not isinstance(self.request.user, AnonymousUser):
                context['is_not_subscriber'] = self.request.user.category_set.filter(pk=category.pk).exists()
                return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(pk=id)
    is_subscribers = category.subscribers.filter(id=user.id).exists()
    if not is_subscribers:
        category.subscribers.add(user)
        html_content = render_to_string('posts/subscribe.html',
                                        {
                                            'user': user,
                                            'category': category.name,
                                }
                                        )
        message = EmailMultiAlternatives(
            subject=f'{user} подписка на новости {category.name} оформлена!',
            from_email=settings.EMAIL,
            to = [user.email],
        )
        message.attach_alternative(html_content, 'text/html')
        try:
            message.send()
        except Exception as e:
            print(e)
        finally:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def unsubscribe(request, postCategory):
    user = request.user
    category = Category.objects.get(pk=postCategory)
    is_subscribers = category.subscribers.filter(id=user.id).exists()
    if is_subscribers:
        category.subscribers.delete(user)
        return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class PostCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'edit.html'
    permission_required = ('news.add_post')
    contex_object_name = 'create'

    def create_post(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/posts/')

        form = PostForm()
        return render(request, 'news_create.html', {'form': form})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author_post = Author.objects.get(
            author_user = self.request.user
        )
        self.object.save()
        return super().form_valid(form)


class ArticlesPostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_create.html'

    def create_articles(request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/posts/')

        form = PostForm()
        return render(request, 'articles_create.html', {'form': form})

    def form_valid(self, form):
        articles = form.save(commit=False)
        articles.categories = 'AR'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    context_object_name = 'new_edit'


class ArticlesPostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'
    context_object_name = 'articles_edit'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts')


class ArticlesPostDelete(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('posts')

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = User.objects.get(name = 'author')
    if not request.user.groups.filter(name='author').exists():
        premium_group.user_set.add(user)
    return redirect('/posts/')


class CategoryListView(ListView):
    model = Post
    template_name = 'posts/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self. categoryThrough = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.categoryThroughy).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber']= self.request.user not in self.categoryThrough.subscribers.all()
        context['category']=self.categoryThrough
        return context







