from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Talk(models.Model):
    body = models.CharField(max_length=255)
    pic = models.ImageField(upload_to='uploads/', blank=True, null=True)
    tags = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(
        User, related_name='talks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.body


## TESTING COMMENT (¿CONVERSATION MODEL ATTACHMENT?) ##
""" 
# Comment model links a comment with the post and the user.
 
class Comments(models.Model):
	post = models.ForeignKey(Post, related_name='details', on_delete=models.CASCADE)
	username = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
	comment = models.CharField(max_length=255)
	comment_date = models.DateTimeField(default=timezone.now)

"""

class Like(models.Model):
    talk = models.ForeignKey(Talk, related_name='likes',
                             on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
