from rest_framework import serializers
from .models import user, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        exclude = ["password_hash"]
