from django.db import models
from django.conf import settings
from advice_generation.models import Conversation

class Analytics(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_analytics"
    )

    conversation = models.OneToOneField(
        Conversation,
        on_delete=models.CASCADE,
        related_name="analytics"
    )

    
    emotional = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Analytics for Conversation {self.conversation.id}"
    
    @property
    def user_input(self):
        return self.conversation.user_input
    
    #유저 정보 외래키 참조 형식으로 변환
# 상담하는 api하고 감정만 추출하는 api있는거