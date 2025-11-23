from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import PermissionDenied
from .models import Conversation, User, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.none()  # pyright: ignore

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
    queryset = Message.objects.none()  # pyright: ignore
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        return (
            Message.objects.filter(  # pyright: ignore
                conversation_id=self.kwargs["conversation_pk"],
            )
            .select_related("sender_id")
            .order_by("sent_at")
        )

    def perform_create(self, serializer):
        conversation_uid = self.kwargs["conversation_pk"]

        serializer.save(sender_id=self.request.user, conversation_id=conversation_uid)
