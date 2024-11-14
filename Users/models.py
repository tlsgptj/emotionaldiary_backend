# Users/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    # 기본 User 모델과의 OneToOne 관계
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    additional_field = models.CharField(max_length=100, blank=True)
    
    # 추가 필드
    email = models.EmailField(unique=True)  # 이메일 필드
    username = models.CharField(max_length=30, blank=True)  # 사용자 이름 필드
    is_active = models.BooleanField(default=True)  # 활성 상태
    is_staff = models.BooleanField(default=False)  # 스태프 여부

    def __str__(self):
        return self.user.username

