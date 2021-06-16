from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comments
from .serializers import PostSerializers
from account.pagination import CustomPagination
from rest_framework.parsers import JSONParser
import requests
import io
from colorthief import ColorThief


def rgb2hex(r,g,b):
    return "{:02x}{:02x}{:02x}".format(r,g,b)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    if request.method == 'GET':
        user = request.user
        paginator = CustomPagination()
        user_following = user.following.all()
        following_users = [i.following_user_id for i in user_following]
        post = Post.objects.filter(posted_by__in=following_users).order_by("-posted_at")
        pagination_data = paginator.paginate_queryset(post, request)
        serializer = PostSerializers(pagination_data, many=True)
        json_data = serializer.data
        data = paginator.get_paginated_response(json_data)
        return Response(data, status=200)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def explore(request):
    paginator = CustomPagination()
    post = Post.objects.all().order_by("-posted_at")
    pagination_data = paginator.paginate_queryset(post, request)
    serializer = PostSerializers(pagination_data, many=True)
    json_data = serializer.data
    data = paginator.get_paginated_response(json_data)
    return Response(data, status=200)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_post(request):
    user = request.user
    post_data = JSONParser().parse(request)
    if "post_url" in post_data:
        fd = requests.get(post_data["post_url"], stream=True)
        f = io.BytesIO(fd.content)
        color_thief = ColorThief(f)
        rgb = (color_thief.get_color(quality=1))
        _hex = rgb2hex(rgb[0], rgb[1], rgb[2])
        post = Post(post_url=post_data['post_url'], bg_color=_hex, posted_by=user, is_video_post=post_data['is_video'])
        post.save()
        serializer = PostSerializers(post)
        data = serializer.data
        return Response(data, status=201)


@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    print(post_id)
    if request.method == 'PUT':
        liked_user = request.user
        if post_id:
            post = Post.objects.get(id=post_id)
            post.likes.add(liked_user)
            post.save()
            return Response("saved")
        else:
            return Response("Post Id Missing", status=400)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_comment(request):
    comment_data = JSONParser().parse(request)
    user = request.user
    if 'post_id' in comment_data:
        try:
            post = Post.objects.get(id=comment_data["post_id"])
            comment = Comments(commented_by=user, comment_body=comment_data["comment_body"], )
            comment.save()
            post.comments.add(comment)
            post.save()
            return Response("comment Saved Successfully", status=201)
        except Post.DoesNotExist:
            return Response("Post Not Found", status=404)
    else:
        return Response("Post ID is missing", status=400)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_comment_reply(request):
    user = request.user
    reply_data = JSONParser().parse(request)
    if "comment_id" in reply_data:
        try:
            comment = Comments.objects.get(id=reply_data["comment_id"])
            reply = Comments(commented_by=user, comment_body=reply_data["comment_body"], )
            reply.save()
            comment.replies.add(reply)
            comment.save()
            return Response("saved", status=201)
        except Comments.DoesNotExist:
            return Response("Comment Does Not Exist", status=404)
    else:
        return Response("Comment Id is missing", status=400)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    post.delete()
    return Response("Post Deleted Successfully", status=200)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    user = request.user
    comment = Comments.objects.get(id=comment_id)
    if comment.commented_by == user:
        print(comment.replies.all())
        reply_id = [reply.id for reply in comment.replies.all()]
        replies = Comments.objects.filter(id__in=reply_id)
        replies.delete()
        comment.delete()
        return Response("Comment Deleted SuccessFully",status=200)
    else:
        return Response("Not Authorize to delete this comment",status=401)