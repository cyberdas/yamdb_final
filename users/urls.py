from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users import views
from .views import ObtainConfirmationCode, UsersViewSet

router = DefaultRouter()

router.register('users', UsersViewSet, basename='users')

auth_patterns = [
    path('email/', ObtainConfirmationCode.as_view(), name='obtain_code'),
    path('token/', views.obtain_token, name='obtain_token')
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_patterns))
]