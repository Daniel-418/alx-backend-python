from rest_framework import serializers
from .models import User, Message, Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["message_id", "sender", "message_body", "edit_historysent_at"]


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    message = MessageSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"
