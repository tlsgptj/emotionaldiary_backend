from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Users import views
from posts.views import CreateEmotionAPIView, EmotionListAPIView
from Users.views import RegisterAPIView, LoginAPIView

# DRF의 DefaultRouter를 사용하여 뷰셋을 등록할 수 있습니다.
router = DefaultRouter()
router.register(r'Users', views.UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  
    path('emotions/create/', CreateEmotionAPIView.as_view(), name='create'),
    path('emotions/list/', EmotionListAPIView.as_view(), name='list'),
    path('register/', RegisterAPIView.as_view(), name='register'),  
    path('login/', LoginAPIView.as_view(), name='login'),  
]
