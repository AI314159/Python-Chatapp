from django.db import models
import uuid
from django.contrib.auth.models import User

class Server(models.Model):
    # This is the unique identifier that keeps chats (mostly) secure.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # This ForeignKey keeps track of the owner. on_delete means that if
    # The owning user is deleted, the servers they own will also be deleted.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_owner")

    # Keeps track of the members
    members = models.ManyToManyField(User)

    # The server name!
    title = models.CharField(max_length=32)

    def __str__(self):
        # This function changes the admin page view
        return f"'{self.title}' owned by {self.owner}"