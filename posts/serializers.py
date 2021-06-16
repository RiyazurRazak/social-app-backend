from rest_framework import serializers
from .models import Post, Comments
from account.models import Account


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "username", "avatar"]


class ReplySerializer(serializers.ModelSerializer):
    comment_user = PostUserSerializer(source='commented_by', read_only=True)

    class Meta:
        model = Comments
        fields = ["id", "comment_body", "comment_user", "commented_at", ]


class CommentSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(source='replies', read_only=True, many=True)
    comment_user = PostUserSerializer(source='commented_by', read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'comment_body', 'comment_user', 'commented_at', 'replies', 'reply', ]


class PostSerializers(serializers.ModelSerializer):
    posted_user = PostUserSerializer(source="posted_by", read_only=True)
    post_likes = PostUserSerializer(source="likes", many=True, read_only=True)
    post_comments = CommentSerializer(source='comments', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'post_url', 'bg_color', 'posted_at', 'posted_user',  "post_likes", 'post_comments', 'is_video_post', ]

