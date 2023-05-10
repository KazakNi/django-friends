from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .views import RequestViewSet, FriendShipViewset

app_name = 'api'
router = DefaultRouter()

router.register('requests', RequestViewSet, basename='requests')
router.register('friends', FriendShipViewset, basename='requests_list')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
