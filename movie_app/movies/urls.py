from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import register, get_movies, CollectionViewSet, request_count, reset_request_count

router = DefaultRouter()
router.register(r'collection', CollectionViewSet)

urlpatterns = [
    path('register/', register),
    path('movies/', get_movies),
    path('request-count/', request_count),
    path('request-count/reset/', reset_request_count),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
