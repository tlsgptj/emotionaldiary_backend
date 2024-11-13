from django.db import models
from django.conf import settings  # settings.AUTH_USER_MODEL을 사용하기 위해 추가

class Emotion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 커스텀 사용자 모델 참조
    date = models.DateTimeField(auto_now_add=True)  # 자동으로 현재 시간 설정
    emotions = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.emotions} on {self.date}"

