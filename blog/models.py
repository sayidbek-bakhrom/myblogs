from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from django.shortcuts import reverse


class Post(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='images/', blank=True)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.author.username}-{self.title}')
        return super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    comment = models.CharField(max_length=140)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs=self.post.pk)
