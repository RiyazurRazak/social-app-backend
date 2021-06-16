from rest_framework import serializers
from .models import Account, UserFollowing


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'username', 'fullname', 'avatar', ]


class UserFollowingSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source="following_user_id", read_only=True,)

    class Meta:
        model = UserFollowing
        fields = ["id", "user_data", "created_at", ]


class UserFollowSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source="user_id", read_only=True, )

    class Meta:
        model = UserFollowing
        fields = ["id", "user_data", "created_at", ]
