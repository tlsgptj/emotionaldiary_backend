# Users/apps.py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'Users'

    def ready(self):
        import Users.signals  # 시그널을 등록
