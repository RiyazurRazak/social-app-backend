from rest_framework.response import Response
from django.conf import settings
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
import redis


client = redis.from_url(settings.REDIS_URL)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_story(request):
    user = request.user
    raw_story = client.get(user.id)
    if raw_story is None:
        data = {
            "isAvailable": False,
            "result": [],
        }
        return Response(data, status=404)
    story_dic = eval(raw_story)
    data = {
        "isAvailable": True,
        "result": story_dic,

    }
    return Response(data, status=200)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_stories(request):
    user = request.user
    user_following = user.following.all()
    following_users = [i.following_user_id.id for i in user_following]
    raw_stories = client.mget(following_users)
    stories = filter(None.__ne__, raw_stories)
    result = [eval(dic) for dic in stories]
    data = {
        "count": len(result),
        "results": result,
    }
    return Response(data, status=200)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_story(request):
    user = request.user
    avatar = user.avatar
    username = user.username,
    user_id = user.id
    story = JSONParser().parse(request)
    if 'story_url' in story:
        data = {
            "id": user_id,
            "avatar": avatar,
            "username": username[0],
            "story_url": story['story_url']
        }
        client.setex(user_id, 86400, str(data))
        return Response("Story Post Successfully", status=201)
    else:
        return Response("Data Missing", status=400)
