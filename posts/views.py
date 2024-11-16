from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .models import Emotion
from .serializers import EmotionSerializer
from advice_generation.models import Conversation
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
    
class EmotionViewSet(viewsets.ModelViewSet):
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        #현재 로그인한 유저의 데이터만 반환
        return self.queryset.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        #Emotion 데이터 생성
        response = super().create(request, *args, **kwargs) #Emotion 객체 생성
        emotion_instance = Emotion.objects.get(id=response.data['id'])

        #Conversation 데이터 동기화
        Conversation.objects.create(
            user=emotion_instance.user,
            user_input=emotion_instance.content,
            bot_response="와 개꿀", #이건 나중에 api떡칠 후 수정할 예정
            timestamp=emotion_instance.date,     
        )

        return response

