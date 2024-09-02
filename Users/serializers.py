from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import serializers
from Users.models import UserProfile
from django.contrib.auth import get_user_model
from rest_framework import serializers

CustomUser = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'birthday']  # 원하는 필드를 지정하세요


class RegistrationUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    birthday = serializers.DateField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'birthday']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        birthday = validated_data.pop('birthday')

        user = User(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        # UserProfile에 생일 저장
        UserProfile.objects.create(user=user, birthday=birthday)

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # 사용자가 있는지 확인하고, 인증 시도
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError('이메일 또는 비밀번호가 올바르지 않습니다.')

        data['user'] = user
        return data

