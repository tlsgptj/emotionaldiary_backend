from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Emotion
from .serializers import EmotionSerializer
from rest_framework.permissions import IsAuthenticated

# 감정 데이터 읽기 (리스트 조회)
class EmotionListAPIView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, *args, **kwargs):
        emotions = Emotion.objects.filter(user=request.user)
        serializer = EmotionSerializer(emotions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 감정 데이터 쓰기 (생성)
class CreateEmotionAPIView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        serializer = EmotionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # 현재 로그인한 사용자로 데이터 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
