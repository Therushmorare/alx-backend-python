# Django-Chat/Models/messaging/models.py

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Self-referential FK to support threaded replies
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"

    # Recursive method to get all replies
    def get_all_replies(self):
        all_replies = []
        for reply in self.replies.all():
            all_replies.append(reply)
            all_replies.extend(reply.get_all_replies())
        return all_replies

