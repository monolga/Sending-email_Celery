from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'author',
           'title',
           'text',
           'categoryType',
       ]

       def clean(self):
           cleaned_data = super().clean()
           author = cleaned_data.get("author")
           title = cleaned_data.get("title")
           text = cleaned_data.get("text")
           if title == text:
               raise ValidationError(
                   "Описание не должно быть идентично названию."
               )
           return cleaned_data


class ArticlesPostForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'author',
           'title',
           'text',
           'categoryType',
       ]

       def clean(self):
           cleaned_data = super().clean()
           title = cleaned_data.get("title")
           text = cleaned_data.get("text")
           if title == text:
               raise ValidationError(
                   "Описание не должно быть идентично названию."
               )
           return cleaned_data

class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
        ]
