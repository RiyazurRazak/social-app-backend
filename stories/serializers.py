from rest_framework import serializers


class StoryiesSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    avatar = serializers.URLField()
    username = serializers.CharField()
    story_url = serializers.URLField()