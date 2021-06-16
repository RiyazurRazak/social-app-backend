from rest_framework.response import Response
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from account.models import Account
import redis


client = redis.from_url(settings.REDIS_URL)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def generate_uuid(request):
    user = request.user
    uuid = get_random_string(4)
    client.setex(uuid, 120, str(user.username))
    data = {
        "uuid": uuid
    }
    return Response(data, status=201)


@api_view(["GET"])
def verify_uuid(request):
    uuid = request.GET.get("uuid")
    raw_user = client.get(uuid)
    if raw_user != None:
        client.delete(uuid)
        username = raw_user.decode('utf-8')
        print(username)
        if username != None:
            try:
                user = Account.objects.get(username=username)
                print(user)
                token = Token.objects.get(user=user).key
                data = {
                    "token": token,
                }
                return Response(data, status=200)
            except Account.DoesNotExist:
                return Response("User Not Found", status=404)
        else:
            return Response("UUID NOT Valid", status=401)
    else:
        return Response("UUID NOT Valid", status=400)






