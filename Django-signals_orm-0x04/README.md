0. Implement Signals for User Notifications
mandatory

Objective: Automatically notify users when they receive a new message.

Instructions:

    Create a Message model with fields like sender, receiver, content, and timestamp.

    Use Django signals (e.g., post_save) to trigger a notification when a new Message instance is created.

    Create a Notification model to store notifications, linking it to the User and Message models.

    Write a signal that listens for new messages and automatically creates a notification for the receiving user.


