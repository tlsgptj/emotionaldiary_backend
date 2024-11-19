from django.db import models
from django.conf import settings
from advice_generation.models import Conversation

class wordCloud(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_wordCloud"
    )

    conversations = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="wordCloud_conversations"
    )

    word = models.TextField() #모델이랑 연결이 필요함

    often = models.TextField() #글자의 빈도를 추출해야함

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"wordCloud를 추출해봅시다. {self.conversations.id}"
    
    @property
    def user_input(self):
        return self.conversations.user_input
        
