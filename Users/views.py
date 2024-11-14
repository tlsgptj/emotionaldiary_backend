# Users/views.py
from django.contrib.auth.models import User
from Users.models import UserProfile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from .serializers import UserSerializer 
from rest_framework.permissions import AllowAny 

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        password2 = request.data.get("password2")

        if password != password2:
            return Response({"error" : "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 기본 User 생성
        user = User.objects.create_user(username=email, email=email, password=password)
        
        # UserProfile 생성
        profile = UserProfile.objects.create(user=user, is_active=True, is_staff=False)
        
        return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "로그인 성공"})
        return Response({"message": "로그인 실패"}, status=400)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer