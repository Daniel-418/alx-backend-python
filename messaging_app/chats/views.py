from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsParticipantOfConversation, IsAuthenticated]

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

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get("conversation_pk")

        is_participant = Conversation.objects.filter(
            pk=conversation_id, participants=request.user
        ).exists()

        if not is_participant:
            return Response(
                {"detail": "You are not a participant of this conversation"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().create(request, *args, **kwargs)
