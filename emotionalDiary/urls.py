from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Users import views
from posts.views import EmotionViewSet
from blog.views import BlogPostsAPIView

# DRF의 DefaultRouter를 사용하여 뷰셋을 등록할 수 있습니다.
router = DefaultRouter()
router.register(r'Users', views.UserViewSet)
router.register(r'emotions', EmotionViewSet, basename='emotion')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # API 엔드포인트를 등록
    path("api/blog-posts/", BlogPostsAPIView.as_view(), name="blog-posts"),
    path('api/register/', views.RegisterAPIView.as_view(), name='register'),  # 회원가입 엔드포인트
    path('api/login/', views.LoginAPIView.as_view(), name='login'),  # 로그인 엔드포인트
]
