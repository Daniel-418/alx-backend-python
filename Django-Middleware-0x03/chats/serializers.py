from rest_framework import serializers
from .models import user, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
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
        fields = ["message_id", "sender", "message_body", "sent_at"]


class ConversationSerializer(serializers.ModelSerializer):
    participants_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, source="participants"
    )
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
            "messages",
        ]


# serializers.CharField
# serializers.SerializerMethodField()
# serializers.ValidationError
