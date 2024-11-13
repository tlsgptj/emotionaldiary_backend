from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 이메일로 로그인하기
        try:
            user = CustomUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
