from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'subtitle', 'content', 'image',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment', 'name', 'post',)