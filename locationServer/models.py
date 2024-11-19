from django.db import models
from advice_generation.models import Conversation
from django.conf import settings

class Locations(models.Model):
     user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_locations"
    )
     conversations = models.ForeignKey(
          Conversation,
          on_delete=models.CASCADE,
          related_name="conversation_locations"
     )
     user_Locations = models.TextField()
     timestamp = models.ForeignKey(
          Conversation,
          on_delete=models.CASCADE,
          related_name="locations"
     )

     def __str__(self):
          return f"Location for Conversation {self.conversations.id}"
     
     @property
     def user_input(self):
          return self.conversations.user_input
     

# Create your models here.
