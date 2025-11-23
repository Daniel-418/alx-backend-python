from django.shortcuts import get_object_or_404
from rest_framework import permissions

from messaging_app.chats.models import Conversation


class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        conversation_id = view.kwargs.get("conversation_pk")
        return Conversation.objects.filter(
            pk=conversation_id, participants=request.user
        ).exists()
