from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.db.models import signals
from main.tasks import send_verification_email


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete = models.CASCADE)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating = Sum('rating'))
        pRat = 0
        pRat +=postRat.get('postRating')
        commentRat = self.authorUser.comment_set.aggregate(commentRating = Sum('rating'))
        cRat = 0
        cRat =+commentRat.get('commentRating')
        cRat =+commentRat.get('commentRating')

        self.ratingAuthor = pRat*3+cRat
        self.save()

        def __str__(self):
            return self.authorUser.username


class Category(models.Model):
    name = models.CharField(max_length = 64, unique = True)
    subscribers = models.ManyToManyField(
        User,
        related_name='categories',
    )

    def __str__(self):
        return self.name()

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = [
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    ]
    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name='author')
    categoryType = models.CharField(max_length = 2, choices = CATEGORY_CHOICES, default = ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add = True)
    postCategory = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 128)
    text = models.TextField()
    rating = models.SmallIntegerField(default = 0)

    def preview(self):
        preview=f'{self.text[:124]}...'
        return preview

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

    def __str__(self):
        return f'{self.title} | {self.author}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def get_absolute_url(self):
        return f'posts/{self.id}'

def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_verified:
        # Send verification email
        send_mail(
            'Verify your QuickPublisher account',
            'Follow this link to verify your account: '
                'http://localhost:8000%s' % reverse('verify', kwargs={'uuid': str(instance.verification_uuid)}),
            'from@quickpublisher.dev',
            [instance.email],
            fail_silently=False,
        )
        signal.post_save.connect(user_post_save, sender=User)


def verify(request, uuid):
    try:
        user = User.objects.get(verification_uuid=uuid, is_verified=False)
    except User.DoesNotExist:
        raise Http404("User does not exist or is already verified")

    user.is_verified = True
    user.save()

    return redirect('news')


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete = models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete = models.CASCADE)

    def __str__(self):
        return f'{self.postThrough.title} | {self.categoryThrough.name}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete = models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete =  models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add = True)
    rating = models.SmallIntegerField(default = 0)

    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()

