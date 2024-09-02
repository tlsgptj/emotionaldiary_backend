from django.db import models
from django.contrib.auth.models import User

class Emotion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 유저와 연관된 외래키
    date = models.DateTimeField(auto_now_add=True)  # 자동으로 현재 시간 설정
    emotions = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.emotions} on {self.date}"
