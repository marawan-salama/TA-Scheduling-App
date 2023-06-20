from project_app.models import Notification


class NotificationClass:
    def __init__(self, sender, recipient, subject, message, primary_key=None):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.message = message
        self.primary_key = primary_key

    @classmethod
    def get_instance(cls, notification):
        return cls(
            notification.sender, 
            notification.recipient, 
            notification.subject, 
            notification.message, 
            notification.id
        )

    def save_details(self):
        notification = Notification(sender=self.sender, recipient=self.recipient,
                                    subject=self.subject, message=self.message)
        notification.save()

        self.sender.sent_notifications.add(notification)
        self.recipient.received_notifications.add(notification)

        self.primary_key = notification.id

    def get_model_instance(self):
        return Notification.objects.get(pk=self.primary_key)

    def validate(self):
        pass

    def delete(self):
        notification = self.get_model_instance()
        notification.delete()

    def get_sender(self):
        return self.sender

    def get_recipient(self):
        return self.recipient

    def get_subject(self):
        return self.subject

    def get_message(self):
        return self.message

    def get_primary_key(self):
        return self.primary_key
