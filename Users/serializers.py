from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate

CustomUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email']  # 원하는 필드를 지정하세요


class RegistrationUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser  # CustomUser 모델 사용
        fields = ['email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')

        user = CustomUser(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])  # 비밀번호 해싱
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # 이메일을 username으로 사용하여 인증 시도
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError('이메일 또는 비밀번호가 올바르지 않습니다.')

        data['user'] = user
        return data

