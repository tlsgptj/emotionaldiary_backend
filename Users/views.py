from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        password2 = request.data.get("password2")

        # 이메일 유효성 검사
        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "유효한 이메일 주소를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호 확인
        if password != password2:
            return Response({"error": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 기본 User 생성
        user = User.objects.create_user(username=email, email=email, password=password)

        return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # 인증 시도
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # 토큰 생성 또는 가져오기
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "로그인 성공", "token": token.key})

        return Response({"message": "로그인 실패"}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
