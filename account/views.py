from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Account, UserFollowing
from .serialisers import UserSerializer, UserFollowingSerializer, UserFollowSerializer
from .pagination import CustomPagination
from rest_framework.parsers import JSONParser
from posts.models import Post
from posts.serializers import PostSerializers
from rest_framework.authtoken.models import Token
from django.db.models import Q


# Create your views here.


@api_view(["GET", "PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def index(request):
    if request.method == 'GET':
        current_user = request.user
        users = Account.objects.filter(is_superuser=False, is_staff=False).exclude(username=current_user.username)
        paginator = CustomPagination()
        result = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result, many=True)
        json_data = serializer.data
        data = paginator.get_paginated_response(json_data)
        return Response(data)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def create_user(request):
    if request.method == "POST":
        post_data = JSONParser().parse(request)
        try:
            Account.objects.get(username=post_data['username'])
            return Response("UserName Already Exist")
        except Account.DoesNotExist:
            try:
                Account.objects.get(email=post_data['email'])
                return Response("Email Already Exist")
            except Account.DoesNotExist:
                new_user = Account.objects.create_user(post_data['username'], post_data['email'], post_data['password'])
                if 'fullname' in post_data:
                    new_user.fullname = post_data['fullname']
                if 'avatar' in post_data:
                    new_user.avatar = post_data['avatar']
                new_user.save()
                serializer = UserSerializer(new_user)
                data = serializer.data
                token = Token.objects.get(user=new_user).key
                data['token'] = token
                return Response(data, status=201)


@api_view(["GET", "PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_user_(request):
    if request.method == "GET":
        user = request.user
        serialize = UserSerializer(user)
        data = serialize.data
        return Response(data, status=200)
    if request.method == "PUT":
        user = request.user
        post_data = JSONParser().parse(request)
        if 'fullname' in post_data:
            user.fullname = post_data['fullname']
            user.save()
        if 'avatar' in post_data:
            user.avatar = post_data['avatar']
            user.save()
        serializer = UserSerializer(user)
        data = serializer.data
        return Response(data, status=201)


@authentication_classes([TokenAuthentication])
@permission_classes({IsAuthenticated})
@api_view(["GET"])
def logout(request):
    if request.method == "GET":
        request.user.auth_token.delete()
        serialize = UserSerializer(request.user)
        data = serialize.data
        return Response(data)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(["DELETE"])
def delete(request):
    if request.method == "DELETE":
        try:
            user = request.user
            user.delete()
            return Response("User Deleted Successfully", status=201)
        except Account.DoesNotExist:
            return Response("Unable To Delete User Not Exist", status=500)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(["GET"])
def profile(request):
    if request.method == "GET":
        user_id = request.GET.get("id")
        try:
            user = Account.objects.get(id=user_id)
            serializer = UserSerializer(user)
            data = serializer.data
            serializer1 = UserFollowingSerializer(user.following.all(), many=True)
            data['following'] = serializer1.data
            serializer2 = UserFollowSerializer(user.followers.all(), many=True, )
            data['followers'] = serializer2.data
            posts = Post.objects.filter(posted_by=user).order_by("-posted_at")
            post_data = PostSerializers(posts, many=True)
            data['posts'] = post_data.data
            return Response(data, status=200)
        except Account.DoesNotExist:
            return Response("User Not Found", status=404)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_following(request):
    if request.method == "POST":
        post_data = JSONParser().parse(request)
        if 'following_id' in post_data:
            try:
                user = request.user
                print(user.id, post_data["following_id"])
                follower = Account.objects.get(id=post_data['following_id'])
                data = UserFollowing.objects.filter(Q(user_id=user.id) &
                                                 Q(following_user_id=follower.id))
                if len(data) > 0:
                    return Response("User Already Following", status=400)
                else:
                    UserFollowing(user_id=user, following_user_id=follower).save()
                    return Response("SuccessFully Saved", status=201)

            except Account.DoesNotExist:
                return Response("Some User Missing. Invalid Request", status=404)
        else:
            return Response("Invalid Request", status=400)
