from django.shortcuts import get_object_or_404
from rest_framework import permissions

from messaging_app.chats.models import Conversation


class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):  # pyright: ignore
        if not request.user or not request.user.is_authenticated:
            return False

        allowed_methods = ["GET", "POST", "PATCH", "PUT", "DELETE"]
        if request.method in allowed_methods:
            conversation_id = view.kwargs.get("conversation_pk")
            return Conversation.objects.filter(  # pyright: ignore
                pk=conversation_id, participants=request.User
            ).exists()

        return False
