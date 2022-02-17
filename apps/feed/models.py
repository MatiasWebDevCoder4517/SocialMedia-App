from django.db import models

from django.contrib.auth.models import User


class Post(models.Model):
    body = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.body


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes',
                             on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post
