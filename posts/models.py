from django.db import models
from account.models import Account
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Comments(models.Model):
    commented_by = models.ForeignKey(Account, related_name="commented_user", on_delete=models.CASCADE)
    comment_body = models.TextField(max_length=150)
    commented_at = models.DateTimeField(auto_now_add=True)
    replies = models.ManyToManyField("Comments", related_name="reply",)


class Post(models.Model):
    post_url = models.URLField(null=True)
    bg_color = models.CharField(max_length=6)
    posted_by = models.ForeignKey(Account, related_name="posted_by", on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Account, related_name="user_likes")
    comments = models.ManyToManyField(Comments, related_name="comment")
    is_video_post = models.BooleanField(default=False)
