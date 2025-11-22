from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import PermissionDenied
from .models import Conversation, user, Message
from .serializers import ConversationSerializer, MessageSerializer


# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        return self.request.user.conversations.prefetch_related(
            "participants", "messages"
        ).all()

    def perform_create(self, serializer):
        participants = serializer.validated_data.get("participants", [])
        if self.request.user not in participants:
            participants.append(self.request.user)
        serializer.save(participants=participants)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return (
            Message.objects.filter(conversation_id__participants=self.request.user)
            .select_related("sender_id")
            .order_by("sent_at")
        )

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get("conversation_id")
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("you are not a part of this conversation")

        serializer.save(sender_id=self.request.user)
