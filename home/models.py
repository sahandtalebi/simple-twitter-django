from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

UserModel = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.body}'

    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id, ))

    def likes_count(self):
        return self.pvote.count()

    def user_can_like(self, user):
        user_like = user.uvote.filter(post=self)
        if user_like:
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pcomments')
    replay = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='rcomment')
    is_replay = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body} - {self.post}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvote')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='pvote')

    def __str__(self):
        return f'{self.user} liked {self.post.slug}'
