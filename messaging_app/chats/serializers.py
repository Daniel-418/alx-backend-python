from rest_framework import serializers
from .models import user, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        exclude = ["password_hash"]


class MessageSerializer(serializers.ModelSerializer):
    sender_id = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = "__all__"


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, related_name="messages")

    class Meta:
        model = Conversation
        fields = "__all__"


# serializer.Charfield
# serializers.SerializerMethodField()
# serializers.ValidationError
