from rest_framework.routers import DefaultRouter
from .views import MissionViewSet, TargetUpdateViewSet


router = DefaultRouter()
router.register('', MissionViewSet)
router.register('targets', TargetUpdateViewSet)

urlpatterns = router.urls
