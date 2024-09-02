from rest_framework import viewsets, permissions
from .models import Emotion
from .serializers import EmotionSerializer

class EmotionViewSet(viewsets.ModelViewSet):
    serializer_class = EmotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 현재 로그인한 사용자의 데이터만 반환
        return Emotion.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 데이터를 생성할 때 현재 사용자를 설정
        serializer.save(user=self.request.user)

