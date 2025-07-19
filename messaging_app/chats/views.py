from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Creates a new conversation with participants.
        Request data should contain a list of participant user_ids.
        """
        participant_ids = request.data.get('participants', [])
        if not participant_ids or len(participant_ids) < 2:
            return Response({"error": "A conversation needs at least 2 participants."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        Return only conversations where the current user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Expects `conversation` ID and `content` in request data.
        """
        data = request.data.copy()
        data['sender'] = request.user.id  # set sender to current user
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        """
        Return only messages for conversations the current user is part of.
        """
        return Message.objects.filter(conversation__participants=self.request.user)

